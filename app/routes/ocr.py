import logging
import time
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

from app.services.vision import extract_text_from_image


class OCRResponse(BaseModel):
    success: bool
    text: str
    processing_time_ms: int
    message: Optional[str] = None

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg"}
JPEG_MAGIC_BYTES = b"\xff\xd8\xff"


def validate_image(file: UploadFile, content: bytes) -> None:
    """Validate uploaded file is a valid JPEG image."""
    # Check content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file format. Only JPG/JPEG images are allowed."
        )

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is 10MB."
        )

    # Check magic bytes
    if not content.startswith(JPEG_MAGIC_BYTES):
        raise HTTPException(
            status_code=415,
            detail="Invalid JPEG file. File does not appear to be a valid JPEG image."
        )


@router.post("/extract-text", response_model=OCRResponse)
async def extract_text(image: UploadFile = File(...)) -> OCRResponse:
    """
    Extract text from uploaded JPG image using OCR.

    Returns:
        JSON with extracted text and processing time.
    """
    start_time = time.time()

    # Check if file was provided
    if not image or not image.filename:
        raise HTTPException(status_code=400, detail="No image file provided.")

    # Read file content
    content = await image.read()

    if not content:
        raise HTTPException(status_code=400, detail="Empty file provided.")

    # Validate image
    validate_image(image, content)

    try:
        # Extract text using Vision API
        result = extract_text_from_image(content)

        processing_time_ms = int((time.time() - start_time) * 1000)

        if not result["text"]:
            return OCRResponse(
                success=True,
                text="",
                processing_time_ms=processing_time_ms,
                message="No text found in the image."
            )

        return OCRResponse(
            success=True,
            text=result["text"],
            processing_time_ms=processing_time_ms
        )

    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process image: {str(e)}"
        )
