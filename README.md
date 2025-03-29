# Smart Traffic Management System

A real-time traffic management system that uses computer vision and machine learning to optimize traffic flow and handle emergency vehicle scenarios.

## Features

- Real-time vehicle detection using YOLOv8
- Lane-based traffic monitoring
- Adaptive traffic signal control
- Emergency vehicle priority system
- Real-time web dashboard
- Traffic analytics and visualization
- Responsive design for all devices

## Prerequisites

- Python 3.8 or higher
- OpenCV
- YOLOv8
- Flask
- Flask-SocketIO
- NumPy
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Smart-Traffic-Management-System.git
cd Smart-Traffic-Management-System
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the YOLOv8 model:
```bash
# The model will be downloaded automatically on first run
```

## Project Structure

```
Smart-Traffic-Management-System/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── traffic_monitor.py
│   ├── car_detection.py
│   └── traffic_control/
│       ├── __init__.py
│       └── signal_controller.py
├── src/templates/
│   ├── base.html
│   ├── index.html
│   └── emergency_modal.html
├── src/static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── logs/
├── requirements.txt
└── README.md
```

## Configuration

The system can be configured through the `src/config.py` file. Key settings include:

- Camera settings (resolution, FPS)
- Lane definitions and priorities
- Traffic signal timing
- Emergency vehicle handling
- Analytics settings

## Usage

1. Start the system:
```bash
python -m src.main
```

2. Open a web browser and navigate to:
```
http://localhost:5000
```

3. The dashboard will show:
- Live traffic camera feed
- Vehicle counts per lane
- Traffic signal states
- Emergency controls
- Traffic analytics

## Emergency Vehicle Handling

The system provides priority handling for emergency vehicles:

1. Click the "Emergency Mode" button in the navigation bar
2. Select the type of emergency vehicle:
   - Ambulance
   - Fire Truck
   - Police Vehicle
3. The system will:
   - Set all signals to flashing yellow
   - Maintain emergency mode for the configured duration
   - Return to normal operation automatically

## Development

### Adding New Features

1. Create new modules in the `src` directory
2. Update the configuration in `src/config.py`
3. Modify the web interface templates as needed
4. Update the main application to integrate new features

### Testing

Run tests using:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YOLOv8 for object detection
- OpenCV for computer vision
- Flask for web framework
- Bootstrap for UI components
- Chart.js for data visualization

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

# Smart-Traffic-Management-System
Project Implementation Steps:

1. Define the Problem and Scope

Objective: Build a system that monitors traffic in real-time, detects cars, and optimizes traffic flow.

Target Users: City traffic management authorities and drivers.

Key Metrics: Number of cars detected, traffic signal control logic, and route recommendations.

2. Data Collection

Data Source: Use a simulated camera or a pre-recorded video of traffic.

Example Dataset: Use publicly available traffic datasets or simulate traffic images using tools like OpenCV.

Data Preprocessing: Resize and normalize images for AI model input.

Python Example: Simulate Traffic Images
```python
import cv2
import numpy as np

# Simulate a traffic image (random noise for demonstration)
traffic_image = np.random.randint(0, 256, (300, 500, 3), dtype=np.uint8)

# Display the image
cv2.imshow("Traffic Image", traffic_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

3. Model Selection

Task: Car detection and counting.

Algorithms:

Use a pre-trained object detection model like YOLO (You Only Look Once) or SSD (Single Shot Detector).

Alternatively, use OpenCV with Haar cascades for simpler car detection.

Libraries: Use OpenCV, TensorFlow, or PyTorch.

Python Example: Car Detection Using OpenCV
```python
import cv2

# Load pre-trained car detection model (Haar cascade)
car_cascade = cv2.CascadeClassifier('cars.xml')

# Load a traffic image
traffic_image = cv2.imread('traffic.jpg')

# Convert to grayscale
gray = cv2.cvtColor(traffic_image, cv2.COLOR_BGR2GRAY)

