from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import time
from datetime import datetime
import threading
import random
from src.traffic_control import SignalController, SignalState

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize signal controller
signal_controller = SignalController()

# Traffic data structure
traffic_data = {
    'lanes': {
        'lane1': {'cars': 5, 'wait_time': 30},
        'lane2': {'cars': 8, 'wait_time': 45},
        'lane3': {'cars': 3, 'wait_time': 20},
        'lane4': {'cars': 12, 'wait_time': 60}
    },
    'signal_state': {
        'state': 'red',
        'elapsed_time': 0,
        'total_duration': 30
    },
    'recommendations': [
        {'type': 'congestion', 'message': 'High congestion on lane4', 'severity': 'high'},
        {'type': 'alternative', 'message': 'Consider using Main Street as alternative route', 'severity': 'medium'}
    ]
}

def update_traffic_data():
    """Simulate real-time traffic data updates"""
    while True:
        # Update car counts and wait times randomly
        for lane_id in traffic_data['lanes']:
            # Update car count
            traffic_data['lanes'][lane_id]['cars'] = max(0, traffic_data['lanes'][lane_id]['cars'] + random.randint(-2, 3))
            
            # Update wait time based on car count
            cars = traffic_data['lanes'][lane_id]['cars']
            if cars < 5:
                traffic_data['lanes'][lane_id]['wait_time'] = max(0, traffic_data['lanes'][lane_id]['wait_time'] - 5)
            elif cars < 10:
                traffic_data['lanes'][lane_id]['wait_time'] += 2
            else:
                traffic_data['lanes'][lane_id]['wait_time'] += 5
            
            # Update signal controller with new data
            signal_controller.update_traffic_data(
                lane_id,
                traffic_data['lanes'][lane_id]['cars'],
                traffic_data['lanes'][lane_id]['wait_time']
            )
        
        # Update signal state
        new_state = signal_controller.update_state()
        if new_state:
            signal_controller.set_state(new_state)
        
        # Get current signal state
        state_info = signal_controller.get_current_state()
        traffic_data['signal_state'] = {
            'state': state_info['state'],
            'elapsed_time': state_info['elapsed_time'],
            'total_duration': state_info['total_duration']
        }
        
        # Update recommendations based on traffic conditions
        high_congestion_lanes = [
            lane_id for lane_id, data in traffic_data['lanes'].items()
            if data['cars'] >= 10
        ]
        
        if high_congestion_lanes:
            traffic_data['recommendations'] = [
                {
                    'type': 'congestion',
                    'message': f'High congestion on lane(s): {", ".join(high_congestion_lanes)}',
                    'severity': 'high'
                },
                {
                    'type': 'alternative',
                    'message': 'Consider using alternate routes',
                    'severity': 'medium'
                }
            ]
        else:
            traffic_data['recommendations'] = [
                {
                    'type': 'info',
                    'message': 'Traffic flow is normal',
                    'severity': 'low'
                }
            ]
        
        # Add timestamp
        traffic_data['timestamp'] = datetime.now().isoformat()
        
        # Emit updated data to all connected clients
        socketio.emit('traffic_update', traffic_data)
        time.sleep(2)  # Update every 2 seconds

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('traffic_update', traffic_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the traffic data update thread
    update_thread = threading.Thread(target=update_traffic_data, daemon=True)
    update_thread.start()
    
    # Run the Flask application
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 