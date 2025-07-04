import logging
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Try to import models, but handle missing dependencies gracefully
try:
    import cv2
    import numpy as np
    from app.models.head_pose_estimation import HeadPoseEstimator
    from app.models.one_is_present import PersonDetector
    from app.models.blocked_things import BlockedThingsDetector
    from app.models.sleep_detector import SleepDetector
    
    # Initialize models
    head_pose_estimator = HeadPoseEstimator()
    person_detector = PersonDetector()
    blocked_things_detector = BlockedThingsDetector()
    sleep_detector = SleepDetector()
    
    MODELS_AVAILABLE = True
    logger.info("All AI models loaded successfully")
    
except ImportError as e:
    logger.warning(f"Some AI models could not be loaded: {e}")
    MODELS_AVAILABLE = False
    # Set models to None to avoid errors
    head_pose_estimator = None
    person_detector = None
    blocked_things_detector = None
    sleep_detector = None

def arrBuff_to_npArr(image_data):
    """Convert image buffer to numpy array"""
    try:
        np_arr = np.frombuffer(image_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except ImportError:
        logger.warning("OpenCV not available, cannot process image")
        return None
    except Exception as e:
        logger.error(f"Error converting image buffer: {str(e)}")
        raise ValueError("Invalid image data")

def safe_model_prediction(model_func, frame, model_name: str) -> Optional[bool]:
    """Safely execute a model prediction with error handling"""
    try:
        result = model_func(frame)
        logger.info(f"{model_name} prediction successful: {result}")
        return result
    except Exception as e:
        logger.error(f"{model_name} prediction failed: {str(e)}")
        return None

def predict_from_image(image_data):
    """Predict using available models, return mock results if models unavailable"""
    try:
        if not MODELS_AVAILABLE:
            # Return mock results if models are not available
            logger.info("Models not available, returning mock results")
            return {
                "is_focus": True,  # Mock result
                "is_person": True,  # Mock result
                "is_have_thing": False,  # Mock result
                "is_sleep": False,  # Mock result
                "successful_models": ["mock_model"],
                "failed_models": []
            }
        
        # Process with real models
        frame = arrBuff_to_npArr(image_data)
        if frame is None:
            return {
                "is_focus": None,
                "is_person": None,
                "is_have_thing": None,
                "is_sleep": None,
                "successful_models": [],
                "failed_models": ["image_processing"]
            }
        
        # Initialize result dictionary
        result = {
            "is_focus": None,
            "is_person": None,
            "is_have_thing": None,
            "is_sleep": None,
            "successful_models": [],
            "failed_models": []
        }
        
        # Run predictions with error handling
        if head_pose_estimator:
            focus_result = safe_model_prediction(
                head_pose_estimator.estimate_pose, 
                frame, 
                "Head Pose Estimation"
            )
            if focus_result is not None:
                result["is_focus"] = focus_result
                result["successful_models"].append("head_pose")
            else:
                result["failed_models"].append("head_pose")
        
        if person_detector:
            person_result = safe_model_prediction(
                person_detector.detect_person, 
                frame, 
                "Person Detection"
            )
            if person_result is not None:
                result["is_person"] = person_result
                result["successful_models"].append("person_detection")
            else:
                result["failed_models"].append("person_detection")
        
        if blocked_things_detector:
            blocked_result = safe_model_prediction(
                blocked_things_detector.detect_blocked_things, 
                frame, 
                "Blocked Things Detection"
            )
            if blocked_result is not None:
                result["is_have_thing"] = blocked_result
                result["successful_models"].append("blocked_things")
            else:
                result["failed_models"].append("blocked_things")
        
        if sleep_detector:
            sleep_result = safe_model_prediction(
                sleep_detector.detect_sleep, 
                frame, 
                "Sleep Detection"
            )
            if sleep_result is not None:
                result["is_sleep"] = sleep_result
                result["successful_models"].append("sleep_detection")
            else:
                result["failed_models"].append("sleep_detection")
        
        # Log summary
        logger.info(f"Prediction completed. Successful: {len(result['successful_models'])}, Failed: {len(result['failed_models'])}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in predict_from_image: {str(e)}")
        raise ValueError(f"Error processing image: {str(e)}")