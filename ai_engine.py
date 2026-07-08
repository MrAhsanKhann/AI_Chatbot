import ollama
from config import MODEL_NAME

SYSTEM_PROMPT = """
You are a professional AI assistant.

Rules:
- Give direct answers.
- Keep responses concise.
- Do not reveal your internal reasoning.
- Be friendly and professional.
"""

def get_ai_response(messages):

    response = ollama.chat(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + messages,

        options={
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 180
        }

    )

    return response["message"]["content"]