import streamlit as st
import random
import time

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Brawl Memory", layout="wide")

BRAWLERS = [
    {"id": 16000000, "name": "Shelly"},
    {"id": 16000001, "name": "Colt"},
    {"id": 16000002, "name": "Bull"},
    {"id": 16000003, "name": "Brock"},
    {"id": 16000004, "name": "Rico"},
    {"id": 16000005, "name": "Spike"},
    {"id": 16000006, "name": "Barley"},
    {"id": 16000007, "name": "Jessie"},
    {"id": 16000008, "name": "Nita"},
    {"id": 16000009, "name": "Dynamike"},
    {"id": 16000010, "name": "El Primo"},
    {"id": 16000011, "name": "Mortis"},
]

def portrait_url(brawler_id):
    return f"https://cdn.brawlify.com/brawlers/borderless/{brawler_id}.png"


DIFFICULTIES = {
    "Easy": 6,
    "Medium": 8,
    "Hard": 12,
}

# -----------------------------
# STATE INIT
# -----------------------------
if "cards" not in st.session_state:
    st.session_state.cards = []
if "selected" not in st.session_state:
    st.session_state.selected = []
if "moves" not in st.session_state:
    st.session_state.moves = 0
if "matched" not in st.session_state:
    st.session_state.matched = set()
if "started" not in st.session_state:
    st.session_state.started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

# -----------------------------
# GAME LOGIC
# -----------------------------
def build_deck(pairs):
    picked = random.sample(BRAWLERS, pairs)
    deck = picked * 2
    random.shuffle(deck)
    return deck


def reset_game(difficulty):
    pairs = DIFFICULTIES[difficulty]
    st.session_state.cards = build_deck(pairs)
    st.session_state.selected = []
    st.session_state.moves = 0
    st.session_state.matched = set()
    st.session_state.started = False
    st.session_state.start_time = None
    st.session_state.difficulty = difficulty


# -----------------------------
# HEADER
# -----------------------------
st.title("🎮 Brawl Memory (Streamlit Edition)")
st.caption("Match all brawler pairs!")

# -----------------------------
# SIDEBAR
# -----------------------------
difficulty = st.sidebar.selectbox(
    "Difficulty",
    list(DIFFICULTIES.keys()),
    index=list(DIFFICULTIES.keys()).index(st.session_state.difficulty),
)

if st.sidebar.button("🔄 Restart Game"):
    reset_game(difficulty)

if not st.session_state.cards:
    reset_game(difficulty)

# -----------------------------
# TIMER
# -----------------------------
if st.session_state.started and st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
else:
    elapsed = 0

# -----------------------------
# STATUS
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("⏱ Time", f"{elapsed}s")
col2.metric("🎯 Moves", st.session_state.moves)
col3.metric("✅ Matches", len(st.session_state.matched) // 2)

st.divider()

# -----------------------------
# CLICK HANDLER
# -----------------------------
def select_card(i):
    if not st.session_state.started:
        st.session_state.started = True
        st.session_state.start_time = time.time()

    if i in st.session_state.matched:
        return

    if i in st.session_state.selected:
        return

    if len(st.session_state.selected) == 2:
        return

    st.session_state.selected.append(i)

    # when 2 cards selected
    if len(st.session_state.selected) == 2:
        a, b = st.session_state.selected
        st.session_state.moves += 1

        if st.session_state.cards[a]["id"] == st.session_state.cards[b]["id"]:
            st.session_state.matched.add(a)
            st.session_state.matched.add(b)
            st.session_state.selected = []
        else:
            time.sleep(0.6)
            st.session_state.selected = []


# -----------------------------
# RENDER GRID
# -----------------------------
pairs = DIFFICULTIES[st.session_state.difficulty]
cols = 4 if pairs <= 8 else 6

grid = st.columns(cols)

for i, card in enumerate(st.session_state.cards):
    col = grid[i % cols]

    is_flipped = i in st.session_state.selected or i in st.session_state.matched
    is_matched = i in st.session_state.matched

    with col:
        if is_flipped:
            st.image(portrait_url(card["id"]), width=120)
            st.caption(card["name"])
        else:
            if st.button("❓", key=f"card_{i}"):
                select_card(i)
                st.rerun()

# -----------------------------
# WIN CONDITION
# -----------------------------
if len(st.session_state.matched) == len(st.session_state.cards):
    st.success(f"🏆 You won in {st.session_state.moves} moves and {elapsed} seconds!")
    if st.button("Play again"):
        reset_game(st.session_state.difficulty)
        st.rerun()
