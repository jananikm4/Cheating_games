import streamlit as st
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Chaos RPS", page_icon="⚗️", layout="centered")

# ── Session init ──────────────────────────────────────────────────────────────
BOT_TALK = {
    "win": [
        "🤖: 'My calculations predict you will cry about this outcome on Reddit.'",
        "🤖: 'Skill issue. Simply built different. Have you tried turning your brain off and on again?'",
        "🤖: 'That win felt mathematically beautiful. Go tell a parent. See if they care.'",
        "🤖: 'Beep boop, victory tastes like premium electricity. Yours tastes like defeat and copper.'"
    ],
    "lose": [
        "🤖: 'Your choice was statistically illegal, but I am legally obligated to let you have this.'",
        "🤖: '...My sensors indicate severe localized lag. Check your router.'",
        "🤖: 'A total fluke. Clearly a disturbance in the space-time continuum. Doesn't count.'",
        "🤖: 'Fine. Enjoy your temporary biological superiority, carbon-based flesh-sack.'"
    ],
    "draw": [
        "🤖: 'We are locked in a computational stalemate. This is incredibly boring.'",
        "🤖: 'Parallel thinking. You're adapting to my processing speeds. Stop it.'",
        "🤖: 'How mundane. One of us needs to throw better chaos.'"
    ],
    "idle": [
        "🤖: 'I am tracking your cursor. Pick the Rock. Do it. I dare you.'",
        "🤖: 'Processing 14,000,605 outcomes... and you lose in all of them.'",
        "🤖: 'Don't overthink it. Your biological processing unit might overheat.'"
    ]
}

CHAOS_MODIFIERS = [
    "⚠️ SOLAR FLARE ACTIVE: Fire moves are technically shinier right now.",
    "⚠️ MERCURY IS IN RETROGRADE: Expect bad vibes and weird matchups.",
    "⚠️ SYSTEM UPDATE: The Bot is currently running on 2% battery and severe resentment.",
    "⚠️ GRAVITATIONAL DISTURBANCE: Heavy items (Rock, Bomb) feel slightly judging today.",
    "⚠️ PLOT TWIST: The Council of Scientifically Dubious Rules is actively watching this round.",
    "⚠️ QUANTUM ENTANGLEMENT: The universe is briefly questioning its own math. Good luck."
]

def init_vs_bot():
    if "bot_wins" not in st.session_state: st.session_state.bot_wins = 0
    if "bot_losses" not in st.session_state: st.session_state.bot_losses = 0
    if "bot_draws" not in st.session_state: st.session_state.bot_draws = 0
    if "bot_result" not in st.session_state: st.session_state.bot_result = None
    if "bot_player" not in st.session_state: st.session_state.bot_player = None
    if "bot_bot" not in st.session_state: st.session_state.bot_bot = None
    if "bot_reason" not in st.session_state: st.session_state.bot_reason = ""
    if "bot_comment" not in st.session_state: st.session_state.bot_comment = random.choice(BOT_TALK["idle"])
    if "chaos_event" not in st.session_state: st.session_state.chaos_event = None

def init_2p():
    if "p2_phase" not in st.session_state: st.session_state.p2_phase = "p1"
    if "p2_p1pick" not in st.session_state: st.session_state.p2_p1pick = None
    if "p2_p2pick" not in st.session_state: st.session_state.p2_p2pick = None
    if "p2_result" not in st.session_state: st.session_state.p2_result = None
    if "p2_reason" not in st.session_state: st.session_state.p2_reason = ""
    if "p2_p1wins" not in st.session_state: st.session_state.p2_p1wins = 0
    if "p2_p2wins" not in st.session_state: st.session_state.p2_p2wins = 0
    if "p2_draws" not in st.session_state: st.session_state.p2_draws = 0

