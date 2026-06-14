import streamlit as st
import random
import time

st.set_page_config(page_title="Brawl Memory", layout="wide")

CARD_BACK = "https://i.imgur.com/4Y6X2g1.png"

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

DIFF = {"Easy": 6, "Medium": 8, "Hard": 12}

def img(i):
    return f"https://cdn.brawlify.com/brawlers/borderless/{i}.png"


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


def build(n):
    p = random.sample(BRAWLERS, n)
    d = p * 2
    random.shuffle(d)
    return d


def reset():
    st.session_state.cards = build(6)
    st.session_state.selected = []
    st.session_state.matched = set()
    st.session_state.moves = 0
    st.session_state.resolve_time = None


if not st.session_state.cards:
    reset()


# -----------------------------
# FLIP LOGIC
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
# CSS FLIP
# -----------------------------
st.markdown("""
<style>

.card {
  width: 120px;
  height: 120px;
  perspective: 1000px;
  margin: auto;
}

.inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flipped {
  transform: rotateY(180deg);
}

.front, .back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 12px;
}

.front {
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  display:flex;
  align-items:center;
  justify-content:center;
  color:white;
  font-weight:bold;
  font-size:24px;
}

.back {
  transform: rotateY(180deg);
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  background:white;
}

.back img {
  width:80px;
  height:80px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# UI
# -----------------------------
st.title("🎮 Brawl Memory (FLIP VERSION)")
st.metric("🎯 Moves", st.session_state.moves)

cols = st.columns(4)

for i, c in enumerate(st.session_state.cards):

    open_card = i in st.session_state.selected or i in st.session_state.matched
    flipped = "flipped" if open_card else ""

    html = f"""
    <div class="card">
      <div class="inner {flipped}">
        <div class="front">?</div>
        <div class="back">
          <img src="{img(c['id'])}">
          <div>{c['name']}</div>
        </div>
      </div>
    </div>
    """

    with cols[i % 4]:
        if st.button(" ", key=f"b{i}"):
            click(i)
            st.rerun()

        st.markdown(html, unsafe_allow_html=True)


# -----------------------------
# WIN
# -----------------------------
if len(st.session_state.matched) == len(st.session_state.cards):
    st.success(f"🏆 You won in {st.session_state.moves} moves!")
