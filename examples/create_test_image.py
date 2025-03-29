"""
Script to create a test image with multiple rectangles simulating cars.
"""
import cv2
import numpy as np
import os

def create_test_image():
    # Create a black image
    image = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Add some white rectangles to simulate cars
    rectangles = [
        ((100, 100), (200, 150)),  # Car 1
        ((300, 200), (400, 250)),  # Car 2
        ((500, 300), (600, 350)),  # Car 3
        ((200, 400), (300, 450)),  # Car 4
    ]
    
    # Draw the rectangles
    for start, end in rectangles:
        cv2.rectangle(image, start, end, (255, 255, 255), -1)
    
    # Save the image
    output_dir = os.path.join('examples', 'images')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'test_cars.jpg')
    cv2.imwrite(output_path, image)
    print(f"Created test image at: {output_path}")

if __name__ == '__main__':
    create_test_image() 