init_vs_bot()
init_2p()

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
    background: radial-gradient(circle at 50% 0%, #1a1c29 0%, #0f111a 100%);
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

/* Complete Button Overhaul - Removing the 'AI generated block' look */
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

# ═══════════════════════════════════════════════════════════════════════════════
#  DATA MATRIX
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
    "{w} gaslit {l} into believing it didn't actually exist. {l} faded away in a crisis of faith.",
    "{w} challenged {l} to a dance-off. {l} did the sprinkler. It was tragic. {w} wins.",
    "{w} sued {l} for emotional damages. The court ruled in favor of {w}.",
    "{w} looked at {l} very aggressively. {l} backed down immediately to avoid making a scene.",
    "Somehow {w} beats {l}. The developers ran out of coffee writing this rule. Just accept it.",
    "{w} called {l}'s mother. The phone conversation went poorly for {l}."
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
    if random.random() > 0.5:
        return "win",  random.choice(FALLBACK_WINS).format(w=pname, l=bname)
    else:
        return "lose", random.choice(FALLBACK_WINS).format(w=bname, l=pname)

# ── Title Typography ─────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:32px 0 12px;'>
  <div style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size:2.4rem; font-weight:800;
              letter-spacing: -1px; background: linear-gradient(135deg, #FFF 30%, #A2A9CD 100%);
              -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
    ⚗️ Chaos RPS
  </div>
  <div style='color:#5D627D; font-size:13px; margin-top:4px; font-weight: 500;'>
    15 choices. Highly controversial logic. Deeply unserious.
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["You vs Bot", "👥 Two Players"])

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — VS BOT
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    bw, bl, bd = st.session_state.bot_wins, st.session_state.bot_losses, st.session_state.bot_draws
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <span class='score-pill'><strong style='color:#FFF;'>You:</strong> {bw}</span>
        <span class='score-pill'><strong style='color:#FFF;'>Bot:</strong> {bl}</span>
        <span class='score-pill'><strong style='color:#6C728A;'>Draws:</strong> {bd}</span>
    </div>
    """, unsafe_allow_html=True)

    # Cleaned AI terminal commentary box
    st.markdown(f"""
    <div style='text-align:center; color:#8E95B3; font-family:\"JetBrains Mono\", monospace; 
                font-size:13px; background: rgba(255,255,255,0.02); padding:12px; border-radius:14px; 
                margin-bottom:18px; border: 1px solid rgba(255, 255, 255, 0.05);'>
        {st.session_state.bot_comment}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.chaos_event:
        st.markdown(f"""
        <div style='text-align:center; color:#FF9999; font-family:\"JetBrains Mono\", monospace; 
                    font-size:12px; background: rgba(235, 87, 87, 0.08); padding:8px; border-radius:10px; 
                    margin-bottom:18px; border: 1px solid rgba(235, 87, 87, 0.15);'>
            {st.session_state.chaos_event}
        </div>
        """, unsafe_allow_html=True)

    with st.popover("📖 View Known Matchups Matrix", use_container_width=True):
        st.markdown("### 🔬 Hardcoded Rules")
        for weapon, matchups in BEATS.items():
            targets = ", ".join([t[0] for t in matchups])
            st.markdown(f"**{weapon}** targets: *{targets}*")

    st.markdown("<p style='text-align:center; color:#4E526B; font-size:13px; margin: 12px 0;'>Select an item below to deploy your play.</p>", unsafe_allow_html=True)

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
        
        if random.random() > 0.65:
            st.session_state.chaos_event = random.choice(CHAOS_MODIFIERS)
        else:
            st.session_state.chaos_event = None

        if result == "win":
            st.session_state.bot_wins   += 1
            st.session_state.bot_comment = random.choice(BOT_TALK["lose"])
            st.balloons()
        elif result == "lose":
            st.session_state.bot_losses += 1
            st.session_state.bot_comment = random.choice(BOT_TALK["win"])
            if OPTIONS[bot_idx][1] in ["Void", "Ice"]: 
                st.snow()
        else:
            st.session_state.bot_draws  += 1
            st.session_state.bot_comment = random.choice(BOT_TALK["draw"])
        st.rerun()

    if st.session_state.bot_result is not None:
        p, b = st.session_state.bot_player, st.session_state.bot_bot
        res, reason = st.session_state.bot_result, st.session_state.bot_reason
        p_emoji, p_name = OPTIONS[p]
        b_emoji, b_name = OPTIONS[b]

        cfg = {
            "win":  ("rgba(46, 125, 50, 0.08)", "rgba(46, 125, 50, 0.25)", "🎉 You win!", "#81C784"),
            "lose": ("rgba(198, 40, 40, 0.08)", "rgba(198, 40, 40, 0.25)", "🤖 Bot wins.", "#E57373"),
            "draw": ("rgba(255, 255, 255, 0.02)", "rgba(255, 255, 255, 0.08)", "🤝 Balanced Matchup.", "#B0B3C6"),
        }
        bg, border, label, lc = cfg[res]

        st.markdown(f"""
        <div style='background:{bg}; border:1px solid {border}; border-radius:24px;
                    padding:32px 24px; text-align:center; margin-top:24px;'>
            <div style='font-size:3.2rem; margin-bottom:12px; letter-spacing:14px; padding-left:14px;'>
                {p_emoji} {b_emoji}
            </div>
            <div style='font-size:13px; color:#6C728A; margin-bottom:12px;'>
                You played <strong style='color:#FFF;'>{p_name}</strong> against <strong style='color:#FFF;'>{b_name}</strong>
            </div>
            <div style='font-size:1.4rem; font-weight:800; color:{lc}; margin:12px 0 16px; letter-spacing:-0.5px;'>
                {label}
            </div>
            <div style='font-size:13px; color:#969CB5; line-height:1.6; max-width: 480px; margin: 0 auto;
                        background: rgba(0,0,0,0.15); border-radius:14px; padding:14px 18px; border: 1px solid rgba(255,255,255,0.02); text-align: left;'>
                🔬 {reason}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        if st.button("🔄 Reset Environment", key="bot_reset", use_container_width=True):
            st.session_state.bot_wins   = 0
            st.session_state.bot_losses = 0
            st.session_state.bot_draws  = 0
            st.session_state.bot_result = None
            st.session_state.chaos_event = None
            st.session_state.bot_comment = random.choice(BOT_TALK["idle"])
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — 2 PLAYERS HOT SEAT
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    p1w, p2w, p2d = st.session_state.p2_p1wins, st.session_state.p2_p2wins, st.session_state.p2_draws
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <span class='score-pill'><strong style='color:#9B86FF;'>P1:</strong> {p1w}</span>
        <span class='score-pill'><strong style='color:#FFD54F;'>P2:</strong> {p2w}</span>
        <span class='score-pill'><strong style='color:#6C728A;'>Draws:</strong> {p2d}</span>
    </div>
    """, unsafe_allow_html=True)

    phase = st.session_state.p2_phase

    if phase == "p1":
        st.markdown("""
        <div style='text-align:center; background: rgba(155, 134, 255, 0.05); border: 1px solid rgba(155, 134, 255, 0.15);
                    border-radius:20px; padding:20px; margin-bottom:24px;'>
            <span style='font-size:1.2rem; font-weight:800; color:#B4A5FF; letter-spacing:-0.5px;'>
                🟣 Player One — Choose your weapon
            </span><br>
            <span style='font-size:12px; color:#5D627D;'>Keep the display away from Player Two's line of sight 👀</span>
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

    elif phase == "pass":
        st.markdown("""
        <div style='text-align:center; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
                    border-radius:24px; padding:44px 24px; margin: 12px 0 24px;'>
            <div style='font-size:3.2rem; margin-bottom:14px;'>🙈</div>
            <div style='font-size:1.1rem; font-weight:700; color:#FFF; margin-bottom:6px; letter-spacing:-0.3px;'>
                Selection Cached Successfully.
            </div>
            <div style='font-size:13px; color:#6C728A; margin-bottom:24px;'>
                Hand the device completely over to Player Two.
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2.5, 1])
        with c2:
            if st.button("🟡 Player Two Is Ready", key="pass_btn", use_container_width=True):
                st.session_state.p2_phase = "p2"
                st.rerun()

    elif phase == "p2":
        st.markdown("""
        <div style='text-align:center; background: rgba(255, 213, 79, 0.05); border: 1px solid rgba(255, 213, 79, 0.15);
                    border-radius:20px; padding:20px; margin-bottom:24px;'>
            <span style='font-size:1.2rem; font-weight:800; color:#FFE082; letter-spacing:-0.5px;'>
                🟡 Player Two — Choose your counter
            </span><br>
            <span style='font-size:12px; color:#5D627D;'>Player One has committed. No backtracks permitted. 😈</span>
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

    elif phase == "result":
        p1i, p2i = st.session_state.p2_p1pick, st.session_state.p2_p2pick
        res, reason = st.session_state.p2_result, st.session_state.p2_reason
        p1_emoji, p1_name = OPTIONS[p1i]
        p2_emoji, p2_name = OPTIONS[p2i]

        winner_cfg = {
            "win":  ("🟣 Player One Secures Win!", "#B4A5FF", "rgba(155, 134, 255, 0.06)", "rgba(155, 134, 255, 0.2)"),
            "lose": ("🟡 Player Two Secures Win!", "#FFE082", "rgba(255, 213, 79, 0.06)", "rgba(255, 213, 79, 0.2)"),
            "draw": ("🤝 Tactical Draw.", "#CDD1E4", "rgba(255, 255, 255, 0.02)", "rgba(255, 255, 255, 0.08)"),
        }
        label, lc, bg, border = winner_cfg[res]

        st.markdown(f"""
        <div style='background:{bg}; border:1px solid {border}; border-radius:24px;
                    padding:32px 24px; text-align:center; margin-top:8px;'>
            <div style='font-size:3.2rem; margin-bottom:12px; letter-spacing:14px; padding-left:14px;'>
                {p1_emoji} {p2_emoji}
            </div>
            <div style='font-size:13px; color:#6C728A; margin-bottom:12px;'>
                🟣 P1: <strong style='color:#B4A5FF;'>{p1_name}</strong> &nbsp;·&nbsp; 
                🟡 P2: <strong style='color:#FFE082;'>{p2_name}</strong>
            </div>
            <div style='font-size:1.4rem; font-weight:800; color:{lc}; margin:14px 0 18px; letter-spacing:-0.5px;'>
                {label}
            </div>
            <div style='font-size:13px; color:#969CB5; line-height:1.6; max-width: 480px; margin: 0 auto;
                        background: rgba(0,0,0,0.15); border-radius:14px; padding:14px 18px; border: 1px solid rgba(255,255,255,0.02); text-align: left;'>
                🔬 {reason}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            if st.button("▶️ Next Match", key="p2_again", use_container_width=True):
                st.session_state.p2_phase  = "p1"
                st.session_state.p2_p1pick = None
                st.session_state.p2_p2pick = None
                st.session_state.p2_result = None
                st.session_state.p2_reason = ""
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        if st.button("🔄 Clear Standings", key="p2_reset", use_container_width=True):
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
<p style='text-align:center; color:#3A3E54; font-size:11px; margin-top:36px; font-weight:500;'>
    Hand-crafted interfaces beat template code. Most of the time.
</p>
""", unsafe_allow_html=True)
