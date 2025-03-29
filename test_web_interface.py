"""
Test script to simulate traffic data updates for the web interface.
"""
import socketio
import time
import random

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def traffic_update(data):
    print('Received traffic update:', data)

def simulate_traffic():
    """Simulate traffic data updates."""
    # Initial car counts
    car_counts = {
        'north': 0,
        'south': 0,
        'east': 0,
        'west': 0
    }
    
    while True:
        # Simulate new cars arriving
        for direction in car_counts:
            # Add 1-3 new cars randomly to each direction
            new_cars = random.randint(1, 3)
            car_counts[direction] += new_cars  # Accumulate cars instead of resetting
        
        # Emit car count updates
        sio.emit('update_car_counts', car_counts)
        print('Sent car counts:', car_counts)
        
        # Wait for a few seconds before next update
        time.sleep(5)

if __name__ == '__main__':
    try:
        # Connect to the server
        sio.connect('http://localhost:5000')
        
        # Start traffic simulation
        simulate_traffic()
    except KeyboardInterrupt:
        print('\nStopping traffic simulation...')
    finally:
        sio.disconnect() 