"""
Example script demonstrating car detection.
"""
import cv2
import os
from src.car_detection import CarDetector

def main():
    # Initialize the car detector
    detector = CarDetector()
    
    # Load the test image
    image_path = os.path.join('examples', 'images', 'test_cars.jpg')
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return
    
    # Detect cars
    cars = detector.detect_cars(image)
    print(f"Found {len(cars)} cars in the image")
    
    # Draw bounding boxes
    result = detector.draw_detections(image, cars)
    
    # Display the result
    cv2.imshow('Detected Cars', result)
    print("Press any key to close the window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 