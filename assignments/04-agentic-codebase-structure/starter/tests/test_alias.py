from contextlib import closing
import pytest
from fastapi.testclient import TestClient

from main import app, get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    with closing(get_db()) as conn:
        conn.execute("DELETE FROM links")
        conn.commit()


def test_custom_alias_empty_400():
    r = client.post("/shorten", json={"url": "https://example.com/empty", "alias": "   "})
    assert r.status_code == 400


def test_custom_alias_reserved_400():
    r = client.post("/shorten", json={"url": "https://example.com/reserved", "alias": "shorten"})
    assert r.status_code == 400


def test_custom_alias_success():
    r = client.post("/shorten", json={"url": "https://example.com/custom", "alias": "my-alias"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == "my-alias"
    assert data["short_url"] == "/my-alias"

    # Verify redirection
    r_red = client.get("/my-alias", follow_redirects=False)
    assert r_red.status_code == 307
    assert r_red.headers["location"] == "https://example.com/custom"


def test_custom_alias_duplicate_409():
    r1 = client.post("/shorten", json={"url": "https://example.com/first", "alias": "duplicate-alias"})
    assert r1.status_code == 200

    r2 = client.post("/shorten", json={"url": "https://example.com/second", "alias": "duplicate-alias"})
    assert r2.status_code == 409


def test_shorten_without_alias_backward_compatibility():
    r = client.post("/shorten", json={"url": "https://example.com/default"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"]
    assert data["short_url"] == f"/{data['code']}"

    r_red = client.get(f"/{data['code']}", follow_redirects=False)
    assert r_red.status_code == 307
    assert r_red.headers["location"] == "https://example.com/default"
