"""Chain for generating image metadata."""

from __future__ import annotations

from typing import TYPE_CHECKING

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage
from langchain_core.messages import BaseMessage, HumanMessage

from imagemetadatageneratorbackend.models import GeneratedMetadata, GenerateOptions

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel

MODEL_NAME = "gpt-5-nano"


def get_model() -> BaseChatModel:
    """Return the chat model used for knowledge base summarisation.

    Returns:
        An initialized chat model instance.
    """
    return init_chat_model(MODEL_NAME)


def get_messages(image_base64: str, config: GenerateOptions) -> list[BaseMessage]:
    """Build the message list for the knowledge base summarisation chain.

    Args:
        image_base64: The image data to generate metadata for.
        config: The image data to generate metadata for.

    Returns:
        A list of messages to send to the chat model.
    """
    system_msg = SystemMessage(
        """
        Given the image, generate metadata for it. Use the response spec as reference.
        Only populate the fields that are requested in the config.
        The other fields should be None.
        """.strip()
    )
    human_msgs = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "base64": image_base64,
                    "mime_type": "image/png",
                },
            ],
        },
        HumanMessage(f"Config: {config.model_dump_json()}"),
    ]

    messages = [system_msg] + human_msgs

    return messages


def chain(image_base64, config) -> GeneratedMetadata:
    """Run the image metadata generation chain.

    Args:
        image_base64: The image data to generate metadata for.
        config: The image data to generate metadata for.

    Returns:
        The generated metadata as a string.
    """
    response = get_model().with_structured_output(GeneratedMetadata).invoke(get_messages(image_base64, config))
    assert isinstance(response, GeneratedMetadata), f"Expected response to be a dict, got {type(response)}: {response}"
    return response
