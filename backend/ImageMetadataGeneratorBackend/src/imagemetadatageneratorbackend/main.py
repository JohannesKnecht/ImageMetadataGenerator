"""FastAPI application for Image Metadata Generation."""

import os

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from imagemetadatageneratorbackend.models import (
    GeneratedMetadata,
    MetaDataRequest,
    MetaDataResponse,
)

app = FastAPI()
router = APIRouter(prefix="/api/v1")

origins = [
    "http://localhost",
]

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

    return MetaDataResponse(
        status="success",
        data=GeneratedMetadata(
            image_title="tbd",
            image_description="tbd",
            image_sentiment=None,
        ),
    )


app.include_router(router)
