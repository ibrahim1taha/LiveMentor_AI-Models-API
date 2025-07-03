import cv2
import mediapipe as mp
import time

class PersonDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        
        self.MULTIPLE_PEOPLE_TIME = 3.0  # 3 seconds
        self.multiple_people_start_time = None

    def detect_person(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        if results.detections:
            face_count = len(results.detections)
        else:
            face_count = 0

        if face_count > 1:
            if self.multiple_people_start_time is None:
                self.multiple_people_start_time = time.time()
                return "DETECTING_MULTIPLE"
            elif time.time() - self.multiple_people_start_time >= self.MULTIPLE_PEOPLE_TIME:
                return "ALERT"
            else:
                return "DETECTING_MULTIPLE"
        elif face_count == 1:
            self.multiple_people_start_time = None
            return "OK"
        else:
            self.multiple_people_start_time = None
            return "NO_PERSON"

cap = cv2.VideoCapture(0)  # 0 = default webcam
detector = PersonDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    status = detector.detect_person(frame)
    print("Status:", status)

    cv2.putText(frame, status, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
