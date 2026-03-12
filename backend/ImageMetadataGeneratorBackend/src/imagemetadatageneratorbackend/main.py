"""FastAPI application for Image Metadata Generation."""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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


class RequestData(BaseModel):
    """Request body for the image metadata generation endpoint."""

    text: str


def resource_check() -> None:
    """Verify that required environment variables are set."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")


@app.post("/image/metadatagenerator")
async def metadata_generator(request_data: RequestData) -> str:
    """Generate metadata from the image.

    Args:
        request_data: image

    Returns:
        The generated metadata

    """
    resource_check()

    text = request_data.text
    if len(text) > 1000:
        raise HTTPException(status_code=400, detail="text too long")

    return "success"
