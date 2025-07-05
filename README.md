# AI Focus Detection API

A FastAPI-based API that uses multiple AI models to detect focus-related behaviors from images, including head pose estimation, person detection, blocked objects detection, and sleep detection.

## Features

- **Multi-Model Architecture**: Uses 4 different AI models for comprehensive analysis
- **Fault-Tolerant**: If one model fails, others continue to work and return results
- **Batch Processing**: Process multiple frames in a single request
- **CORS Enabled**: Ready for frontend integration
- **Comprehensive Error Handling**: Detailed error responses and logging
- **Production Ready**: Configured for deployment to various platforms (Vercel, EC2, Render)

## System Requirements

### Minimum Requirements

- **CPU**: 4 cores (recommended: 8+ cores)
- **RAM**: 8GB (recommended: 16GB+)
- **Storage**: 20GB free space
- **GPU**: Optional but recommended for faster inference (NVIDIA GPU with CUDA support)
- **OS**: Ubuntu 20.04 LTS or later / Amazon Linux 2

### Software Versions

- **Python**: 3.11.x
- **CUDA**: 11.8+ (if using GPU)
- **Docker**: 20.10+ (optional)

## Technology Stack & Versions

### Core Framework

- **FastAPI**: 0.104.1
- **Uvicorn**: 0.34.2
- **Python**: 3.11.x

### AI/ML Libraries

- **PyTorch**: 2.7.1
- **TorchVision**: 0.22.1
- **TorchAudio**: 2.7.1
- **OpenCV**: 4.11.0.86
- **Ultralytics**: 8.3.160
- **MediaPipe**: 0.10.21
- **NumPy**: 1.26.4
- **Pandas**: 2.3.0
- **SciPy**: 1.15.2

### Utility Libraries

- **Pydantic**: 2.11.4
- **Pillow**: 11.2.1
- **Requests**: 2.31.0
- **Matplotlib**: 3.10.1

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

## Deployment Information for DevOps

### Required Ports

- **Application**: 8000 (default for FastAPI/Uvicorn)
- **HTTP**: 80 (if using reverse proxy)
- **HTTPS**: 443 (if using SSL/TLS)

### Main Run Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Process Management (Recommended)

```bash
pm2 start uvicorn --name "ai-focus-api" -- app.main:app --host 0.0.0.0 --port 8000
pm2 save
pm2 startup
```

### Health Check Endpoint

- `GET /health` or `GET /api/health`

### Monitoring & Logs

```bash
pm2 status
pm2 logs ai-focus-api
pm2 monit
```

### System Requirements (Summary)

- **Python**: 3.11.x
- **RAM**: 8GB+ (16GB+ recommended)
- **CPU**: 4+ cores
- **GPU**: Optional (CUDA 11.8+)

### Environment Variables

- None required for default operation

---

_For all other details (dependencies, backup, troubleshooting, etc.), see the rest of this README._
