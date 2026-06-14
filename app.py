import streamlit as st
import random
import time

st.set_page_config(page_title="Brawl Memory", layout="wide")

# -----------------------------
# LOGO (рубашка карты)
# -----------------------------
BRAWL_LOGO = "https://upload.wikimedia.org/wikipedia/en/5/5c/Brawl_Stars_logo.png"

# -----------------------------
# DATA
# -----------------------------
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

DIFFICULTY = {
    "Easy": 6,
    "Medium": 8,
    "Hard": 12,
}

def img_url(brawler_id):
    return f"https://cdn.brawlify.com/brawlers/borderless/{brawler_id}.png"


# -----------------------------
# STATE
# -----------------------------
if "cards" not in st.session_state:
    st.session_state.cards = []

if "selected" not in st.session_state:
    st.session_state.selected = []

if "matched" not in st.session_state:
    st.session_state.matched = set()

if "moves" not in st.session_state:
    st.session_state.moves = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "resolve_time" not in st.session_state:
    st.session_state.resolve_time = None


# -----------------------------
# GAME SETUP
# -----------------------------
def build_deck(n_pairs):
    chosen = random.sample(BRAWLERS, n_pairs)
    deck = chosen * 2
    random.shuffle(deck)
    return deck


def reset_game(diff):
    st.session_state.cards = build_deck(DIFFICULTY[diff])
    st.session_state.selected = []
    st.session_state.matched = set()
    st.session_state.moves = 0
    st.session_state.resolve_time = None
    st.session_state.difficulty = diff


if not st.session_state.cards:
    reset_game("Medium")


# -----------------------------
# RESOLVE LOGIC
# -----------------------------
if st.session_state.resolve_time is not None:
    if time.time() >= st.session_state.resolve_time:

        a, b = st.session_state.selected
        st.session_state.moves += 1

        if st.session_state.cards[a]["id"] == st.session_state.cards[b]["id"]:
            st.session_state.matched.add(a)
            st.session_state.matched.add(b)

        st.session_state.selected = []
        st.session_state.resolve_time = None

        st.rerun()


# -----------------------------
# UI
# -----------------------------
st.title("🎮 Brawl Memory")

diff = st.selectbox(
    "Difficulty",
    list(DIFFICULTY.keys()),
    index=list(DIFFICULTY.keys()).index(st.session_state.difficulty)
)

if st.button("🔄 Restart"):
    reset_game(diff)
    st.rerun()

st.metric("🎯 Moves", st.session_state.moves)
st.metric("🏆 Matches", len(st.session_state.matched) // 2)

st.divider()


# -----------------------------
# CLICK LOGIC
# -----------------------------
def select(i):
    if i in st.session_state.matched:
        return

    if i in st.session_state.selected:
        return

    if len(st.session_state.selected) == 2:
        return

    st.session_state.selected.append(i)

    if len(st.session_state.selected) == 2:
        st.session_state.resolve_time = time.time() + 0.8


# -----------------------------
# RENDER GRID
# -----------------------------
cols = 4 if DIFFICULTY[st.session_state.difficulty] <= 8 else 6
grid = st.columns(cols)

for i, card in enumerate(st.session_state.cards):
    col = grid[i % cols]

    is_open = i in st.session_state.selected or i in st.session_state.matched

    with col:
        if is_open:
            st.image(img_url(card["id"]), width=120)
            st.caption(card["name"])
        else:
            # 🎮 ЛОГОТИП вместо ❓
            if st.button(" ", key=f"card_{i}"):
                select(i)
                st.rerun()

            st.image(BRAWL_LOGO, width=80)


# -----------------------------
# WIN CHECK
# -----------------------------
if len(st.session_state.matched) == len(st.session_state.cards):
    st.success(f"🏆 You won in {st.session_state.moves} moves!")

    if st.button("Play again"):
        reset_game(st.session_state.difficulty)
        st.rerun()
