"""Logic for generating image metadata."""

from __future__ import annotations

from typing import TYPE_CHECKING

from imagemetadatageneratorbackend.chain import chain

if TYPE_CHECKING:
    from imagemetadatageneratorbackend.models import GeneratedMetadata, GenerateOptions


class BadLLMResponseError(Exception):
    """Exception raised when the LLM response is malformed."""

    pass


class LLMServiceError(Exception):
    """Exception raised when the LLM service returns an error."""

    pass


def call_vision_llm(image_base64, requested_fields_list: GenerateOptions) -> GeneratedMetadata:
    """Call the vision LLM to generate metadata for the image.

    Args:
        image_base64: The image to generate metadata for.
        requested_fields_list: The list of metadata fields to generate.

    Returns:
        The generated metadata.
    """
    return chain(image_base64, requested_fields_list)
