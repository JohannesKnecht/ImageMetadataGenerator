"""Image Metadata Generator Backend."""

import asyncio
import base64

from dotenv import load_dotenv

from imagemetadatageneratorbackend.main import metadata_generator
from imagemetadatageneratorbackend.models import GenerateOptions, MetaDataRequest

load_dotenv()


def main() -> None:
    """Call the main endpoint with some data."""
    with open("tests/img.png", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

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
