import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. GLOBÁLNÍ KONFIGURACE ---
st.set_page_config(page_title="RealityGenius | AI Enterprise", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. PREMIUM CSS (STEJNÝ KVALITNÍ DESIGN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #172554 0%, #050505 60%); /* Darker Blue Glow */
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Inputs styling */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        background-color: #171717 !important;
        color: #ffffff !important;
        border: 1px solid #333333;
        border-radius: 8px;
    }
    
    /* Text colors */
    h1, h2, h3, p, li, div { color: #ffffff !important; }
    .subtext { color: #9ca3af !important; font-size: 0.95rem; line-height: 1.5; }
    .highlight { color: #60a5fa !important; font-weight: bold; }
    .strike { text-decoration: line-through; color: #ef4444 !important; }

    /* Cards */
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
    
    /* Comparison Box */
    .comparison-box {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s;
        width: 100%;
    }
    div.stButton > button:hover { transform: scale(1.02); }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. STATE ---
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'auth' not in st.session_state: st.session_state.auth = False

def navigate(page):
    st.session_state.page = page
    st.rerun()

# --- 4. LANDING PAGE (OBSAHOVĚ VYLADĚNÁ) ---
def show_landing():
    # NAVBAR
    c1, c2 = st.columns([6, 1])
    with c1: st.markdown("### 💎 RealityGenius | by Cogniterra")
    with c2: 
        if st.button("Klientská zóna"): navigate('login')
    st.markdown("---")

    # 1. HERO SEKCE (Silnější Value Prop)
    col_text, col_visual = st.columns([1.1, 1])
    
    with col_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("# Přestaňte psát inzeráty.<br>Začněte prodávat.", unsafe_allow_html=True)
        st.markdown("""
        <p class="subtext" style="font-size: 1.2rem; margin-bottom: 20px;">
        První AI nástroj v ČR, který <span class="highlight">vidí to, co kupující</span>. 
        Nahrajte fotku a získejte hotový prodejní text, Instagram post a LinkedIn strategii. 
        <b>Za 5 sekund.</b>
        </p>
        """, unsafe_allow_html=True)
        
        # HARD DATA (Social Proof)
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown("✅ **Úspora 12h** / týden")
        with c_b:
            st.markdown("✅ **+35 %** vyšší dosah")

        # LEAD GEN FORM
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #2563eb;">
                <h4 style="margin:0;">🚀 Získejte konkurenční výhodu</h4>
                <p class="subtext" style="font-size:0.9em;">Přístup momentálně na pozvánky. Zadejte email.</p>
            </div>
            """, unsafe_allow_html=True)
            email = st.text_input("Váš pracovní email", placeholder="jan.novak@remax.cz", label_visibility="collapsed")
            if st.button("Požádat o Early Access", type="primary"):
                if "@" in email:
                    st.success("Děkujeme. Váš email byl zařazen do prioritní fronty.")
                else:
                    st.warning("Zadejte platný email.")

    with col_visual:
        # VIZUÁL "PŘED A PO" (To nejdůležitější)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h4 style="text-align:center; margin-bottom:20px;">VS. Běžný Makléř vs. RealityGenius</h4>
            
            <div class="comparison-box" style="border-left: 3px solid #ef4444; margin-bottom: 15px;">
                <b style="color: #ef4444;">❌ Člověk (20 minut):</b><br>
                <span class="subtext">"Prodám pěkný byt 2kk po rekonstrukci. Volejte ihned. RK nevolat."</span>
            </div>
            
            <div class="comparison-box" style="border-left: 3px solid #22c55e;">
                <b style="color: #22c55e;">✅ RealityGenius AI (3 sekundy):</b><br>
                <span class="subtext">"🔥 <b>Investiční příležitost na Vinohradech!</b><br>
                Představte si ranní kávu na terase s výhledem na Prahu. Tento designový loft (65 m²) s italskou dlažbou..."</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. PROČ NE CHATGPT? (Řešení námitky)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center'>Proč nestačí ChatGPT?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>👁️ Multimodální Vidění</h3>
            <p class="subtext">ChatGPT nevidí detaily. Náš engine analyzuje <b>světlo, materiály podlahy a atmosféru</b> přímo z fotky.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🇨🇿 České Reálie</h3>
            <p class="subtext">Jsme trénováni na datech z <b>Sreality a Bezrealitky</b>. Známe rozdíl mezi "cihlou" a "panelem".</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>📈 Virální Strategie 2025</h3>
            <p class="subtext">Nejen texty. Generujeme <b>hashtagy a scénáře pro Reels</b>, které algoritmy milují.</p>
        </div>
        """, unsafe_allow_html=True)

    # 3. ROI KALKULAČKA (Psychologie ceny)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding: 40px; border-top: 1px solid #333;">
        <h2>Kolik stojí váš čas?</h2>
        <p class="subtext">Průměrný makléř stráví psaním inzerátů a postů 4 hodiny týdně.</p>
        <h1 style="color: #3b82f6 !important;">Úspora: 16 000 Kč / měsíčně</h1>
        <p class="subtext">Cena RealityGenius je zlomkem této částky.</p>
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
            if st.button("Přihlásit", use_container_width=True):
                if (user == "admin" and pwd == "cogniterra") or (user == "demo" and pwd == "demo"):
                    st.session_state.auth = True
                    navigate('app')
                else:
                    st.error("Neplatné údaje.")
        with c_back:
            if st.button("Zpět", use_container_width=True): navigate('landing')

# --- 6. APP (THE PRODUCT) ---
def show_app():
    # HEADER
    c1, c2 = st.columns([8, 1])
    with c1: st.markdown("## ⚡ RealityGenius | Workspace")
    with c2: 
        if st.button("Odhlásit"):
            st.session_state.auth = False
            navigate('landing')
    st.markdown("---")

    # HLAVNÍ FUNKCE
    col_left, col_right = st.columns([1, 1.3], gap="large")

    with col_left:
        # API CONFIG
        with st.expander("⚙️ Aktivace Engine (API Key)", expanded=True):
            api_key = st.text_input("Vložte klíč", type="password", label_visibility="collapsed", placeholder="Vložte Google API Key")
            
        st.markdown("### 1. Zdrojová data")
        uploaded_file = st.file_uploader("Nahrajte 1 nejlepší fotku", type=["jpg", "png", "jpeg"])
        
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
            generate_btn = st.button("✨ GENEROVAT KOMPLETNÍ KAMPAŇ", type="primary", use_container_width=True)

        # VÝSTUPY
        if generate_btn:
            if not api_key or not uploaded_file:
                st.error("⚠️ Chybí API klíč nebo fotografie.")
            else:
                genai.configure(api_key=api_key)
                # Model logic
                model_name = 'gemini-1.5-flash'
                try:
                    ms = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    if ms: model_name = ms[0]
                except: pass
                
                model = genai.GenerativeModel(model_name)
                
                with st.spinner("AI Copywriter tvoří texty..."):
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
                        t1, t2, t3 = st.tabs(["📄 Inzerát", "📱 Social Media", "📋 Strategie"])
                        
                        with t1: st.markdown(response.text)
                        with t2: st.code(response.text, language='markdown')
                        with t3: st.info("Tip: Tento text použijte v kombinaci s 9:16 videem.")
                        
                    except Exception as e:
                        st.error(f"Chyba: {e}")

# --- 7. ROUTER ---
if st.session_state.page == 'landing': show_landing()
elif st.session_state.page == 'login': show_login()
elif st.session_state.page == 'app': 
    if st.session_state.auth: show_app()
    else: navigate('login')
