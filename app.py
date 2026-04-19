import streamlit as st
from dotenv import load_dotenv
import os
import base64

from core.pdf_processor import load_and_split
from core.vector_store import create_vector_store
from core.rag_chain import build_rag_chain
from core.summarizer import generate_summary
from core.quiz_engine import generate_quiz
from core.mind_map import generate_mind_map
from core.analytics import LearningAnalytics, ACHIEVEMENTS
from streamlit_echarts import st_echarts
from core.export_utils import export_to_pdf

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="Lumina AI - Smart Learning Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: #0f0f1a; color: #e2e8f0; }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ── Hero header ── */
    .lumina-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 0.5rem 0.8rem; 
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        text-align: center;
    }
    .lumina-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .lumina-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(to right, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
        line-height: 1 !important;
        margin-top: -0.2rem !important;
    }
    .lumina-subtitle {
        color: #e2e8f0;
        font-size: 1.15rem;
        margin-top: 0.8rem;
        font-weight: 400;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #12121f !important;
        border-right: 1px solid rgba(99,102,241,0.2) !important;
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #818cf8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    /* ── Animated Glowing Orb Logo Style ── */
    .sidebar-logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }
    
    @keyframes orb-pulse {
        0% { transform: scale(1); box-shadow: 0 0 20px rgba(244, 114, 182, 0.4); }
        50% { transform: scale(1.08); box-shadow: 0 0 35px rgba(244, 114, 182, 0.7); }
        100% { transform: scale(1); box-shadow: 0 0 20px rgba(244, 114, 182, 0.4); }
    }

    @keyframes brain-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    
    .glow-orb {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #4c1d95, #f472b6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: orb-pulse 3s infinite ease-in-out;
    }

    .glow-orb span {
        animation: brain-float 2.5s infinite ease-in-out;
        display: inline-block;
    }

    .glow-orb:hover {
        transform: scale(1.2) rotate(15deg); 
        filter: brightness(1.2);
        box-shadow: 0 0 45px rgba(167, 139, 250, 0.8);
        border-color: rgba(255, 255, 255, 0.5);
    }

    /* ── Sidebar Brand (logo) ── */
    .sidebar-brand {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        text-align: center;
        display: block;
    }
    
    .sidebar-tagline {
        font-size: 0.75rem;
        color: #94a3b8;
        text-align: center;
        margin-top: -1.2rem;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* ── Inputs ── */
    .stTextInput input, .stTextArea textarea {
        background: #1e1e30 !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129,140,248,0.2) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a2e;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.5rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
    }

    /* ── Chat messages ── */
    .chat-bubble-user {
        background: linear-gradient(135deg, #312e81, #4c1d95);
        border: 1px solid rgba(129,140,248,0.3);
        border-radius: 16px 16px 4px 16px;
        padding: 1rem 1.2rem;
        margin: 0.75rem 0 0.75rem 15%;
        color: #e2e8f0;
        position: relative;
    }
    .chat-bubble-ai {
        background: linear-gradient(135deg, #0f2744, #1e3a5f);
        border: 1px solid rgba(56,189,248,0.3);
        border-radius: 16px 16px 16px 4px;
        padding: 1rem 1.2rem;
        margin: 0.75rem 15% 0.75rem 0;
        color: #e2e8f0;
        position: relative;
    }
    .chat-label-user {
        font-size: 0.7rem;
        font-weight: 600;
        color: #a5b4fc;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
        text-align: right;
    }
    .chat-label-ai {
        font-size: 0.7rem;
        font-weight: 600;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }
    .citation-badge {
        display: inline-block;
        background: rgba(56,189,248,0.15);
        border: 1px solid rgba(56,189,248,0.3);
        color: #38bdf8;
        font-size: 0.72rem;
        padding: 0.1rem 0.5rem;
        border-radius: 20px;
        margin-top: 0.5rem;
        margin-right: 0.3rem;
        font-weight: 500;
    }

    /* ── Summary card ── */
    .summary-card {
        background: #1a1a2e;
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        color: #e2e8f0;
    }

    /* ── Quiz cards ── */
    .quiz-card {
        background: #1a1a2e;
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .quiz-q-num {
        font-size: 0.75rem;
        font-weight: 700;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .quiz-question {
        font-size: 1.05rem;
        font-weight: 500;
        color: #f1f5f9;
        margin-bottom: 1rem;
    }
    .correct-answer { color: #4ade80 !important; font-weight: 600 !important; }
    .wrong-answer   { color: #f87171 !important; font-weight: 600 !important; }
    .explanation-box {
        background: rgba(74,222,128,0.08);
        border-left: 3px solid #4ade80;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin-top: 0.75rem;
        font-size: 0.9rem;
        color: #cbd5e1;
    }
    .wrong-explanation-box {
        background: rgba(248,113,113,0.08);
        border-left: 3px solid #f87171;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin-top: 0.75rem;
        font-size: 0.9rem;
        color: #cbd5e1;
    }
    .score-banner {
        background: linear-gradient(135deg, #0f2744, #1e3a5f);
        border: 1px solid rgba(56,189,248,0.4);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .score-number { font-size: 3rem; font-weight: 700; color: #38bdf8; line-height: 1; }
    .score-label  { font-size: 0.9rem; color: #94a3b8; margin-top: 0.25rem; }

    /* ── Status / info boxes ── */
    .status-box {
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.88rem;
        color: #a5b4fc;
        margin-top: 0.75rem;
    }
    .warning-box {
        background: rgba(251,191,36,0.08);
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.88rem;
        color: #fbbf24;
        margin-top: 0.5rem;
    }
    .success-box {
        background: rgba(74,222,128,0.08);
        border: 1px solid rgba(74,222,128,0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.88rem;
        color: #4ade80;
        margin-top: 0.5rem;
    }

    /* ── Radio buttons ── */
    .stRadio label { color: #cbd5e1 !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #cbd5e1 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #12121f; }
    ::-webkit-scrollbar-thumb { background: #4c1d95; border-radius: 3px; }

    /* ── Divider ── */
    hr { border-color: rgba(99,102,241,0.2) !important; }

    /* ── File uploader ── */
    [data-testid="stFileUploaderDropzone"] {
        background: #1a1a2e !important;
        border: 1px dashed rgba(99,102,241,0.4) !important;
        border-radius: 10px !important;
        color: #94a3b8 !important;
    }

    /* ── Selectbox ── */
    .stSelectbox [data-baseweb="select"] {
        background: #1e1e30 !important;
        border-color: rgba(99,102,241,0.3) !important;
    }

    /* ── Mastery Points ── */
    .level-badge {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: linear-gradient(135deg, #1e1e30, #2d1f4e);
        border: 1px solid rgba(129,140,248,0.4);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.6rem;
    }
    .level-icon { font-size: 1.8rem; line-height: 1; }
    .level-name { font-size: 1rem; font-weight: 700; color: #c084fc; }
    .level-mp   { font-size: 0.75rem; color: #94a3b8; margin-top: 0.1rem; }

    .mp-bar-wrap {
        background: #1e1e30;
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 8px;
        padding: 0.6rem 0.85rem;
        margin-bottom: 0.6rem;
        font-size: 0.8rem;
        color: #94a3b8;
    }
    .mp-bar-track {
        background: #0f0f1a;
        border-radius: 4px;
        height: 8px;
        margin-top: 0.4rem;
        overflow: hidden;
    }
    .mp-bar-fill {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #6366f1, #c084fc);
        transition: width 0.4s ease;
    }

    .stat-row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.6rem;
    }
    .stat-pill {
        flex: 1;
        background: #1e1e30;
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 10px;
        padding: 0.5rem 0.4rem;
        text-align: center;
        font-size: 0.75rem;
        color: #94a3b8;
    }
    .stat-pill b { display: block; font-size: 1.1rem; color: #e2e8f0; }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.4rem;
    }
    .badge-chip {
        background: rgba(192,132,252,0.12);
        border: 1px solid rgba(192,132,252,0.3);
        border-radius: 20px;
        padding: 0.25rem 0.6rem;
        font-size: 0.72rem;
        color: #c084fc;
        white-space: nowrap;
    }

    .mp-toast {
        display: inline-block;
        background: linear-gradient(135deg, #4c1d95, #1e3a5f);
        border: 1px solid rgba(129,140,248,0.4);
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #c084fc;
        margin-bottom: 0.5rem;
    }
    .difficulty-easy   { color: #4ade80; font-weight: 600; }
    .difficulty-medium { color: #fbbf24; font-weight: 600; }
    .difficulty-hard   { color: #f87171; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


def init_session():
    defaults = {
        "documents": None,
        "vector_store": None,
        "rag_chain": None,
        "chat_history": [],
        "summary": None,
        "quiz": None,
        "quiz_answers": {},
        "quiz_submitted": False,
        "doc_name": None,
        "doc_pages": 0,
        "doc_chunks": 0,
        "mp_notification": None,
        "raw_files": {},
        "flashcards": [],         
        "current_card_idx": 0,    
        "card_flipped": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "analytics" not in st.session_state:
        st.session_state.analytics = LearningAnalytics()

    if "flashcard_stats" not in st.session_state:
        st.session_state.flashcard_stats = {"Hard": 0, "Good": 0, "Easy": 0}


def reset_document_state():
    for key in ["documents", "vector_store", "rag_chain", "chat_history",
                "summary", "quiz", "quiz_answers", "quiz_submitted",
                "doc_name", "doc_pages", "doc_chunks", "raw_files", "flashcards"]:
        st.session_state[key] = None if key not in ("chat_history", "quiz_answers", "raw_files", "flashcards") else ([] if key in ("chat_history", "flashcards") else {})
    st.session_state["quiz_submitted"] = False
    st.session_state["doc_pages"] = 0
    st.session_state["doc_chunks"] = 0
    st.session_state["current_card_idx"] = 0
    st.session_state["card_flipped"] = False

init_session()

def handle_api_error(e):
    """Handles API-related errors centrally to keep code DRY."""
    error_msg = str(e)
    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
        st.error("⚠️ API quota exceeded. Please wait a moment or switch to your backup API key.")
    else:
        st.error(f"System Error: {error_msg}")


# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .lumina-title {
    margin-bottom: 2px !important;
    }

    .lumina-subtitle {
    margin-top: 0px !important;
    line-height: 1.2;
    }
</style>

<div class="lumina-header">
    <h1 class="lumina-title">🧠 Lumina AI</h1>
    <div class="lumina-subtitle">Smart Adaptive Learning Assistant · Powered by Google Gemini & RAG</div>
</div>
""", unsafe_allow_html=True)

# ── MASTERY POINTS NOTIFICATION ─────────────────────────────────────────────────────────
if st.session_state.get("mp_notification"):
    mp_val, new_ach = st.session_state.mp_notification
    st.session_state.mp_notification = None
    if mp_val > 0:
        st.toast(f"+ {mp_val} Insight Points (IP) gained!", icon="✨")
    for aid in new_ach:
        badge = next((a for a in ACHIEVEMENTS if a["id"] == aid), None)
        if badge:
            st.toast(f"{badge['icon']} Badge unlocked: {badge['name']} (+{badge['mp']} IP)", icon="🏅")


# ── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
        <div class="sidebar-logo-container">
            <div class="glow-orb">
                <span>🧠</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-brand">LUMINA AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">INTELLIGENT LEARNING</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📄 Document")

    uploaded_files = st.file_uploader(
        "Upload Study Materials",
        type=["pdf", "txt", "docx", "pptx", "csv"], 
        accept_multiple_files=True,
        help="Upload lecture notes, textbook chapters, slides, or data files.",
    )

    if uploaded_files:
        col_proc, col_clr = st.columns(2)
        with col_proc:
            process_btn = st.button("⚡ Process", use_container_width=True)
        with col_clr:
            if st.button("🗑️ Reset All", use_container_width=True, help="Clears memory and starts a new session"):
                reset_document_state()
                st.rerun()

        if process_btn:
            with st.spinner(f"Processing {len(uploaded_files)} documents…"):
                try:
                    all_docs = [] 
                    total_pages = 0
                    doc_names = []

                    st.session_state.raw_files = {}

                    for file in uploaded_files:
                        file_bytes = file.read()

                        st.session_state.raw_files[file.name] = file_bytes
                        
                        docs = load_and_split(file_bytes, file.name)
                        all_docs.extend(docs) 
                        doc_names.append(file.name)

                        pages = docs[0].metadata.get("total_pages", 1) if docs else 0
                        total_pages += pages

                    if "analytics" in st.session_state:
                        st.session_state.analytics.increment_counter("docs_uploaded")
                        st.session_state.analytics.award_mp("upload_document")
                    
                    vs = create_vector_store(all_docs, api_key)
                    chain = build_rag_chain(vs, api_key)

                    st.session_state.documents = all_docs
                    st.session_state.vector_store = vs
                    st.session_state.rag_chain = chain
                    
                    st.session_state.doc_name = ", ".join(doc_names) 
                    st.session_state.doc_pages = total_pages
                    st.session_state.doc_chunks = len(all_docs)
                    
                    st.session_state.chat_history = []
                    st.session_state.summary = None

                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.get("doc_name"):
        st.markdown("## 📊 Document Overview")
        
        doc_name = st.session_state.doc_name
        file_count = len(doc_name.split(",")) if doc_name and "," in doc_name else 1
        
        st.markdown(f"""
<div style="display: flex; flex-direction: column; gap: 5px;">
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #1e1e2f; padding: 1px 1px; border-radius: 8px; border-left: 8px solid #8b5cf6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; gap: 5px;">
            <span style="font-size: 1rem;">📄</span>
            <span style="color: #94a3b8; font-size: 1rem; margin: 0; font-weight: 500;">Files</span>
        </div>
        <h3 style="color: #f8fafc; margin: 0; margin-right: 20px; font-size: 1.3rem;">{file_count}</h3>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #1e1e2f; padding: 1px 1px; border-radius: 8px; border-left: 8px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; gap: 5px;">
            <span style="font-size: 1rem;">📑</span>
            <span style="color: #94a3b8; font-size: 1rem; margin: 0; font-weight: 500;">Pages</span>
        </div>
        <h3 style="color: #f8fafc; margin: 0; margin-right: 20px; font-size: 1.3rem;">{st.session_state.doc_pages}</h3>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #1e1e2f; padding: 1px 1px; border-radius: 8px; border-left: 8px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; gap: 5px;">
            <span style="font-size: 1rem;">🧩</span>
            <span style="color: #94a3b8; font-size: 1rem; margin: 0; font-weight: 500;">Chunks</span>
        </div>
        <h3 style="color: #f8fafc; margin: 0; margin-right: 20px; font-size: 1.3rem;">{st.session_state.doc_chunks}</h3>
    </div>
</div>
<br>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🏆 Your Progress") 
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "analytics" in st.session_state:
        current_mp = st.session_state.analytics.total_mp
        streak_days = st.session_state.analytics.streak
        quizzes = st.session_state.analytics.data.get("quizzes_done", 0)
        docs = st.session_state.analytics.data.get("docs_uploaded", 0)
        
        current_lvl, next_lvl, mp_in, mp_need, progress_pct = st.session_state.analytics.get_level_info()
        pct = int(progress_pct * 100)
        level_name = current_lvl["name"]
        
        st.markdown(f"""
<div style="background-color: #1e1e30; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
    <span style="color: #cbd5e1; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">{level_name}</span>
    <span style="color: #818cf8; font-size: 0.85rem; font-weight: bold;">{current_mp} MP</span>
</div>
    
<div style="width: 100%; background-color: #334155; border-radius: 4px; height: 6px; margin-bottom: 12px;">
    <div style="background: linear-gradient(90deg, #6366f1, #a855f7); height: 6px; border-radius: 4px; width: {pct}%;"></div>
</div>
    
<div style="display: flex; justify-content: space-between; color: #64748b; font-size: 0.75rem;">
    <span>Mastery Progress</span>
    <span>{mp_need - mp_in} MP to next rank</span>
</div>
    
<hr style="border-color: #334155; margin: 12px 0;">
    
<div style="display: flex; justify-content: space-between;">
    <div style="text-align: center;">
        <div style="font-size: 1.2rem;">🔥</div>
        <div style="color: #94a3b8; font-size: 0.7rem;">{streak_days} Days</div>
    </div>
    <div style="text-align: center;">
        <div style="font-size: 1.2rem;">🎯</div>
        <div style="color: #94a3b8; font-size: 0.7rem;">{quizzes} Tests</div>
    </div>
    <div style="text-align: center;">
        <div style="font-size: 1.2rem;">📚</div>
        <div style="color: #94a3b8; font-size: 0.7rem;">{docs} Docs</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🌌 System Info")
    st.markdown("""
<div style="background-color: #1e1e30; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    
<div style="color: #e2e8f0; font-size: 0.82rem; line-height: 1.5; margin-bottom: 1rem;">
    <b>Lumina AI</b> is an intelligent academic workspace engineered to transform static study materials into dynamic, data-driven learning experiences.
</div>

<div style="color: #818cf8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.6rem;">Core Modules</div>

<div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.8rem; color: #cbd5e1; margin-bottom: 1.2rem;">
    <div style="display: flex; align-items: center; gap: 8px;"><span>🧠</span> RAG-Powered Q&A & Citation</div>
    <div style="display: flex; align-items: center; gap: 8px;"><span>📊</span> Mastery Analytics Dashboard</div>
    <div style="display: flex; align-items: center; gap: 8px;"><span>📇</span> Leitner Flashcard Engine</div>
    <div style="display: flex; align-items: center; gap: 8px;"><span>🕸️</span> Neural Mind Mapping</div>
    <div style="display: flex; align-items: center; gap: 8px;"><span>🧪</span> Adaptive Assessment</div>
</div>

<div style="color: #818cf8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.6rem;">Engineered By</div>

<div style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 0.75rem; color: #e2e8f0;">
    <div style="background: rgba(99,102,241,0.15); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(99,102,241,0.3);">
        👩‍💻 İrem Yılmaz
    </div>
    <div style="background: rgba(99,102,241,0.15); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(99,102,241,0.3);">
        👩‍💻 Hande Reyyan Fidan
    </div>
</div>

<hr style="border-color: #334155; margin: 15px 0 10px 0;">

<div style="text-align: center; color: #64748b; font-size: 0.7rem; line-height: 1.4;">
    Powered by Google Gemini
</div>
</div>
    """, unsafe_allow_html=True)


# ── MAIN AREA ────────────────────────────────────────────────────────────────
if not st.session_state.vector_store:
    st.markdown("""
<div style="text-align:center; padding: 4rem 2rem; color:#475569;">
    <div style="font-size:4rem; margin-bottom:1rem;">📚</div>
    <div style="font-size:1.3rem; font-weight:600; color:#64748b;">Upload a document to get started</div>
    <div style="font-size:0.95rem; margin-top:0.5rem;">
        Upload a PDF or TXT file in the sidebar.
    </div>
</div>
""", unsafe_allow_html=True)
    st.stop()


tab_viewer, tab_chat, tab_summary, tab_quiz, tab_map, tab_cards = st.tabs(["📄 Viewer", "💬 Chat", "📋 Summary", "🧪 Quiz", "🕸️ Mind Map", "📇 Flashcards"])

# ── TAB 0: VIEWER  ─────────────────────────────────────────────
with tab_viewer:
    st.markdown("### 📄 Document Viewer")
    
    if st.session_state.get("raw_files"):
        file_names = list(st.session_state.raw_files.keys())
        
        if len(file_names) > 1:
            selected_file = st.selectbox("Select document to view:", file_names)
        else:
            selected_file = file_names[0]
            
        file_bytes = st.session_state.raw_files[selected_file]
        
        if selected_file.lower().endswith('.pdf'):
            base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="750px" style="border-radius: 10px; border: 1px solid rgba(99,102,241,0.3);"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        elif selected_file.lower().endswith(('.txt', '.csv')):
            try:
                text_content = file_bytes.decode('utf-8')
                st.text_area("Document Content:", text_content, height=600, disabled=True)
            except:
                st.warning("Could not read text encoding.")
                
        else:
            st.info(f"Visual preview is not natively supported for {selected_file.split('.')[-1].upper()} files in this browser.")
            st.markdown("Don't worry! **Lumina AI has successfully read the text content** of this file and is ready to answer your questions or generate quizzes.")
            
    else:
        st.markdown("""
        <div style="text-align:center; color:#475569; padding:3rem 0;">
            <div style="font-size:2.5rem; margin-bottom:0.75rem;">👀</div>
            <div>Upload a PDF or text file to view it directly in this window.</div>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 1: CHAT ──────────────────────────────────────────────────────────────
with tab_chat:
    st.markdown("### Ask anything about your document")

    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
<div style="text-align:center; color:#475569; padding:2rem 0;">
    <div style="font-size:2rem; margin-bottom:0.5rem;">💡</div>
    <div>Start by asking a question about your document.<br>
    Lumina AI will answer using only the uploaded content and cite page numbers.</div>
</div>
""", unsafe_allow_html=True)
        else:
            for turn in st.session_state.chat_history:
                st.markdown(f"""
<div class="chat-label-user">You</div>
<div class="chat-bubble-user">{turn['question']}</div>
<div class="chat-label-ai">🧠 Lumina AI</div>
<div class="chat-bubble-ai">{turn['answer']}</div>
""", unsafe_allow_html=True)
                if turn.get("pages"):
                    badges = " ".join(
                        f'<span class="citation-badge">📖 Page {p}</span>'
                        for p in sorted(set(turn["pages"]))
                    )
                    st.markdown(f'<div style="margin-bottom:0.5rem;">{badges}</div>',
                                unsafe_allow_html=True)

    st.markdown("---")

    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1], vertical_alignment="bottom") 
        
        with col_input:
            user_question = st.text_input(
                "Your question",
                placeholder="e.g. What are the main topics covered?",
                label_visibility="collapsed", 
            )
            
        with col_send:
            send = st.form_submit_button("Send ➤", use_container_width=True)

    if send and user_question.strip():
        with chat_container:
            with st.spinner("Lumina AI is thinking…"):
                try:
                    from langchain_core.messages import HumanMessage, AIMessage
                    lc_history = []
                    for turn in st.session_state.chat_history:
                        lc_history.append(HumanMessage(content=turn["question"]))
                        lc_history.append(AIMessage(content=turn["answer"]))

                    result = st.session_state.rag_chain.invoke({
                        "question": user_question,
                        "chat_history": lc_history,
                    })
                    answer = result.get("answer", "")
                    source_docs = result.get("_source_docs", [])
                    pages = [d.metadata.get("page") for d in source_docs if d.metadata.get("page")]

                    st.session_state.chat_history.append({
                        "question": user_question,
                        "answer": answer,
                        "pages": pages,
                    })
                    analytics = st.session_state.analytics
                    analytics.increment_counter("questions_asked")
                    mp_gained, new_ach = analytics.award_mp("ask_question")
                    st.session_state.mp_notification = (mp_gained, new_ach)
                    st.rerun()

                except Exception as e:
                    handle_api_error(e)


# ── TAB 2: SUMMARY ──────────────────────────────────────────────────────────
with tab_summary:
    st.markdown("### 📋 One-Click Document Summary")
    st.markdown(
        "<div style='color: #94a3b8; margin-bottom: 1.5rem; font-size: 1.05rem;'>"
        "Generate a structured study guide with key takeaways, glossary, and important sections."
        "</div>", 
        unsafe_allow_html=True
    )

    col_opt, col_btn = st.columns([2, 1], vertical_alignment="bottom")
    
    with col_opt:
        summary_len = st.radio(
            "Summary Depth:", 
            options=["Short", "Medium", "Detailed"], 
            horizontal=True, 
            index=1
        )
    
    with col_btn:
        gen_sum_btn = st.button("✨ Generate Summary", use_container_width=True)
        
    if gen_sum_btn:
        with st.spinner(f"Generating {summary_len.lower()} summary..."):
            try:
                st.session_state.summary = generate_summary(st.session_state.documents, api_key, summary_len)

            except Exception as e:
                handle_api_error(e)

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")

        col_sp1, col_export, col_sp2 = st.columns([1, 1.5, 1])

        with col_export:
            try:
                from core.export_utils import export_to_pdf
                summary_pdf = export_to_pdf(st.session_state.summary, f"Document Summary ({summary_len})")
                
                st.download_button(
                    label="📥 Export Summary as PDF",
                    data=bytes(summary_pdf),
                    file_name=f"Lumina_Summary_{summary_len}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    help="Click to download this summary as a professional PDF report"
                )
            except Exception as e:
                handle_api_error(e)

        st.markdown("<br>", unsafe_allow_html=True)

# ── TAB 3: QUIZ ───────────────────────────────────────────────────────────────
with tab_quiz:
    st.markdown("### Adaptive Quiz Engine")

    col_diff, col_num, col_gen, col_reset = st.columns([2, 2, 2, 1], vertical_alignment="bottom")

    with col_diff:
        selected_diff = st.selectbox(
            "Difficulty",
            options=["Easy", "Medium", "Hard"],
            index=1
        )

    with col_num:
        selected_num = st.selectbox(
            "Number of Questions",
            options=[3, 5, 7, 10],
            index=1
        )

    with col_gen:
        generate_quiz_btn = st.button("🎯 Generate Quiz", use_container_width=True)
        
    with col_reset:
        reset_quiz_btn = st.button("↺ Reset", use_container_width=True)

    if reset_quiz_btn:
        st.session_state.quiz = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.rerun()

    if generate_quiz_btn:
        with st.spinner("Creating quiz questions…"):
            try:
                diff_mapping = {
                    "Easy":   {"mult": 1.0, "css": "difficulty-easy"},
                    "Medium": {"mult": 1.5, "css": "difficulty-medium"},
                    "Hard":   {"mult": 2.0, "css": "difficulty-hard"}
                }
                diff_dict = diff_mapping[selected_diff]

                questions = generate_quiz(st.session_state.documents, api_key, selected_num)
                
                if questions:
                    st.session_state.quiz = questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state["quiz_difficulty"] = diff_dict

                    st.toast("Quiz completed successfully!", icon="🎉")

                else:
                    st.error("Could not generate quiz questions. Please try again.")
            
            except Exception as e:
                handle_api_error(e)

    if st.session_state.quiz:
        questions = st.session_state.quiz
        q_diff = st.session_state.get("quiz_difficulty", {"mult": 1.0, "css": "difficulty-easy"})

        if st.session_state.quiz_submitted:
            correct = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.quiz_answers.get(i) == q.get("correct_answer")
            )
            total = len(questions)
            pct = int(correct / total * 100)

            emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📖"
            msg = "Excellent work!" if pct >= 80 else "Good effort!" if pct >= 60 else "Keep studying!"

            mp_earned = int(correct * 10 * q_diff["mult"]) + (20 if correct == total else 0)
            st.markdown(f"""
<div class="score-banner">
    <div class="score-number">{emoji} {correct}/{total}</div>
    <div class="score-label">{pct}% · {msg}</div>
    <div style="margin-top:0.5rem; font-size:0.85rem; color:#818cf8;">+{mp_earned} IP earned this quiz</div>
</div>
""", unsafe_allow_html=True)

        for i, q in enumerate(questions):
            options_dict = q.get("options", {})
            option_list = [f"{k}: {v}" for k, v in options_dict.items()]
            correct_key = q.get("correct_answer", "A")

            user_ans = st.session_state.quiz_answers.get(i)
            submitted = st.session_state.quiz_submitted

            with st.container():
                st.markdown(f"""
<div class="quiz-card">
    <div class="quiz-q-num">Question {i + 1} &nbsp;·&nbsp; {q.get("page_reference", "")}</div>
    <div class="quiz-question">{q.get("question", "")}</div>
</div>
""", unsafe_allow_html=True)

                selected = st.radio(
                    f"q_{i}",
                    options=option_list,
                    index=None if not submitted else next(
                        (j for j, o in enumerate(option_list) if o.startswith(user_ans or "~")),
                        None
                    ),
                    key=f"radio_{i}",
                    label_visibility="collapsed",
                    disabled=submitted,
                )

                if not submitted and selected:
                    chosen_key = selected.split(":")[0].strip()
                    st.session_state.quiz_answers[i] = chosen_key

                if submitted and user_ans:
                    is_correct = (user_ans == correct_key)
                    correct_text = f"{correct_key}: {options_dict.get(correct_key, '')}"
                    if is_correct:
                        st.markdown(f"""
<div class="explanation-box">
    ✅ <b class="correct-answer">Correct!</b><br>
    {q.get("explanation", "")}
</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
<div class="wrong-explanation-box">
    ❌ <b class="wrong-answer">Incorrect.</b> The correct answer is <b>{correct_text}</b><br>
    {q.get("explanation", "")}
</div>""", unsafe_allow_html=True)

        st.markdown("---")
        if not st.session_state.quiz_submitted:
            answered = len(st.session_state.quiz_answers)
            total = len(questions)

            st.markdown(
                f'<div style="text-align: center; color: #94a3b8; font-size: 0.95rem; margin-bottom: 1rem;">'
                f'Answered: <b style="color: #a5b4fc;">{answered} / {total}</b> questions'
                f'</div>',
                unsafe_allow_html=True,
            )

            col_sp1, col_sub, col_exp, col_sp2 = st.columns([1, 1.5, 1.5, 1])

            with col_sub:
                if st.button("✅ Submit Quiz", use_container_width=True):
                    if len(st.session_state.quiz_answers) < total:
                        st.warning(f"Please answer all {total} questions before submitting.")
                    else:
                        correct_count = sum(1 for i, q in enumerate(questions) if st.session_state.quiz_answers.get(i) == q.get("correct_answer"))
                        mult = st.session_state.get("quiz_difficulty", {}).get("mult", 1.0)
                        if "analytics" in st.session_state:
                            mp_gained, new_ach = st.session_state.analytics.award_quiz_mp(correct_count, total, mult)
                            st.session_state.mp_notification = (mp_gained, new_ach)
                        st.session_state.quiz_submitted = True
                        st.rerun()

            with col_exp:
                quiz_text = ""
                for i, q in enumerate(st.session_state.quiz):
                    quiz_text += f"Question {i+1}: {q.get('question', '')}\n"
                    for k, v in q.get('options', {}).items():
                        quiz_text += f"{k}) {v}\n"
                    quiz_text += f"Correct Answer: {q.get('correct_answer', '')}\n\n"

                from core.export_utils import export_to_pdf
                quiz_pdf = export_to_pdf(quiz_text, "Practice Quiz")

                st.download_button(
                    "📥 Export as PDF",
                    data=bytes(quiz_pdf),
                    file_name="Lumina_Quiz.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        else:
            col_sp1, col_exp_center, col_sp2 = st.columns([1, 2, 1])
            
            with col_exp_center:
                quiz_text = ""
                for i, q in enumerate(st.session_state.quiz):
                    quiz_text += f"Question {i+1}: {q.get('question', '')}\n"
                    for k, v in q.get('options', {}).items():
                        quiz_text += f"{k}) {v}\n"
                    quiz_text += f"Correct Answer: {q.get('correct_answer', '')}\n\n"

                from core.export_utils import export_to_pdf
                quiz_pdf = export_to_pdf(quiz_text, "Practice Quiz")

                st.download_button(
                    "📥 Export Quiz & Answers as PDF",
                    data=bytes(quiz_pdf),
                    file_name="Lumina_Quiz_Results.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# ── TAB 4: MIND MAP ──────────────────────────────────────────────────────────
with tab_map:
    st.markdown("### 🕸️ Document Mind Map")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "Visualize the structural hierarchy and main topics of your document."
        )
    with col2:
        generate_map_btn = st.button("✨ Generate Mind Map", use_container_width=True)

    if generate_map_btn:
        with st.spinner("Analyzing document structure..."):
            try:
                map_data = generate_mind_map(st.session_state.documents, api_key)
                st.session_state.mind_map = map_data

                if "analytics" in st.session_state:
                    st.session_state.analytics.increment_counter("mindmaps_generated")
                    mp_gained, new_ach = st.session_state.analytics.award_mp("generate_mindmap")
                    st.session_state.mp_notification = (mp_gained, new_ach)
                        
            except Exception as e:
                handle_api_error(e)

    if st.session_state.get("mind_map"):
        st.markdown("<br>", unsafe_allow_html=True)
        
        options = {
            "toolbox": { 
                "show": True,
                "itemSize": 26,  
                "right": "4%",
                "top": "3%",
                "feature": {
                    "saveAsImage": {
                        "type": "png",
                        "title": "💾 Save as PNG",
                        "pixelRatio": 3,
                        "backgroundColor": "#1a1a2e", 
                        "iconStyle": {
                            "borderColor": "#818cf8", 
                            "borderWidth": 2
                        }
                    }
                }
            },
            "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
            "series": [
                {
                    "type": "tree",
                    "data": [st.session_state.mind_map],

                    "top": "10%",
                    "bottom": "10%",
                    "left": "20%",
                    "right": "23%",

                    "symbolSize": 10, 
                    "symbol": "circle",
                    "itemStyle": {
                        "color": "#818cf8",
                        "borderColor": "#4f46e5", 
                        "borderWidth": 2
                    },
                    "lineStyle": {
                        "color": "#4f46e5", 
                        "width": 2,
                        "curveness": 0.6 
                    },
                    "label": {
                        "position": "left",
                        "verticalAlign": "middle",
                        "align": "right",
                        "fontSize": 13,
                        "fontWeight": "bold",
                        "color": "#ffffff",
                        "backgroundColor": "#312e81", 
                        "borderColor": "#6366f1",     
                        "borderWidth": 1.5,
                        "borderRadius": 6,            
                        "padding": [8, 12, 8, 12],    
                        "shadowColor": "rgba(0,0,0,0.2)",
                        "shadowBlur": 5 
                    },
                    "leaves": {
                        "label": {
                            "position": "right",
                            "verticalAlign": "middle",
                            "align": "left",
                            "color": "#e2e8f0",
                            "backgroundColor": "#1e1e30", 
                            "borderColor": "#475569",
                            "borderWidth": 1,
                            "borderRadius": 5,
                            "padding": [6, 10, 6, 10],
                            "fontWeight": "normal"
                        }
                    },
                    "expandAndCollapse": True, 
                    "animationDuration": 550,
                    "animationDurationUpdate": 750
                }
            ]
        }
        
        with st.container(border=True):
            st_echarts(options, height="850px")
    

# ── TAB 6: FLASHCARDS ────────────────────────────────────────
with tab_cards:
    
    if not st.session_state.get("flashcards"):
        col_title, col_input, col_action = st.columns([2.5, 0.8, 1.2])
        
        with col_title:
            st.markdown("### 📇 Flashcards")
            st.caption("Master concepts with the scientifically proven Leitner Spaced Repetition system.")
            
        with col_input:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            num_cards = st.number_input("Number of cards", min_value=5, max_value=30, value=12, step=1)

        with col_action:
            st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Generate Cards", use_container_width=True):
                with st.spinner("Extracting concepts..."):
                    try:
                        from core.flashcard_engine import generate_flashcards
                        cards = generate_flashcards(st.session_state.documents, api_key, num_cards=num_cards)
                        if cards:
                            st.session_state.flashcards = cards
                            st.session_state.current_card_idx = 0
                            st.session_state.card_flipped = False
                            st.session_state.flashcard_stats = {"Hard": 0, "Good": 0, "Easy": 0}
                            
                            if "analytics" in st.session_state:
                                st.session_state.analytics.increment_counter("flashcards_generated")
                                mp_gained, new_ach = st.session_state.analytics.award_mp("generate_flashcards")
                                st.session_state.mp_notification = (mp_gained, new_ach)
                            st.rerun()
                    except Exception as e:
                        handle_api_error(e)
    
    else:
        import datetime
        today_str = datetime.datetime.now().date().isoformat()
        
        due_cards = [(i, card) for i, card in enumerate(st.session_state.flashcards) if card["next_review"] <= today_str]

        if not due_cards:
            st.success("🎉 All caught up! No cards are due for review today. Great job!")
            st.info(f"Session Results: 🔴 {st.session_state.flashcard_stats['Hard']} Hard | 🟡 {st.session_state.flashcard_stats['Good']} Good | 🟢 {st.session_state.flashcard_stats['Easy']} Easy")
            
            st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #94a3b8;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">⌛</div>
                    <p>The system is scheduling your next review sessions.</p>
                    <p style="font-size: 0.8rem;">Your progress is saved. Come back tomorrow for new cards.</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔍 View Card Collection (Read-Only)"):
                for c in st.session_state.flashcards:
                    st.write(f"**{c['term']}**: {c['definition']}")

        else:
            total_due = len(due_cards)
            current_pos = (st.session_state.current_card_idx % total_due) + 1
            
            col_info_1, col_info_2 = st.columns([1, 1])
            with col_info_1:
                st.caption(f"Reviewing {current_pos} of {total_due} due cards")
            with col_info_2:
                st.markdown(f"<div style='text-align:right; font-size:0.8rem;'>🔴 {st.session_state.flashcard_stats['Hard']} &nbsp; 🟡 {st.session_state.flashcard_stats['Good']} &nbsp; 🟢 {st.session_state.flashcard_stats['Easy']}</div>", unsafe_allow_html=True)
            
            st.progress(current_pos / total_due)

            original_idx, current_card = due_cards[current_pos - 1]
            
            flip_class = "is-flipped" if st.session_state.card_flipped else ""
            _, col_card, _ = st.columns([1, 2, 1]) 
            with col_card:
                st.markdown(f"""
                <style>
                .flashcard-scene {{ width: 100%; max-width: 500px; height: 300px; perspective: 1000px; margin: 0 auto; }}
                .flashcard-inner {{ width: 100%; height: 100%; position: relative; transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1); transform-style: preserve-3d; }}
                .flashcard-inner.is-flipped {{ transform: rotateY(180deg); }}
                .flashcard-face {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 2rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow-y: auto; }}
                .flashcard-front {{ background: linear-gradient(135deg, #1e1e2f, #2a2a4a); border: 2px solid #6366f1; }}
                .flashcard-back {{ background: linear-gradient(135deg, #2a2a4a, #1e1e2f); border: 2px solid #10b981; transform: rotateY(180deg); }}
                </style>
                <div class="flashcard-scene">
                    <div class="flashcard-inner {flip_class}">
                        <div class="flashcard-face flashcard-front">
                            <div style="position:absolute; top:15px; right:20px; background:rgba(99,102,241,0.2); padding:2px 10px; border-radius:10px; font-size:0.7rem; color:#818cf8;">BOX {current_card['box']}</div>
                            <h2 style="color: #f8fafc; font-size: 2rem;">{current_card['term']}</h2>
                        </div>
                        <div class="flashcard-face flashcard-back">
                            <h3 style="color: #34d399; font-size: 1.4rem;">{current_card['term']}</h3>
                            <p style="color: #cbd5e1; font-size: 1.05rem;">{current_card['definition']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)

                if not st.session_state.card_flipped:
                    c_prev, c_flip, c_empty = st.columns([1, 2, 1])
                    with c_prev:
                        if st.session_state.current_card_idx > 0:
                            if st.button("⬅️ Back", use_container_width=True):
                                st.session_state.current_card_idx -= 1
                                st.rerun()
                    with c_flip:
                        if st.button("🔄 Flip Card", use_container_width=True):
                            st.session_state.card_flipped = True
                            st.rerun()
                else:
                    c1, c2, c3 = st.columns(3)
                    today_date = datetime.datetime.now().date()
                    with c1:
                        if st.button("🔴 Hard", use_container_width=True):
                            st.session_state.flashcard_stats["Hard"] += 1
                            st.session_state.flashcards[original_idx]["box"] = 1
                            st.session_state.flashcards[original_idx]["next_review"] = (today_date + datetime.timedelta(days=1)).isoformat()
                            st.session_state.card_flipped = False
                            st.session_state.current_card_idx += 1
                            st.rerun()
                    with c2:
                        if st.button("🟡 Good", use_container_width=True):
                            st.session_state.flashcard_stats["Good"] += 1
                            new_box = min(5, current_card["box"] + 1)
                            st.session_state.flashcards[original_idx]["box"] = new_box
                            st.session_state.flashcards[original_idx]["next_review"] = (today_date + datetime.timedelta(days=new_box * 2)).isoformat()
                            st.session_state.card_flipped = False
                            st.session_state.current_card_idx += 1
                            st.rerun()
                    with c3:
                        if st.button("🟢 Easy", use_container_width=True):
                            st.session_state.flashcard_stats["Easy"] += 1
                            new_box = min(5, current_card["box"] + 2)
                            st.session_state.flashcards[original_idx]["box"] = new_box
                            st.session_state.flashcards[original_idx]["next_review"] = (today_date + datetime.timedelta(days=new_box * 4)).isoformat()
                            st.session_state.card_flipped = False
                            st.session_state.current_card_idx += 1
                            st.rerun()