"""Camera management module."""

import cv2
import numpy as np
from typing import Optional, Tuple
import logging
from ..config import CAMERA_SETTINGS

class CameraManager:
    """Class for managing camera input."""

    def __init__(self, source: str = 'simulation'):
        """Initialize the camera manager.

        Args:
            source: Camera source ('simulation' or camera index/path)
        """
        self.source = source
        self.frame_width = CAMERA_SETTINGS['width']
        self.frame_height = CAMERA_SETTINGS['height']
        self.fps = CAMERA_SETTINGS['fps']
        self.camera = None
        self.frame_count = 0
        self.logger = logging.getLogger(__name__)

    def start(self) -> bool:
        """Start the camera.

        Returns:
            bool: True if successful, False otherwise
        """
        if self.source == 'simulation':
            return True

        try:
            self.camera = cv2.VideoCapture(self.source)
            if not self.camera.isOpened():
                self.logger.error("Failed to open camera")
                return False

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            return True
        except Exception as e:
            self.logger.error(f"Error starting camera: {e}")
            return False

    def stop(self):
        """Stop the camera."""
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def get_frame(self) -> Optional[np.ndarray]:
        """Get a frame from the camera.

        Returns:
            Frame as numpy array, or None if capture fails
        """
        if self.source == 'simulation':
            return self._get_simulated_frame()

        if self.camera is None or not self.camera.isOpened():
            return None

        ret, frame = self.camera.read()
        if not ret:
            self.logger.error("Failed to read frame")
            return None

        # Resize frame if needed
        if frame.shape[1] != self.frame_width or frame.shape[0] != self.frame_height:
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))

        return frame

    def _get_simulated_frame(self) -> np.ndarray:
        """Generate a simulated frame for testing.

        Returns:
            Simulated frame as numpy array
        """
        # Create a black frame
        frame = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)

        # Draw some moving "vehicles"
        self.frame_count += 1
        y = (self.frame_count % 100) + 200

        # Draw rectangles representing vehicles
        cv2.rectangle(frame, (100, y), (150, y+40), (0, 255, 0), -1)  # Green vehicle
        cv2.rectangle(frame, (300, 480-y), (350, 520-y), (0, 0, 255), -1)  # Red vehicle
        cv2.rectangle(frame, (500, y-100), (550, y-60), (255, 0, 0), -1)  # Blue vehicle

        # Draw lane markings
        for x in range(0, self.frame_width, 100):
            cv2.line(frame, (x, 0), (x, self.frame_height), (255, 255, 255), 2)

        return frame 