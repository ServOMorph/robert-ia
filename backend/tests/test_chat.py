import json
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
import database
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()


def _mock_ollama(reply: str):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value={"response": reply})
    return mock_response


def test_chat_returns_reply():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = _mock_ollama("Bonjour !")
        res = client.post("/api/chat", json={
            "session_id": "s1",
            "pseudo": "Alice",
            "message": "Salut",
        })
    assert res.status_code == 200
    assert res.json()["reply"] == "Bonjour !"


def test_chat_saves_messages_to_db():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = _mock_ollama("Réponse")
        client.post("/api/chat", json={
            "session_id": "s2",
            "pseudo": "Bob",
            "message": "Question",
        })
    conn = database.get_connection()
    rows = conn.execute("SELECT role FROM messages WHERE session_id='s2'").fetchall()
    roles = [r["role"] for r in rows]
    assert "user" in roles
    assert "assistant" in roles


def test_chat_503_when_ollama_unavailable():
    with patch("httpx.AsyncClient.post", side_effect=httpx.ConnectError("down")):
        res = client.post("/api/chat", json={
            "session_id": "s3",
            "pseudo": "X",
            "message": "test",
        })
    assert res.status_code == 503
    assert "Ollama" in res.json()["detail"]
