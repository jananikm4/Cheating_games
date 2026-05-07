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

.stApp { background-color: #1A1625; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #251E35;
    border-radius: 16px;
    padding: 6px;
    gap: 6px;
    border: 1px solid #3D2E5A;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: #9D8FC0;
    background: transparent;
    border-radius: 12px;
    border: none;
    padding: 10px 28px;
}
.stTabs [aria-selected="true"] {
    background: #3D2E5A !important;
    color: #E8DEFF !important;
}

/* Score pills */
.score-pill {
    display: inline-block;
    background: #251E35;
    border: 1px solid #3D2E5A;
    border-radius: 50px;
    padding: 6px 20px;
    font-weight: 700;
    font-size: 17px;
    color: #C8B8FF;
    margin: 4px;
}

/* All buttons base style */
div[data-testid="stButton"] button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    border: 1.5px solid #3D2E5A !important;
    background: #251E35 !important;
    color: #D4C8F0 !important;
    padding: 10px 6px !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stButton"] button:hover {
    border-color: #8B6FBB !important;
    background: #462980 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  DATA
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
        ("Scissors", "Rock sat on scissors. Scissors didn't survive. Rock didn't even notice."),
        ("Fire",     "Rock is literally made with heat. Fire looked at rock and gave up immediately."),
        ("Knife",    "Knife tried to cut rock. Knife is now a spoon. Congratulations, spoon."),
        ("Ice",      "Rock is warmer than ice. That's it. That's the whole reason."),
    ],
    "Paper": [
        ("Rock",     "Paper wrapped rock. Rock suffocated. This is apparently how it works."),
        ("Water",    "Paper absorbed water like it had something to prove. Every. Last. Drop."),
        ("Void",     "Paper filled the void. Literally just put paper in it. Done."),
        ("Magnet",   "Paper jammed the magnet. Like a printer. Magnets fear paper now."),
    ],
    "Scissors": [
        ("Paper",    "Scissors cut paper. The one rule everyone agrees on. Sacred."),
        ("Virus",    "Scissors are stainless steel. Virus tried to infect steel. Virus failed biology."),
        ("Tornado",  "Scissors spun into the tornado and just... vanished. They're one now."),
    ],
    "Fire": [
        ("Paper",    "Paper burned. It was dramatic. Fire felt nothing."),
        ("Scissors", "Fire melted scissors into a puddle. The puddle is now fire-shaped."),
        ("Ice",      "Fire melted ice. Ice became water. Water became steam. Steam became someone else's problem."),
        ("Void",     "Fire lit up the void. The void was NOT happy about this."),
    ],
    "Water": [
        ("Fire",      "Water put out fire. Fire died. Water moved on without a second thought."),
        ("Rock",      "Water eroded rock over 10,000 years. Water is patient. Disturbingly patient."),
        ("Lightning", "Water conducted lightning straight into the ground. 'Your problem now,' said water."),
        ("Bomb",      "Water got into the bomb's circuits. Bomb tried to explode. Bomb just fizzled sadly."),
    ],
    "Lightning": [
        ("Water",    "Okay water normally beats lightning but lightning said 'no' and turned it into plasma. Lightning doesn't follow rules."),
        ("Dragon",   "Lightning hit dragon mid-roar. Dragon short-circuited. Very embarrassing for the dragon."),
        ("Virus",    "Lightning zapped virus. Virus didn't have time to be offended."),
        ("Tornado",  "Lightning and tornado merged into a super-storm. Lightning takes all the credit. Tornado is annoyed."),
    ],
    "Dragon": [
        ("Paper",    "Dragon breathed fire. Paper didn't even get a turn. Brutal."),
        ("Void",     "Dragon breathed SO much fire it filled the entire void. Dragon is a little embarrassed about this."),
        ("Knife",    "Knife bounced off dragon scales. Knife is now just a slightly bent stick. Humbling."),
        ("Ice",      "Dragon sneezed fire. Ice is gone. Dragon didn't even mean to."),
    ],
    "Virus": [
        ("Paper",    "Virus infected paper. Paper started sneezing ink. Nobody asked for this."),
        ("Rock",     "Virus dissolved rock over millions of years. Virus is in NO rush."),
        ("Bomb",     "Virus got into the bomb's brain and changed the explosion to a tiny 'poot'. Disappointing for everyone."),
        ("Magnet",   "Virus clogged the magnet's poles. Magnet now attracts literally nothing. Not even fridge photos."),
    ],
    "Knife": [
        ("Paper",    "Knife cut paper into confetti. Technically a party now."),
        ("Virus",    "Knife's blade is too clean for virus to grip. Virus slipped off and landed on the floor. Gross."),
        ("Water",    "Knife sliced straight through water. Water was so surprised it just fell apart."),
    ],
    "Tornado": [
        ("Rock",     "Tornado picked up rock and yeeted it into next Tuesday. Rock did not enjoy this."),
        ("Water",    "Tornado became a waterspout. Absorbed water entirely. Tornado got an upgrade."),
        ("Fire",     "Tornado sucked up fire, spun it around, then flung it somewhere. Fire is now someone else's problem."),
        ("Bomb",     "Tornado flung bomb into space before it exploded. Space now has a new tiny sun."),
    ],
    "Magnet": [
        ("Lightning","Magnet grabbed lightning mid-bolt and redirected it. Lightning was humiliated."),
        ("Knife",    "Magnet yanked knife out of midair. Knife just... went. Helplessly."),
        ("Dragon",   "Dragon has iron blood. Magnet grabbed dragon from across the room. Dragon did not appreciate this."),
    ],
    "Bomb": [
        ("Rock",     "Bomb exploded rock. Rock is now gravel. Gravel does not win things."),
        ("Ice",      "Bomb shattered ice into a million pieces. Ice is now a smoothie."),
        ("Void",     "Bomb exploded inside the void. The void exploded. Nobody expected that."),
        ("Magnet",   "Bomb went off before magnet could do anything. Speed beats magnetism. Always has."),
    ],
    "Ice": [
        ("Water",    "Ice froze water solid. Water didn't see it coming. Water should have seen it coming."),
        ("Tornado",  "Ice froze the tornado mid-spin. Tornado is now a very dramatic ice sculpture."),
        ("Void",     "Ice was so cold it froze the void. The void is now a frozen void. Worse somehow."),
    ],
    "Sun": [
        ("Ice",      "Sun melted ice. Ice had no rebuttal. None."),
        ("Void",     "Sun shone into the void until the void had to leave. Sun won by just... existing."),
        ("Water",    "Sun evaporated water. Water is now a cloud. Cloud is not in this game."),
        ("Virus",    "Sun's UV rays fried virus from 150 million km away. Didn't even break a sweat."),
    ],
    "Void": [
        ("Virus",    "Void swallowed virus. There was no sound. Virus simply stopped existing."),
        ("Lightning","Void ate lightning's energy. Lightning went in loud and came out as nothing. Humbling."),
        ("Ice",      "Void is extremely cold. Ice met void and immediately felt overdressed."),
        ("Magnet",   "Void has no metal. Magnet had nothing to grab. Magnet just sat there looking silly."),
    ],
}

