"""Image Metadata Generator Backend."""

import asyncio

from dotenv import load_dotenv

from imagemetadatageneratorbackend.main import RequestData, metadata_generator

load_dotenv()


def main() -> None:
    """Call the main endpoint with some data."""
    asyncio.run(metadata_generator(RequestData(text="tbd")))
