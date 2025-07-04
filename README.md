# AI Focus Detection API

A FastAPI-based API that uses multiple AI models to detect focus-related behaviors from images, including head pose estimation, person detection, blocked objects detection, and sleep detection.

## Features

- **Multi-Model Architecture**: Uses 4 different AI models for comprehensive analysis
- **Fault-Tolerant**: If one model fails, others continue to work and return results
- **Batch Processing**: Process multiple frames in a single request
- **CORS Enabled**: Ready for frontend integration
- **Comprehensive Error Handling**: Detailed error responses and logging
- **Vercel Ready**: Configured for easy deployment to Vercel

## API Endpoints

### Health Check

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/health` - API health check

### Prediction

- `POST /api/predict` - **Batch prediction** - Upload multiple frames for analysis
- `POST /api/predict-single` - **Single prediction** - Upload single image for analysis

## Request Format

### Batch Prediction (`/api/predict`)

```json
{
  "frames": [
    {
      "id": "frame_001",
      "frame": "base64_encoded_image_data"
    },
    {
      "id": "frame_002",
      "frame": "base64_encoded_image_data"
    }
  ]
}
```

**Note**: Send as form data with key `frames` containing the JSON string.

### Single Prediction (`/api/predict-single`)

Upload a single image file using multipart form data.

## Response Format

### Batch Prediction Response

```json
{
  "results": [
    {
      "id": "frame_001",
      "result": {
        "is_focus": true,
        "is_person": true,
        "is_have_thing": false,
        "is_sleep": false,
        "successful_models": [
          "head_pose",
          "person_detection",
          "blocked_things",
          "sleep_detection"
        ],
        "failed_models": [],
        "error": false,
        "message": "Successfully processed with 4 models"
      }
    },
    {
      "id": "frame_002",
      "result": {
        "is_focus": null,
        "is_person": true,
        "is_have_thing": null,
        "is_sleep": false,
        "successful_models": ["person_detection", "sleep_detection"],
        "failed_models": ["head_pose", "blocked_things"],
        "error": false,
        "message": "Successfully processed with 2 models"
      }
    }
  ],
  "total_processed": 2,
  "successful_frames": 2,
  "failed_frames": 0,
  "error": false,
  "message": "Processed 2 frames. Successful: 2, Failed: 0"
}
```

### Single Prediction Response

```json
{
  "is_focus": true,
  "is_person": true,
  "is_have_thing": false,
  "is_sleep": false,
  "successful_models": [
    "head_pose",
    "person_detection",
    "blocked_things",
    "sleep_detection"
  ],
  "failed_models": [],
  "error": false,
  "message": "Successfully processed with 4 models"
}
```

## Models

1. **Head Pose Estimation** - Detects if person is focused/attentive
2. **Person Detection** - Detects if a person is present in the image
3. **Blocked Things Detection** - Detects if objects are blocking the view
4. **Sleep Detection** - Detects if person appears to be sleeping

## Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn app.main:app --reload
```

3. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

Run the test script to verify the API:

```bash
python test_batch_api.py
```

## Deployment to Vercel

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy:

```bash
vercel
```

3. For production deployment:

```bash
vercel --prod
```

## Environment Variables

No environment variables are required for basic functionality. The API is configured to work out of the box.

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input (wrong file type, file too large, invalid JSON)
- **422 Validation Error**: Request validation failures
- **500 Internal Server Error**: Unexpected server errors

All errors return structured JSON responses with error details.

## CORS Configuration

CORS is enabled for all origins to allow frontend integration. In production, you may want to restrict this to specific domains.

## File Upload Limits

- **Single prediction**: Maximum file size 10MB
- **Batch prediction**: Maximum 10 frames per request, 10MB per frame
- **Supported formats**: All image formats (JPEG, PNG, GIF, etc.)

## Model Failure Handling

If any individual model fails during prediction:

- Other models continue to work
- Failed models return `null` in the response
- The `failed_models` array lists which models failed
- The `successful_models` array lists which models worked
- The API still returns a successful response with available results

This ensures the API remains functional even if some models encounter issues.

## Batch Processing Features

- **Parallel Processing**: Each frame is processed independently
- **Fault Tolerance**: Individual frame failures don't affect other frames
- **Detailed Reporting**: Complete status for each frame and overall batch
- **Size Limits**: Maximum 10 frames per batch request
- **Base64 Encoding**: Images must be base64 encoded in the JSON payload
