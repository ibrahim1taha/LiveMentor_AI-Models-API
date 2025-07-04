import cv2
import numpy as np
import mediapipe as mp


class SleepDetector:
    def __init__(self, ear_threshold=0.2, closed_frames_threshold=20):
        self.ear_threshold = ear_threshold
        self.closed_frames_threshold = closed_frames_threshold
        self.closed_frames = 0
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Eye landmarks indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
    
    def calculate_ear(self, eye):
        """
        Calculate the Eye Aspect Ratio (EAR)
        
        Args:
            eye: numpy array of eye landmarks
            
        Returns:
            float: Eye aspect ratio
        """
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_sleep(self, frame):
        """
        Detect if person is sleeping based on eye closure
        
        Args:
            frame: numpy array of the image
            
        Returns:
            bool: True if person is sleeping, False otherwise
        """
        try:
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Convert landmarks to numpy array
                    landmarks = np.array([(lm.x * w, lm.y * h) for lm in face_landmarks.landmark])
                    
                    # Get eye landmarks
                    left_eye = landmarks[self.LEFT_EYE]
                    right_eye = landmarks[self.RIGHT_EYE]
                    
                    # Calculate EAR for both eyes
                    left_ear = self.calculate_ear(left_eye)
                    right_ear = self.calculate_ear(right_eye)
                    avg_ear = (left_ear + right_ear) / 2.0
                    
                    # Check if eyes are closed
                    if avg_ear < self.ear_threshold:
                        self.closed_frames += 1
                        if self.closed_frames > self.closed_frames_threshold:
                            return True  # Sleeping
                    else:
                        self.closed_frames = 0
                
                # If we get here, eyes are open or not closed long enough
                return False  # Awake
            else:
                # No face detected
                return False  # No face - not sleeping
                
        except Exception as e:
            return False  # Error occurred, assume not sleeping 