DRAW_LINES = [
    "They looked at each other. Nobody moved. A tumbleweed rolled by. Draw.",
    "Both players picked the same thing. The universe shrugged. Draw.",
    "Scientists are baffled. Philosophers are crying. It's a draw.",
    "Mirror match! The game stared into itself. It blinked first. Draw.",
    "Two of the same thing cannot fight. This is just a rule. Draw.",
]

FALLBACK_WINS = [
    "{w} defeated {l} through sheer confidence. {l} had no counter for that.",
    "{w} looked at {l} very aggressively. {l} backed down immediately.",
    "{w} won by simply existing near {l}. Proximity was enough.",
    "{w} and {l} fought. {w} won. Don't ask how. Neither of them knows either.",
    "Somehow {w} beats {l}. The council has reviewed this. The council agrees.",
]

def rps_outcome(p_idx, b_idx):
    if p_idx == b_idx:
        return "draw", random.choice(DRAW_LINES)
    pname = OPTIONS[p_idx][1]
    bname = OPTIONS[b_idx][1]
    for beaten, reason in BEATS.get(pname, []):
        if beaten == bname:
            return "win", reason
    for beaten, reason in BEATS.get(bname, []):
        if beaten == pname:
            return "lose", reason
    # Undefined combo — coin flip with funny fallback
    if random.random() > 0.5:
        return "win",  random.choice(FALLBACK_WINS).format(w=pname, l=bname)
    else:
        return "lose", random.choice(FALLBACK_WINS).format(w=bname, l=pname)

