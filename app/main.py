import logging
from fastapi import FastAPI

from app.routes import ocr

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="OCR Image Text Extraction API",
    description="Extract text from JPG images using Google Cloud Vision API",
    version="1.0.0"
)

# Include routers
app.include_router(ocr.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