# Detect cars
cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Draw rectangles around detected cars
for (x, y, w, h) in cars:
    cv2.rectangle(traffic_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the result
cv2.imshow("Detected Cars", traffic_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

4. Model Training and Evaluation

Training: If using a custom model, train it on a dataset of traffic images with labeled cars.

Evaluation Metrics: Use precision, recall, and F1-score to evaluate car detection accuracy.

Cross-Validation: Ensure the model generalizes well to different traffic scenarios.

5. Traffic Signal Control Logic

Logic: Based on the number of cars detected, control traffic signals dynamically.

If one lane has fewer cars, keep its signal green longer.

Redirect cars to less congested routes.

Python Example: Traffic Signal Control
```python
def control_traffic_signal(car_count_lane1, car_count_lane2):
    if car_count_lane1 > car_count_lane2:
        print("Lane 1 is congested. Redirecting cars to Lane 2.")
        return "Lane 2: Green, Lane 1: Red"
    else:
        print("Lane 2 is congested. Redirecting cars to Lane 1.")
        return "Lane 1: Green, Lane 2: Red"

# Example usage
car_count_lane1 = 10  # Number of cars in Lane 1
car_count_lane2 = 5   # Number of cars in Lane 2
signal_status = control_traffic_signal(car_count_lane1, car_count_lane2)
print(signal_status)
```

6. Build a User Interface

Platform: Develop a simple web or desktop interface to display traffic data and signal status.

Features:

Show real-time traffic images with detected cars.

Display traffic signal status and recommendations.

Python Example: Flask Web App
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Simulate traffic data
    traffic_data = {
        'lane1_cars': 10,
        'lane2_cars': 5,
        'signal_status': "Lane 1: Green, Lane 2: Red"
    }
    return render_template('index.html', data=traffic_data)

if __name__ == '__main__':
    app.run(debug=True)
```

7. Deployment

Platform: Deploy the system on a local machine or cloud platform.

Steps:

Use Flask or Django for the web interface.

Use OpenCV for real-time image processing.

8. Testing and Validation

Unit Testing: Test individual components (e.g., car detection, signal control).

Integration Testing: Ensure the system works end-to-end.

User Testing: Collect feedback from users to improve the system.

9. Documentation and Reporting

Document: Write a detailed report explaining the project's objectives, methodology, and results.

Visualize: Include screenshots of the system and traffic data.

Present: Prepare a presentation to showcase the project.

Expected Outcomes:

A functional AI-powered traffic management system.

A user-friendly interface to display traffic data and signal status.

A well-documented report and presentation.

Grading Criteria:

Functionality (40 points):

Car detection and counting.

Traffic signal control logic.

Route recommendations.

Code Quality (30 points):

Well-commented and modular code.

Proper use of libraries and frameworks.

User Interface (20 points):

Simple and intuitive interface.

Documentation (10 points):

Clear and detailed report.

Submission Guidelines:

Submit your code as a git hub repo link having well documented readme file containing:

Python scripts for car detection and traffic control.

Web app files (if applicable).

Submit a PDF report explaining your approach, results, and challenges.

Email your submission to [Insert Email Address] with the subject line: "Smart Traffic Management System - [Your Name]".

---

## Project Overview:

This project aims to develop a smart traffic management system that uses AI to monitor traffic in real-time. The system will capture images from traffic cameras, process them to count the number of cars, and dynamically control traffic signals to optimize traffic flow. The system will:

- **Capture Images**: Use a camera to capture real-time traffic images.
- **Process Images**: Use AI to detect and count cars in the images.
- **Optimize Traffic Flow**: Direct cars to less congested routes by controlling traffic signals or providing recommendations.

### Key Features:

- **Real-Time Image Capture**: Use a camera (simulated or real) to capture traffic images.
- **Car Detection and Counting**: Use AI to detect and count cars in the captured images.
- **Traffic Signal Control**: Dynamically control traffic signals based on car counts.
- **Route Recommendations**: Provide recommendations to drivers to choose less congested routes.
