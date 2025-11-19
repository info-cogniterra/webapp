import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURACE ---
st.set_page_config(page_title="RealityGenius AI", page_icon="🏠", layout="wide")

# --- SIDEBAR (Nastavení) ---
st.sidebar.header("⚙️ Nastavení")
api_key = st.sidebar.text_input("Vložte Google Gemini API Key", type="password")
st.sidebar.markdown("[Získat API klíč zdarma zde](https://aistudio.google.com/app/apikey)")

# --- HLAVNÍ ROZHRANÍ ---
st.title("🏠 RealityGenius.ai")
st.markdown("### Proměňte fotku nemovitosti v hotový inzerát a virální post.")

# 1. VSTUPY
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Nahrajte fotku nemovitosti (Obývák, Kuchyně...)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Nahraný obrázek', use_column_width=True)

with col2:
    typ_nemovitosti = st.selectbox("Typ nemovitosti", ["Byt na prodej", "Dům na prodej", "Airbnb pronájem", "Kancelář"])
    lokalita = st.text_input("Lokalita (např. Praha - Vinohrady)")
    cena = st.text_input("Cena (např. 7.5 mil CZK nebo 2000 CZK/noc)")
    klicove_vlastnosti = st.text_area("Klíčové vlastnosti (např. po rekonstrukci, blízko metra, tichá ulice)")
    
    generate_btn = st.button("✨ Vygenerovat inzerát a posty", type="primary")

# --- LOGIKA AI ---
if generate_btn and api_key and uploaded_file:
    genai.configure(api_key=api_key)
    # Používáme Gemini 1.5 Flash pro rychlost a multimodalitu
    model = genai.GenerativeModel('gemini-1.5-flash')

    with st.spinner('AI analyzuje fotku a píše texty...'):
        try:
            # Prompt pro AI
            prompt = f"""
            Jsi expert na realitní marketing a copywriting. 
            
            Zadání:
            1. Analyzuj přiložený obrázek nemovitosti. Popiš atmosféru a detaily viditelné na fotce.
            2. Vytvoř atraktivní inzerát pro typ: {typ_nemovitosti} v lokalitě {lokalita} s cenou {cena}.
            3. Zahrň tyto vlastnosti: {klicove_vlastnosti}.
            
            Výstup musí být ve formátu Markdown a obsahovat tyto sekce:
            
            ## 📋 Inzerát na realitní portál
            (Profesionální, lákavý text, zdůrazňující benefity a atmosféru z fotky)
            
            ## 📱 Instagram/Facebook Post
            (Krátký, úderný, emoji, zaměřený na emoce)
            
            ## 💼 LinkedIn Post
            (Profesionální, zaměřený na investiční příležitost nebo kvalitu bydlení)
            
            ## #️⃣ Hashtagy
            (Použij nejvíce virální hashtagy pro realitní trh v ČR i globálně)
            """
            
            response = model.generate_content([prompt, image])
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Chyba: {e}")

elif generate_btn and not api_key:
    st.warning("⚠️ Prosím vložte svůj API klíč v levém menu.")
