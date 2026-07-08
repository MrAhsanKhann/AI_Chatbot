import streamlit as st
import ai_engine

from config import (
    APP_TITLE,
    APP_CAPTION,
    PAGE_ICON,
    LAYOUT,
    MODEL_NAME
)

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# =====================================
# Session State
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# Sidebar
# =====================================

with st.sidebar:

    st.title("⚙️ AI Chatbot")

    st.markdown("---")

    st.write("### 🤖 Model")
    st.code(MODEL_NAME)

    st.markdown("---")

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    st.success("🟢 Connected")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =====================================
# Header
# =====================================

st.title(APP_TITLE)
st.caption(APP_CAPTION)

# =====================================
# Show Previous Messages
# =====================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================
# Chat Input
# =====================================

prompt = st.chat_input("Ask me anything...")

if prompt:

    # ------------------------
    # Save User Message
    # ------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ------------------------
    # AI Streaming Response
    # ------------------------

    history = st.session_state.messages[-8:]

    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        try:

            for chunk in ai_engine.stream_ai_response(history):

                full_response += chunk

                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )

        except Exception as e:

            st.error(str(e))