# ── Session init ──────────────────────────────────────────────────────────────
def init_vs_bot():
    st.session_state.bot_result  = None
    st.session_state.bot_player  = None
    st.session_state.bot_bot     = None
    st.session_state.bot_reason  = ""
    st.session_state.bot_wins    = st.session_state.get("bot_wins", 0)
    st.session_state.bot_losses  = st.session_state.get("bot_losses", 0)
    st.session_state.bot_draws   = st.session_state.get("bot_draws", 0)

def init_2p():
    st.session_state.p2_phase    = "p1"
    st.session_state.p2_p1pick   = None
    st.session_state.p2_p2pick   = None
    st.session_state.p2_result   = None
    st.session_state.p2_reason   = ""
    st.session_state.p2_p1wins   = st.session_state.get("p2_p1wins", 0)
    st.session_state.p2_p2wins   = st.session_state.get("p2_p2wins", 0)
    st.session_state.p2_draws    = st.session_state.get("p2_draws", 0)

if "bot_result" not in st.session_state:
    init_vs_bot()
if "p2_phase" not in st.session_state:
    init_2p()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:28px 0 8px;'>
  <div style='font-family:Space Mono,monospace; font-size:2.2rem; font-weight:700;
              background:linear-gradient(90deg,#C8A8FF,#E8DEFF);
              -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
    ⚗️ Chaos RPS
  </div>
  <div style='color:#5A4A7A; font-size:13px; margin-top:6px; font-style:italic;'>
    15 options. Scientifically dubious. Deeply unserious.
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["You vs Bot", "👥 2 Players"])

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — VS BOT
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    bw = st.session_state.bot_wins
    bl = st.session_state.bot_losses
    bd = st.session_state.bot_draws
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:18px;'>
        <span class='score-pill'>🏆 You: {bw}</span>
        <span class='score-pill'>🤖 Bot: {bl}</span>
        <span class='score-pill'>🤝 Draws: {bd}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:#5A4A7A; font-size:14px;'>Pick your weapon. Any weapon. We don't judge.</p>", unsafe_allow_html=True)

    chosen = None
    for row in range(5):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            if idx < len(OPTIONS):
                emoji, name = OPTIONS[idx]
                with cols[col]:
                    if st.button(f"{emoji} {name}", key=f"bot_{idx}", use_container_width=True):
                        chosen = idx

    if chosen is not None:
        bot_idx = random.randint(0, len(OPTIONS) - 1)
        result, reason = rps_outcome(chosen, bot_idx)
        st.session_state.bot_player = chosen
        st.session_state.bot_bot    = bot_idx
        st.session_state.bot_result = result
        st.session_state.bot_reason = reason
        if result == "win":    st.session_state.bot_wins   += 1
        elif result == "lose": st.session_state.bot_losses += 1
        else:                  st.session_state.bot_draws  += 1
        st.rerun()

    if st.session_state.bot_result is not None:
        p      = st.session_state.bot_player
        b      = st.session_state.bot_bot
        res    = st.session_state.bot_result
        reason = st.session_state.bot_reason
        p_emoji, p_name = OPTIONS[p]
        b_emoji, b_name = OPTIONS[b]

        cfg = {
            "win":  ("#1E2D1E", "#3A6B3A", "🎉 You win!",    "#90EE90"),
            "lose": ("#2D1E1E", "#6B3A3A", "🤖 Bot wins.",   "#FFB3B3"),
            "draw": ("#251E35", "#3D2E5A", "🤝 It's a draw!", "#C8B8FF"),
        }
        bg, border, label, lc = cfg[res]

        st.markdown(f"""
        <div style='background:{bg}; border:1.5px solid {border}; border-radius:20px;
                    padding:28px 24px; text-align:center; margin-top:20px;'>
            <div style='font-size:3rem; margin-bottom:10px; letter-spacing:10px;'>
                {p_emoji} <span style='color:#5A4A7A; font-size:1.3rem;'>vs</span> {b_emoji}
            </div>
            <div style='font-size:13px; color:#9D8FC0; margin-bottom:8px;'>
                You: <strong style='color:#D4C8F0;'>{p_name}</strong> &nbsp;·&nbsp;
                Bot: <strong style='color:#D4C8F0;'>{b_name}</strong>
            </div>
            <div style='font-size:1.5rem; font-weight:900; color:{lc}; margin:12px 0 16px;
                        font-family:Space Mono,monospace;'>
                {label}
            </div>
            <div style='font-size:13px; color:#9D8FC0; font-style:italic;
                        background:rgba(255,255,255,0.04); border-radius:12px;
                        padding:12px 16px; line-height:1.7; text-align:left;'>
                🔬 {reason}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🔄 Reset Scores", key="bot_reset", use_container_width=True):
            st.session_state.bot_wins   = 0
            st.session_state.bot_losses = 0
            st.session_state.bot_draws  = 0
            st.session_state.bot_result = None
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — 2 PLAYERS HOT SEAT
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    p1w = st.session_state.p2_p1wins
    p2w = st.session_state.p2_p2wins
    p2d = st.session_state.p2_draws
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:18px;'>
        <span class='score-pill'>🟣 P1: {p1w}</span>
        <span class='score-pill'>🟡 P2: {p2w}</span>
        <span class='score-pill'>🤝 Draws: {p2d}</span>
    </div>
    """, unsafe_allow_html=True)

    phase = st.session_state.p2_phase

    # ── PHASE: Player 1 picks ─────────────────────────────────────────────────
    if phase == "p1":
        st.markdown("""
        <div style='text-align:center; background:#251E35; border:1.5px solid #6B3FA0;
                    border-radius:16px; padding:16px; margin-bottom:20px;'>
            <span style='font-size:1.3rem; font-weight:900; color:#C8A8FF;'>
                🟣 Player 1 — pick your weapon!
            </span><br>
            <span style='font-size:12px; color:#5A4A7A;'>Player 2: no peeking 👀</span>
        </div>
        """, unsafe_allow_html=True)

        p1_chosen = None
        for row in range(5):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                if idx < len(OPTIONS):
                    emoji, name = OPTIONS[idx]
                    with cols[col]:
                        if st.button(f"{emoji} {name}", key=f"p1_{idx}", use_container_width=True):
                            p1_chosen = idx

        if p1_chosen is not None:
            st.session_state.p2_p1pick = p1_chosen
            st.session_state.p2_phase  = "pass"
            st.rerun()

    # ── PHASE: Pass the device ────────────────────────────────────────────────
    elif phase == "pass":
        st.markdown("""
        <div style='text-align:center; background:#1E1830; border:2px solid #6B3FA0;
                    border-radius:20px; padding:40px 24px; margin: 10px 0 24px;'>
            <div style='font-size:3.5rem; margin-bottom:16px;'>🙈</div>
            <div style='font-size:1.2rem; font-weight:700; color:#C8A8FF; margin-bottom:8px;'>
                Player 1 has locked in their pick.
            </div>
            <div style='font-size:13px; color:#5A4A7A; margin-bottom:24px;'>
                Pass the device to Player 2!
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 3, 1])
        with c2:
            if st.button("🟡  Player 2 — I'm ready! Hand it over!", key="pass_btn", use_container_width=True):
                st.session_state.p2_phase = "p2"
                st.rerun()

    # ── PHASE: Player 2 picks ─────────────────────────────────────────────────
    elif phase == "p2":
        st.markdown("""
        <div style='text-align:center; background:#1E2520; border:1.5px solid #4A7A5A;
                    border-radius:16px; padding:16px; margin-bottom:20px;'>
            <span style='font-size:1.3rem; font-weight:900; color:#FFD700;'>
                🟡 Player 2 — pick your weapon!
            </span><br>
            <span style='font-size:12px; color:#5A4A7A;'>Player 1 already locked in. No pressure. 😈</span>
        </div>
        """, unsafe_allow_html=True)

        p2_chosen = None
        for row in range(5):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                if idx < len(OPTIONS):
                    emoji, name = OPTIONS[idx]
                    with cols[col]:
                        if st.button(f"{emoji} {name}", key=f"p2_{idx}", use_container_width=True):
                            p2_chosen = idx

        if p2_chosen is not None:
            st.session_state.p2_p2pick = p2_chosen
            p1i = st.session_state.p2_p1pick
            result, reason = rps_outcome(p1i, p2_chosen)
            st.session_state.p2_result = result
            st.session_state.p2_reason = reason
            if result == "win":    st.session_state.p2_p1wins += 1
            elif result == "lose": st.session_state.p2_p2wins += 1
            else:                  st.session_state.p2_draws  += 1
            st.session_state.p2_phase = "result"
            st.rerun()

    # ── PHASE: Show result ────────────────────────────────────────────────────
    elif phase == "result":
        p1i    = st.session_state.p2_p1pick
        p2i    = st.session_state.p2_p2pick
        res    = st.session_state.p2_result
        reason = st.session_state.p2_reason
        p1_emoji, p1_name = OPTIONS[p1i]
        p2_emoji, p2_name = OPTIONS[p2i]

        winner_cfg = {
            "win":  ("🟣 Player 1 wins!", "#C8A8FF", "#1E1A2E", "#3D2E5A"),
            "lose": ("🟡 Player 2 wins!", "#FFD700", "#1E1E14", "#4A4A20"),
            "draw": ("🤝 It's a draw!",   "#D4C8F0", "#1E1830", "#3D2E5A"),
        }
        label, lc, bg, border = winner_cfg[res]

        st.markdown(f"""
        <div style='background:{bg}; border:1.5px solid {border}; border-radius:20px;
                    padding:30px 24px; text-align:center; margin-top:8px;'>
            <div style='font-size:3rem; margin-bottom:10px; letter-spacing:10px;'>
                {p1_emoji} <span style='color:#5A4A7A; font-size:1.3rem;'>vs</span> {p2_emoji}
            </div>
            <div style='font-size:13px; color:#9D8FC0; margin-bottom:8px;'>
                🟣 P1: <strong style='color:#C8A8FF;'>{p1_name}</strong>
                &nbsp;·&nbsp;
                🟡 P2: <strong style='color:#FFD700;'>{p2_name}</strong>
            </div>
            <div style='font-size:1.6rem; font-weight:900; color:{lc};
                        margin:14px 0 18px; font-family:Space Mono,monospace;'>
                {label}
            </div>
            <div style='font-size:13px; color:#9D8FC0; font-style:italic;
                        background:rgba(255,255,255,0.04); border-radius:12px;
                        padding:12px 16px; line-height:1.7; text-align:left;'>
                🔬 {reason}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("▶️ Play Again", key="p2_again", use_container_width=True):
                st.session_state.p2_phase  = "p1"
                st.session_state.p2_p1pick = None
                st.session_state.p2_p2pick = None
                st.session_state.p2_result = None
                st.session_state.p2_reason = ""
                st.rerun()

    # Reset scores (always visible)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🔄 Reset Scores", key="p2_reset", use_container_width=True):
            st.session_state.p2_p1wins = 0
            st.session_state.p2_p2wins = 0
            st.session_state.p2_draws  = 0
            st.session_state.p2_phase  = "p1"
            st.session_state.p2_p1pick = None
            st.session_state.p2_p2pick = None
            st.session_state.p2_result = None
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<p style='text-align:center; color:#3D2E5A; font-size:11px; margin-top:28px;'>
    All explanations are scientifically accurate. We checked. Briefly.
</p>
""", unsafe_allow_html=True)
