from fastapi.testclient import TestClient
from mpesa_client import settings

from app import app

client = TestClient(app)

sandbox = settings.MpesaSandboxSettings()


def test_generate_oauth_token():
    response = client.get(f"/app/v1/m-pesa/generate-token?username={sandbox.consumer_key}&password={sandbox.consumer_secret}")
    assert response.status_code == 200

