"""Tests for the FastAPI Image Metadata Generation API."""

import base64

from fastapi.testclient import TestClient

from imagemetadatageneratorbackend.error_responses import MALFORMED_B64, NO_OPTIONS
from imagemetadatageneratorbackend.main import app
from imagemetadatageneratorbackend.models import MetaDataResponse

client = TestClient(app)


str_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="


def test_metadatagenerator_success_file():
    """Verify that the Image Metadata Generation API is working end-to-end."""
    with open("tests/img.png", "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": image_b64,
            "generate_options": {"image_description": True, "image_title": True, "image_sentiment": True},
        },
    )
    assert response.status_code == 200, f"failed with status code {response.status_code}: {response.text}"
    metadata_response = MetaDataResponse(**response.json())
    assert metadata_response.status.lower() == "success"


def test_metadatagenerator_success_str():
    """Verify that the Image Metadata Generation API is working end-to-end."""
    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": str_data,
            "generate_options": {"image_description": True, "image_title": True, "image_sentiment": True},
        },
    )
    assert response.status_code == 200, f"failed with status code {response.status_code}: {response.text}"
    metadata_response = MetaDataResponse(**response.json())
    assert metadata_response.status.lower() == "success"


def test_metadatagenerator_failure_no_options():
    """Verify that the Image Metadata Generation API returns an error if no metadata fields are requested."""
    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": str_data,
            "generate_options": {"image_description": False, "image_title": False, "image_sentiment": False},
        },
    )
    assert response.status_code == 400
    assert NO_OPTIONS in response.text


def test_metadatagenerator_failure_malformed_b64():
    """Verify that the Image Metadata Generation API returns an error if the base64 image data is malformed."""
    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": "bad_base64_data",
            "generate_options": {"image_description": True, "image_title": True, "image_sentiment": True},
        },
    )
    assert response.status_code == 400
    assert MALFORMED_B64 in response.text


def test_metadatagenerator_config():
    """Verify that the Image Metadata Generation API is using the config values."""
    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": str_data,
            "generate_options": {"image_description": True, "image_title": True, "image_sentiment": True},
        },
    )
    assert response.status_code == 200, f"failed with status code {response.status_code}: {response.text}"
    metadata_response = MetaDataResponse(**response.json())
    assert metadata_response.status.lower() == "success"
    assert metadata_response.data.image_description is not None
    assert metadata_response.data.image_title is not None
    assert metadata_response.data.image_sentiment is not None

    response = client.post(
        "/api/v1/image/metadatagenerator",
        json={
            "image_base64": str_data,
            "generate_options": {"image_description": True, "image_title": False, "image_sentiment": True},
        },
    )
    assert response.status_code == 200, f"failed with status code {response.status_code}: {response.text}"
    metadata_response = MetaDataResponse(**response.json())
    assert metadata_response.status.lower() == "success"
    assert metadata_response.data.image_description is not None
    assert metadata_response.data.image_title is None
    assert metadata_response.data.image_sentiment is not None
