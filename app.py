from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from config import SYSTEM_PROMPT

# 🔐 .env load
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"

# 🚀 FastAPI app
app = FastAPI()

# 📩 Request body (UPDATED)
class ChatRequest(BaseModel):
    message: str
    caption: str = ""   # 👈 caption support

# 🤖 LLM function (same logic)
def chat_with_ai(user_input):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("DEBUG ERROR:", e)
        return "⚠️ Konjam issue 😅 later try pannunga."

# 🌐 API endpoint (UPDATED)
@app.post("/chat")
def chat_api(req: ChatRequest):

    # 🔥 Combine caption + comment
    final_input = f"""
Post Caption:
{req.caption}

User Comment:
{req.message}

Instructions:
- Understand the caption first
- Then understand the comment
- Give a relevant, short, friendly reply
- Use same language as user
"""

    reply = chat_with_ai(final_input)

    return {"reply": reply}
