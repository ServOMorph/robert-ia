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
