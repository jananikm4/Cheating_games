import streamlit as st
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Chaos RPS", page_icon="⚗️", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

.stApp { background-color: #FAF7F2; }

.score-pill {
    display: inline-block;
    background: #EDE8DF;
    border-radius: 50px;
    padding: 6px 20px;
    font-weight: 700;
    font-size: 18px;
    color: #3D3530;
    margin: 4px;
}

div[data-testid="stButton"] button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    border: 2px solid #EDE8DF !important;
    background: white !important;
    color: #3D3530 !important;
    padding: 10px 6px !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stButton"] button:hover {
    border-color: #8B7D6B !important;
    background: #EDE8DF !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  OPTIONS + BEATS (pure pseudo-science)
# ═══════════════════════════════════════════════════════════════════════════════

OPTIONS = [
    ("🪨", "Rock"),      ("📄", "Paper"),     ("✂️", "Scissors"),
    ("🔥", "Fire"),      ("🌊", "Water"),      ("⚡", "Lightning"),
    ("🐉", "Dragon"),    ("🦠", "Virus"),      ("🗡️", "Knife"),
    ("🌪️", "Tornado"),   ("🧲", "Magnet"),     ("💣", "Bomb"),
    ("🧊", "Ice"),       ("☀️", "Sun"),        ("🌑", "Void"),
]

BEATS = {
    "Rock": [
        ("Scissors", "Rock's compressive force (≈200 MPa) exceeds scissors' tensile strength. Structural failure confirmed."),
        ("Fire",     "Rock's thermal conductivity (0.3 W/m·K) dissipates fire's BTUs below ignition threshold. Extinguished."),
        ("Knife",    "Knife edge contacts rock at 15° angle, inducing micro-fractures in the blade. Rockwell hardness wins."),
        ("Ice",      "Rock transfers residual geothermal energy at 0.06 W/m², raising ice surface above 0°C. Melted.")
    ],
    "Paper": [
        ("Rock",     "Paper envelops rock, increasing surface drag coefficient by 340%. Rock's kinetic energy: zero."),
        ("Water",    "Paper's cellulose fibres absorb water via capillary action at 8mm/min until full saturation. Neutralised."),
        ("Void",     "Paper's photon-reflective surface prevents light absorption. Void cannot form without absorbed photons."),
        ("Magnet",   "Paper introduces 0.3mm air gap, increasing magnetic reluctance by 10⁴. Field collapses entirely.")
    ],
    "Scissors": [
        ("Paper",    "Scissors apply 4.2 N/mm² shear stress along paper's grain. Fracture propagates at 340 m/s."),
        ("Virus",    "Stainless steel scissors maintain pH 4.2 surface acidity. Viral protein coat denatures on contact."),
        ("Tornado",  "Scissors' aerofoil geometry generates counter-rotation vortex, cancelling tornado's angular momentum.")
    ],
    "Fire": [
        ("Paper",    "Paper's autoignition temperature (233°C) exceeded in 0.003 seconds. Combustion efficiency: 97%."),
        ("Scissors", "Fire oxidises steel scissors at 800°C, reducing tensile strength by 78%. Structural collapse imminent."),
        ("Ice",      "Fire radiates 50 kW/m², exceeding ice's latent heat of fusion (334 J/g). Phase transition: complete."),
        ("Void",     "Fire emits photons at 5×10¹⁴ Hz, filling the electromagnetic vacuum. Void structurally destabilised.")
    ],
    "Water": [
        ("Fire",      "Water's specific heat (4.18 J/g·K) absorbs fire's thermal output. Quench time: 0.8 seconds."),
        ("Rock",      "Water exploits rock's existing stress fractures via hydraulic wedging at 0.1 MPa. Erosion confirmed."),
        ("Lightning", "Water's ionic conductivity (500 μS/cm) redirects lightning current into ground. Dissipated safely."),
        ("Bomb",      "Water's incompressibility (bulk modulus 2.2 GPa) absorbs shockwave. Overpressure neutralised.")
    ],
    "Lightning": [
        ("Water",    "Wait — lightning ionises water into plasma at 30,000K. Conductivity advantage: nullified. Lightning wins."),
        ("Dragon",   "Lightning induces 80,000A through dragon's iron-rich scales. Faraday heating: lethal dose in 0.2ms."),
        ("Virus",    "UV radiation from lightning's plasma channel denatures viral RNA at 260nm wavelength. Sterilised."),
        ("Tornado",  "Lightning's plasma channel superheats tornado's core air by 6,000°C. Pressure differential collapses.")
    ],
    "Dragon": [
        ("Paper",    "Dragon's exhalation reaches 1,200°C, far exceeding paper's 233°C autoignition point. Instantaneous."),
        ("Void",     "Dragon's bioluminescent photon output (10¹⁸ lux) saturates void's absorption capacity. Overloaded."),
        ("Knife",    "Dragon's keratin scales (Mohs 7.5) deflect knife's steel edge (Mohs 6.5). Thermodynamic loss confirmed."),
        ("Ice",      "Dragon metabolises stored ATP at 840 kJ/mol, sustaining 1,100°C flame. Ice sublimation: 4 seconds.")
    ],
    "Virus": [
        ("Paper",    "Virus binds to paper's cellulose hydroxyl groups via hydrogen bonding. Structural integrity: degraded."),
        ("Rock",     "Virus secretes carbonic acid (H₂CO₃), dissolving rock's calcium carbonate matrix at 2mg/year. Inevitable."),
        ("Bomb",     "Virus infiltrates bomb's electronic detonator, mutating trigger algorithm. Detonation probability: 0%."),
        ("Magnet",   "Virus's iron-containing proteins align with magnetic field, jamming flux lines. Output reduced by 89%.")
    ],
    "Knife": [
        ("Paper",    "Knife applies 12 N/mm² concentrated shear load to paper's 0.1mm cross-section. Immediate failure."),
        ("Virus",    "Knife's chromium oxide surface layer (Cr₂O₃) maintains pH 3.8, denaturing viral lipid envelope instantly."),
        ("Water",    "Knife disrupts water's hydrogen bond network at point of contact, reducing surface tension to near zero.")
    ],
    "Tornado": [
        ("Rock",     "Tornado's 300km/h winds exert 1,800 Pa lift force, exceeding rock's 2.5g/cm³ density resistance. Airborne."),
        ("Water",    "Tornado's low-pressure core (870 hPa) causes explosive water vaporisation. Absorbed entirely."),
        ("Fire",     "Tornado's 10⁶ m³/s airflow supplies excess O₂, accelerating combustion, then disperses the ash at Mach 0.3."),
        ("Bomb",     "Tornado disperses bomb's chemical reactants below detonation concentration threshold. Rendered inert.")
    ],
    "Magnet": [
        ("Lightning", "Magnet's 1.5T field redirects lightning's charge carriers via Lorentz force. Vector deflection: 90°."),
        ("Knife",     "Magnet induces eddy currents in knife's steel, generating opposing magnetic field. Knife repelled at 4.7N."),
        ("Dragon",    "Dragon's haemoglobin iron (Fe²⁺) responds to magnet's gradient field at 0.5 T/m. Dragon: frozen mid-flight.")
    ],
    "Bomb": [
        ("Rock",     "Bomb's overpressure wave (35 PSI) exceeds rock's compressive strength (10,000 PSI)... barely. Bomb wins on technicality."),
        ("Ice",      "Bomb's exothermic detonation (3,000°C peak) sublimes ice directly to vapour. Phase change: instantaneous."),
        ("Void",     "Bomb releases 4.2 MJ of energy into void, exceeding void's vacuum energy density. Structural collapse."),
        ("Magnet",   "Bomb detonates before magnet's field (propagating at c) can redirect shrapnel. Time wins.")
    ],
    "Ice": [
        ("Water",    "Ice nucleation seeds surrounding water molecules via epitaxial crystal growth at -0.01°C. Fully frozen."),
        ("Tornado",  "Ice crystal formation increases air viscosity by 400%, reducing tornado's angular velocity to zero."),
        ("Void",     "Ice emits blackbody radiation at 273K, filling void's zero-point energy field. Void equilibrates and collapses.")
    ],
    "Sun": [
        ("Ice",      "Sun delivers 1,361 W/m² solar irradiance, exceeding ice's latent heat of fusion. Melt rate: 1.4mm/minute."),
        ("Void",     "Sun's luminosity (3.8×10²⁶ W) fills void with photons at 8-minute intervals. Void photon-saturated."),
        ("Water",    "Sun drives evaporation at 2.45 MJ/kg latent heat. Ocean evaporation rate: 1,400 km³/year. Wins eventually."),
        ("Virus",    "Solar UV-B radiation (280–315nm) causes thymine dimer formation in viral DNA. Replication: halted.")
    ],
    "Void": [
        ("Virus",    "Void's vacuum pressure (10⁻¹⁷ Pa) causes viral capsid to explosively decompress. Lysis: immediate."),
        ("Lightning","Void absorbs lightning's EM radiation across all frequencies. Energy density: undetectable post-absorption."),
        ("Ice",      "Void's 2.7K ambient temperature extracts ice's thermal energy via radiative cooling. Absolute zero achieved."),
        ("Magnet",   "Void's absence of permeability (μ=0) causes magnetic field lines to diverge infinitely. Field: dissipated.")
    ],
}

DRAW_LINES = [
    "Identical quantum states detected. Pauli exclusion principle prevents a winner.",
    "Both entities share the same molecular weight. Newton's third law produces net zero outcome.",
    "Thermodynamic equilibrium achieved instantaneously. Entropy change: 0 J/K. Draw.",
    "Interference pattern observed. Wave functions cancelled symmetrically. No outcome.",
    "Both parties emit at identical frequencies. Destructive interference: complete.",
]

FALLBACK_LINES = [
    "{b} emits a frequency that disrupts {p}'s electron orbital configuration. Molecular destabilisation confirmed.",
    "{b}'s entropic output (ΔS = +12 J/mol·K) exceeds {p}'s thermodynamic stability threshold.",
    "Spectral analysis shows {b} resonates at {p}'s natural frequency. Mechanical resonance: catastrophic.",
    "{b} introduces a 0.3 Tesla field perpendicular to {p}'s axis of motion. Lorentz deflection: fatal.",
]

def rps_outcome(player_idx, bot_idx):
    if player_idx == bot_idx:
        return "draw", random.choice(DRAW_LINES)
    pname = OPTIONS[player_idx][1]
    bname = OPTIONS[bot_idx][1]
    for beaten, reason in BEATS.get(pname, []):
        if beaten == bname:
            return "win", reason
    for beaten, reason in BEATS.get(bname, []):
        if beaten == pname:
            return "lose", reason
    # Undefined combo — bot wins with pseudo-science fallback
    reason = random.choice(FALLBACK_LINES).format(b=bname, p=pname)
    return "lose", reason

# ── Session init ──────────────────────────────────────────────────────────────
if "rps_result" not in st.session_state:
    st.session_state.rps_result = None
    st.session_state.rps_player = None
    st.session_state.rps_bot = None
    st.session_state.rps_reason = ""
    st.session_state.rps_wins = 0
    st.session_state.rps_losses = 0
    st.session_state.rps_draws = 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:28px 0 4px;'>
  <div style='font-family:Space Mono,monospace; font-size:2rem; font-weight:700; color:#3D3530;'>
    ⚗️ Chaos RPS
  </div>
  <div style='color:#8B7D6B; font-size:13px; margin-top:6px; font-style:italic;'>
    15 options. 100% peer-reviewed science. Probably.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Scoreboard ────────────────────────────────────────────────────────────────
rw = st.session_state.rps_wins
rl = st.session_state.rps_losses
rd = st.session_state.rps_draws
st.markdown(f"""
<div style='text-align:center; margin-bottom:20px;'>
    <span class='score-pill'>🏆 You: {rw}</span>
    <span class='score-pill'>🤖 Bot: {rl}</span>
    <span class='score-pill'>🤝 Draws: {rd}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:#8B7D6B; font-size:14px; margin-bottom:8px;'>
    Pick your element. The science will explain itself.
</p>
""", unsafe_allow_html=True)

# ── Option Grid ───────────────────────────────────────────────────────────────
chosen = None
for row in range(5):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        if idx < len(OPTIONS):
            emoji, name = OPTIONS[idx]
            with cols[col]:
                if st.button(f"{emoji}\n{name}", key=f"rps_{idx}", use_container_width=True):
                    chosen = idx

if chosen is not None:
    bot_idx = random.randint(0, len(OPTIONS) - 1)
    result, reason = rps_outcome(chosen, bot_idx)
    st.session_state.rps_player = chosen
    st.session_state.rps_bot = bot_idx
    st.session_state.rps_result = result
    st.session_state.rps_reason = reason
    if result == "win":   st.session_state.rps_wins += 1
    elif result == "lose": st.session_state.rps_losses += 1
    else:                  st.session_state.rps_draws += 1
    st.rerun()

# ── Result Card ───────────────────────────────────────────────────────────────
if st.session_state.rps_result is not None:
    p      = st.session_state.rps_player
    b      = st.session_state.rps_bot
    res    = st.session_state.rps_result
    reason = st.session_state.rps_reason

    p_emoji, p_name = OPTIONS[p]
    b_emoji, b_name = OPTIONS[b]

    colors = {
        "win":  ("#F0F7F2", "#B8D4C0", "You win! 🎉"),
        "lose": ("#FDF5F5", "#DDB8B8", "Bot wins. 🤖"),
        "draw": ("#FAFAF5", "#D4D4B0", "It's a draw! 🤝"),
    }
    bg, border, label = colors[res]

    st.markdown(f"""
    <div style='background:{bg}; border:2px solid {border}; border-radius:20px;
                padding:28px 24px; text-align:center; margin-top:24px;'>
        <div style='font-size:3.2rem; margin-bottom:10px; letter-spacing:8px;'>
            {p_emoji} <span style='color:#C9BFB0; font-size:1.4rem;'>vs</span> {b_emoji}
        </div>
        <div style='font-size:13px; color:#8B7D6B; margin-bottom:8px;'>
            You played <strong>{p_name}</strong> &nbsp;·&nbsp; Bot played <strong>{b_name}</strong>
        </div>
        <div style='font-size:1.5rem; font-weight:900; color:#3D3530; margin:12px 0 16px;
                    font-family:Space Mono,monospace;'>
            {label}
        </div>
        <div style='font-size:12.5px; color:#6B6055; font-style:italic;
                    background:rgba(0,0,0,0.04); border-radius:12px;
                    padding:12px 16px; line-height:1.6; text-align:left;'>
            🔬 <strong>Scientific explanation:</strong> {reason}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Reset ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Reset Scores", use_container_width=True):
        st.session_state.rps_wins = 0
        st.session_state.rps_losses = 0
        st.session_state.rps_draws = 0
        st.session_state.rps_result = None
        st.rerun()

st.markdown("""
<p style='text-align:center; color:#C9BFB0; font-size:11px; margin-top:20px;'>
    All explanations are scientifically accurate. We checked. Briefly.
</p>
""", unsafe_allow_html=True)
