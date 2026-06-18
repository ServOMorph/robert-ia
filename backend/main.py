from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from database import init_db, save_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Robert-IA", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"


class ChatRequest(BaseModel):
    session_id: str
    pseudo: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    save_message(req.session_id, req.pseudo, "user", req.message)

    payload = {
        "model": MODEL,
        "prompt": req.message,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            res = await client.post(OLLAMA_URL, json=payload)
            res.raise_for_status()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Ollama non disponible")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=str(e))

    reply = res.json()["response"]
    save_message(req.session_id, req.pseudo, "assistant", reply)
    return {"reply": reply}
