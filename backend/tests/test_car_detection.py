"""
Test file for the car detection module.
"""
import sys
import os
from pathlib import Path
import pytest
import cv2
import numpy as np

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.car_detection import CarDetector

@pytest.fixture
def detector():
    """Create a CarDetector instance for testing."""
    return CarDetector()

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create a blank image
    image = np.zeros((300, 400, 3), dtype=np.uint8)
    # Add some random noise to simulate a real image
    noise = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
    image = cv2.addWeighted(image, 0.7, noise, 0.3, 0)
    return image

def test_detector_initialization(detector):
    """Test if the detector is initialized correctly."""
    assert detector is not None
    assert detector.car_cascade is not None

def test_preprocess_image(detector, sample_image):
    """Test image preprocessing."""
    processed = detector.preprocess_image(sample_image)
    assert processed is not None
    assert processed.shape == (300, 400)
    assert processed.dtype == np.uint8

def test_detect_cars(detector, sample_image):
    """Test car detection."""
    cars = detector.detect_cars(sample_image)
    assert isinstance(cars, np.ndarray)
    assert len(cars.shape) == 2
    assert cars.shape[1] == 4  # Each detection has x, y, w, h

def test_count_cars(detector, sample_image):
    """Test car counting."""
    count = detector.count_cars(sample_image)
    assert isinstance(count, int)
    assert count >= 0

def test_draw_detections(detector, sample_image):
    """Test drawing detections on image."""
    cars = detector.detect_cars(sample_image)
    result = detector.draw_detections(sample_image, cars)
    assert result is not None
    assert result.shape == sample_image.shape
    assert result.dtype == sample_image.dtype

def test_analyze_traffic_density(detector, sample_image):
    """Test traffic density analysis."""
    analysis = detector.analyze_traffic_density(sample_image)
    assert isinstance(analysis, dict)
    assert 'car_count' in analysis
    assert 'density' in analysis
    assert 'detections' in analysis
    assert analysis['density'] in ['low', 'medium', 'high']

def test_invalid_input(detector):
    """Test handling of invalid input."""
    with pytest.raises(ValueError):
        detector.detect_cars(None)
    
    with pytest.raises(ValueError):
        detector.preprocess_image(None) 