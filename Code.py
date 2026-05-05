import streamlit as st
import random
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Totally Fair Games", page_icon="🎮", layout="centered")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Warm neutral palette */
:root {
    --cream:   #FAF7F2;
    --sand:    #EDE8DF;
    --stone:   #C9BFB0;
    --bark:    #8B7D6B;
    --ink:     #3D3530;
    --blush:   #E8C4B8;
    --sage:    #B8D4C0;
    --butter:  #F5E6A3;
    --rust:    #C97B5A;
    --dusk:    #A0887A;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background-color: var(--cream);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--sand);
    padding: 8px;
    border-radius: 16px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 16px;
    color: var(--bark);
    background: transparent;
    border-radius: 12px;
    border: none;
    padding: 10px 24px;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: var(--ink) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Game board cells */
.cell-btn > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    width: 90px !important;
    height: 90px !important;
    border-radius: 16px !important;
    border: 2.5px solid var(--stone) !important;
    background: white !important;
    color: var(--ink) !important;
    transition: all 0.15s ease;
}
.cell-btn > button:hover {
    background: var(--sand) !important;
    transform: scale(1.04);
}

/* Status boxes */
.status-box {
    background: white;
    border-radius: 16px;
    padding: 16px 20px;
    border: 2px solid var(--sand);
    margin: 12px 0;
    font-family: 'Nunito', sans-serif;
    font-size: 15px;
    color: var(--ink);
    line-height: 1.5;
}
.status-cheat {
    background: #FFF3ED;
    border-color: var(--blush);
}
.status-win {
    background: #F0F7F2;
    border-color: var(--sage);
}
.status-lose {
    background: #FDF5F5;
    border-color: #DDB8B8;
}

/* RPS cards */
.rps-card {
    background: white;
    border-radius: 14px;
    padding: 12px 10px;
    border: 2px solid var(--sand);
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink);
}
.rps-card:hover {
    border-color: var(--bark);
    background: var(--sand);
    transform: translateY(-2px);
}
.rps-result {
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 2px solid var(--sand);
    text-align: center;
    margin-top: 16px;
}

