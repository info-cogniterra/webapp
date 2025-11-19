import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. KONFIGURACE A STYLY ---
st.set_page_config(page_title="RealityGenius AI", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# MODERNÍ SAAS DESIGN SYSTEM (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Globální nastavení */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1F2937;
        background-color: #F9FAFB; /* Světlé moderní pozadí */
    }

    /* Odstranění defaultního Streamlit headeru */
    header {visibility: hidden;}
    
    /* Tlačítka - Primary */
    div.stButton > button {
        background-color: #2563EB; /* Moderní modrá */
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8;
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3);
    }

    /* Karty a kontejnery */
    .css-1r6slb0, .stMarkdown, .stTextInput {
        background-color: transparent;
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 10px;
        color: #374151;
    }
    
    /* Custom třídy pro Landing Page */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #111827;
        line-height: 1.2;
        margin-bottom: 1rem;
        text-align: center;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT (Navigace) ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# --- 3. LANDING PAGE ---
def show_landing_page():
    # Navbar placeholder
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### **🏢 RealityGenius.ai**")
    with col2:
        if st.button("Přihlásit se"):
            navigate_to('login')

    st.markdown("---")
    
    # Hero Section
    st.markdown('<div class="hero-title">Automatizujte prodej nemovitostí<br>pomocí umělé inteligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Vytvářejte virální inzeráty, Instagram posty a LinkedIn analýzy z jediné fotografie. Ušetřete 90 % času a prodávejte rychleji.</div>', unsafe_allow_html=True)
    
    # CTA
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Vyzkoušet demo zdarma", type="primary", use_container_width=True):
            navigate_to('login')

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Features Section
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>📸 Vizuální Analýza</h3>
            <p>AI vidí to, co kupující. Detekuje materiály, světlo a atmosféru z fotky.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>✍️ Copywriting 3.0</h3>
            <p>Texty, které prodávají. Od emocí na Instagramu po fakta na Sreality.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Virální Dosah</h3>
            <p>Automatický výběr nejlepších hashtagů a strategií pro rok 2025.</p>
        </div>
        """, unsafe_allow_html=True)

# --- 4. LOGIN PAGE ---
def show_login_page():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### 👋 Vítejte zpět")
            st.markdown("Přihlaste se do svého klientského účtu.")
            
            username = st.text_input("Email")
            password = st.text_input("Heslo", type="password")
            
            if st.button("Vstoupit do aplikace", use_container_width=True):
                # HARDCODED AUTH (Pro MVP stačí)
                if (username == "admin" and password == "cogniterra") or (username == "demo" and password == "demo"):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    navigate_to('app')
                else:
                    st.error("Nesprávné údaje. (Zkuste: admin / cogniterra)")
            
            st.markdown("<div style='text-align: center; color: #666; margin-top: 10px;'>Nemáte účet? Kontaktujte Cogniterra Group.</div>", unsafe_allow_html=True)
        
        if st.button("← Zpět na web", type="secondary"):
            navigate_to('landing')

# --- 5. APP INTERFACE (Samotný produkt) ---
def show_app_page():
    # Header Appky
    sidebar = st.sidebar
    sidebar.title("⚙️ Nastavení")
    api_key = sidebar.text_input("Google API Key", type="password")
    
    if sidebar.button("Odhlásit se"):
        st.session_state.authenticated = False
        navigate_to('landing')

    # Hlavní layout
    st.title("Nová kampaň")
    
    col_left, col_right = st.columns([1, 1.5], gap="large")

    with col_left:
        st.markdown("#### 1. Vstupní data")
        with st.container(border=True):
            uploaded_file = st.file_uploader("Nahrajte fotografii", type=["jpg", "png", "jpeg"])
            if uploaded_file:
                st.image(uploaded_file, use_column_width=True, caption="Náhled nemovitosti")
    
    with col_right:
        st.markdown("#### 2. Cílení a parametry")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                nemovitost = st.selectbox("Typ", ["Byt", "Dům", "Komerce", "Pozemek"])
                cena = st.text_input("Cena", placeholder="25.000.000 CZK")
            with c2:
                lokalita = st.text_input("Lokalita", placeholder="Praha - Vinohrady")
                ton = st.selectbox("Tón", ["Luxusní & Emoční", "Věcný & Profesionální", "Urgentní & Investiční"])
            
            features = st.text_area("Klíčové benefity (oddělte čárkou)", placeholder="Terasa, parkování, výhled, po rekonstrukci...")
            
            generate = st.button("✨ Vygenerovat kampaň", type="primary", use_container_width=True)

    # VÝSLEDKY
    if generate:
        if not api_key:
            st.warning("⚠️ Pro generování vložte prosím API klíč v levém menu.")
            return

        # Logika AI
        genai.configure(api_key=api_key)
        # Auto-select best model logic
        model_name = 'gemini-1.5-flash' # Fallback
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                    model_name = m.name
        except:
            pass
            
        model = genai.GenerativeModel(model_name)

        with st.spinner("Analyzuji obraz a píšu texty..."):
            try:
                prompt = f"""
                Jsi senior marketing strategist. Vytvoř kampaň pro: {nemovitost}, {lokalita}, {cena}.
                Vlastnosti: {features}. Tón: {ton}.
                
                Výstup strukturovaně:
                1. Nadpis (Catchy)
                2. Popis pro web (Sreality/Reas)
                3. Social Media Post (Instagram/TikTok)
                4. Hashtagy
                """
                response = model.generate_content([prompt, Image.open(uploaded_file)])
                
                st.markdown("---")
                st.subheader("🚀 Výsledek kampaně")
                st.info("Texty jsou připraveny k okamžitému použití.")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Chyba: {e}")

# --- 6. MAIN ROUTER ---
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'login':
    show_login_page()
elif st.session_state.page == 'app':
    if st.session_state.authenticated:
        show_app_page()
    else:
        navigate_to('login')
