import pytest
from fastapi.testclient import TestClient
import database
from main import app, WATER_LITERS_PER_REQUEST

client = TestClient(app)


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()


def test_water_stats_zero_when_no_messages():
    res = client.get("/api/water-stats")
    assert res.status_code == 200
    assert res.json() == {"liters": 0}


def test_water_stats_counts_user_messages_only():
    database.save_message("s1", "Alice", "user", "Q1")
    database.save_message("s1", "Alice", "assistant", "R1")
    database.save_message("s2", "Bob", "user", "Q2")

    res = client.get("/api/water-stats")
    assert res.json() == {"liters": round(2 * WATER_LITERS_PER_REQUEST, 1)}


def test_water_stats_persists_across_sessions():
    for i in range(5):
        database.save_message(f"s{i}", f"User{i}", "user", f"Q{i}")

    res = client.get("/api/water-stats")
    assert res.json() == {"liters": round(5 * WATER_LITERS_PER_REQUEST, 1)}
