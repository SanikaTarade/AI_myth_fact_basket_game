import streamlit as st
from streamlit_sortables import sort_items

st.set_page_config(page_title="AI Myth vs Fact", layout="wide")

st.title("🧺 AI Myth vs Fact – Drag the Cards into the Correct Basket")
st.caption("👉 Drag each card into **MYTH** or **FACT** basket. Then click **Check Score**.")

# -----------------------------
# QUESTIONS (10 difficult ones)
# -----------------------------
QUESTIONS = [
    {"id": "Q1", "text": "If you just give a generic prompt and accept the model’s output, that alone is usually enough to claim you ‘invented’ something created by AI.", "answer": "MYTH"},
    {"id": "Q2", "text": "AI inventions can still be patentable, as long as there is clear inventive contribution from a human.", "answer": "FACT"},
    {"id": "Q3", "text": "Generative AI is always the best solution for business problems compared to rules engines, analytics, or process redesign.", "answer": "MYTH"},
    {"id": "Q4", "text": "If you cannot quantify scale, value, friction, and evidence of a problem, you are not ready to build an AI solution.", "answer": "FACT"},
    {"id": "Q5", "text": "AI systems can drift from the original intent of a business decision if there is no oversight and trust architecture.", "answer": "FACT"},
    {"id": "Q6", "text": "If a model gives a confident answer, that confidence guarantees the answer is correct.", "answer": "MYTH"},
    {"id": "Q7", "text": "Using non-endorsed AI assistants for work is safe as long as you avoid uploading files; typing text is always okay.", "answer": "MYTH"},
    {"id": "Q8", "text": "Keeping clear records of what you did and how AI supported your work is a good practice for innovation and IP protection.", "answer": "FACT"},
    {"id": "Q9", "text": "Improving how data is organized/handled to improve accuracy or reduce latency/compute can still qualify as innovation worth protecting.", "answer": "FACT"},
    {"id": "Q10", "text": "If an invention is created entirely by AI with no human inventive contribution, it can still list AI as the inventor on a patent.", "answer": "MYTH"},
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
# CSS: text always visible
# -----------------------------
custom_style = """
/* Layout: 3 columns with better width distribution */
.sortable-component{
  display:grid !important;
  grid-template-columns: 1.35fr 1fr 1fr !important;  /* cards pile wider + baskets wider */
  gap:18px !important;
  align-items:start !important;
}

/* Each basket container */
.sortable-container{
  background:#f8f9fb;
  border:2px dashed #c7c7c7;
  border-radius:14px;
  padding:14px;
  min-height:520px;                 /* ✅ bigger baskets */
}

/* Basket headers */
.sortable-container-header{
  font-weight:800;
  font-size:18px;
  margin-bottom:12px;
  color:#111 !important;
}

/* Make basket body scroll if many cards come */
.sortable-container-body{
  max-height:480px;                 /* ✅ keeps header visible */
  overflow-y:auto;                  /* ✅ scroll inside baskets */
  padding-right:6px;
}

/* Cards */
.sortable-item{
  background:#ffffff !important;
  border:1px solid #e1e1e1 !important;
  border-radius:12px !important;
  padding:14px !important;
  margin-bottom:12px !important;
  box-shadow:0 2px 6px rgba(0,0,0,0.06) !important;

  color:#111 !important;
  opacity:1 !important;
  visibility:visible !important;

  /* Better wrapping for long text */
  white-space: normal !important;
  overflow-wrap: anywhere !important;
  word-break: break-word !important;

  font-size:14px !important;        /* ✅ slightly smaller so long questions fit nicely */
  line-height:1.4 !important;
}

/* Hover (optional) */
.sortable-item:hover{
  border-color:#9a9a9a !important;
  background:#ffffff !important;
  color:#111 !important;
}

/* Responsive: on small screens stack vertically */
@media (max-width: 1100px){
  .sortable-component{
    grid-template-columns: 1fr !important;
  }
  .sortable-container-body{
    max-height:none;
  }
}
"""

# -----------------------------
# Drag & Drop Board (SAFE UPDATE to avoid React #185 loop)
# -----------------------------
old_board = st.session_state.board

new_board = sort_items(
    old_board,
    multi_containers=True,
    direction="horizontal",
    custom_style=custom_style,
)

# ✅ Only write to session_state if something actually changed
if new_board != old_board:
    st.session_state.board = new_board

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
            {"header": "🧺 MYTH Basket", "items": []},
            {"header": "🧺 FACT Basket", "items": []},
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
