import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx

from database import init_db, save_message, get_head, get_history
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
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8001", "http://127.0.0.1:8001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"
HEAD_K = 4
HISTORY_WINDOW = 16
NUM_CTX = 4096


class ChatRequest(BaseModel):
    session_id: str
    pseudo: str
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/ready")
async def model_ready():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get("http://localhost:11434/api/ps")
            models = res.json().get("models", [])
            loaded = any(m.get("name", "").startswith(MODEL) for m in models)
            return {"ready": loaded}
    except Exception:
        return {"ready": False}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    save_message(req.session_id, req.pseudo, "user", req.message)

    head = get_head(req.session_id, k=HEAD_K)
    tail = get_history(req.session_id, limit=HISTORY_WINDOW)
    head_ids = {r["id"] for r in head}
    combined = head + [r for r in tail if r["id"] not in head_ids]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
        {"role": r["role"], "content": r["content"]} for r in combined
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "keep_alive": -1,
        "options": {"num_ctx": NUM_CTX},
    }

    async def stream():
        full_reply = []
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", OLLAMA_URL, json=payload) as res:
                    if res.status_code != 200:
                        yield json.dumps({"error": f"Erreur Ollama {res.status_code}"}) + "\n"
                        return
                    async for line in res.aiter_lines():
                        if not line:
                            continue
                        chunk = json.loads(line)
                        token = chunk.get("message", {}).get("content", "")
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


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/{path:path}")
def serve_static(path: str):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


if os.path.isdir(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")
