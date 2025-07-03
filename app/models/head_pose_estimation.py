import cv2
import mediapipe as mp
import numpy as np
import math
import time

class HeadPoseEstimator:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      
        ])

        self.DISTRACTION_TIME = 5.0  # seconds
        self.distraction_start_time = None

    def rotationMatrixToEulerAngles(self, R):
        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6
        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0
        return np.array([x, y, z])

    def estimate_pose(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = frame.shape

        results = self.face_mesh.process(rgb_image)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = [
                    face_landmarks.landmark[1],   # Nose tip
                    face_landmarks.landmark[152], # Chin
                    face_landmarks.landmark[263], # Right eye right corner
                    face_landmarks.landmark[33],  # Left eye left corner
                    face_landmarks.landmark[287], # Right mouth corner
                    face_landmarks.landmark[57]   # Left mouth corner
                ]

                image_points = np.array([
                    (landmark.x * image_width, landmark.y * image_height) for landmark in landmarks
                ], dtype="double")

                focal_length = image_width
                center = (image_width / 2, image_height / 2)
                camera_matrix = np.array([
                    [focal_length, 0, center[0]],
                    [0, focal_length, center[1]],
                    [0, 0, 1]
                ], dtype="double")

                dist_coeffs = np.zeros((4, 1))

                success, rotation_vector, translation_vector = cv2.solvePnP(
                    self.model_points, image_points, camera_matrix, dist_coeffs
                )

                rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
                euler_angles = self.rotationMatrixToEulerAngles(rotation_matrix)
                pitch, yaw, roll = [math.degrees(angle) for angle in euler_angles]

                if abs(yaw) < 45 and abs(pitch) < 45:
                    self.distraction_start_time = None
                    return "Focused"
                else:
                    if self.distraction_start_time is None:
                        self.distraction_start_time = time.time()
                        return "Checking_Focus"
                    elif time.time() - self.distraction_start_time >= self.DISTRACTION_TIME:
                        return "Distracted"
                    else:
                        return "Checking_Focus"
        
        return "No Face"


cap = cv2.VideoCapture(0)
pose_estimator = HeadPoseEstimator()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    status = pose_estimator.estimate_pose(frame)
    print("Status:", status)

    
    cv2.putText(frame, status, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.imshow("Head Pose Estimation", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
