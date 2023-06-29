from fastapi.testclient import TestClient
from app.mpesa_client import settings

from app.main import app

client = TestClient(app)

sandbox = settings.MpesaSandboxSettings()


def test_generate_oauth_token():
    response = client.get(f"/app/v1/m-pesa/generate-token?username={sandbox.c2b_consumer_key}&password={sandbox.c2b_consumer_secret}")
    assert response.status_code == 200

