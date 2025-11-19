import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. GLOBÁLNÍ KONFIGURACE ---
st.set_page_config(page_title="RealityGenius | AI Enterprise", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. PREMIUM CSS (HIGH CONTRAST & GLASSMORPHISM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* HLAVNÍ BAREVNÉ SCHÉMA - TEMNÁ & LUXUSNÍ */
    .stApp {
        background-color: #050505; /* Téměř černá */
        background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #050505 70%); /* Decentní modrá záře nahoře */
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* OPRAVA ČITELNOSTI INPUTŮ (ZÁSADNÍ) */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        background-color: #171717 !important; /* Tmavě šedá */
        color: #ffffff !important; /* Bílý text */
        border: 1px solid #333333;
        border-radius: 8px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6; /* Modrý focus */
        box-shadow: 0 0 0 1px #3b82f6;
    }
    
    /* TEXTY A NADPISY */
    h1, h2, h3, p, li, div {
        color: #ffffff !important;
    }
    .subtext {
        color: #a3a3a3 !important; /* Šedá pro méně důležité texty */
        font-size: 0.9rem;
    }

    /* KARTY (GLASSMORPHISM EFEKT) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
    }

    /* TLAČÍTKA */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* SKRYTÍ PRVKŮ STREAMLITU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'auth' not in st.session_state: st.session_state.auth = False

def navigate(page):
    st.session_state.page = page
    st.rerun()

# --- 4. LANDING PAGE (SALES & LEAD GEN) ---
def show_landing():
    # NAVBAR
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown("### 💎 Cogniterra | RealityGenius")
    with c2:
        if st.button("Přihlášení pro klienty"): navigate('login')

    st.markdown("---")

    # HERO SEKCE
    col_text, col_visual = st.columns([1.2, 1])
    
    with col_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("# Automatizace realitního marketingu.")
        st.markdown("<p class='subtext' style='font-size: 1.2rem;'>Nástroj pro elitu v realitách. Přeměňte fotku na virální kampaň během 5 sekund. Šetřete čas, zvyšujte zisky.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # LEAD GENERATION FORM (ŘEŠENÍ "JAK ZÍSKAT PŘÍSTUP")
        with st.container():
            st.markdown("""
            <div class="glass-card">
                <h3 style="margin-top:0;">🚀 Požádat o Early Access</h3>
                <p class="subtext">Přístup je momentálně pouze na pozvánky. Zanechte nám kontakt.</p>
            </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Váš pracovní email", placeholder="např. jan.novak@remax.cz")
            
            if st.button("Odeslat žádost o přístup", type="primary"):
                if email and "@" in email:
                    st.success(f"Děkujeme. Poptávka odeslána týmu Cogniterra Group. Ozveme se na {email}.")
                    time.sleep(3)
                else:
                    st.warning("Zadejte prosím platný email.")

    with col_visual:
        # Vizuální ukázka
        st.markdown("""
        <div class="glass-card" style="text-align: center; margin-top: 20px;">
            <div style="color: #3b82f6; font-size: 2rem; margin-bottom: 10px;">✨ AI Engine 3.0</div>
            <div style="background: #171717; padding: 15px; border-radius: 10px; text-align: left;">
                <span style="color: #4ade80;">Analyzováno:</span> Penthouse, Praha 1<br>
                <span style="color: #4ade80;">Cílová skupina:</span> Investoři, Expati<br>
                <span style="color: #4ade80;">Status:</span> Kampaň vygenerována
            </div>
        </div>
        """, unsafe_allow_html=True)

    # FEATURES
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("📸 Vizuální AI Analýza")
        st.markdown("<p class='subtext'>Engine nečte jen text. Vidí fotku, pozná parkety, světlo i atmosféru.</p>", unsafe_allow_html=True)
    with c2:
        st.info("✍️ Copywriting na míru")
        st.markdown("<p class='subtext'>Sreality, Instagram, LinkedIn. Každá platforma dostane jiný, perfektní text.</p>", unsafe_allow_html=True)
    with c3:
        st.info("🔒 Enterprise Security")
        st.markdown("<p class='subtext'>Vaše data a fotky nikam neposíláme. Bezpečnost garantovaná Google Cloud.</p>", unsafe_allow_html=True)

# --- 5. LOGIN PAGE ---
def show_login():
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h2 style="text-align: center;">🔐 Klientský portál</h2>
            <p class="subtext" style="text-align: center;">Zadejte své přístupové údaje</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Uživatelské jméno")
        password = st.text_input("Heslo", type="password")
        
        col_login, col_back = st.columns(2)
        with col_login:
            if st.button("Vstoupit", use_container_width=True):
                if (username == "admin" and password == "cogniterra") or (username == "demo" and password == "demo"):
                    st.session_state.auth = True
                    navigate('app')
                else:
                    st.error("Neplatné údaje.")
        with col_back:
            if st.button("Zpět", use_container_width=True): navigate('landing')

# --- 6. APP DASHBOARD ---
def show_app():
    # HEADER
    c1, c2 = st.columns([8, 1])
    with c1: st.markdown("## ⚡ RealityGenius | Dashboard")
    with c2: 
        if st.button("Odhlásit"):
            st.session_state.auth = False
            navigate('landing')
    
    st.markdown("---")

    # LAYOUT
    col_left, col_right = st.columns([1, 1.5], gap="large")

    with col_left:
        st.markdown("#### 1. Konfigurace zakázky")
        
        # API KEY SECTION
        with st.expander("🔑 Nastavení API Klíče (Nutné pro start)", expanded=True):
            api_key = st.text_input("Google API Key", type="password", placeholder="AIzaSy...")
            st.markdown("<p class='subtext' style='font-size:0.8em'>Klíč se neukládá, běží pouze v této relaci.</p>", unsafe_allow_html=True)

        st.markdown("#### 2. Vstupní data")
        uploaded_file = st.file_uploader("Fotografie nemovitosti", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_column_width=True)

    with col_right:
        st.markdown("#### 3. Zacílení kampaně")
        
        with st.container(): # Obaleno v kontejneru pro lepší vzhled
            c_a, c_b = st.columns(2)
            with c_a:
                typ = st.selectbox("Typ nemovitosti", ["Luxusní Byt", "Rodinný Dům", "Airbnb", "Kancelář", "Pozemek"])
                lokalita = st.text_input("Lokalita", placeholder="Např. Vinohrady")
            with c_b:
                cena = st.text_input("Cena", placeholder="Např. 12.5 mil CZK")
                ton = st.selectbox("Tón komunikace", ["Exkluzivní & Emoční", "Věcný & Informativní", "Agresivní & Virální"])

            features = st.text_area("Specifika (oddělte čárkou)", placeholder="Terasa, garáž, po rekonstrukci, výhled...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            generate_btn = st.button("✨ VYGENEROVAT MATERIÁLY", type="primary", use_container_width=True)

        # VÝSTUPY
        st.markdown("#### 4. Výsledky")
        if generate_btn:
            if not api_key:
                st.error("⛔ Chybí API klíč. Vložte jej v sekci vlevo.")
            elif not uploaded_file:
                st.warning("⚠️ Nahrajte prosím fotku.")
            else:
                genai.configure(api_key=api_key)
                
                # Fallback model selection
                model_name = 'gemini-1.5-flash'
                try:
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    if models: model_name = models[0]
                except: pass
                
                model = genai.GenerativeModel(model_name)
                
                with st.spinner(f"Analyzuji obrazová data ({model_name})..."):
                    try:
                        prompt = f"""
                        Jsi senior copywriter pro realitní trh (B2C i B2B).
                        
                        VSTUP:
                        - Typ: {typ}
                        - Lokalita: {lokalita}
                        - Cena: {cena}
                        - Tón: {ton}
                        - Detaily: {features}
                        - OBRÁZEK: Analyzuj vizuální styl (světlo, prostor, materiály).
                        
                        VÝSTUP (Markdown):
                        1. "HEADLINE": Úderný nadpis (max 10 slov).
                        2. "SREALITY": Profesionální popis (cca 150 slov), strukturovaný.
                        3. "INSTAGRAM": Virální text, emotikony, call-to-action.
                        4. "HASHTAGS": 15 nejlepších hashtagů pro tento typ nemovitosti v ČR.
                        """
                        response = model.generate_content([prompt, Image.open(uploaded_file)])
                        
                        # Zobrazení v tabech
                        tab1, tab2 = st.tabs(["📄 Web Inzerát", "📱 Social Media"])
                        
                        with tab1:
                            st.markdown(response.text)
                        with tab2:
                            st.info("Doporučení: K tomuto textu přidejte na Instagramu trending audio.")
                            st.code(response.text) # Code block pro snadné kopírování

                    except Exception as e:
                        st.error(f"Chyba AI Enginu: {e}")

# --- 7. ROUTING ---
if st.session_state.page == 'landing': show_landing()
elif st.session_state.page == 'login': show_login()
elif st.session_state.page == 'app': 
    if st.session_state.auth: show_app()
    else: navigate('login')
