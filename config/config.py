"""
Configuration settings for the Smart Traffic Management System.
"""

# Camera settings
CAMERA_SOURCE = 0  # 0 for default camera, or path to video file
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Car detection settings
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.3

# Traffic control settings
MIN_CARS_FOR_SIGNAL_CHANGE = 5
SIGNAL_CHANGE_INTERVAL = 30  # seconds

# Web interface settings
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Data storage
DATA_DIR = 'data'
MODEL_DIR = 'models' 