import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURACE ---
st.set_page_config(page_title="RealityGenius AI", page_icon="🏠", layout="wide")

# --- SIDEBAR (Nastavení) ---
st.sidebar.header("⚙️ Nastavení")

# 1. API KLÍČ
api_key = st.sidebar.text_input("Vložte Google Gemini API Key", type="password")
st.sidebar.markdown("[Získat API klíč zdarma zde](https://aistudio.google.com/app/apikey)")

# 2. DYNAMICKÝ VÝBĚR MODELU (OPRAVA CHYBY)
selected_model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Získáme seznam modelů, které podporují generování obsahu
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Pokud jsme nějaké našli, dáme je do výběru. Pokud ne, dáme fallback.
        if available_models:
            # Zkusíme najít něco s "flash" v názvu jako default, jinak bereme první
            default_index = 0
            for i, model_name in enumerate(available_models):
                if "flash" in model_name.lower():
                    default_index = i
                    break
            
            selected_model_name = st.sidebar.selectbox("Vyberte AI Model", available_models, index=default_index)
            # Ořízneme "models/" z názvu, pokud to knihovna vyžaduje bez prefixu
            selected_model = selected_model_name 
        else:
            st.sidebar.error("Klíč je platný, ale nenašli jsme žádné modely.")
    except Exception as e:
        st.sidebar.error(f"Chyba API klíče: {e}")

# --- HLAVNÍ ROZHRANÍ ---
st.title("🏠 RealityGenius.ai")
st.markdown("### Proměňte fotku nemovitosti v hotový inzerát a virální post.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Nahrajte fotku nemovitosti", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Nahraný obrázek', use_column_width=True)

with col2:
    typ_nemovitosti = st.selectbox("Typ nemovitosti", ["Byt na prodej", "Dům na prodej", "Airbnb pronájem", "Kancelář"])
    lokalita = st.text_input("Lokalita", placeholder="Např. Praha - Vinohrady")
    cena = st.text_input("Cena", placeholder="Např. 7.5 mil CZK")
    klicove_vlastnosti = st.text_area("Klíčové vlastnosti", placeholder="Po rekonstrukci, balkon, tichá ulice...")
    
    generate_btn = st.button("✨ Vygenerovat inzerát a posty", type="primary")

# --- LOGIKA AI ---
if generate_btn:
    if not api_key:
        st.warning("⚠️ Nejdříve vložte API klíč v levém menu.")
    elif not selected_model:
        st.warning("⚠️ Nepodařilo se načíst model. Zkontrolujte API klíč.")
    elif not uploaded_file:
        st.warning("⚠️ Musíte nahrát fotku.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(selected_model)

        with st.spinner(f'AI pracuje (Model: {selected_model})...'):
            try:
                prompt = f"""
                Jsi expert na realitní marketing. 
                Analyzuj obrázek a vytvoř texty pro: {typ_nemovitosti}, lokalita {lokalita}, cena {cena}.
                Klíčové vlastnosti: {klicove_vlastnosti}.
                
                Výstup Markdown:
                ## 📋 Inzerát (Realitní portál)
                ## 📱 Instagram/Facebook (Virální styl)
                ## 💼 LinkedIn (B2B styl)
                ## #️⃣ Hashtagy (Použij nejvíce virální hashtagy pro daný sektor)
                """
                
                response = model.generate_content([prompt, image])
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Chyba při generování: {e}")
