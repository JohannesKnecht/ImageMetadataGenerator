"""Helper functions."""

import base64


def image_to_base64(image_path: str = "tests/img.png") -> None:
    """Convert an image file to a base64 string."""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    # save data to text file in temp directory
    with open("temp_data/image_base64.txt", "w") as f:
        f.write(data)
