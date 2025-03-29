"""
Main application module for the Smart Traffic Management System.
"""
import cv2
import numpy as np
import logging
import os
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import threading
import time

from .traffic_monitor import TrafficMonitor
from .traffic_control.signal_controller import SignalController, SignalState
from .config import WEB_SETTINGS, ANALYTICS_SETTINGS, LOGGING_CONFIG

# Configure logging
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f'traffic_system_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=LOGGING_CONFIG['level'],
    format=LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = WEB_SETTINGS['secret_key']
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize system components
traffic_monitor = TrafficMonitor()
signal_controller = SignalController()

# Global variables for system state
system_running = False
processing_thread = None

def process_traffic_data():
    """Background thread for processing traffic data and updating signals."""
    global system_running
    
    while system_running:
        try:
            # Process frame and get vehicle counts
            frame, vehicle_counts = traffic_monitor.process_frame()
            if frame is None:
                logging.error("Failed to process frame")
                continue
                
            # Get current system data
            traffic_data = traffic_monitor.get_traffic_data()
            signal_data = signal_controller.get_states()
            
            # Combine data for frontend
            system_data = {
                'traffic': traffic_data,
                'signals': signal_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Emit data to connected clients
            socketio.emit('system_update', system_data)
            
            # Control frame rate
            time.sleep(1.0 / WEB_SETTINGS['fps'])
            
        except Exception as e:
            logging.error(f"Error in processing thread: {e}")
            time.sleep(1)  # Wait before retrying

def store_analytics_data(data: dict):
    """
    Store system data for analytics.
    
    Args:
        data: Dictionary containing system data
    """
    # TODO: Implement analytics storage
    # This could involve writing to a database or file
    pass

def generate_frames():
    """Generate video frames with traffic data overlay."""
    while True:
        frame, vehicle_counts = traffic_monitor.process_frame()
        if frame is None:
            continue
            
        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        # Yield frame in bytes
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/traffic_data')
def get_traffic_data():
    """Get current traffic data."""
    return jsonify(traffic_monitor.get_traffic_data())

@app.route('/signal_states')
def get_signal_states():
    """Get current signal states."""
    return jsonify(signal_controller.get_states())

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logging.info("Client connected")
    # Send initial system state
    system_data = {
        'traffic': traffic_monitor.get_traffic_data(),
        'signals': signal_controller.get_signal_data(),
        'timestamp': datetime.now().isoformat()
    }
    socketio.emit('system_update', system_data)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logging.info("Client disconnected")

@socketio.on('emergency_vehicle')
def handle_emergency(data):
    """Handle emergency vehicle events."""
    vehicle_type = data.get('type')
    if vehicle_type:
        signal_controller.handle_emergency(vehicle_type)
        socketio.emit('system_update', {
            'message': f'Emergency mode activated for {vehicle_type}',
            'type': 'emergency'
        })

def start_system():
    """Start the traffic management system."""
    global system_running, processing_thread
    
    try:
        # Start traffic monitor
        if not traffic_monitor.start():
            raise RuntimeError("Failed to start traffic monitor")
            
        # Start signal controller
        if not signal_controller.start():
            raise RuntimeError("Failed to start signal controller")
        
        # Start processing thread
        system_running = True
        processing_thread = threading.Thread(target=process_traffic_data)
        processing_thread.daemon = True
        processing_thread.start()
        
        logging.info("Traffic management system started successfully")
        return True
        
    except Exception as e:
        logging.error(f"Failed to start system: {e}")
        return False

def stop_system():
    """Stop the traffic management system."""
    global system_running, processing_thread
    
    try:
        # Stop processing thread
        system_running = False
        if processing_thread:
            processing_thread.join()
            
        # Stop traffic monitor
        traffic_monitor.stop()
        
        # Stop signal controller
        signal_controller.stop()
        
        logging.info("Traffic management system stopped successfully")
        return True
        
    except Exception as e:
        logging.error(f"Error stopping system: {e}")
        return False

def main():
    """Main entry point for the application."""
    try:
        # Start the system
        if not start_system():
            raise RuntimeError("Failed to start traffic management system")
            
        # Start web server
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_PORT', 5000))
        
        logging.info(f"Starting web server on {host}:{port}")
        socketio.run(app, host=host, port=port, debug=False)
        
    except Exception as e:
        logging.error(f"Application error: {e}")
    finally:
        stop_system()

if __name__ == '__main__':
    main() 