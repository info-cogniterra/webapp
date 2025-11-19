import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. GLOBÁLNÍ KONFIGURACE ---
st.set_page_config(page_title="RealityGenius | AI Enterprise", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. PREMIUM CSS (DESIGN SYSTEM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* POZADÍ A FONTY */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #050505 70%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* OPRAVA INPUTŮ (ABY BYLY ČITELNÉ) */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        background-color: #171717 !important;
        color: #ffffff !important;
        border: 1px solid #333333;
        border-radius: 8px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
    }

    /* TEXTY */
    h1, h2, h3, h4, p, li, div { color: #ffffff !important; }
    .subtext { color: #a3a3a3 !important; font-size: 0.9rem; line-height: 1.5; }
    .highlight { color: #60a5fa !important; font-weight: 700; }

    /* KARTY (GLASSMORPHISM) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
        height: 100%;
    }

    /* COMPARISON BOX (PŘED A PO) */
    .comparison-box {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* TLAČÍTKA */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: transform 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.02); }

    /* SKRYTÍ PRVKŮ */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. NAVIGACE ---
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'auth' not in st.session_state: st.session_state.auth = False

def navigate(page):
    st.session_state.page = page
    st.rerun()

# --- 4. LANDING PAGE ---
def show_landing():
    # Navbar
    c1, c2 = st.columns([6, 1])
    with c1: st.markdown("### 💎 RealityGenius | by Cogniterra")
    with c2: 
        if st.button("Klientská zóna"): navigate('login')
    st.markdown("---")

    # Hero Section
    col_text, col_visual = st.columns([1.1, 1])
    
    with col_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("# Přestaňte psát inzeráty.<br>Začněte prodávat.", unsafe_allow_html=True)
        st.markdown("""
        <p class="subtext" style="font-size: 1.1rem; margin-bottom: 20px;">
        První AI nástroj v ČR, který <span class="highlight">vidí to, co kupující</span>. 
        Nahrajte fotku a získejte hotový prodejní text, Instagram post a LinkedIn strategii. 
        <b>Za 5 sekund.</b>
        </p>
        """, unsafe_allow_html=True)
        
        # ROI Data
        c_a, c_b = st.columns(2)
        with c_a: st.markdown("✅ **Úspora 12h** / týden")
        with c_b: st.markdown("✅ **+35 %** vyšší dosah")

        # Lead Gen Form
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #2563eb;">
                <h4 style="margin:0;">🚀 Získejte konkurenční výhodu</h4>
                <p class="subtext" style="font-size:0.8em;">Přístup momentálně na pozvánky.</p>
            </div>
            """, unsafe_allow_html=True)
            email = st.text_input("Váš pracovní email", placeholder="jan.novak@remax.cz", label_visibility="collapsed")
            if st.button("Požádat o Early Access", type="primary"):
                if "@" in email:
                    st.success("Děkujeme. Jste zařazeni do prioritní fronty.")
                else:
                    st.warning("Zadejte platný email.")

    with col_visual:
        # VS. Sekce
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h4 style="text-align:center; margin-bottom:20px;">VS. Běžný Makléř vs. RealityGenius</h4>
            
            <div class="comparison-box" style="border-left: 3px solid #ef4444;">
                <b style="color: #ef4444;">❌ Člověk (20 minut):</b><br>
                <span class="subtext">"Prodám byt 2kk po rekonstrukci. Volejte ihned. RK nevolat."</span>
            </div>
            
            <div class="comparison-box" style="border-left: 3px solid #22c55e;">
                <b style="color: #22c55e;">✅ RealityGenius AI (3 sekundy):</b><br>
                <span class="subtext">"🔥 <b>Investiční příležitost na Vinohradech!</b><br>
                Ranní káva na terase s výhledem na Prahu? Tento designový loft (65 m²) s italskou dlažbou..."</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ROI Sekce
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding: 30px; border-top: 1px solid #333;">
        <h2>Kolik stojí váš čas?</h2>
        <p class="subtext">Průměrný makléř stráví psaním inzerátů 4 hodiny týdně.</p>
        <h2 style="color: #3b82f6 !important;">Úspora: 16 000 Kč / měsíčně</h2>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGIN PAGE ---
def show_login():
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h2 style="text-align: center;">🔐 Vstup pro partnery</h2>
            <p class="subtext" style="text-align: center;">Cogniterra Group Enterprise</p>
        </div>
        """, unsafe_allow_html=True)
        
        user = st.text_input("ID Partnera")
        pwd = st.text_input("Heslo", type="password")
        
        c_log, c_back = st.columns(2)
        with c_log:
            if st.button("Přihlásit"):
                if (user == "admin" and pwd == "cogniterra") or (user == "demo" and pwd == "demo"):
                    st.session_state.auth = True
                    navigate('app')
                else:
                    st.error("Neplatné údaje.")
        with c_back:
            if st.button("Zpět"): navigate('landing')

# --- 6. APP WORKSPACE ---
def show_app():
    # Header
    c1, c2 = st.columns([8, 1])
    with c1: st.markdown("## ⚡ RealityGenius | Workspace")
    with c2: 
        if st.button("Odhlásit"):
            st.session_state.auth = False
            navigate('landing')
    st.markdown("---")

    # Layout
    col_left, col_right = st.columns([1, 1.3], gap="large")

    with col_left:
        with st.expander("⚙️ Aktivace Engine (API Key)", expanded=True):
            api_key = st.text_input("Vložte klíč", type="password", label_visibility="collapsed", placeholder="Vložte Google API Key")
            
        st.markdown("### 1. Zdrojová data")
        uploaded_file = st.file_uploader("Nahrajte fotku nemovitosti", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Analýza...", use_column_width=True)

    with col_right:
        st.markdown("### 2. Cílení kampaně")
        with st.container():
            c_a, c_b = st.columns(2)
            with c_a:
                typ = st.selectbox("Typ nemovitosti", ["Byt na investici", "Rodinný dům", "Luxusní Penthouse", "Komerční prostor"])
                lokalita = st.text_input("Lokalita", placeholder="Praha 1 - Staré Město")
            with c_b:
                cena = st.text_input("Cena", placeholder="22.500.000 CZK")
                ton = st.selectbox("Strategie", ["Emoční (Prodej snu)", "Racionální (Investoři)", "Virální (Gen Z / TikTok)"])
            
            features = st.text_area("Klíčové benefity", placeholder="Terasa 20m2, parkování v zakladači, výhled na hrad...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            generate_btn = st.button("✨ GENEROVAT KOMPLETNÍ KAMPAŇ", type="primary")

        # GENERATION LOGIC (SMART SELECTOR)
        if generate_btn:
            if not api_key or not uploaded_file:
                st.error("⚠️ Chybí API klíč nebo fotografie.")
            else:
                genai.configure(api_key=api_key)
                
                # --- INTELIGENTNÍ VÝBĚR MODELU (Fix pro chyby 429/404) ---
                active_model = "models/gemini-1.5-flash" # Default safe choice
                try:
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    # Hledáme model, který má v názvu "flash" (je levný a rychlý)
                    flash_models = [m for m in available_models if 'flash' in m]
                    if flash_models:
                        active_model = flash_models[0]
                    elif available_models:
                        # Pokud není flash, vezmeme první co funguje a není experimental
                        stable_models = [m for m in available_models if 'exp' not in m]
                        if stable_models:
                            active_model = stable_models[0]
                except Exception:
                    pass # Pokud listování selže, použijeme defaultní string
                # --------------------------------------------------------

                model = genai.GenerativeModel(active_model)
                
                with st.spinner(f"AI Copywriter tvoří texty ({active_model})..."):
                    try:
                        prompt = f"""
                        Jsi špičkový realitní marketér.
                        Analyzuj fotku a vytvoř texty pro: {typ}, {lokalita}, {cena}.
                        Strategie: {ton}. Benefity: {features}.
                        
                        Výstup Markdown:
                        1. **HEADLINE**: (Max 7 slov, úderný)
                        2. **SREALITY POPIS**: (Strukturovaný, prodejní, 150 slov)
                        3. **INSTAGRAM CAPTION**: (Včetně emoji, mezer, CTA)
                        4. **VIRAL TAGS**: (15 hashtagů pro rok 2025)
                        """
                        response = model.generate_content([prompt, Image.open(uploaded_file)])
                        
                        st.markdown("### 🎉 Hotová kampaň")
                        t1, t2 = st.tabs(["📄 Inzerát & Socials", "📋 Strategie"])
                        
                        with t1: st.markdown(response.text)
                        with t2: 
                            st.info("Tip: Tento text je optimalizovaný pro SEO.")
                            st.code(response.text)
                        
                    except Exception as e:
                        st.error(f"Chyba: {e}")
                        st.info("Pokud vidíš chybu 429, vygeneruj nový API klíč v Google AI Studio.")

# --- 7. ROUTER ---
if st.session_state.page == 'landing': show_landing()
elif st.session_state.page == 'login': show_login()
elif st.session_state.page == 'app': 
    if st.session_state.auth: show_app()
    else: navigate('login')
