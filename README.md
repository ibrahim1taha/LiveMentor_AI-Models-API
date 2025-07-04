# AI Focus Detection API

A FastAPI-based API that uses multiple AI models to detect focus-related behaviors from images, including head pose estimation, person detection, blocked objects detection, and sleep detection.

## Features

- **Multi-Model Architecture**: Uses 4 different AI models for comprehensive analysis
- **Fault-Tolerant**: If one model fails, others continue to work and return results
- **CORS Enabled**: Ready for frontend integration
- **Comprehensive Error Handling**: Detailed error responses and logging
- **Vercel Ready**: Configured for easy deployment to Vercel

## API Endpoints

### Health Check

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/health` - API health check

### Prediction

- `POST /api/predict` - Upload image for focus detection analysis

## Response Format

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

- **400 Bad Request**: Invalid input (wrong file type, file too large)
- **422 Validation Error**: Request validation failures
- **500 Internal Server Error**: Unexpected server errors

All errors return structured JSON responses with error details.

## CORS Configuration

CORS is enabled for all origins to allow frontend integration. In production, you may want to restrict this to specific domains.

## File Upload Limits

- Maximum file size: 10MB
- Supported formats: All image formats (JPEG, PNG, GIF, etc.)

## Model Failure Handling

If any individual model fails during prediction:

- Other models continue to work
- Failed models return `null` in the response
- The `failed_models` array lists which models failed
- The `successful_models` array lists which models worked
- The API still returns a successful response with available results

This ensures the API remains functional even if some models encounter issues.
