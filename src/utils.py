"""ScanSheet utils functions"""
import base64

def encode_image(image_path):
    """
    Encodes an image file to a base64 string.
    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")