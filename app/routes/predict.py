from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import base64
import logging
from typing import Optional, List
import json

from app.schemas.output import PredictionResult, FrameResult, BatchPredictionResponse
from app.services.prediction_service import predict_from_image

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict", response_model=BatchPredictionResponse)
async def predict(frames: str = Form(...)):
    """
    Predict focus detection from multiple frames.
    
    Expected format:
    {
        "frames": [
            {"id": "frame1", "frame": "base64_encoded_image"},
            {"id": "frame2", "frame": "base64_encoded_image"}
        ]
    }
    
    Returns results for all frames, even if some models fail.
    """
    try:
        # Parse the JSON string
        try:
            data = json.loads(frames)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON format in frames parameter"
            )
        
        # Validate the structure
        if not isinstance(data, dict) or "frames" not in data:
            raise HTTPException(
                status_code=400,
                detail="Request must contain 'frames' array"
            )
        
        frames_data = data["frames"]
        if not isinstance(frames_data, list):
            raise HTTPException(
                status_code=400,
                detail="'frames' must be an array"
            )
        
        if len(frames_data) == 0:
            raise HTTPException(
                status_code=400,
                detail="'frames' array cannot be empty"
            )
        
        if len(frames_data) > 10:  # Limit to 10 frames per request
            raise HTTPException(
                status_code=400,
                detail="Maximum 10 frames allowed per request"
            )
        
        results = []
        successful_frames = 0
        failed_frames = 0
        
        # Process each frame
        for frame_data in frames_data:
            try:
                # Validate frame data structure
                if not isinstance(frame_data, dict) or "id" not in frame_data or "frame" not in frame_data:
                    logger.warning(f"Invalid frame data structure: {frame_data}")
                    failed_frames += 1
                    continue
                
                frame_id = frame_data["id"]
                frame_base64 = frame_data["frame"]
                
                # Validate frame ID
                if not isinstance(frame_id, str) or not frame_id.strip():
                    logger.warning(f"Invalid frame ID: {frame_id}")
                    failed_frames += 1
                    continue
                
                # Decode base64 image
                try:
                    image_bytes = base64.b64decode(frame_base64)
                except Exception as e:
                    logger.error(f"Failed to decode base64 for frame {frame_id}: {str(e)}")
                    failed_frames += 1
                    continue
                
                # Check file size (limit to 10MB)
                if len(image_bytes) > 10 * 1024 * 1024:  # 10MB
                    logger.warning(f"Frame {frame_id} too large: {len(image_bytes)} bytes")
                    failed_frames += 1
                    continue
                
                logger.info(f"Processing frame {frame_id}, size: {len(image_bytes)} bytes")
                
                # Get prediction results
                result = predict_from_image(image_bytes)
                
                # Add success message if any models worked
                if result["successful_models"]:
                    result["error"] = False
                    result["message"] = f"Successfully processed with {len(result['successful_models'])} models"
                    successful_frames += 1
                else:
                    result["error"] = True
                    result["message"] = "All models failed to process the frame"
                    failed_frames += 1
                
                # Create frame result
                frame_result = FrameResult(
                    id=frame_id,
                    result=PredictionResult(**result)
                )
                results.append(frame_result)
                
            except Exception as e:
                logger.error(f"Error processing frame {frame_data.get('id', 'unknown')}: {str(e)}")
                failed_frames += 1
                # Add failed frame result
                failed_result = FrameResult(
                    id=frame_data.get('id', 'unknown'),
                    result=PredictionResult(
                        error=True,
                        message=f"Failed to process frame: {str(e)}"
                    )
                )
                results.append(failed_result)
        
        # Create batch response
        total_processed = len(frames_data)
        batch_response = BatchPredictionResponse(
            results=results,
            total_processed=total_processed,
            successful_frames=successful_frames,
            failed_frames=failed_frames,
            error=False if successful_frames > 0 else True,
            message=f"Processed {total_processed} frames. Successful: {successful_frames}, Failed: {failed_frames}"
        )
        
        logger.info(f"Batch prediction completed: {batch_response.message}")
        return JSONResponse(content=batch_response.dict())
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        logger.error(f"Value error in batch prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in batch prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during batch prediction"
        )

# Keep the original single frame endpoint for backward compatibility
@router.post("/predict-single", response_model=PredictionResult)
async def predict_single(image: UploadFile = File(...)):
    """
    Predict focus detection from a single uploaded image.
    
    Returns results from all working models, even if some models fail.
    """
    try:
        # Validate file type
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="File must be an image"
            )
        
        # Check file size (limit to 10MB)
        image_bytes = await image.read()
        if len(image_bytes) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400, 
                detail="File size too large. Maximum size is 10MB"
            )
        
        logger.info(f"Processing single image: {image.filename}, size: {len(image_bytes)} bytes")
        
        # Get prediction results
        result = predict_from_image(image_bytes)
        
        # Add success message if any models worked
        if result["successful_models"]:
            result["error"] = False
            result["message"] = f"Successfully processed with {len(result['successful_models'])} models"
        else:
            result["error"] = True
            result["message"] = "All models failed to process the image"
        
        logger.info(f"Single prediction completed: {result}")
        return JSONResponse(content=result)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        logger.error(f"Value error in single prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in single prediction: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during prediction"
        )