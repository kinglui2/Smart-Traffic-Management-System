"""Traffic signal controller module."""

import logging
from enum import Enum
from datetime import datetime
from typing import Dict, Optional
import threading
import time

class SignalState(Enum):
    """Traffic signal states."""
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    FLASHING_YELLOW = "flashing_yellow"

class SignalController:
    """Controls traffic signals based on traffic data and emergency vehicles."""
    
    def __init__(self):
        """Initialize the signal controller."""
        self.signals = {
            'north': SignalState.RED,
            'south': SignalState.RED,
            'east': SignalState.RED,
            'west': SignalState.RED
        }
        self.emergency_mode = False
        self.emergency_vehicle = None
        self.running = False
        self.control_thread = None
        self.last_update = datetime.now()
        logging.info("Signal controller initialized")

    def start(self) -> bool:
        """Start the signal controller.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            self.running = True
            self.control_thread = threading.Thread(target=self._control_loop)
            self.control_thread.daemon = True
            self.control_thread.start()
            logging.info("Signal controller started")
            return True
        except Exception as e:
            logging.error(f"Failed to start signal controller: {e}")
            return False

    def stop(self):
        """Stop the signal controller."""
        self.running = False
        if self.control_thread:
            self.control_thread.join()
        logging.info("Signal controller stopped")

    def handle_emergency(self, vehicle_type: str):
        """Handle emergency vehicle detection.
        
        Args:
            vehicle_type: Type of emergency vehicle ('ambulance', 'fire', 'police')
        """
        if vehicle_type not in ['ambulance', 'fire', 'police']:
            logging.warning(f"Invalid emergency vehicle type: {vehicle_type}")
            return
            
        self.emergency_mode = True
        self.emergency_vehicle = vehicle_type
        logging.info(f"Emergency mode activated for {vehicle_type}")
        
        # Set all signals to flashing yellow
        for direction in self.signals:
            self.signals[direction] = SignalState.FLASHING_YELLOW

    def clear_emergency(self):
        """Clear emergency mode."""
        self.emergency_mode = False
        self.emergency_vehicle = None
        logging.info("Emergency mode cleared")

    def get_states(self) -> Dict:
        """Get current signal states.
        
        Returns:
            Dictionary containing signal states and emergency info
        """
        return {
            'signals': {k: v.value for k, v in self.signals.items()},
            'emergency_mode': self.emergency_mode,
            'emergency_vehicle': self.emergency_vehicle,
            'timestamp': datetime.now().isoformat()
        }

    def _control_loop(self):
        """Main control loop for traffic signal management."""
        cycle_time = 30  # seconds per direction
        yellow_time = 5  # seconds for yellow light
        
        directions = ['north', 'south', 'east', 'west']
        current_direction = 0
        
        while self.running:
            if self.emergency_mode:
                time.sleep(1)
                continue
                
            # Get current direction
            direction = directions[current_direction]
            
            # Set current direction to green
            self.signals[direction] = SignalState.GREEN
            
            # Set other directions to red
            for other_dir in directions:
                if other_dir != direction:
                    self.signals[other_dir] = SignalState.RED
            
            # Wait for cycle time
            time.sleep(cycle_time - yellow_time)
            
            if not self.running:
                break
                
            # Yellow phase
            self.signals[direction] = SignalState.YELLOW
            time.sleep(yellow_time)
            
            if not self.running:
                break
                
            # Move to next direction
            current_direction = (current_direction + 1) % len(directions)
            
        # Set all signals to red when stopping
        for direction in directions:
            self.signals[direction] = SignalState.RED 