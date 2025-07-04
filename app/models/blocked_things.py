import os
import requests
from ultralytics import YOLO
import cv2
import numpy as np


class BlockedThingsDetector:
    def __init__(self):
        MODEL_PATH = "yolov8n.pt"
        MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"

        if not os.path.exists(MODEL_PATH):
            print("Downloading YOLOv8 model...")
            r = requests.get(MODEL_URL, stream=True)
            with open(MODEL_PATH, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("Model downloaded successfully.")

        self.model = YOLO(MODEL_PATH)
        self.denied_objects = ["cell phone", "laptop", "tv", "remote", "computer", "phone"]
    
    def detect_blocked_things(self, frame):
        """
        Detect denied objects in the given frame
        
        Args:
            frame: numpy array of the image
            
        Returns:
            bool: True if denied objects are detected, False otherwise
        """
        try:
            # Run YOLO detection
            results = self.model(frame)[0]
            
            # Get detected classes
            detected_classes = []
            if results.boxes is not None and len(results.boxes) > 0:
                detected_classes = [self.model.names[int(cls)] for cls in results.boxes.cls]
            
            # Check for denied objects
            denied_items_found = []
            for item in self.denied_objects:
                if item in detected_classes:
                    denied_items_found.append(item)
            
            # Return boolean based on whether denied items were found
            return len(denied_items_found) > 0
            
        except Exception as e:
            return False  # Error occurred, assume no blocked things 