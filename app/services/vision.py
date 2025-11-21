import logging
from google.cloud import vision

logger = logging.getLogger(__name__)


def extract_text_from_image(image_content: bytes) -> dict:
    """
    Extract text from image using Google Cloud Vision API.

    Args:
        image_content: Raw image bytes

    Returns:
        dict with 'text' key
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)

    if response.error.message:
        logger.error(f"Vision API error: {response.error.message}")
        raise Exception(f"Vision API error: {response.error.message}")

    annotations = response.text_annotations

    if not annotations:
        return {"text": ""}

    full_text = annotations[0].description

    return {"text": full_text.strip()}