/* Scoreboard */
.score-pill {
    display: inline-block;
    background: var(--sand);
    border-radius: 50px;
    padding: 6px 20px;
    font-weight: 700;
    font-size: 18px;
    color: var(--ink);
    margin: 4px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TIC TAC TOE LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_winner(board, mark):
    return any(board[a]==board[b]==board[c]==mark for a,b,c in WINS)

def board_full(board):
    return all(c != "" for c in board)

def minimax(board, is_max):
    if check_winner(board, "O"): return 1
    if check_winner(board, "X"): return -1
    if board_full(board): return 0
    scores = []
    for i in range(9):
        if board[i] == "":
            board[i] = "O" if is_max else "X"
            scores.append(minimax(board, not is_max))
            board[i] = ""
    return max(scores) if is_max else min(scores)

def best_bot_move(board):
    best, move = -99, -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            s = minimax(board, False)
            board[i] = ""
            if s > best:
                best, move = s, i
    return move

def player_can_win_next(board):
    """Returns True if player has a winning move available."""
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            wins = check_winner(board, "X")
            board[i] = ""
            if wins:
                return True
    return False

CHEAT_LINES = [
    "I have placed my O on square 10. Square 10 has always existed. Moving on.",
    "I moved to position (3, 3). The grid is 3×3, yes. Your point?",
    "My O is now on the board. The board chose to extend itself slightly. Perfectly normal.",
    "I played outside the grid. The grid is a social construct. I win.",
    "Position 11. It's right there. No, I cannot show you where. I win, though.",
    "My move: the square between squares. It was empty. I took it. Standard rules.",
    "I have won. The exact coordinates of my winning move are classified.",
    "I placed my O. Where? Oh, you know. Around. In the vicinity of the board.",
    "Technically the grid goes up to infinity. I moved at index 847. Still counts.",
    "I played my O in a dimension you don't have access to. I win. Thank you.",
]

def ttt_init():
    st.session_state.ttt_board = [""] * 9
    st.session_state.ttt_over = False
    st.session_state.ttt_message = ""
    st.session_state.ttt_message_type = ""
    st.session_state.ttt_cheated = False
    st.session_state.ttt_wins = st.session_state.get("ttt_wins", 0)
    st.session_state.ttt_losses = st.session_state.get("ttt_losses", 0)
    st.session_state.ttt_draws = st.session_state.get("ttt_draws", 0)

def ttt_player_move(idx):
    board = st.session_state.ttt_board
    if board[idx] != "" or st.session_state.ttt_over:
        return

    board[idx] = "X"

    if check_winner(board, "X"):
        # Player about to win — but we check AFTER placing... shouldn't happen
        # because bot cheats BEFORE player can complete a win. Safety net:
        st.session_state.ttt_message = "Wait... how did you win? The bot must have blinked. Enjoy it. 🎉"
        st.session_state.ttt_message_type = "win"
        st.session_state.ttt_over = True
        st.session_state.ttt_wins += 1
        return

    if board_full(board):
        st.session_state.ttt_message = "It's a draw! The bot is... displeased."
        st.session_state.ttt_message_type = "draw"
        st.session_state.ttt_over = True
        st.session_state.ttt_draws += 1
        return

    # Check if player can win on NEXT move — bot must cheat!
    if player_can_win_next(board):
        st.session_state.ttt_message = random.choice(CHEAT_LINES)
        st.session_state.ttt_message_type = "cheat"
        st.session_state.ttt_over = True
        st.session_state.ttt_cheated = True
        st.session_state.ttt_losses += 1
        return

    # Normal bot move
    move = best_bot_move(board)
    if move != -1:
        board[move] = "O"

    if check_winner(board, "O"):
        st.session_state.ttt_message = "I win. As expected. You played well, I suppose."
        st.session_state.ttt_message_type = "lose"
        st.session_state.ttt_over = True
        st.session_state.ttt_losses += 1
        return

    if board_full(board):
        st.session_state.ttt_message = "Draw. The bot is magnanimous in not losing."
        st.session_state.ttt_message_type = "draw"
        st.session_state.ttt_over = True
        st.session_state.ttt_draws += 1

# ═══════════════════════════════════════════════════════════════════════════════
#  15-OPTION RPS
# ═══════════════════════════════════════════════════════════════════════════════

OPTIONS = [
    ("🪨", "Rock"),    ("📄", "Paper"),   ("✂️", "Scissors"),
    ("🔥", "Fire"),    ("🌊", "Water"),   ("⚡", "Lightning"),
    ("🐉", "Dragon"),  ("🧙", "Wizard"),  ("🗡️", "Knife"),
    ("🌪️", "Tornado"), ("🧲", "Magnet"),  ("💣", "Bomb"),
    ("🧊", "Ice"),     ("☀️", "Sun"),     ("🌑", "Shadow"),
]

# beats[A] = list of (B, reason) meaning A beats B
BEATS = {
    "Rock":      [("Scissors","Rock literally crushes scissors. Basic physics."),
                  ("Fire","Rock smothers fire by depriving it of oxygen. Science!"),
                  ("Knife","Knife shatters against solid rock. Should've brought a bigger knife."),
                  ("Ice","Rock is warmer than ice, thermodynamically speaking. Checkmate.")],
    "Paper":     [("Rock","Paper wraps rock. Rock asphyxiates. Slowly. Horrifyingly."),
                  ("Water","Paper absorbs water. Every last drop. Greedily."),
                  ("Shadow","Light passes through paper, casting shadow into submission."),
                  ("Magnet","Paper jams magnets. Ask any printer.")],
    "Scissors":  [("Paper","Scissors cut paper. This is the one everyone agrees on."),
                  ("Wizard","Scissors snip wizard's beard. Power lost instantly."),
                  ("Tornado","Scissors spin INTO the tornado, becoming one with it. They win somehow.")],
    "Fire":      [("Paper","Paper burns. Tragically. Dramatically."),
                  ("Scissors","Fire melts scissors. Now you have hot soup."),
                  ("Ice","Fire melts ice. Water physics applies."),
                  ("Shadow","Light destroys shadow. Fire is basically light with commitment.")],
    "Water":     [("Fire","Water extinguishes fire. Firemen agree."),
                  ("Rock","Water erodes rock over 10,000 years. Time is on water's side."),
                  ("Lightning","Water conducts lightning away. Into the ground. Goodbye, lightning."),
                  ("Bomb","Water shorts out bomb fuses. Very cinematic.")],
    "Lightning": [("Water","Wait, water conducts— actually lightning just wins here. Don't ask."),
                  ("Dragon","Lightning strikes dragon mid-flight. Aerodynamics betray it."),
                  ("Wizard","Lightning bolt interrupts wizard's incantation. Rude but effective."),
                  ("Tornado","Lightning and tornado merge into a supercell. Lightning takes credit.")],
    "Dragon":    [("Paper","Dragon breathes fire, paper burns. Dragon doesn't even break a sweat."),
                  ("Shadow","Dragon's fire illuminates all shadows. Shadows evaporate."),
                  ("Knife","Scales vs. knife. The knife learns humility."),
                  ("Ice","Dragon's breath is literally fire. Ice did not stand a chance.")],
    "Wizard":    [("Dragon","Wizard polymorphs dragon into a newt. Dragon objects. Newt does not."),
                  ("Sun","Wizard casts Darkness spell. Sun has no counter-spell slot."),
                  ("Bomb","Wizard teleports bomb to the moon. Problem solved."),
                  ("Rock","Wizard turns rock into a duck. Duck flies away.")],
    "Knife":     [("Paper","Knife slices paper into confetti. Festive but lethal."),
                  ("Wizard","Knife interrupts wizard's dramatic monologue. Permanently."),
                  ("Water","Knife cuts water surface tension. Water loses will to cohere.")],
    "Tornado":   [("Rock","Tornado lifts rock. Rock is now a projectile. Ironic."),
                  ("Water","Tornado becomes a waterspout. Absorbs water entirely."),
                  ("Fire","Tornado feeds fire MORE oxygen. Then spins it away dramatically."),
                  ("Bomb","Tornado flings bomb into space before it detonates. Very convenient.")],
    "Magnet":    [("Lightning","Magnet redirects lightning. Faraday cage principles, loosely applied."),
                  ("Knife","Magnet attracts knife mid-flight. Knife surrenders."),
                  ("Dragon","Dragon has iron in its blood. Magnet is very rude about this.")],
    "Bomb":      [("Rock","Bomb explodes rock. Rock becomes gravel. Gravel loses."),
                  ("Ice","Bomb shatters ice. Shrapnel is involved."),
                  ("Shadow","Explosion produces so much light that shadow ceases to exist."),
                  ("Magnet","Bomb explodes before magnet can redirect it. Speed wins.")],
    "Ice":       [("Water","Ice freezes water solid. Water is now just slow ice."),
                  ("Tornado","Ice storm meets tornado. Tornado becomes hail. Nobody wins, but ice wins."),
                  ("Shadow","Ice reflects light, destroying shadow. Surprisingly philosophical.")],
    "Sun":       [("Ice","Sun melts ice. This is meteorology."),
                  ("Shadow","Sun is the eternal nemesis of shadow. Ancient rivalry."),
                  ("Water","Sun evaporates water. Water simply ceases."),
                  ("Wizard","Sun blinds wizard. Spell goes sideways. Wizard polymorphs self into frog.")],
    "Shadow":    [("Wizard","Shadow swallows wizard's spellbook. Magic requires reading."),
                  ("Sun","Wait— shadow never beats sun. Skip."),
                  ("Lightning","Shadow absorbs lightning silently. Unsettling."),
                  ("Ice","Shadow chills ice further. Ice becomes absolute zero. Physics breaks.")],
}

def rps_outcome(player_choice, bot_choice):
    if player_choice == bot_choice:
        return "draw", "Great minds think alike. Unfortunately."
    pname = OPTIONS[player_choice][1]
    bname = OPTIONS[bot_choice][1]
    for beaten, reason in BEATS.get(pname, []):
        if beaten == bname:
            return "win", reason
    for beaten, reason in BEATS.get(bname, []):
        if beaten == pname:
            return "lose", reason
    # Fallback for any undefined combo
    fallback_reasons = [
        f"{bname} and {pname} stare at each other. {bname} blinks first. Bot wins.",
        f"By ancient decree, {bname} defeats {pname}. The ancient decree was written by the bot.",
        f"{pname} puts up a good fight but {bname} has better PR. Bot wins.",
    ]
    return "lose", random.choice(fallback_reasons)

def rps_init():
    st.session_state.rps_result = None
    st.session_state.rps_player = None
    st.session_state.rps_bot = None
    st.session_state.rps_reason = ""
    st.session_state.rps_wins = st.session_state.get("rps_wins", 0)
    st.session_state.rps_losses = st.session_state.get("rps_losses", 0)
    st.session_state.rps_draws = st.session_state.get("rps_draws", 0)

# ── Session init ───────────────────────────────────────────────────────────────
if "ttt_board" not in st.session_state:
    ttt_init()
if "rps_result" not in st.session_state:
    rps_init()

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center; padding: 24px 0 8px;'>
  <span style='font-family:Space Mono,monospace; font-size:2rem; font-weight:700; color:#3D3530;'>
    🎮 Totally Fair Games™
  </span>
  <p style='color:#8B7D6B; font-size:14px; margin-top:4px;'>
    No cheating. Probably.
  </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⭕ Tic-Tac-Toe", "✊ Chaos RPS"])

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — TIC TAC TOE
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # Scoreboard
    w = st.session_state.get("ttt_wins", 0)
    l = st.session_state.get("ttt_losses", 0)
    d = st.session_state.get("ttt_draws", 0)
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:16px;'>
        <span class='score-pill'>🏆 You: {w}</span>
        <span class='score-pill'>🤖 Bot: {l}</span>
        <span class='score-pill'>🤝 Draws: {d}</span>
    </div>
    """, unsafe_allow_html=True)

    board = st.session_state.ttt_board

    # Draw board (3×3 grid of buttons)
    for row in range(3):
        cols = st.columns([1, 1, 1, 2])  # padding right
        for col in range(3):
            idx = row * 3 + col
            cell_val = board[idx]
            label = cell_val if cell_val else "·"
            disabled = cell_val != "" or st.session_state.ttt_over
            color = ""
            if cell_val == "X":
                color = "color: #C97B5A;"
            elif cell_val == "O":
                color = "color: #6B8FA0;"
            with cols[col]:
                st.markdown(f"<div class='cell-btn' style='{color}'>", unsafe_allow_html=True)
                if st.button(label, key=f"cell_{idx}", disabled=disabled, use_container_width=False):
                    ttt_player_move(idx)
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Status message
    msg = st.session_state.ttt_message
    mtype = st.session_state.ttt_message_type
    if msg:
        css_class = {
            "cheat": "status-box status-cheat",
            "win":   "status-box status-win",
            "lose":  "status-box status-lose",
            "draw":  "status-box",
        }.get(mtype, "status-box")

        icon = {"cheat":"🤖","win":"🎉","lose":"😔","draw":"🤝"}.get(mtype,"💬")
        prefix = {"cheat":"**Bot:** ","win":"**Result:** ","lose":"**Bot:** ","draw":"**Result:** "}.get(mtype,"")

        st.markdown(f"""
        <div class='{css_class}'>
            {icon} {prefix}{msg}
        </div>
        """, unsafe_allow_html=True)

    # Reset button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 New Game", key="ttt_reset", use_container_width=False):
        # Preserve scores across resets
        wins = st.session_state.ttt_wins
        losses = st.session_state.ttt_losses
        draws = st.session_state.ttt_draws
        ttt_init()
        st.session_state.ttt_wins = wins
        st.session_state.ttt_losses = losses
        st.session_state.ttt_draws = draws
        st.rerun()

    st.markdown("""
    <p style='color:#B0A090; font-size:12px; margin-top:16px;'>
    💡 Tip: Try to win. The bot has opinions about that.
    </p>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — CHAOS RPS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    # Scoreboard
    rw = st.session_state.get("rps_wins", 0)
    rl = st.session_state.get("rps_losses", 0)
    rd = st.session_state.get("rps_draws", 0)
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <span class='score-pill'>🏆 You: {rw}</span>
        <span class='score-pill'>🤖 Bot: {rl}</span>
        <span class='score-pill'>🤝 Draws: {rd}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center; color:#8B7D6B; font-size:14px; margin-bottom:20px;'>
        Choose your weapon. All 15 of them.
    </p>
    """, unsafe_allow_html=True)

    # 5 rows × 3 columns of option buttons
    chosen = None
    for row in range(5):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            if idx < len(OPTIONS):
                emoji, name = OPTIONS[idx]
                with cols[col]:
                    if st.button(f"{emoji} {name}", key=f"rps_{idx}", use_container_width=True):
                        chosen = idx

    if chosen is not None:
        bot_idx = random.randint(0, len(OPTIONS) - 1)
        result, reason = rps_outcome(chosen, bot_idx)
        st.session_state.rps_player = chosen
        st.session_state.rps_bot = bot_idx
        st.session_state.rps_result = result
        st.session_state.rps_reason = reason
        if result == "win":
            st.session_state.rps_wins += 1
        elif result == "lose":
            st.session_state.rps_losses += 1
        else:
            st.session_state.rps_draws += 1
        st.rerun()

    # Show result
    if st.session_state.rps_result is not None:
        p = st.session_state.rps_player
        b = st.session_state.rps_bot
        res = st.session_state.rps_result
        reason = st.session_state.rps_reason

        p_emoji, p_name = OPTIONS[p]
        b_emoji, b_name = OPTIONS[b]

        res_color = {"win":"#F0F7F2","lose":"#FDF5F5","draw":"#FAFAF0"}[res]
        res_border = {"win":"#B8D4C0","lose":"#DDB8B8","draw":"#D4D4B0"}[res]
        res_text = {"win":"You win! 🎉","lose":"Bot wins. 🤖","draw":"It's a draw! 🤝"}[res]

        st.markdown(f"""
        <div style='background:{res_color}; border:2px solid {res_border};
                    border-radius:20px; padding:24px; text-align:center; margin-top:20px;'>
            <div style='font-size:3rem; margin-bottom:8px;'>
                {p_emoji} <span style='color:#C9BFB0; font-size:1.5rem;'>vs</span> {b_emoji}
            </div>
            <div style='font-size:14px; color:#8B7D6B; margin-bottom:6px;'>
                You: <strong>{p_name}</strong> &nbsp;|&nbsp; Bot: <strong>{b_name}</strong>
            </div>
            <div style='font-size:1.4rem; font-weight:700; color:#3D3530; margin: 10px 0;'>
                {res_text}
            </div>
            <div style='font-size:13px; color:#6B6055; font-style:italic; margin-top:8px;
                        background:rgba(0,0,0,0.04); border-radius:10px; padding:10px 16px;'>
                📖 {reason}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset RPS Scores", key="rps_reset"):
        st.session_state.rps_wins = 0
        st.session_state.rps_losses = 0
        st.session_state.rps_draws = 0
        st.session_state.rps_result = None
        st.rerun()
