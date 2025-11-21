# OCR Image Text Extraction API

A serverless API deployed on Google Cloud Run that extracts text from JPG images using Google Cloud Vision API.

## Live URL

**https://ocr-api-343321912939.us-central1.run.app**

- Swagger UI: https://ocr-api-343321912939.us-central1.run.app/docs
- Health Check: https://ocr-api-343321912939.us-central1.run.app/health

## API Documentation

### HTTP Method and Endpoint

**POST** `/extract-text`

### Request Format

- **Content-Type:** `multipart/form-data`
- **Field name:** `image`
- **Supported format:** JPG/JPEG only
- **Max file size:** 10MB

### Response Format

**Success (200):**
```json
{
  "success": true,
  "text": "extracted text content here",
  "processing_time_ms": 1234
}
```

**No text found (200):**
```json
{
  "success": true,
  "text": "",
  "processing_time_ms": 500,
  "message": "No text found in the image."
}
```

### Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | No file provided or empty file |
| 413 | File too large (>10MB) |
| 415 | Unsupported format (non-JPG) |
| 422 | Validation error |
| 500 | Server/OCR processing error |

### Example curl Command

```bash
curl -X POST -F "image=@test_image.jpg" https://ocr-api-343321912939.us-central1.run.app/extract-text
```

## Implementation Explanation

### OCR Service
- **Google Cloud Vision API** - Chosen for seamless GCP integration and high accuracy text detection
- Uses `text_detection` method which is optimized for extracting text from images
- Handles various image qualities, text orientations, and multiple languages automatically
- Returns full extracted text from the image annotations

### File Upload and Validation
- Accepts `multipart/form-data` uploads via FastAPI's `UploadFile`
- Validates content type (only `image/jpeg`, `image/jpg`)
- Enforces 10MB file size limit
- Verifies JPEG magic bytes (`\xff\xd8\xff`) to prevent spoofed files

### Deployment Strategy
- Containerized using Docker with Python 3.11-slim base image
- Deployed to Google Cloud Run for serverless, auto-scaling infrastructure
- Uses Cloud Run's default service account for Vision API authentication

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app configuration
│   ├── routes/
│   │   ├── __init__.py
│   │   └── ocr.py           # OCR endpoint
│   └── services/
│       ├── __init__.py
│       └── vision.py        # Google Vision API integration
├── Dockerfile
├── requirements.txt
└── README.md
```
