from fastapi.testclient import TestClient
from 1_validation import app

client = TestClient(app)

def test_convert():
    res = client.get("/convert?from_currency=USD&to_currency=EUR&amount=100")
    assert res.status_code == 200
    assert "result" in res.json()