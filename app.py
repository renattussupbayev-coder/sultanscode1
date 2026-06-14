import streamlit as st
import random
import time

st.set_page_config(page_title="Brawl Memory", layout="wide")

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

DIFFICULTIES = {
    "Easy": 6,
    "Medium": 8,
    "Hard": 12,
}

def portrait_url(brawler_id):
    return f"https://cdn.brawlify.com/brawlers/borderless/{brawler_id}.png"


# -----------------------------
# STATE INIT
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

if "check_pending" not in st.session_state:
    st.session_state.check_pending = False


# -----------------------------
# GAME SETUP
# -----------------------------
def build_deck(pairs):
    picked = random.sample(BRAWLERS, pairs)
    deck = picked * 2
    random.shuffle(deck)
    return deck


def reset_game(diff):
    st.session_state.cards = build_deck(DIFFICULTIES[diff])
    st.session_state.selected = []
    st.session_state.matched = set()
    st.session_state.moves = 0
    st.session_state.check_pending = False
    st.session_state.difficulty = diff


if not st.session_state.cards:
    reset_game("Medium")


# -----------------------------
# CHECK LOGIC (ВАЖНО)
# -----------------------------
if st.session_state.check_pending:
    a, b = st.session_state.selected

    st.session_state.moves += 1

    if st.session_state.cards[a]["id"] == st.session_state.cards[b]["id"]:
        st.session_state.matched.add(a)
        st.session_state.matched.add(b)
        st.session_state.selected = []
    else:
        # просто очищаем после rerun (без sleep)
        st.session_state.selected = []

    st.session_state.check_pending = False
    st.rerun()


# -----------------------------
# UI
# -----------------------------
st.title("🎮 Brawl Memory (Fixed Streamlit Version)")

diff = st.selectbox("Difficulty", list(DIFFICULTIES.keys()), index=list(DIFFICULTIES.keys()).index(st.session_state.difficulty))

if st.button("🔄 Restart"):
    reset_game(diff)
    st.rerun()

st.divider()

col1, col2 = st.columns(2)
col1.metric("🎯 Moves", st.session_state.moves)
col2.metric("✅ Matches", len(st.session_state.matched) // 2)


# -----------------------------
# CLICK HANDLER
# -----------------------------
def select_card(i):
    if i in st.session_state.matched:
        return

    if i in st.session_state.selected:
        return

    if len(st.session_state.selected) == 2:
        return

    st.session_state.selected.append(i)

    if len(st.session_state.selected) == 2:
        st.session_state.check_pending = True


# -----------------------------
# RENDER GRID
# -----------------------------
cols = 4 if DIFFICULTIES[st.session_state.difficulty] <= 8 else 6
grid = st.columns(cols)

for i, card in enumerate(st.session_state.cards):
    col = grid[i % cols]

    is_open = i in st.session_state.selected or i in st.session_state.matched

    with col:
        if is_open:
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
    st.success(f"🏆 You won in {st.session_state.moves} moves!")

    if st.button("Play again"):
        reset_game(st.session_state.difficulty)
        st.rerun()
