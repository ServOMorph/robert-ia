import tempfile
from pathlib import Path
import pytest
import database


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()


def test_init_db_creates_table():
    conn = database.get_connection()
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    assert cursor.fetchone() is not None


def test_save_message_user():
    database.save_message("sess-1", "Alice", "user", "Bonjour")
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM messages WHERE session_id='sess-1'").fetchone()
    assert row["pseudo"] == "Alice"
    assert row["role"] == "user"
    assert row["content"] == "Bonjour"


def test_save_message_assistant():
    database.save_message("sess-2", "Anonyme", "assistant", "Réponse test")
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM messages WHERE session_id='sess-2'").fetchone()
    assert row["role"] == "assistant"


def test_multiple_messages_same_session():
    database.save_message("sess-3", "Bob", "user", "Q1")
    database.save_message("sess-3", "Bob", "assistant", "R1")
    conn = database.get_connection()
    rows = conn.execute("SELECT * FROM messages WHERE session_id='sess-3'").fetchall()
    assert len(rows) == 2


def test_get_history_returns_ordered_messages():
    database.save_message("sess-4", "Alice", "user", "Q1")
    database.save_message("sess-4", "Alice", "assistant", "R1")
    database.save_message("sess-4", "Alice", "user", "Q2")
    history = database.get_history("sess-4")
    assert len(history) == 3
    assert history[0] == {"role": "user", "content": "Q1"}
    assert history[1] == {"role": "assistant", "content": "R1"}
    assert history[2] == {"role": "user", "content": "Q2"}


def test_get_history_respects_limit():
    for i in range(10):
        database.save_message("sess-5", "Alice", "user", f"Q{i}")
    history = database.get_history("sess-5", limit=4)
    assert len(history) == 4
    assert history[-1]["content"] == "Q9"


def test_get_history_empty_session():
    history = database.get_history("sess-inexistant")
    assert history == []
