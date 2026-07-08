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
# Page Configuration
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

    st.markdown("---")

    st.success("🟢 Ollama Connected")

    st.info("Running Locally")

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
# Display Previous Messages
# =====================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================
# Chat Input
# =====================================

user_prompt = st.chat_input("Type your message...")

if user_prompt:

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:

        with st.spinner("🤖 AI is thinking..."):

            # Send only recent conversation
            history = st.session_state.messages[-8:]

            ai_reply = ai_engine.get_ai_response(history)

        # Save AI Response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

    except Exception as e:

        error_message = f"❌ Error:\n\n{str(e)}"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )

        with st.chat_message("assistant"):
            st.error(error_message)