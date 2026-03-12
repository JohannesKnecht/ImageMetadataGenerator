"""Models for the image metadata generation endpoint."""

from pydantic import BaseModel


class GenerateOptions(BaseModel):
    """Generate options for the image metadata generation endpoint."""

    image_description: bool
    image_title: bool
    image_sentiment: bool


class MetaDataRequest(BaseModel):
    """Request body for the image metadata generation endpoint."""

    image_base64: str
    generate_options: GenerateOptions


class GeneratedMetadata(BaseModel):
    """Generated metadata for the image."""

    image_description: str | None
    image_title: str | None
    image_sentiment: str | None


class MetaDataResponse(BaseModel):
    """Request body for the image metadata generation endpoint."""

    status: str
    data: GeneratedMetadata
