"""Tests for the FastAPI Image Metadata Generation API."""

from fastapi.testclient import TestClient

from imagemetadatageneratorbackend.main import app

client = TestClient(app)


def test_main():
    """Verify that the Image Metadata Generation API is working end-to-end."""
    response = client.post("/image/metadatagenerator", json={"text": "coming soon"})
    assert response.status_code == 200
    response.json()
    assert "success" in response.text.lower()
