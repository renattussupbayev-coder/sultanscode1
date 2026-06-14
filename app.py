import streamlit as st
import random
import time

st.set_page_config(page_title="Brawl Memory", layout="wide")

# -----------------------------
# LOGO (рубашка)
# -----------------------------
CARD_BACK = "https://upload.wikimedia.org/wikipedia/en/5/5c/Brawl_Stars_logo.png"

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

DIFFICULTY = {"Easy": 6, "Medium": 8, "Hard": 12}


def img(id):
    return f"https://cdn.brawlify.com/brawlers/borderless/{id}.png"


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

if "resolve_time" not in st.session_state:
    st.session_state.resolve_time = None


# -----------------------------
# GAME
# -----------------------------
def build_deck(n):
    pick = random.sample(BRAWLERS, n)
    deck = pick * 2
    random.shuffle(deck)
    return deck


def reset(diff):
    st.session_state.cards = build_deck(DIFFICULTY[diff])
    st.session_state.selected = []
    st.session_state.matched = set()
    st.session_state.moves = 0
    st.session_state.resolve_time = None


if not st.session_state.cards:
    reset("Medium")


# -----------------------------
# CHECK LOGIC
# -----------------------------
if st.session_state.resolve_time:
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
# CLICK
# -----------------------------
def click(i):
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
# UI
# -----------------------------
st.title("🎮 Brawl Memory")

st.metric("🎯 Moves", st.session_state.moves)

cols = 4
grid = st.columns(cols)

for i, card in enumerate(st.session_state.cards):
    col = grid[i % cols]

    is_open = i in st.session_state.selected or i in st.session_state.matched

    with col:
        if is_open:
            st.image(img(card["id"]), width=120)
            st.caption(card["name"])
        else:
            st.image(CARD_BACK, width=120)

            if st.button("Select", key=f"c{i}"):
                click(i)
                st.rerun()
