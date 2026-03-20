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

# 📩 Request body
class ChatRequest(BaseModel):
    message: str

# 🤖 Same function (no change)
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
        return "⚠️ Konjam issue bro 😅 later try pannunga."

# 🌐 API endpoint
@app.post("/chat")
def chat_api(req: ChatRequest):
    reply = chat_with_ai(req.message)
    return {"reply": reply}