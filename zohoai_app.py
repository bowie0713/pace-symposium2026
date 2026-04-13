import json
import uuid
import streamlit as st
from datetime import datetime
from pathlib import Path
from mongodb_RAG import ZohoTicket

HISTORY_FILE = Path("/Users/guiallovido/Documents/GitHub/pace-symposium2026/Local Chat Logs/history.json")


def load_history() -> dict:
    """Load sessions from disk. Returns {} if file missing or corrupt."""
    if not HISTORY_FILE.exists():
        return {}
    try:
        raw = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        for session in raw.values():
            session["created_at"] = datetime.fromisoformat(session["created_at"])
        return raw
    except Exception:
        return {}

def save_history(sessions: dict) -> None:
    """Persist sessions to disk (datetime -> ISO string for JSON serialisation)."""
    serialisable = {}
    for sid, session in sessions.items():
        serialisable[sid] = {
            "title":      session["title"],
            "messages":   session["messages"],
            "created_at": session["created_at"].isoformat(),
        }
    HISTORY_FILE.write_text(
        json.dumps(serialisable, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# App config
@st.cache_resource
def load_chatbot():
    return ZohoTicket()

st.set_page_config(
    page_title="Zoho Tickets AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# CSS for design and layout
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, .stApp {
    background-color: #0b0f1a !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #e8eaf0 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1rem 1.5rem !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0d1120 !important;
    border-right: 1px solid rgba(99,160,255,0.12) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem !important;
    max-width: 100% !important;
}
[data-testid="stSidebarNav"] { display: none !important; }

[data-testid="stSidebar"] div[data-testid="stButton"] button {
    background: transparent !important;
    color: #8a9cc0 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    text-align: left !important;
    padding: 7px 10px !important;
    width: 100% !important;
    transition: background 0.12s, color 0.12s !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    background: #111827 !important;
    color: #e8eaf0 !important;
}

/* ── Top bar ── */
.topbar {
    display: flex; align-items: center; gap: 14px;
    padding: 18px 0 16px; border-bottom: 1px solid rgba(99,160,255,0.15);
    margin-bottom: 10px;
}
.topbar-logo {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #1a6fd4, #c9a227);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; line-height: 1; flex-shrink: 0;
}
.topbar-title { font-size: 26px; font-weight: 700; color: #e8eaf0; letter-spacing: -0.02em; }
.topbar-sub   { font-size: 13px; color: #5a7aaa; margin-top: 2px; }

/* ── Messages ── */
.chat-area { display: flex; flex-direction: column; gap: 8px; padding: 12px 0; }
.msg-row {
    display: flex; align-items: flex-end; gap: 10px; padding: 2px 0;
    animation: rise 0.2s ease both;
}
.msg-row.user-row { flex-direction: row-reverse; }
@keyframes rise {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.avatar {
    width: 30px; height: 30px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: #fff;
}
.av-user { background: linear-gradient(135deg, #1a6fd4, #4d9fff); }
.av-bot  { background: linear-gradient(135deg, #b8891e, #e8bf4a); }
.msg-col { max-width: 75%; min-width: 0; }
.msg-col.user-col { display: flex; flex-direction: column; align-items: flex-end; }
.msg-label {
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: .05em; color: #5a7aaa; margin-bottom: 4px;
}
.msg-bubble { font-size: 15px; line-height: 1.7; color: #e8eaf0; }
.msg-bubble.user {
    background: #1a3a6b; border: 1px solid rgba(26,111,212,0.45);
    border-radius: 18px 18px 4px 18px; padding: 11px 15px;
    display: inline-block;
}
.msg-bubble.bot {
    background: #111c2e; border: 1px solid rgba(99,160,255,0.15);
    border-radius: 18px 18px 18px 4px; padding: 11px 15px;
    display: inline-block; max-width: 100%;
}

/* ── Empty state ── */
.empty-state { text-align: center; padding: 56px 20px 32px; animation: rise 0.35s ease both; }
.empty-icon {
    width: 54px; height: 54px;
    background: linear-gradient(135deg, #1a6fd4, #c9a227);
    border-radius: 14px; font-size: 26px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 18px; box-shadow: 0 6px 28px rgba(26,111,212,0.3);
}
.empty-title { font-size: 22px; font-weight: 600; color: #e8eaf0; margin-bottom: 8px; }
.empty-sub   { font-size: 15px; color: #5a7aaa; line-height: 1.6; max-width: 380px; margin: 0 auto; }

/* ── Input ── */
div[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; }
div[data-testid="stTextInput"] > div > div {
    background: #111827 !important; border: 1px solid rgba(99,160,255,0.2) !important;
    border-radius: 12px !important; color: #e8eaf0 !important;
}
div[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(26,111,212,0.6) !important;
    box-shadow: 0 0 0 3px rgba(26,111,212,0.1) !important;
}
div[data-testid="stTextInput"] input {
    color: #e8eaf0 !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important; background: transparent !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #5a7aaa !important; }
div[data-testid="stTextInput"] label { display: none !important; }

div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #c9a227, #e8bf4a) !important;
    color: #0b0f1a !important; border: none !important; border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 20px !important;
    font-weight: 700 !important; height: 44px !important; width: 100% !important;
    cursor: pointer !important; transition: filter 0.15s, transform 0.15s !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    filter: brightness(1.1) !important; transform: scale(1.02) !important;
}

div[data-testid="stButton"] button {
    background: #111827 !important; color: #5a7aaa !important;
    border: 1px solid rgba(99,160,255,0.15) !important; border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 13px !important;
    padding: 4px 12px !important; transition: color 0.15s, border-color 0.15s !important;
}
div[data-testid="stButton"] button:hover {
    color: #e8eaf0 !important; border-color: rgba(99,160,255,0.35) !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
    background: #111827 !important; border: 1px solid rgba(99,160,255,0.18) !important;
    border-radius: 20px !important; padding: 8px 15px !important; font-size: 14px !important;
    color: #5a7aaa !important; font-family: 'DM Sans', sans-serif !important;
    transition: all 0.14s !important; white-space: normal !important;
    height: auto !important; min-height: 40px !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
    color: #e8eaf0 !important; border-color: rgba(99,160,255,0.4) !important;
    background: #1a2540 !important;
}

hr { border-color: rgba(99,160,255,0.12) !important; margin: 8px 0 !important; }
.stSpinner > div { color: #5a7aaa !important; }
.messages-scroll { max-height: 55vh; overflow-y: auto; padding-right: 4px; margin-bottom: 8px; }
.messages-scroll::-webkit-scrollbar { width: 3px; }
.messages-scroll::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 3px; }
.input-hint { font-size: 12px; color: #5a7aaa; text-align: center; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

# Session state tracking 
if "sessions" not in st.session_state:
    st.session_state.sessions = load_history()

if "active_session_id" not in st.session_state:
    if st.session_state.sessions:
        # Auto-select the most recent session
        st.session_state.active_session_id = max(
            st.session_state.sessions,
            key=lambda sid: st.session_state.sessions[sid]["created_at"],
        )
    else:
        st.session_state.active_session_id = None

if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# Helper functions 
def new_session():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {
        "title":      "New conversation",
        "messages":   [],
        "created_at": datetime.now(),
    }
    st.session_state.active_session_id = sid
    st.session_state.prefill = ""
    save_history(st.session_state.sessions)

def active_messages() -> list:
    sid = st.session_state.active_session_id
    if sid and sid in st.session_state.sessions:
        return st.session_state.sessions[sid]["messages"]
    return []

def append_message(role: str, content: str):
    sid = st.session_state.active_session_id
    if not sid or sid not in st.session_state.sessions:
        return
    st.session_state.sessions[sid]["messages"].append({"role": role, "content": content})
    # Auto-title from first user message
    user_msgs = [m for m in st.session_state.sessions[sid]["messages"] if m["role"] == "user"]
    if user_msgs:
        raw = user_msgs[0]["content"]
        st.session_state.sessions[sid]["title"] = raw[:42] + ("…" if len(raw) > 42 else "")
    save_history(st.session_state.sessions)  # persist every message

def fmt_date(dt: datetime) -> str:
    delta = (datetime.now().date() - dt.date()).days
    if delta == 0: return "Today"
    if delta == 1: return "Yesterday"
    return dt.strftime("%b %d")

def clean_text(text: str) -> str:
    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   
    text = re.sub(r'#+\s*', '', text)              
    return text

chatbot = load_chatbot()

# sidebar for chat history management
with st.sidebar:
    st.markdown(
        "<p style='font-size:12px;font-weight:600;color:#5a7aaa;"
        "text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px'>Chat history</p>",
        unsafe_allow_html=True,
    )

    if st.button("＋  New chat", use_container_width=True):
        new_session()
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    sorted_sessions = sorted(
        st.session_state.sessions.items(),
        key=lambda x: x[1]["created_at"],
        reverse=True,
    )

    for sid, session in sorted_sessions:
        is_active = sid == st.session_state.active_session_id
        prefix = "▸ " if is_active else ""
        col_btn, col_del = st.columns([5, 1])

        with col_btn:
            if st.button(f"{prefix}{session['title']}", key=f"sess_{sid}", use_container_width=True):
                st.session_state.active_session_id = sid
                st.session_state.prefill = ""
                st.rerun()

        with col_del:
            if st.button("✕", key=f"del_{sid}"):
                del st.session_state.sessions[sid]
                save_history(st.session_state.sessions)  # persist deletion
                if st.session_state.active_session_id == sid:
                    st.session_state.active_session_id = (
                        max(st.session_state.sessions,
                            key=lambda s: st.session_state.sessions[s]["created_at"])
                        if st.session_state.sessions else None
                    )
                st.rerun()

        st.markdown(
            f"<div style='font-size:11px;color:#3d5580;margin:-4px 0 6px 4px'>"
            f"{fmt_date(session['created_at'])}</div>",
            unsafe_allow_html=True,
        )

#  auto create session 
if st.session_state.active_session_id is None:
    new_session()

# top bar
col_left, col_right = st.columns([8, 2])
with col_left:
    st.markdown("""
    <div class="topbar">
        <div class="topbar-logo">💬</div>
        <div>
            <div class="topbar-title">Zoho Tickets AI</div>
            <div class="topbar-sub">MongoDB RAG · Voyage AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_right:
    st.markdown("<div style='padding-top:14px'>", unsafe_allow_html=True)
    if st.button("🗑 Clear chat"):
        sid = st.session_state.active_session_id
        if sid and sid in st.session_state.sessions:
            st.session_state.sessions[sid]["messages"] = []
            st.session_state.sessions[sid]["title"] = "New conversation"
            save_history(st.session_state.sessions)
        st.session_state.prefill = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Messages Area
messages = active_messages()

if not messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">💬</div>
        <div class="empty-title">Zoho Tickets Assistant</div>
        <div class="empty-sub">Ask anything about your support tickets. I'll search and summarize relevant answers.</div>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "Summarize recent tickets",
        "What issues came up most?",
        "Any unresolved tickets?",
        "Tickets from this week",
    ]
    cols = st.columns(len(suggestions))
    for col, suggestion in zip(cols, suggestions):
        with col:
            if st.button(suggestion, use_container_width=True):
                st.session_state.prefill = suggestion
                st.rerun()
else:
    msgs_html = '<div class="messages-scroll"><div class="chat-area">'
    for msg in messages:
        if msg["role"] == "user":
            msgs_html += f"""
            <div class="msg-row user-row">
                <div class="avatar av-user">U</div>
                <div class="msg-col user-col">
                    <div class="msg-label">You</div>
                    <div class="msg-bubble user">{msg["content"]}</div>
                </div>
            </div>"""
        else:
            content = clean_text(msg["content"]).replace("\n", "<br>")
            msgs_html += f"""
            <div class="msg-row">
                <div class="avatar av-bot">Z</div>
                <div class="msg-col">
                    <div class="msg-label">Zoho AI</div>
                    <div class="msg-bubble bot">{content}</div>
                </div>
            </div>"""
    msgs_html += '</div></div>'
    msgs_html += "<script>const el=document.querySelector('.messages-scroll');if(el)el.scrollTop=el.scrollHeight;</script>"
    st.markdown(msgs_html, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Input
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([9, 1])
    with col_input:
        user_input = st.text_input(
            "q",
            value=st.session_state.prefill,
            placeholder="Ask about your support tickets…",
        )
    with col_btn:
        submitted = st.form_submit_button("↑")

st.markdown('<div class="input-hint">Enter to send</div>', unsafe_allow_html=True)

# Submission handling
if submitted and user_input.strip():
    st.session_state.prefill = ""
    append_message("user", user_input.strip())
    with st.spinner("Searching tickets…"):
        answer, _ = chatbot.ask(user_input.strip())
    append_message("assistant", answer)
    st.rerun()