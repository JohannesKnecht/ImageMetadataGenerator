"""Image Metadata Generator Backend."""

import asyncio

from dotenv import load_dotenv

from imagemetadatageneratorbackend.main import metadata_generator
from imagemetadatageneratorbackend.models import GenerateOptions, MetaDataRequest

load_dotenv()


def invoke_metadata_generator(image_base64) -> None:
    """Call Invoke main metadata_generator function with some data."""
    asyncio.run(
        metadata_generator(
            MetaDataRequest(
                image_base64=image_base64,
                generate_options=GenerateOptions(
                    image_description=True,
                    image_title=True,
                    image_sentiment=True,
                ),
            )
        )
    )
