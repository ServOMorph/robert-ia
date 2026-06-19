import json
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import database
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()


def _make_stream_mock(tokens: list[str]):
    async def aiter_lines():
        for token in tokens:
            yield json.dumps({"message": {"content": token}, "done": False})
        yield json.dumps({"message": {"content": ""}, "done": True})

    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.aiter_lines = aiter_lines

    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_res)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def _parse_ndjson(response) -> list[dict]:
    return [json.loads(line) for line in response.text.splitlines() if line]


def test_chat_streams_tokens():
    with patch("httpx.AsyncClient.stream", return_value=_make_stream_mock(["Bon", "jour", " !"])):
        res = client.post("/api/chat", json={
            "session_id": "s1",
            "pseudo": "Alice",
            "message": "Salut",
        })
    assert res.status_code == 200
    chunks = _parse_ndjson(res)
    tokens = [c["token"] for c in chunks if "token" in c]
    assert "".join(tokens) == "Bonjour !"


def test_chat_saves_messages_to_db():
    with patch("httpx.AsyncClient.stream", return_value=_make_stream_mock(["Réponse"])):
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


def test_chat_injects_history():
    database.save_message("s3", "Bob", "user", "Bonjour")
    database.save_message("s3", "Bob", "assistant", "Salut")

    captured = {}

    original_stream = httpx.AsyncClient.stream

    def capturing_stream(self, method, url, **kwargs):
        captured["messages"] = kwargs.get("json", {}).get("messages", [])
        return _make_stream_mock(["Ok"])

    with patch("httpx.AsyncClient.stream", capturing_stream):
        client.post("/api/chat", json={
            "session_id": "s3",
            "pseudo": "Bob",
            "message": "Suite",
        })

    roles = [m["role"] for m in captured["messages"]]
    assert roles[0] == "system"
    assert "user" in roles
    assert "assistant" in roles


def test_chat_error_when_ollama_unavailable():
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(side_effect=httpx.ConnectError("down"))
    cm.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient.stream", return_value=cm):
        res = client.post("/api/chat", json={
            "session_id": "s4",
            "pseudo": "X",
            "message": "test",
        })
    assert res.status_code == 200
    chunks = _parse_ndjson(res)
    assert any("error" in c for c in chunks)
