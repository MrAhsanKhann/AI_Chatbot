from groq import Groq
from dotenv import load_dotenv
import os

from config import MODEL_NAME

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

# =====================================
# Create Groq Client
# =====================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================
# System Prompt
# =====================================

SYSTEM_PROMPT = """
You are a professional AI assistant.

Rules:

- Be helpful.
- Be friendly.
- Keep answers concise.
- Use Markdown formatting when appropriate.
- Never reveal internal reasoning.
- If you don't know something, say so honestly.
"""

# =====================================
# Normal Response
# =====================================

def get_ai_response(messages):

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + messages,

        temperature=0.3,
        max_completion_tokens=250,
        top_p=0.9

    )

    return response.choices[0].message.content


# =====================================
# Streaming Response
# =====================================

def stream_ai_response(messages):

    stream = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + messages,

        temperature=0.3,
        max_completion_tokens=250,
        top_p=0.9,

        stream=True

    )

    for chunk in stream:

        if (
            chunk.choices
            and chunk.choices[0].delta
            and chunk.choices[0].delta.content
        ):

            yield chunk.choices[0].delta.content