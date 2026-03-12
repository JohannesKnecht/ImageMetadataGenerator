"""FastAPI application for Image Metadata Generation."""

import base64
import os

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from imagemetadatageneratorbackend.error_responses import MALFORMED_B64, NO_OPTIONS
from imagemetadatageneratorbackend.metadata_creation import BadLLMResponseError, call_vision_llm
from imagemetadatageneratorbackend.models import (
    MetaDataRequest,
    MetaDataResponse,
)

app = FastAPI()
router = APIRouter(prefix="/api/v1")

origins = [
    "http://localhost",
]

DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

app.add_middleware(
    CORSMiddleware,  # type: ignore[invalid-argument-type]
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def resource_check() -> None:
    """Verify that required environment variables are set."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")


@router.post("/image/metadatagenerator")
async def metadata_generator(metadata_request_data: MetaDataRequest) -> MetaDataResponse:
    """Generate metadata from the image.

    Args:
        metadata_request_data: image

    Returns:
        The generated metadata

    """
    resource_check()

    try:
        image_bytes = base64.b64decode(metadata_request_data.image_base64, validate=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=MALFORMED_B64) from e

    if DEBUG:
        os.makedirs("temp_data", exist_ok=True)
        with open("temp_data/img.png", "wb") as f:
            f.write(image_bytes)

    if not (
        metadata_request_data.generate_options.image_description
        or metadata_request_data.generate_options.image_title
        or metadata_request_data.generate_options.image_sentiment
    ):
        raise HTTPException(status_code=400, detail=NO_OPTIONS)

    try:
        call_vision_llm_response = call_vision_llm(image_bytes, metadata_request_data.generate_options)
    except Exception as e:
        if isinstance(e, BadLLMResponseError):
            raise HTTPException(status_code=422, detail="Bad LLM response") from e
        elif isinstance(e, BadLLMResponseError):
            raise HTTPException(status_code=502, detail="LLM service error") from e
        else:
            raise HTTPException(status_code=500, detail="Unknown error") from e

    return MetaDataResponse(
        status="success",
        data=call_vision_llm_response,
    )


app.include_router(router)
