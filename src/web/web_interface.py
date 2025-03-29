"""
Web interface module for the Smart Traffic Management System.
"""
import cv2
import base64
import io
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging
from pathlib import Path
import time

from src.traffic_monitor import TrafficMonitor
from src.traffic_control import SignalController, SignalState

class WebInterface:
    """Class for managing the web interface of the traffic management system."""
    
    def __init__(self, camera_source: int = 0):
        """
        Initialize the web interface.
        
        Args:
            camera_source: Camera index or video file path
        """
        self.logger = logging.getLogger(__name__)
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.monitor = TrafficMonitor(camera_source)
        self.signal_controller = SignalController()
        self.setup_routes()
        
    def setup_routes(self):
        """Set up Flask routes and WebSocket events."""
        @self.app.route('/')
        def index():
            """Render the main dashboard."""
            return render_template('index.html')
            
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            self.logger.info("Client connected")
            if not self.monitor.start():
                emit('error', {'message': 'Failed to start traffic monitoring'})
                return
                
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            self.logger.info("Client disconnected")
            self.monitor.stop()
            
        @self.socketio.on('request_update')
        def handle_update_request():
            """Handle update requests from clients."""
            self.send_update()
            
    def send_update(self):
        """Send current traffic status to all connected clients."""
        # Process a frame
        result = self.monitor.process_frame()
        if result is None:
            emit('error', {'message': 'Failed to process frame'})
            return
            
        # Convert frame to base64 for sending over WebSocket
        _, buffer = cv2.imencode('.jpg', result['frame'])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Update traffic data for each lane
        for lane_id, car_count in result['car_counts'].items():
            wait_time = result['wait_times'].get(lane_id, 0)
            self.signal_controller.update_traffic_data(lane_id, car_count, wait_time)
            
        # Update signal state
        new_state = self.signal_controller.update_state()
        if new_state:
            self.signal_controller.set_state(new_state)
            
        # Get current signal state info
        signal_info = self.signal_controller.get_current_state()
        
        # Send update to clients
        emit('update', {
            'frame': frame_base64,
            'car_counts': result['car_counts'],
            'wait_times': result['wait_times'],
            'signal_state': signal_info['state'],
            'signal_elapsed': signal_info['elapsed_time'],
            'signal_duration': signal_info['total_duration']
        })
        
    def run(self, host: str = '0.0.0.0', port: int = 5000):
        """
        Run the web interface.
        
        Args:
            host: Host address to bind to
            port: Port number to listen on
        """
        self.logger.info(f"Starting web interface on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port) 