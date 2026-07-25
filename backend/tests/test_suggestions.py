from fastapi.testclient import TestClient
from main import app, load_suggestions, CONTEXT_SUGGESTIONS

client = TestClient(app)


def test_suggestions_endpoint_returns_active_context_list():
    res = client.get("/api/suggestions")
    assert res.status_code == 200
    assert res.json() == {"suggestions": CONTEXT_SUGGESTIONS}


def test_suggestions_missing_file_returns_empty_list():
    assert load_suggestions("contexte_inexistant") == []


def test_load_suggestions_skips_blank_and_comment_lines(tmp_path, monkeypatch):
    import main

    path = tmp_path / "demo.suggestions.txt"
    path.write_text("# commentaire\n\nQuestion A\n  Question B  \n\n", encoding="utf-8")
    monkeypatch.setattr(main, "CONTEXTS_DIR", str(tmp_path))

    assert load_suggestions("demo") == ["Question A", "Question B"]


def test_shipped_contexts_have_suggestions():
    for name in ("invariable", "moulin_du_sud"):
        assert len(load_suggestions(name)) == 3
