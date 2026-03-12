"""Tests for the FastAPI Image Metadata Generation API."""

import base64

from fastapi.testclient import TestClient

from imagemetadatageneratorbackend.main import app

client = TestClient(app)


def test_metadatagenerator_success():
    """Verify that the Image Metadata Generation API is working end-to-end."""
    with open("tests/img.png", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read())

    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": image_base64.decode("utf-8"),
            "generate_options": {"image_description": True, "image_title": True, "image_sentiment": True},
        },
    )
    assert response.status_code == 200
    response.json()
    assert "success" in response.text.lower()
