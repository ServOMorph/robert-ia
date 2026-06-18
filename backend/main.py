import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

from database import init_db, save_message
from prompt import SYSTEM_PROMPT


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            await client.post(OLLAMA_URL, json={"model": MODEL, "prompt": "", "keep_alive": -1})
    except Exception:
        pass
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    save_message(req.session_id, req.pseudo, "user", req.message)

    payload = {
        "model": MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": req.message,
        "stream": True,
        "keep_alive": -1,
    }

    async def stream():
        full_reply = []
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", OLLAMA_URL, json=payload) as res:
                    if res.status_code != 200:
                        yield json.dumps({"error": f"Erreur Ollama {res.status_code}"})
                        return
                    async for line in res.aiter_lines():
                        if not line:
                            continue
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        if token:
                            full_reply.append(token)
                            yield json.dumps({"token": token}) + "\n"
                        if chunk.get("done"):
                            break
        except httpx.ConnectError:
            yield json.dumps({"error": "Ollama non disponible"}) + "\n"
            return

        save_message(req.session_id, req.pseudo, "assistant", "".join(full_reply))

    return StreamingResponse(stream(), media_type="application/x-ndjson")
