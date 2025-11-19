import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. KONFIGURACE ---
st.set_page_config(page_title="RealityGenius AI | Enterprise", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ENTERPRISE CSS (Tohle dělá tu magii) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* RESET A ZÁKLAD */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0f172a; /* Dark Navy Blue */
        color: #f8fafc;
    }
    
    /* SKRYTÍ PRVKŮ STREAMLITU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* HLAVNÍ TLAČÍTKA - GRADIENT */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.5);
    }

    /* HERO TEXT */
    .hero-header {
        background: -webkit-linear-gradient(0deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 800;
        text-align: center;
        margin-top: 2rem;
        line-height: 1.1;
        animation: fadeIn 1.5s ease-in;
    }
    
    .hero-sub {
        text-align: center;
        color: #94a3b8;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }

    /* KARTY CENÍKU */
    .pricing-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        transition: transform 0.3s;
    }
    .pricing-card:hover {
        transform: scale(1.03);
        border-color: #60a5fa;
    }
    .price {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    /* VSTUPNÍ POLE */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    /* SIMULACE TELEFONU PRO NÁHLED */
    .phone-mockup {
        background-color: white;
        color: black;
        border-radius: 30px;
        padding: 20px;
        border: 8px solid #333;
        max-width: 320px;
        margin: 0 auto;
        font-family: sans-serif;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. NAVIGACE ---
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'auth' not in st.session_state: st.session_state.auth = False

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- 4. LANDING PAGE (SALES) ---
def show_landing():
    # Navbar
    c1, c2 = st.columns([5,1])
    with c1: st.markdown("### 🧬 RealityGenius.ai")
    with c2: 
        if st.button("CLIENT LOGIN"): go_to('login')

    st.markdown("---")
    
    # Hero
    st.markdown('<div class="hero-header">BUDOUCNOST REALIT<br>JE TADY.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Generujte špičkové inzeráty a virální obsah pomocí AI. Zvyšte prodeje o 300% bez práce navíc. Nástroj pro moderní makléře.</div>', unsafe_allow_html=True)

    # Call to Action
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 ZAČÍT VYDĚLÁVAT TEĎ", type="primary"):
            go_to('login')

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Pricing
    st.markdown("<h2 style='text-align:center'>Vyberte si svůj plán</h2><br>", unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
        <div class="pricing-card">
            <h3>STARTER</h3>
            <div class="price">0 Kč</div>
            <p style="color:#94a3b8">Na zkoušku</p>
            <hr style="border-color:#334155">
            <p>✅ 3 Generování měsíčně</p>
            <p>✅ Základní texty</p>
            <p>❌ Bez virálních hashtagů</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div class="pricing-card" style="border-color: #8b5cf6; background: rgba(139, 92, 246, 0.1);">
            <h3 style="color: #a78bfa">PRO BUSINESS</h3>
            <div class="price">990 Kč</div>
            <p style="color:#94a3b8">měsíčně</p>
            <hr style="border-color:#8b5cf6">
            <p>✅ Neomezené generování</p>
            <p>✅ <b>Gemini 1.5 Flash Engine</b></p>
            <p>✅ Instagram & LinkedIn AI</p>
            <p>✅ Prioritní podpora</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p3:
        st.markdown("""
        <div class="pricing-card">
            <h3>AGENCY</h3>
            <div class="price">4.990 Kč</div>
            <p style="color:#94a3b8">měsíčně</p>
            <hr style="border-color:#334155">
            <p>✅ Pro celé týmy</p>
            <p>✅ API Přístup</p>
            <p>✅ Whitelabel řešení</p>
        </div>
        """, unsafe_allow_html=True)

# --- 5. LOGIN ---
def show_login():
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<h2 style='text-align:center'>🔐 Vstup pro klienty</h2>", unsafe_allow_html=True)
            user = st.text_input("Uživatel")
            pwd = st.text_input("Heslo", type="password")
            
            if st.button("PŘIHLÁSIT SE"):
                if (user == "admin" and pwd == "cogniterra") or (user == "demo" and pwd == "demo"):
                    st.session_state.auth = True
                    go_to('app')
                else:
                    st.error("Špatné heslo. (Hint: admin / cogniterra)")
            
            if st.button("Zpět", type="secondary"): go_to('landing')

# --- 6. APP INTERFACE ---
def show_app():
    # Top Bar
    c1, c2 = st.columns([6,1])
    with c1: st.title("⚡ Kampaň Generátor")
    with c2: 
        if st.button("Odhlásit"): 
            st.session_state.auth = False
            go_to('landing')
    
    # API Settings (Hidden in Expander)
    with st.expander("🔧 Nastavení AI Enginu"):
        api_key = st.text_input("Vložte Google API Key", type="password")
    
    # Main Workspace
    col_input, col_preview = st.columns([1.2, 1])
    
    with col_input:
        st.markdown("#### 1. Data o nemovitosti")
        uploaded_file = st.file_uploader("", type=["jpg", "png"], help="Nahrajte fotku pro analýzu")
        
        if uploaded_file:
            st.image(uploaded_file, use_column_width=True, style="border-radius: 10px;")
        
        c_a, c_b = st.columns(2)
        with c_a:
            typ = st.selectbox("Typ", ["Luxusní Byt", "Rodinný Dům", "Airbnb", "Kanceláře"])
        with c_b:
            vibe = st.select_slider("Styl komunikace", options=["Konzervativní", "Moderní", "Agresivní", "Virální"])
            
        info = st.text_area("Specifika (nepovinné)", placeholder="Bazén, výhled na Prahu, po rekonstrukci...")
        
        # HUGE GENERATE BUTTON
        st.markdown("<br>", unsafe_allow_html=True)
        btn = st.button("✨ GENEROVAT MAGIC OBSAH")

    with col_preview:
        st.markdown("#### 2. Live Náhled")
        
        # Placeholder content
        if not btn:
            st.info("👈 Nahrajte fotku a klikněte na Generovat. AI vytvoří náhledy.")
            
        # AI LOGIC
        if btn and api_key and uploaded_file:
            genai.configure(api_key=api_key)
            # Fallback logic for model
            model_name = 'gemini-1.5-flash'
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                if models: model_name = models[0]
            except: pass
            
            model = genai.GenerativeModel(model_name)
            
            with st.spinner("AI analyzuje pixely a píše bestseller..."):
                try:
                    prompt = f"""
                    Jsi světový copywriter.
                    Obrázek: Analyzuj ho.
                    Typ: {typ}, Styl: {vibe}, Info: {info}.
                    
                    Vytvoř JSON výstup (ne code block, prostě text):
                    1. Nadpis inzerátu
                    2. Krátký text pro Instagram (s emoji)
                    3. 5 Hashtagů
                    """
                    response = model.generate_content([prompt, Image.open(uploaded_file)])
                    text = response.text
                    
                    # Zobrazení výsledků
                    st.success("HOTOVO!")
                    
                    # TABS
                    tab1, tab2 = st.tabs(["📱 Instagram", "📄 Sreality"])
                    
                    with tab1:
                        st.markdown(f"""
                        <div class="phone-mockup">
                            <div style="font-weight:bold; margin-bottom:10px;">instagram_user</div>
                            <img src="https://placehold.co/600x400/png?text=FOTKA" style="width:100%; border-radius:5px; margin-bottom:10px;">
                            <div style="font-size: 14px;">
                            <b>{text[:100]}...</b><br><br>
                            {text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with tab2:
                        st.code(text)

                except Exception as e:
                    st.error(f"Chyba: {e}")
        elif btn and not api_key:
            st.error("⚠️ Chybí API klíč v nastavení nahoře!")

# --- 7. ROUTING ---
if st.session_state.page == 'landing': show_landing()
elif st.session_state.page == 'login': show_login()
elif st.session_state.page == 'app': 
    if st.session_state.auth: show_app()
    else: go_to('login')
