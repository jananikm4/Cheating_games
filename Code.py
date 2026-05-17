# ── ULTRASMOOTH CUSTOM UI SHEET ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset canvas to a high-end dark studio finish */
html, body, [class*="css"] { 
    font-family: 'Plus Jakarta Sans', sans-serif; 
}
#MainMenu, footer, header { visibility: hidden; }

.stApp { 
    background: radial-gradient(circle at 50% 0%, #1a1c29 0%, #0f111a 100%) !important;
}

/* Premium, organic looking Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 20px;
    padding: 6px;
    gap: 4px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 14px;
    color: #6C728A;
    background: transparent;
    border-radius: 14px;
    border: none;
    padding: 10px 24px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.stTabs [aria-selected="true"] {
    background: rgba(255, 255, 255, 0.08) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Smooth custom score indicator pills */
.score-pill {
    display: inline-block;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 30px;
    padding: 6px 18px;
    font-weight: 600;
    font-size: 15px;
    color: #A0A5BF;
    margin: 4px;
}

/* Complete Button Overhaul */
div[data-testid="stButton"] button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    background: rgba(20, 24, 41, 0.6) !important;
    color: #CDD1E4 !important;
    padding: 12px 8px !important;
    font-size: 14px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div[data-testid="stButton"] button:hover {
    border-color: rgba(255, 255, 255, 0.2) !important;
    background: rgba(255, 255, 255, 0.08) !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
}
div[data-testid="stButton"] button:active {
    transform: translateY(0px) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Title Typography (FORCE OVERRIDE THE COLORS SO THEY STAND OUT) ─────────────
st.markdown("""
<div style='text-align:center; padding:32px 0 12px;'>
  <h1 style='font-family: "Plus Jakarta Sans", sans-serif !important; font-size:2.6rem !important; font-weight:800 !important;
              letter-spacing: -1px !important; color: #FFFFFF !important; margin: 0 !important; padding: 0 !important;
              background: linear-gradient(135deg, #FFFFFF 40%, #A2A9CD 100%);
              -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
    ⚗️ Chaos RPS
  </h1>
  <div style='color:#7E84A3 !important; font-size:14px !important; margin-top:8px !important; font-weight: 500 !important;'>
    15 choices. Highly controversial logic. Deeply unserious.
  </div>
</div>
""", unsafe_allow_html=True)
