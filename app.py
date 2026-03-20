from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from config import SYSTEM_PROMPT

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

# 🤖 AI function
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
        raise Exception("AI service error")

# 🏠 Root
@app.get("/")
def home():
    return {"message": "API is running 🚀"}

# 💬 Chat API with error handling
@app.post("/chat")
def chat_api(req: ChatRequest):
    try:
        # 🔹 empty check
        if not req.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        reply = chat_with_ai(req.message)

        return {
            "success": True,
            "reply": reply
        }

    except HTTPException as e:
        # known errors
        raise e

    except Exception as e:
        print("API ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please try again later."
        )
