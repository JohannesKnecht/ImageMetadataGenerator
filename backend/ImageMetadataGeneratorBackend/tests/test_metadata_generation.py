"""Tests for the FastAPI Image Metadata Generation API."""

import base64

from fastapi.testclient import TestClient

from imagemetadatageneratorbackend import invoke_metadata_generator
from imagemetadatageneratorbackend.main import app

client = TestClient(app)


def test_invoke_metadata_generator():
    """Verify that the Image Metadata Generation is working end-to-end."""
    with open("tests/img.png", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    invoke_metadata_generator(image_base64)
