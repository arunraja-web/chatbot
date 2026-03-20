from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
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

# 📩 Request model
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
        raise HTTPException(status_code=500, detail="AI service error")

# 🌍 Global exception handler (🔥 important)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,  # ✅ real HTTP status
        content={
            "status": exc.status_code,  # ✅ body la status
            "success": False,
            "message": exc.detail
        }
    )

# 🏠 Root
@app.get("/")
def home():
    return {
        "status": 200,
        "success": True,
        "message": "API is running 🚀"
    }

# 💬 Chat API
@app.post("/chat")
def chat_api(req: ChatRequest):
    # ❗ validation
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    reply = chat_with_ai(req.message)

    return {
        "status": 200,
        "success": True,
        "user_message": req.message,
        "reply": reply
    }
