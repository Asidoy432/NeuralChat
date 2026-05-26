import streamlit as st
import anthropic
import requests
import base64
from PIL import Image
from io import BytesIO

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuralChat AI · Lab 10.0",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Syne', sans-serif !important;
    background-color: #080c14 !important;
}
.neural-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0 1.2rem 0;
}
.neural-icon { font-size: 1.8rem; color: #00c8ff; }
.neural-title { font-size: 1.5rem; font-weight: 800; color: #e8f0fe; letter-spacing: -0.02em; }
.neural-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #00c8ff;
    background: rgba(0,200,255,0.1);
    border: 1px solid rgba(0,200,255,0.25);
    padding: 3px 9px;
    border-radius: 20px;
    letter-spacing: 0.06em;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0f1623;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e2d42;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7fa3 !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.4rem 1.1rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #00c8ff !important;
    color: #000 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }
.stChatMessage {
    background: #0f1e30 !important;
    border: 1px solid #1e2d42 !important;
    border-radius: 14px !important;
}
[data-testid="stChatMessageContent"] p {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    color: #e8f0fe !important;
}
[data-testid="stChatInputContainer"] {
    background: #0f1623 !important;
    border: 1px solid #1e2d42 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInputContainer"]:focus-within {
    border-color: #00c8ff !important;
}
.stTextArea textarea {
    background: #0f1623 !important;
    border: 1px solid #1e2d42 !important;
    border-radius: 12px !important;
    color: #e8f0fe !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: #00c8ff !important;
    box-shadow: 0 0 0 1px #00c8ff !important;
}
.stTextArea label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    color: #00c8ff !important;
    text-transform: uppercase !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00c8ff, #7b2fff) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1.4rem !important;
    transition: opacity 0.18s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stDownloadButton > button {
    background: transparent !important;
    color: #00c8ff !important;
    border: 1px solid rgba(0,200,255,0.3) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,200,255,0.08) !important;
}
.stImage img {
    border-radius: 14px;
    border: 1px solid #1e2d42;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
.stSpinner > div { border-top-color: #00c8ff !important; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
::-webkit-scrollbar       { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e2d42; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="neural-header">
    <span class="neural-icon">◈</span>
    <span class="neural-title">NeuralChat</span>
    <span class="neural-badge">AI · Lab 10.0</span>
</div>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
APPDEPLOY_API = "https://615d0f360209490887.v2.appdeploy.ai"

# ── Anthropic client ──────────────────────────────────────────────────────────
@st.cache_resource
def get_anthropic_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_chat, tab_image = st.tabs(["💬  Chat", "🎨  Image Gen"])

# ─────────────────────────────────────────────────────────────────────────────
# CHAT TAB
# ─────────────────────────────────────────────────────────────────────────────
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Empty state
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;opacity:0.4;padding:2.5rem 1rem;">
            <div style="font-size:2.5rem;color:#00c8ff;margin-bottom:0.8rem;">◈</div>
            <p style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#00c8ff;
               letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">
               LLM: Large Language Model
            </p>
            <p style="font-size:0.85rem;color:#6b7fa3;">Ask anything. Powered by Claude AI.</p>
        </div>
        """, unsafe_allow_html=True)

    # Render history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input
    if user_input := st.chat_input("Type your message…"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner(""):
                try:
                    client = get_anthropic_client()
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1024,
                        system="You are a helpful, knowledgeable AI assistant for a university AI lab. Be concise but thorough.",
                        messages=st.session_state.messages,
                    )
                    reply = response.content[0].text
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

    # Clear button
    if st.session_state.messages:
        if st.button("🗑 Clear Chat", key="clear"):
            st.session_state.messages = []
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE GEN TAB  —  powered by AppDeploy /api/image (Amazon Nova Canvas)
# ─────────────────────────────────────────────────────────────────────────────
with tab_image:
    prompt = st.text_area(
        "Image Prompt",
        placeholder="Describe the image you want to generate…",
        height=110,
        key="img_prompt",
    )

    generate_clicked = st.button(
        "✦ Generate Image",
        use_container_width=True,
        key="gen_btn",
    )

    if generate_clicked:
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Creating your image…"):
                try:
                    res = requests.post(
                        f"{APPDEPLOY_API}/api/image",
                        json={"prompt": prompt.strip()},
                        timeout=90,
                    )

                    if res.status_code == 200:
                        data      = res.json()
                        img_data  = data["image"]["data"]      # base64 string
                        img_mime  = data["image"]["mimeType"]  # e.g. image/png
                        img_bytes = base64.b64decode(img_data)

                        img = Image.open(BytesIO(img_bytes))
                        st.image(img, use_container_width=True)
                        st.download_button(
                            "↓ Download Image",
                            data=img_bytes,
                            file_name="generated.png",
                            mime=img_mime,
                            use_container_width=True,
                        )
                    else:
                        st.error(
                            f"⚠️ Generation failed (status {res.status_code}). "
                            "Try a different prompt."
                        )

                except requests.Timeout:
                    st.error("⚠️ Request timed out. Please try again.")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

    if not generate_clicked:
        st.markdown("""
        <div style="text-align:center;opacity:0.3;padding:2rem 1rem;">
            <div style="font-size:2.8rem;color:#00c8ff;margin-bottom:0.8rem;">◈</div>
            <p style="font-size:0.85rem;color:#6b7fa3;">Your generated image will appear here</p>
        </div>
        """, unsafe_allow_html=True)
