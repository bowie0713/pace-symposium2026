import streamlit as st
from mongodb_RAG import ZohoTicket

@st.cache_resource
def load_chatbot():
    return ZohoTicket()

st.set_page_config(
    page_title="Zoho Tickets AI",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, .stApp {
    background-color: #0b0f1a !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #e8eaf0 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 0 0 0 !important;
    max-width: 760px !important;
    margin: 0 auto !important;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 0 14px 0;
    border-bottom: 1px solid rgba(99,160,255,0.15);
    margin-bottom: 8px;
}
.topbar-logo {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #1a6fd4, #c9a227);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; line-height: 1;
}
.topbar-title { font-size: 16px; font-weight: 600; color: #e8eaf0; }
.topbar-sub   { font-size: 12px; color: #5a7aaa; margin-top: 1px; }

/* ── Chat messages ── */
.chat-area {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 12px 0;
    min-height: 60px;
}

/* Message row */
.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 6px 0;
    animation: rise 0.2s ease both;
}
@keyframes rise {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.avatar {
    width: 30px; height: 30px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: #fff;
    margin-top: 2px;
}
.av-user { background: linear-gradient(135deg, #1a6fd4, #4d9fff); }
.av-bot  { background: linear-gradient(135deg, #b8891e, #e8bf4a); }

.msg-col { flex: 1; min-width: 0; }
.msg-label {
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.05em;
    color: #5a7aaa; margin-bottom: 5px;
}
.msg-bubble {
    font-size: 16px; line-height: 1.75; color: #e8eaf0;
}
.msg-bubble.user {
    background: #0d1e38;
    border: 1px solid rgba(26,111,212,0.35);
    border-radius: 14px 14px 14px 4px;
    padding: 11px 15px;
    display: inline-block;
    max-width: 100%;
}
.msg-bubble.bot {
    background: transparent;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 56px 20px 32px;
    animation: rise 0.35s ease both;
}
.empty-icon {
    width: 54px; height: 54px;
    background: linear-gradient(135deg, #1a6fd4, #c9a227);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; margin: 0 auto 18px;
    box-shadow: 0 6px 28px rgba(26,111,212,0.3);
}
.empty-title {
    font-size: 22px; font-weight: 600;
    color: #e8eaf0; letter-spacing: -0.03em; margin-bottom: 8px;
}
.empty-sub {
    font-size: 15px; color: #5a7aaa; line-height: 1.6; max-width: 380px; margin: 0 auto;
}

/* ── Input area ── */
div[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Text input styling */
div[data-testid="stTextInput"] > div > div {
    background: #111827 !important;
    border: 1px solid rgba(99,160,255,0.2) !important;
    border-radius: 12px !important;
    color: #e8eaf0 !important;
}
div[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(26,111,212,0.6) !important;
    box-shadow: 0 0 0 3px rgba(26,111,212,0.1) !important;
}
div[data-testid="stTextInput"] input {
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    background: transparent !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #5a7aaa !important; }
div[data-testid="stTextInput"] label { display: none !important; }

/* Submit button — gold */
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #c9a227, #e8bf4a) !important;
    color: #0b0f1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    height: 44px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: filter 0.15s, transform 0.15s !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    filter: brightness(1.1) !important;
    transform: scale(1.02) !important;
}

/* Clear button */
div[data-testid="stButton"] button {
    background: #111827 !important;
    color: #5a7aaa !important;
    border: 1px solid rgba(99,160,255,0.15) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 4px 12px !important;
    transition: color 0.15s, border-color 0.15s !important;
}
div[data-testid="stButton"] button:hover {
    color: #e8eaf0 !important;
    border-color: rgba(99,160,255,0.35) !important;
}

/* ── Suggestion chip buttons ── */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
    background: #111827 !important;
    border: 1px solid rgba(99,160,255,0.18) !important;
    border-radius: 20px !important;
    padding: 8px 15px !important;
    font-size: 14px !important;
    color: #5a7aaa !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.14s !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 40px !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
    color: #e8eaf0 !important;
    border-color: rgba(99,160,255,0.4) !important;
    background: #1a2540 !important;
}

/* Divider */
hr { border-color: rgba(99,160,255,0.12) !important; margin: 8px 0 !important; }

/* Spinner */
.stSpinner > div { color: #5a7aaa !important; }

/* Scrollable messages container */
.messages-scroll {
    max-height: 55vh;
    overflow-y: auto;
    padding-right: 4px;
    margin-bottom: 8px;
}
.messages-scroll::-webkit-scrollbar { width: 3px; }
.messages-scroll::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 3px; }

/* Bottom hint */
.input-hint { font-size: 12px; color: #5a7aaa; text-align: center; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

chatbot = load_chatbot()

# ── Top bar ────────────────────────────────────────────────────────────────────
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
        st.session_state.messages = []
        st.session_state.prefill = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ──Chat Messages ───────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon"></div>
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
    # Scrollable message container
    msgs_html = '<div class="messages-scroll"><div class="chat-area">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            msgs_html += f"""
            <div class="msg-row">
                <div class="avatar av-user">U</div>
                <div class="msg-col">
                    <div class="msg-label">You</div>
                    <div class="msg-bubble user">{msg["content"]}</div>
                </div>
            </div>"""
        else:
            content = msg["content"].replace("\n", "<br>")
            msgs_html += f"""
            <div class="msg-row">
                <div class="avatar av-bot">Z</div>
                <div class="msg-col">
                    <div class="msg-label">Zoho AI</div>
                    <div class="msg-bubble bot">{content}</div>
                </div>
            </div>"""
    msgs_html += '</div></div>'

    # Auto-scroll to bottom via JS
    msgs_html += """
    <script>
        const el = document.querySelector('.messages-scroll');
        if (el) el.scrollTop = el.scrollHeight;
    </script>"""

    st.markdown(msgs_html, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Input form ─────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([9, 1])
    with col_input:
        user_input = st.text_input(
            "q",
            value=st.session_state.prefill,
            placeholder="Ask about your support tickets…"
        )
    with col_btn:
        submitted = st.form_submit_button("↑")

# question = st.text_input(label="Your Question", placeholder="E.g., Summarize Tickets for the last 10 days?")
# with st.spinner("Searching tickets and generating answer..."):
#     answer, _ = chatbot.ask(question)


st.markdown('<div class="input-hint">Enter to send</div>', unsafe_allow_html=True)

# ── Handle submission ──────────────────────────────────────────────────────────
if submitted and user_input.strip():
    st.session_state.prefill = ""
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner("Searching tickets…"):
        answer, _ = chatbot.ask(user_input.strip())
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()