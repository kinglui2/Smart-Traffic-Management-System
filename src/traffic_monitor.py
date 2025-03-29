"""
Traffic monitoring module for the Smart Traffic Management System.
"""
import cv2
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime
from .car_detection.detector import CarDetector
from .camera.camera_manager import CameraManager
from .config import (
    CAMERA_SETTINGS,
    LANES,
    DETECTION_SETTINGS,
    logging
)

class TrafficMonitor:
    def __init__(self):
        """Initialize the traffic monitoring system."""
        self.camera = CameraManager(CAMERA_SETTINGS['source'])
        self.car_detector = CarDetector(
            model_path=DETECTION_SETTINGS['model_path'],
            conf_threshold=DETECTION_SETTINGS['confidence_threshold']
        )
        self.lanes = LANES
        self.vehicle_counts = {lane: 0 for lane in self.lanes}
        self.last_update = datetime.now()
        self.frame_interval = DETECTION_SETTINGS['frame_interval']
        logging.info("Traffic monitor initialized successfully")

    def start(self) -> bool:
        """Start the traffic monitoring system."""
        try:
            if not self.camera.start():
                logging.error("Failed to start camera")
                return False
            logging.info("Traffic monitoring started successfully")
            return True
        except Exception as e:
            logging.error(f"Error starting traffic monitor: {e}")
            return False

    def stop(self):
        """Stop the traffic monitoring system."""
        self.camera.stop()
        logging.info("Traffic monitoring stopped")

    def count_vehicles_in_lane(self, frame: np.ndarray, lane_name: str) -> int:
        """
        Count vehicles in a specific lane.
        
        Args:
            frame: Input frame
            lane_name: Name of the lane to count vehicles in
            
        Returns:
            Number of vehicles detected in the lane
        """
        # Get lane region
        lane_region = self.lanes[lane_name]
        
        # Crop frame to lane region
        lane_frame = frame[lane_region[1]:lane_region[3], lane_region[0]:lane_region[2]]
        
        # Detect vehicles in lane
        detections = self.car_detector.detect_vehicles(lane_frame)
        
        return len(detections)

    def process_frame(self):
        """
        Process a frame from the camera.
        
        Returns:
            Tuple of processed frame and vehicle counts, or None if processing fails
        """
        frame = self.camera.get_frame()
        if frame is None:
            return None, self.vehicle_counts
            
        # Update vehicle counts if enough time has passed
        current_time = datetime.now()
        if (current_time - self.last_update).total_seconds() >= self.frame_interval:
            for lane in self.lanes:
                self.vehicle_counts[lane] = self.count_vehicles_in_lane(frame, lane)
            self.last_update = current_time
            
        # Draw lane regions and vehicle counts
        for lane in self.lanes:
            x1, y1, x2, y2 = self.lanes[lane]
            
            # Draw lane region
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw lane name
            cv2.putText(
                frame,
                lane,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            
            # Draw vehicle count
            count = self.vehicle_counts[lane]
            cv2.putText(
                frame,
                f"Count: {count}",
                (x1, y2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            
        return frame, self.vehicle_counts

    def get_traffic_data(self) -> Dict:
        """
        Get current traffic data.
        
        Returns:
            Dictionary containing traffic data
        """
        return {
            'vehicle_counts': self.vehicle_counts,
            'timestamp': datetime.now().isoformat(),
            'lanes': self.lanes
        } 