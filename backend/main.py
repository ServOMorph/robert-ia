from fastapi import FastAPI

app = FastAPI(title="Robert-IA")


@app.get("/health")
def health():
    return {"status": "ok"}
