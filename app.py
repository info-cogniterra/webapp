import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. KONFIGURACE STRÁNKY ---
st.set_page_config(page_title="REALITY GENIUS | Premium AI", page_icon="💎", layout="wide")

# --- 2. LUXUSNÍ DESIGN (CSS INJECTION) ---
# Toto změní vzhled celé aplikace na "Dark Premium"
st.markdown("""
<style>
    /* Hlavní pozadí */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Nadpisy */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37 !important; /* Zlatá barva */
        font-weight: 700;
    }
    /* Tlačítka */
    div.stButton > button {
        background-color: #D4AF37;
        color: #000000;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        border-radius: 5px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #F4CF57;
        color: #000000;
        transform: scale(1.02);
    }
    /* Inputy */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
        border: 1px solid #444;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161A25;
        border-right: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SPRÁVA UŽIVATELŮ (PAYWALL) ---
# Zde si definujete platící klienty. Formát: "uzivatelske_jmeno": "heslo"
USERS = {
    "admin": "cogniterra2025",   # Váš master účet
    "klient1": "reality123",     # Účet pro prvního klienta
    "demo": "start"              # Demo účet
}

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in USERS and st.session_state["password"] == USERS[st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>REALITY GENIUS <span style='color:white; font-size:0.5em;'>AI</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Exkluzivní nástroj pro realitní profesionály</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            st.text_input("Uživatelské jméno", key="username")
            st.text_input("Heslo", type="password", key="password")
            st.button("Vstoupit do systému", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>REALITY GENIUS</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            st.text_input("Uživatelské jméno", key="username")
            st.text_input("Heslo", type="password", key="password")
            st.button("Vstoupit do systému", on_click=password_entered)
            st.error("⛔ Chybně zadané údaje nebo vypršela licence.")
        return False
    
    else:
        # Password correct
        return True

# --- 4. HLAVNÍ APLIKACE ---
if check_password():
    # --- SIDEBAR ---
    st.sidebar.title("💎 NASTAVENÍ")
    st.sidebar.info(f"Přihlášen: {st.session_state['username']}")
    
    # API KEY INPUT
    api_key = st.sidebar.text_input("Google API Key", type="password", help="Vložte klíč pro aktivaci AI enginu")
    
    # DYNAMICKÝ VÝBĚR MODELU
    selected_model = None
    if api_key:
        try:
            genai.configure(api_key=api_key)
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            if available_models:
                default_index = 0
                for i, model_name in enumerate(available_models):
                    if "flash" in model_name.lower():
                        default_index = i
                        break
                selected_model_name = st.sidebar.selectbox("AI Model Engine", available_models, index=default_index)
                selected_model = selected_model_name 
            else:
                st.sidebar.error("Klíč je platný, ale nebyly nalezeny modely.")
        except Exception as e:
            st.sidebar.error(f"Chyba API klíče: {e}")

    if st.sidebar.button("Odhlásit se"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- WORKSPACE ---
    st.title("Nová zakázka")
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("### 1. Vizuální vstup")
        uploaded_file = st.file_uploader("Nahrajte fotografii nemovitosti", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Náhled', use_column_width=True)

    with col2:
        st.markdown("### 2. Parametry inzerátu")
        typ_nemovitosti = st.selectbox("Typ nemovitosti", ["Luxusní Byt", "Rodinný Dům", "Penthouse", "Komerční prostor", "Airbnb Investice"])
        lokalita = st.text_input("Lokalita", placeholder="např. Pařížská, Praha 1")
        cena = st.text_input("Cena", placeholder="např. 25.000.000 CZK")
        styl_komunikace = st.select_slider("Tón komunikace", options=["Formální", "Profesionální", "Emoční", "Virální/Agresivní"])
        klicove_vlastnosti = st.text_area("Detaily a benefity", placeholder="Terasa, výhled na hrad, parkování v garáži, smart home...")
        
        st.write("") # Spacing
        generate_btn = st.button("✨ GENEROVAT MARKETINGOVÉ MATERIÁLY", type="primary")

    # --- VÝSTUP ---
    if generate_btn:
        if not api_key or not selected_model or not uploaded_file:
            st.warning("⚠️ Pro generování vyplňte API klíč a nahrajte fotografii.")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(selected_model)

            with st.spinner('AI Copywriter pracuje na textu...'):
                try:
                    prompt = f"""
                    Jsi špičkový realitní makléř a copywriter pro luxusní segment.
                    Tón komunikace: {styl_komunikace}.
                    
                    Zadání:
                    1. Analyzuj přiložený obrázek (interiér/exteriér, světlo, materiály).
                    2. Vytvoř prodejní texty pro: {typ_nemovitosti}, lokalita {lokalita}, cena {cena}.
                    3. Zahrň tyto benefity: {klicove_vlastnosti}.
                    
                    Výstup formátuj v Markdownu:
                    
                    ## ⚜️ EXKLUZIVNÍ INZERÁT (Web)
                    (Headline, Poutavý úvod, Detailní popis atmosféry, Call to Action)
                    
                    ## 📱 INSTAGRAM & TIKTOK (Virální)
                    (Krátký, úderný text, zaměřený na "fear of missing out" a luxus)
                    
                    ## 💼 LINKEDIN (Investiční)
                    (Analytičtější pohled, vhodnost investice, ROI potenciál)
                    
                    ## #️⃣ HASHTAGY
                    (Vypiš 15 nejvíce virálních hashtagů pro rok 2025 v oblasti realit a investic v ČR a globálně)
                    """
                    
                    response = model.generate_content([prompt, image])
                    
                    st.success("Generování dokončeno!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Nastala chyba: {e}")
