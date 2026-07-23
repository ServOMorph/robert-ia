import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "robert.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                pseudo TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)")
        conn.commit()


def save_message(session_id: str, pseudo: str, role: str, content: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, pseudo, role, content) VALUES (?, ?, ?, ?)",
            (session_id, pseudo, role, content),
        )
        conn.commit()


def get_head(session_id: str, k: int = 4) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, role, content FROM messages WHERE session_id = ? ORDER BY id ASC LIMIT ?",
            (session_id, k),
        ).fetchall()
    return [{"id": r["id"], "role": r["role"], "content": r["content"]} for r in rows]


def count_user_messages() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM messages WHERE role = 'user'").fetchone()
    return row["n"]


def get_history(session_id: str, limit: int = 8) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, role, content FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
    return [{"id": r["id"], "role": r["role"], "content": r["content"]} for r in reversed(rows)]
