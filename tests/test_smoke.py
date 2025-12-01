# tests/test_smoke.py
from app import create_app

def test_create_app():
    app = create_app()
    assert app is not None
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code in (200, 302)
