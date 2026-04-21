import streamlit as st
from streamlit_sortables import sort_items

st.set_page_config(page_title="AI Myth vs Fact", layout="wide")

st.title("🧺 AI Myth vs Fact – Drag the Cards into the Correct Basket")
st.caption("👉 Drag each card into **MYTH** or **FACT** basket. Then click **Check Score**.")

# -----------------------------
# QUESTIONS (Edit as you want)
# -----------------------------
QUESTIONS = [
    {"id": "Q1", "text": "AI will completely replace human jobs.", "answer": "MYTH"},
    {"id": "Q2", "text": "AI needs clean, reliable data to work well.", "answer": "FACT"},
    {"id": "Q3", "text": "AI outputs are always correct because it is ‘smart’.", "answer": "MYTH"},
    {"id": "Q4", "text": "Innovation can be done using low-code/no-code tools, not only coding.", "answer": "FACT"},
    {"id": "Q5", "text": "AI is only useful for IT teams.", "answer": "MYTH"},
]

ANSWER_BY_ID = {q["id"]: q["answer"] for q in QUESTIONS}


# -----------------------------
# Helper functions (strings are most reliable)
# -----------------------------
def card_label(q):
    return f"{q['id']} | {q['text']}"

def get_id_from_label(label: str):
    return label.split(" | ", 1)[0].strip()


# -----------------------------
# Session state init
# -----------------------------
if "board" not in st.session_state:
    st.session_state.board = [
        {"header": "🃏 Question Cards", "items": [card_label(q) for q in QUESTIONS]},
        {"header": "🧺 MYTH Basket", "items": []},
        {"header": "🧺 FACT Basket", "items": []},
    ]

if "last_score" not in st.session_state:
    st.session_state.last_score = None


# -----------------------------
# CSS FIX: Make text always visible (no hover needed)
# -----------------------------
custom_style = """
.sortable-component{
  display:flex;
  gap:16px;
  flex-wrap:wrap;               /* wraps on small screens */
}

/* Baskets */
.sortable-container{
  flex:1;
  min-width: 280px;
  background:#f8f9fb;
  border:2px dashed #c7c7c7;
  border-radius:14px;
  padding:12px;
  min-height:360px;
}

/* Basket titles */
.sortable-container-header{
  font-weight:800;
  font-size:18px;
  margin-bottom:10px;
  color:#111 !important;
}

/* Cards */
.sortable-item{
  background:#ffffff !important;
  border:1px solid #e1e1e1 !important;
  border-radius:12px !important;
  padding:12px !important;
  margin-bottom:10px !important;
  box-shadow:0 2px 6px rgba(0,0,0,0.06) !important;

  /* ✅ IMPORTANT: text always visible */
  color:#111 !important;
  opacity:1 !important;
  visibility:visible !important;

  /* Wrap long questions */
  white-space: normal !important;
  overflow-wrap: anywhere !important;
  word-break: break-word !important;

  font-size:15px !important;
  line-height:1.35 !important;
}

/* Optional hover effect (text stays visible) */
.sortable-item:hover{
  border-color:#9a9a9a !important;
  background:#ffffff !important;
  color:#111 !important;
}
"""

# -----------------------------
# Drag & Drop Board (Multi containers)
# -----------------------------
# multi_containers=True enables moving items between containers. [1](https://engage.cloud.microsoft/main/threads/eyJfdHlwZSI6IlRocmVhZCIsImlkIjoiMzgwNTY0Mzc5NTI1MTIwMCJ9)
st.session_state.board = sort_items(
    st.session_state.board,
    multi_containers=True,
    direction="horizontal",
    custom_style=custom_style,
)

# -----------------------------
# Buttons
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Check Score", use_container_width=True):
        myth_labels = st.session_state.board[1]["items"]
        fact_labels = st.session_state.board[2]["items"]
        remaining_labels = st.session_state.board[0]["items"]

        myth_ids = {get_id_from_label(x) for x in myth_labels}
        fact_ids = {get_id_from_label(x) for x in fact_labels}
        remaining_ids = {get_id_from_label(x) for x in remaining_labels}

        score = 0
        wrong = []
        unplaced = []

        for q in QUESTIONS:
            qid = q["id"]
            correct = q["answer"]

            if qid in remaining_ids:
                unplaced.append(qid)
                continue

            user_choice = "MYTH" if qid in myth_ids else ("FACT" if qid in fact_ids else None)

            if user_choice == correct:
                score += 1
            else:
                wrong.append((qid, user_choice, correct))

        st.session_state.last_score = (score, len(QUESTIONS), wrong, unplaced)
        st.rerun()

with col2:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.board = [
            {"header": "🃏 Question Cards", "items": [card_label(q) for q in QUESTIONS]},
            {"header": "🧺 MYTH", "items": []},
            {"header": "🧺 FACT", "items": []},
        ]
        st.session_state.last_score = None
        st.rerun()


# -----------------------------
# Results
# -----------------------------
if st.session_state.last_score:
    score, total, wrong, unplaced = st.session_state.last_score
    st.subheader(f"🏁 Score: {score} / {total}")

    if unplaced:
        st.warning(f"⚠️ Unplaced cards: {', '.join(unplaced)}")

    if wrong:
        st.error("❌ Wrong placements:")
        for qid, user_choice, correct in wrong:
            st.write(f"- **{qid}** → you chose **{user_choice}**, correct is **{correct}**")
    else:
        st.success("🎉 All correct!")