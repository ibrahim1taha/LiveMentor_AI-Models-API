import cv2
import base64
import numpy as np
from app.models.head_pose_estimation import HeadPoseEstimator
from app.models.one_is_present import PersonDetector

head_pose_estimator = HeadPoseEstimator()
person_detector = PersonDetector()

def arrBuff_to_npArr(image_data):
    np_arr = np.frombuffer(image_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def predict_from_image(image_data):
    frame = arrBuff_to_npArr(image_data)
    focus_status = head_pose_estimator.estimate_pose(frame)
    person_status = person_detector.detect_person(frame)
    return {
        "focus_status": focus_status,
        "person_status": person_status
    }