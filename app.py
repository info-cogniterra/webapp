import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. GLOBÁLNÍ KONFIGURACE ---
st.set_page_config(page_title="RealityGenius AI | Enterprise Platform", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ENTERPRISE CSS (ULTIMATE EDITION) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');

    /* ZÁKLAD */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        background-color: #0B0F19; /* Deepest Navy */
        color: #E2E8F0;
    }
    
    /* STYLOVÁNÍ OBRÁZKŮ GLOBÁLNĚ (Místo chybného parametru style) */
    img {
        border-radius: 15px;
        transition: transform 0.3s ease;
    }
    img:hover {
        transform: scale(1.01);
    }
    
    /* SKRYTÍ PRVKŮ */
    #MainMenu, footer, header {visibility: hidden;}

    /* TYPOGRAFIE LANDING PAGE */
    .lp-h1 {
        font-size: 4rem; font-weight: 800; line-height: 1.1;
        background: linear-gradient(120deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }
    .lp-h2 {
        font-size: 2.5rem; font-weight: 700; color: white; margin-top: 3rem; margin-bottom: 1.5rem; text-align: center;
    }
    .lp-lead {
        font-size: 1.25rem; color: #94a3b8; max-width: 800px; margin: 0 auto 2rem auto; line-height: 1.6;
    }
    .highlight-blue { color: #3B82F6; }
    
    /* KOMPONENTY */
    .feature-box {
        background: rgba(30, 41, 59, 0.4); border: 1px solid #1E293B;
        padding: 2rem; border-radius: 16px; height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-box:hover { transform: translateY(-5px); border-color: #3B82F6; }
    
    .step-number {
        font-size: 4rem; font-weight: 900; color: #1E293B; position: absolute; top: 10px; right: 20px; z-index: 0;
    }
    
    .trust-bar {
        display: flex; justify-content: center; gap: 3rem; opacity: 0.5; margin: 3rem 0; flex-wrap: wrap;
    }
    .trust-logo { font-size: 1.5rem; font-weight: 700; color: #64748B; }

    /* PRICING TABLES */
    .pricing-container {
        background: #111827; border: 1px solid #374151; border-radius: 20px; padding: 2rem; text-align: center; position: relative;
    }
    .pricing-popular {
        border: 2px solid #3B82F6; background: rgba(59, 130, 246, 0.05); transform: scale(1.05); z-index: 10;
    }
    .price-tag { font-size: 3rem; font-weight: 800; color: white; margin: 1rem 0; }
    .check-item { text-align: left; margin: 0.5rem 0; color: #CBD5E1; }

    /* CTA BUTTONS */
    div.stButton > button {
        background: #2563EB; color: white; border: none; padding: 0.8rem 2rem;
        font-weight: 600; border-radius: 8px; width: 100%; transition: all 0.3s;
    }
    div.stButton > button:hover { background: #1D4ED8; transform: translateY(-2px); }
    .secondary-btn > button { background: transparent; border: 1px solid #475569; }

    /* PHONE MOCKUP */
    .iphone {
        border: 10px solid #333; border-radius: 30px; overflow: hidden; background: white; color: black; max-width: 350px; margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. NAVIGACE ---
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'auth' not in st.session_state: st.session_state.auth = False

def nav(to):
    st.session_state.page = to
    st.rerun()

# --- 4. LANDING PAGE (FULL PRODUCT) ---
def show_landing():
    # -- HERO SECTION --
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div style='color:#3B82F6; font-weight:700; letter-spacing:1px; margin-bottom:10px;'>COGNITERRA GROUP PRESENTS</div>", unsafe_allow_html=True)
        st.markdown('<h1 class="lp-h1">Automatizujte prodej realit <br><span class="highlight-blue">jedním kliknutím.</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="lp-lead" style="margin:0; text-align:left;">Náš AI engine analyzuje fotografie nemovitostí a okamžitě generuje virální inzeráty, Instagram Reels scénáře a LinkedIn analýzy. <br><br>Šetříme makléřům 12 hodin týdně.</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("🚀 VYZKOUŠET ZDARMA"): nav('login')
        with c2:
            # Použití prázdného kontejneru pro zarovnání tlačítka, styl řešen přes CSS
            st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
            if st.button("DEMO UKÁZKA"): nav('login')
            st.markdown("</div>", unsafe_allow_html=True)
            
    with col2:
        # Vizuál dashboardu (OPRAVENO: Odstraněn parametr style, který způsoboval chybu)
        st.image("https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=2053&auto=format&fit=crop", caption="Analyzováno AI Enginem 3.0")

    # -- SOCIAL PROOF --
    st.markdown("""
    <div class="trust-bar">
        <div class="trust-logo">RE/MAX</div>
        <div class="trust-logo">CENTURY 21</div>
        <div class="trust-logo">SREALITY.CZ</div>
        <div class="trust-logo">AIRBNB</div>
        <div class="trust-logo">SVOBODA & WILLIAMS</div>
    </div>
    <hr style="border-color: #1E293B;">
    """, unsafe_allow_html=True)

    # -- PROBLEM / SOLUTION --
    st.markdown('<h2 class="lp-h2">Proč 80 % makléřů selhává na sociálních sítích?</h2>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-box">
            <h3>❌ Nudné texty</h3>
            <p style="color:#94a3b8">Makléři píší stále dokola "slunný byt po rekonstrukci". To nikoho nezaujme. Naše AI používá psychologii prodeje.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-box">
            <h3>❌ Špatné cílení</h3>
            <p style="color:#94a3b8">LinkedIn vyžaduje jiný jazyk než TikTok. Ruční přepisování trvá hodiny. My to děláme vteřiny.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-box">
            <h3>❌ Nulová viralita</h3>
            <p style="color:#94a3b8">Bez správných hashtagů a "háčků" (hooks) váš inzerát zapadne. Náš algoritmus zná trendy roku 2025.</p>
        </div>""", unsafe_allow_html=True)

    # -- USE CASES (PŘÍPADY UŽITÍ) --
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h2 class="lp-h2">Jeden nástroj. Nekonečno možností.</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🏠 Realitní Makléři", "🏗️ Developeři", "✈️ Airbnb Hostitelé"])
    
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            st.info("CASE STUDY: Byt 2kk, Praha Žižkov")
            st.markdown("**Před AI:** 2 týdny na trhu, 3 prohlídky.\n\n**S RealityGenius:** AI vygenerovala agresivní Instagram kampaň cílenou na Gen Z. \n\n**Výsledek:** Prodáno za 4 dny, o 5 % dráž.")
        with col2:
             st.markdown("### Co získá makléř:")
             st.markdown("✅ Generování popisků na Sreality\n\n✅ Scénáře pro video prohlídky\n\n✅ Newslettery pro investory")

    with tab2:
        st.markdown("### Pro velké projekty")
        st.write("Developeři využívají náš nástroj pro generování obsahu pro celé čtvrti. Nahrajte vizualizaci a získejte příběh o 'novém životním stylu'.")
        
    with tab3:
        st.markdown("### Airbnb Automatizace")
        st.write("Máte byt v centru? AI vytvoří popis v angličtině, němčině a španělštině, který zdůrazní turistické atrakce v okolí (automaticky detekované podle lokality).")

    # -- PRICING --
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h2 class="lp-h2">Investice, která se vrátí s prvním prodejem</h2>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.1, 1])
    
    with c1:
        st.markdown("""
        <div class="pricing-container">
            <h3>STARTER</h3>
            <div class="price-tag">0 Kč</div>
            <div class="check-item">🔹 3 Generování měsíčně</div>
            <div class="check-item">🔹 Základní AI Model</div>
            <div class="check-item">🔹 Standardní podpora</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="pricing-container pricing-popular">
            <div style="background:#3B82F6; color:white; padding:2px 10px; border-radius:10px; display:inline-block; font-size:12px; margin-bottom:10px;">DOPORUČENO</div>
            <h3>PROFESSIONAL</h3>
            <div class="price-tag">1.290 Kč</div>
            <p style="color:#94a3b8">/ měsíčně</p>
            <div class="check-item">✅ <b>Neomezené generování</b></div>
            <div class="check-item">✅ <b>Gemini 1.5 Flash Engine</b></div>
            <div class="check-item">✅ Instagram, LinkedIn, TikTok</div>
            <div class="check-item">✅ Virální Hashtag Generator</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("VYBRAT PROFI PLAN", type="primary"): nav('login')

    with c3:
        st.markdown("""
        <div class="pricing-container">
            <h3>AGENCY</h3>
            <div class="price-tag">Individuální</div>
            <div class="check-item">🔹 API Přístup</div>
            <div class="check-item">🔹 Whitelabel řešení</div>
            <div class="check-item">🔹 Vlastní AI trénink</div>
            <div class="check-item">🔹 Fakturace na firmu</div>
        </div>
        """, unsafe_allow_html=True)

    # -- FAQ --
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h2 class="lp-h2">Časté dotazy</h2>', unsafe_allow_html=True)
    
    with st.expander("❓ Jak se lišíte od ChatGPT?"):
        st.write("ChatGPT je obecný chat. RealityGenius je trénovaný na tisících úspěšných realitních inzerátech a využívá multimodální vidění pro analýzu fotografií. Výsledkem je hotový produkt, ne konverzace.")
    with st.expander("❓ Musím umět programovat?"):
        st.write("Vůbec ne. Ovládání je jednodušší než poslat email. Nahrajete fotku, kliknete na tlačítko.")
    with st.expander("❓ Mohu dostat fakturu pro firmu?"):
        st.write("Samozřejmě. Jsme Cogniterra Group, plátci DPH. Fakturace je automatická.")

    # -- FOOTER --
    st.markdown("<br><br><br><hr style='border-color:#1E293B;'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("© 2025 **Cogniterra Group s.r.o.**<br>Všechna práva vyhrazena.", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='text-align:right'>Obchodní podmínky • GDPR • Podpora</div>", unsafe_allow_html=True)

# --- 5. LOGIN PAGE ---
def show_login():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center;'>🔐 Klientská zóna</h2>", unsafe_allow_html=True)
            st.info("Pro přístup k demo verzi použijte: admin / cogniterra")
            
            username = st.text_input("Email / Uživatelské jméno")
            password = st.text_input("Heslo", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("PŘIHLÁSIT SE", type="primary"):
                    if (username == "admin" and password == "cogniterra") or (username == "demo" and password == "demo"):
                        st.session_state.auth = True
                        nav('app')
                    else:
                        st.error("Chybné údaje.")
            with col_b:
                if st.button("Zpět na web"): nav('landing')

# --- 6. APP INTERFACE (PRODUKT) ---
def show_app():
    # NAVBAR
    col_logo, col_user = st.columns([6, 1])
    with col_logo:
        st.markdown("### ⚡ RealityGenius | Dashboard")
    with col_user:
        if st.button("Odhlásit"):
            st.session_state.auth = False
            nav('landing')

    # API CONFIG (SKRYTÉ V EXPANERU)
    with st.expander("⚙️ Konfigurace AI (API Key)"):
        api_key = st.text_input("Vložte Google API Key", type="password")

    # HLAVNÍ UI
    st.markdown("---")
    
    c1, c2 = st.columns([1, 1.2], gap="large")
    
    with c1:
        st.markdown("#### 1. Vstupní data")
        uploaded_file = st.file_uploader("Nahrajte fotografii", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Analýza obrazu...", use_column_width=True)
        
        st.markdown("#### 2. Parametry kampaně")
        typ = st.selectbox("Typ nemovitosti", ["Luxusní apartmán", "Rodinný dům", "Investiční byt", "Komerční prostor"])
        lokalita = st.text_input("Lokalita", placeholder="např. Praha - Vinohrady")
        cena = st.text_input("Cena", placeholder="např. 15.900.000 CZK")
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("✨ GENEROVAT MARKETINGOVÉ MATERIÁLY", type="primary")

    with c2:
        st.markdown("#### 3. Výstupy")
        
        if not generate_btn:
            st.info("Waiting for input... Nahrajte fotku a spusťte AI.")
            # Placeholder image
            st.markdown("""
            <div style="border: 2px dashed #334155; border-radius: 10px; height: 400px; display: flex; align-items: center; justify-content: center; color: #64748B;">
                Zde se objeví vygenerované texty
            </div>
            """, unsafe_allow_html=True)
            
        if generate_btn:
            if not api_key:
                st.error("⚠️ Vložte prosím API klíč v nastavení nahoře.")
            elif not uploaded_file:
                st.warning("⚠️ Nahrajte fotografii.")
            else:
                # AI GENERATION LOGIC
                genai.configure(api_key=api_key)
                
                # Model selection fallback
                model_name = 'gemini-1.5-flash'
                try:
                    ms = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    if ms: model_name = ms[0]
                except: pass
                
                model = genai.GenerativeModel(model_name)
                
                with st.spinner("Cogniterra AI Engine analyzuje trh..."):
                    try:
                        prompt = f"""
                        Jsi senior realitní marketér. 
                        Vytvoř kampaň pro: {typ}, {lokalita}, {cena}.
                        Analyzuj obrázek pro detaily.
                        
                        Výstup:
                        1. Titulek inzerátu (Catchy)
                        2. Text na Sreality (Profesionální)
                        3. Instagram Post (Virální styl + emoji)
                        4. 10 Virálních hashtagů pro rok 2025 (real estate czech, global)
                        """
                        response = model.generate_content([prompt, Image.open(uploaded_file)])
                        
                        # VÝSLEDEK
                        tabs = st.tabs(["📱 Instagram Preview", "📄 Text Inzerátu", "📊 LinkedIn Strategie"])
                        
                        with tabs[0]:
                            st.markdown(f"""
                            <div class="iphone">
                                <img src="https://placehold.co/600x400/png?text=Image" style="width:100%">
                                <div style="padding:15px; font-size:14px; line-height:1.4;">
                                    <b>reality_genius_official</b><br>
                                    {response.text[:300]}... <span style="color:#3B82F6">více</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with tabs[1]:
                            st.markdown(response.text)
                            
                        with tabs[2]:
                            st.success("LinkedIn strategie: Zaměřit se na ROI a lokalitu. Použít formální tón.")
                            st.code(response.text)

                    except Exception as e:
                        st.error(f"Chyba: {e}")

# --- 7. ROUTING ---
if st.session_state.page == 'landing': show_landing()
elif st.session_state.page == 'login': show_login()
elif st.session_state.page == 'app': 
    if st.session_state.auth: show_app()
    else: nav('login')
