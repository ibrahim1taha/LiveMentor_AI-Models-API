import cv2
import numpy as np
import mediapipe as mp


EAR_THRESHOLD = 0.2
CLOSED_FRAMES_THRESHOLD = 20  
closed_frames = 0


mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)


LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def calculate_EAR(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


cap = cv2.VideoCapture(0)

print("🔍 Monitoring for sleep... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            
            landmarks = np.array([(lm.x * w, lm.y * h) for lm in face_landmarks.landmark])

            left_eye = landmarks[LEFT_EYE]
            right_eye = landmarks[RIGHT_EYE]

            left_ear = calculate_EAR(left_eye)
            right_ear = calculate_EAR(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < EAR_THRESHOLD:
                closed_frames += 1
                if closed_frames > CLOSED_FRAMES_THRESHOLD:
                    cv2.putText(frame, "😴 SLEEPING DETECTED", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            else:
                closed_frames = 0

    cv2.imshow("Sleep Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
