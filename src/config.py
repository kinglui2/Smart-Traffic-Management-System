"""
Configuration settings for the Smart Traffic Management System.
"""
from pathlib import Path
import json
import logging

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'logs' / 'traffic_system.log'),
        logging.StreamHandler()
    ]
)

# Camera settings
CAMERA_SETTINGS = {
    'source': 'simulation',  # Use simulation mode for testing
    'width': 1280,
    'height': 720,
    'fps': 30
}

# Lane configuration
LANES = {
    'north': (580, 0, 700, 360),
    'south': (580, 360, 700, 720),
    'east': (700, 320, 1280, 400),
    'west': (0, 320, 580, 400)
}

# Traffic signal settings
SIGNAL_SETTINGS = {
    'cycle_time': 30,  # seconds per direction
    'yellow_time': 5,  # seconds for yellow light
    'emergency_override': True
}

# Vehicle detection settings
DETECTION_SETTINGS = {
    'model_path': str(PROJECT_ROOT / 'models' / 'yolov8n.pt'),
    'confidence_threshold': 0.5,
    'frame_interval': 1.0  # seconds between detection updates
}

# Web interface settings
WEB_SETTINGS = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'secret_key': 'your-secret-key-here'
}

# Emergency vehicle settings
EMERGENCY_SETTINGS = {
    'enabled': True,
    'priority_levels': {
        'ambulance': 1,
        'fire_truck': 1,
        'police': 2
    },
    'override_duration': 60  # seconds
}

# Analytics settings
ANALYTICS_SETTINGS = {
    'update_interval': 5,  # seconds between analytics updates
    'history_length': 3600  # number of data points to keep
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

def load_config(config_path: Path = None) -> dict:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration settings
    """
    if config_path is None:
        config_path = PROJECT_ROOT / 'config.json'
        
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load configuration file: {e}")
            return {}
    else:
        logging.warning(f"Configuration file not found: {config_path}")
        return {}

def save_config(config: dict, config_path: Path = None) -> bool:
    """
    Save configuration to a JSON file.
    
    Args:
        config: Dictionary containing configuration settings
        config_path: Path to save the configuration file
        
    Returns:
        bool: True if successful, False otherwise
    """
    if config_path is None:
        config_path = PROJECT_ROOT / 'config.json'
        
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Failed to save configuration file: {e}")
        return False 