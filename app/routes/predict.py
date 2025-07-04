from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import base64
import logging
from typing import Optional

from app.schemas.output import PredictionResult
from app.services.prediction_service import predict_from_image

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict", response_model=PredictionResult)
async def predict(image: UploadFile = File(...)):
    """
    Predict focus detection from uploaded image.
    
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
        
        logger.info(f"Processing image: {image.filename}, size: {len(image_bytes)} bytes")
        
        # Get prediction results
        result = predict_from_image(image_bytes)
        
        # Add success message if any models worked
        if result["successful_models"]:
            result["error"] = False
            result["message"] = f"Successfully processed with {len(result['successful_models'])} models"
        else:
            result["error"] = True
            result["message"] = "All models failed to process the image"
        
        logger.info(f"Prediction completed: {result}")
        return JSONResponse(content=result)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        logger.error(f"Value error in prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during prediction"
        )