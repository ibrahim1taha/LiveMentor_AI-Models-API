import cv2
import mediapipe as mp

class PersonDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    def detect_person(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        if results.detections:
            face_count = len(results.detections)
        else:
            face_count = 0

        if face_count > 1:
            return "ALERT"
        elif face_count == 1:
            return "OK"
        else:
            return "NO_PERSON"
