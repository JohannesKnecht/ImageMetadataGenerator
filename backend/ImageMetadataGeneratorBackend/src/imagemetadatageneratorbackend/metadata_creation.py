"""Logic for generating image metadata."""

from imagemetadatageneratorbackend.models import GeneratedMetadata, GenerateOptions


class BadLLMResponseError(Exception):
    """Exception raised when the LLM response is malformed."""

    pass


class LLMServiceError(Exception):
    """Exception raised when the LLM service returns an error."""

    pass


def call_vision_llm(image, requested_fields_list: GenerateOptions) -> GeneratedMetadata:
    """Call the vision LLM to generate metadata for the image.

    Args:
        image: The image to generate metadata for.
        requested_fields_list: The list of metadata fields to generate.

    Returns:
        The generated metadata.
    """
    return GeneratedMetadata(
        image_title="tbd" if requested_fields_list.image_title else None,
        image_description="tbd" if requested_fields_list.image_description else None,
        image_sentiment="tbd" if requested_fields_list.image_sentiment else None,
    )
