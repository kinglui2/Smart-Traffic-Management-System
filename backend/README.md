# Smart Traffic Management System - Backend

The backend service for the Smart Traffic Management System, built with Python, Flask, and YOLOv8 for real-time vehicle detection.

## Features

- Real-time vehicle detection and tracking
- Traffic signal control algorithms
- WebSocket communication for live updates
- RESTful API endpoints
- Data analytics and processing
- Emergency vehicle priority system

## Prerequisites

- Python 3.8 or higher
- OpenCV
- CUDA-capable GPU (recommended for YOLOv8)
- Redis (for caching and real-time updates)

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Project Structure

```
backend/
├── src/
│   ├── traffic_control/        # Traffic signal control
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   └── algorithms.py
│   ├── vehicle_detection/      # YOLOv8 detection
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── tracking.py
│   └── web_interface/         # Flask application
│       ├── __init__.py
│       ├── app.py
│       └── routes.py
├── config/                    # Configuration files
│   ├── __init__.py
│   ├── settings.py
│   └── ml_config.py
├── data/                      # Data and models
│   ├── models/
│   └── cache/
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
└── README.md                 # Documentation
```

## API Endpoints

### Traffic Data

```
GET /api/v1/traffic/current
GET /api/v1/traffic/history
POST /api/v1/traffic/update
```

### Signal Control

```
GET /api/v1/signals/status
POST /api/v1/signals/update
POST /api/v1/signals/emergency
```

### Analytics

```
GET /api/v1/analytics/summary
GET /api/v1/analytics/predictions
```

## WebSocket Events

### Emitted Events

- `system_update`: Real-time traffic data updates
- `signal_change`: Traffic signal state changes
- `emergency_alert`: Emergency vehicle notifications

### Received Events

- `request_update`: Client requests for data
- `emergency_trigger`: Emergency mode activation
- `signal_override`: Manual signal control

## Development

1. Start the development server:
```bash
flask run
```

2. Run tests:
```bash
pytest
```

3. Check code style:
```bash
flake8
black .
```

## Deployment

### Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Add buildpacks:
```bash
heroku buildpacks:add heroku/python
```

4. Configure environment variables:
```bash
heroku config:set FLASK_APP=src.web_interface.app
heroku config:set FLASK_ENV=production
heroku config:set MODEL_PATH=data/models/yolov8n.pt
```

5. Deploy:
```bash
git push heroku main
```

### DigitalOcean Deployment

1. Create a Droplet with Docker support
2. Set up GitHub Actions for CI/CD
3. Configure Nginx as reverse proxy
4. Set up SSL with Let's Encrypt

## Environment Variables

```env
FLASK_APP=src.web_interface.app
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key
MODEL_PATH=data/models/yolov8n.pt
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://localhost/traffic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 