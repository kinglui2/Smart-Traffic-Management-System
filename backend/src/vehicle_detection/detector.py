"""
Vehicle detection module using OpenCV.
"""
import cv2
import numpy as np
from typing import Dict, List, Tuple, Union
import os
from pathlib import Path

class CarDetector:
    def __init__(self, model_path: str = None, conf_threshold: float = 0.5):
        """
        Initialize the car detector.
        
        Args:
            model_path: Path to the detection model file
            conf_threshold: Confidence threshold for detections
        """
        self.conf_threshold = conf_threshold
        
        # If no model path provided, use default Haar cascade
        if model_path is None:
            cascade_path = os.path.join(
                Path(__file__).parent,
                'models',
                'haarcascade_car.xml'
            )
            if not os.path.exists(cascade_path):
                raise FileNotFoundError(
                    f"Car detection model not found at {cascade_path}. "
                    "Please download haarcascade_car.xml and place it in the models directory."
                )
            self.car_cascade = cv2.CascadeClassifier(cascade_path)
        else:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at {model_path}")
            self.car_cascade = cv2.CascadeClassifier(model_path)

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for car detection.
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed grayscale image
        """
        if image is None:
            raise ValueError("Input image is None")
            
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Apply some noise reduction
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        
        return gray

    def detect_vehicles(self, image: np.ndarray) -> np.ndarray:
        """
        Detect vehicles in the image.
        
        Args:
            image: Input image
            
        Returns:
            Array of detections in format [[x, y, w, h], ...]
        """
        if image is None:
            raise ValueError("Input image is None")
            
        # Preprocess the image
        gray = self.preprocess_image(image)
        
        # Detect cars
        cars = self.car_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Convert to numpy array if no cars detected
        if len(cars) == 0:
            return np.array([])
            
        return cars

    def draw_detections(self, image: np.ndarray, detections: np.ndarray) -> np.ndarray:
        """
        Draw detection boxes on the image.
        
        Args:
            image: Input image
            detections: Array of detections [[x, y, w, h], ...]
            
        Returns:
            Image with drawn detections
        """
        result = image.copy()
        for (x, y, w, h) in detections:
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return result

    def analyze_traffic_density(self, image: np.ndarray) -> Dict:
        """
        Analyze traffic density in the image.
        
        Args:
            image: Input image
            
        Returns:
            Dictionary with analysis results
        """
        # Detect cars
        detections = self.detect_vehicles(image)
        car_count = len(detections)
        
        # Calculate density level
        if car_count < 3:
            density = "low"
        elif car_count < 7:
            density = "medium"
        else:
            density = "high"
            
        return {
            'car_count': car_count,
            'density': density,
            'detections': detections.tolist()
        }
