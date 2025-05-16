"""
Traffic control module for managing traffic signals and generating recommendations.
"""
from enum import Enum
import time
import logging
from typing import Dict, List, Tuple, Optional
import numpy as np

class SignalState(Enum):
    """Traffic signal states."""
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class SignalPhase(Enum):
    """Traffic signal phases for different directions."""
    NORTH_SOUTH = "north_south"
    EAST_WEST = "east_west"

class TrafficController:
    """Class for managing traffic signals and generating recommendations."""
    
    def __init__(self):
        """Initialize the traffic controller."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize car counts
        self.car_counts = {
            "north": 0,
            "south": 0,
            "east": 0,
            "west": 0
        }
        
        # Initialize waiting cars (cars at red lights)
        self.waiting_cars = {
            "north": 0,
            "south": 0,
            "east": 0,
            "west": 0
        }
        
        # Initialize congestion levels
        self.congestion_levels = {
            "north": "low",
            "south": "low",
            "east": "low",
            "west": "low"
        }
        
        # Signal timing parameters (in seconds)
        self.min_green_time = 30
        self.max_green_time = 120
        self.yellow_time = 5
        
        # Current phase and its start time
        self.current_phase = SignalPhase.NORTH_SOUTH
        self.phase_start_time = time.time()
        self.yellow_start_time = None
        
        # Initialize signal states with north-south green
        self.signal_states = {
            "north": SignalState.GREEN,
            "south": SignalState.GREEN,
            "east": SignalState.RED,
            "west": SignalState.RED
        }
        
        # Route recommendations
        self.alternative_routes = {
            "north": ["northeast_route", "northwest_route"],
            "south": ["southeast_route", "southwest_route"],
            "east": ["northeast_route", "southeast_route"],
            "west": ["northwest_route", "southwest_route"]
        }
        
        # Cars that can pass per second when light is green
        self.cars_per_second = 2

    def update_car_counts(self, counts: Dict[str, int]) -> None:
        """
        Update car counts for each direction.
        
        Args:
            counts: Dictionary with car counts for each direction
            
        Raises:
            KeyError: If an invalid direction is provided
        """
        # Validate directions
        valid_directions = {"north", "south", "east", "west"}
        invalid_directions = set(counts.keys()) - valid_directions
        if invalid_directions:
            raise KeyError(f"Invalid directions: {invalid_directions}")
        
        # Update car counts and waiting cars
        for direction, count in counts.items():
            if self.signal_states[direction] == SignalState.RED:
                # Add new cars to waiting queue if light is red
                self.waiting_cars[direction] += count
            else:
                # Add to regular car count if light is not red
                self.car_counts[direction] += count
        
        self._update_congestion_levels()
    
    def _update_congestion_levels(self) -> None:
        """Update congestion levels based on car counts and waiting cars."""
        for direction in self.car_counts:
            total_cars = self.car_counts[direction] + self.waiting_cars[direction]
            if total_cars < 5:
                self.congestion_levels[direction] = "low"
            elif total_cars < 10:
                self.congestion_levels[direction] = "medium"
            else:
                self.congestion_levels[direction] = "high"
    
    def calculate_green_time(self, phase: SignalPhase) -> int:
        """
        Calculate green time duration based on traffic conditions.
        
        Args:
            phase: Signal phase to calculate time for
            
        Returns:
            Green time duration in seconds
        """
        if phase == SignalPhase.NORTH_SOUTH:
            total_cars = (self.car_counts["north"] + self.waiting_cars["north"] +
                         self.car_counts["south"] + self.waiting_cars["south"])
        else:
            total_cars = (self.car_counts["east"] + self.waiting_cars["east"] +
                         self.car_counts["west"] + self.waiting_cars["west"])
            
        # Base time proportional to number of cars
        green_time = self.min_green_time + (total_cars * 5)
        
        # Clamp to min/max range
        return min(max(green_time, self.min_green_time), self.max_green_time)
    
    def update_signal_states(self) -> Dict[str, str]:
        """
        Update traffic signal states based on timing and conditions.
        
        Returns:
            Dictionary of current signal states
        """
        current_time = time.time()
        
        # Handle yellow phase
        if self.yellow_start_time is not None:
            if current_time - self.yellow_start_time >= self.yellow_time:
                # Yellow phase complete, switch to next phase
                self._switch_phase()
            return {k: v.value for k, v in self.signal_states.items()}
        
        # Calculate time in current phase
        phase_duration = current_time - self.phase_start_time
        green_time = self.calculate_green_time(self.current_phase)
        
        # Check if it's time to change phase
        if phase_duration >= green_time:
            self._start_yellow_phase()
        
        # Process waiting cars at green lights
        self._process_waiting_cars()
            
        return {k: v.value for k, v in self.signal_states.items()}
    
    def _process_waiting_cars(self) -> None:
        """Process waiting cars at green lights."""
        for direction in self.signal_states:
            if self.signal_states[direction] == SignalState.GREEN:
                # Move more cars per second to make movement more visible
                cars_to_move = min(self.waiting_cars[direction], self.cars_per_second * 2)
                self.waiting_cars[direction] -= cars_to_move
                # Add moving cars to the regular count instead of replacing it
                self.car_counts[direction] += cars_to_move
    
    def _start_yellow_phase(self) -> None:
        """Start yellow signal phase before switching."""
        if self.current_phase == SignalPhase.NORTH_SOUTH:
            self.signal_states["north"] = SignalState.YELLOW
            self.signal_states["south"] = SignalState.YELLOW
        else:
            self.signal_states["east"] = SignalState.YELLOW
            self.signal_states["west"] = SignalState.YELLOW
            
        self.yellow_start_time = time.time()
    
    def _switch_phase(self) -> None:
        """Switch to the next signal phase."""
        # Update phase
        if self.current_phase == SignalPhase.NORTH_SOUTH:
            self.current_phase = SignalPhase.EAST_WEST
            # Set north-south to red and east-west to green
            self.signal_states["north"] = SignalState.RED
            self.signal_states["south"] = SignalState.RED
            self.signal_states["east"] = SignalState.GREEN
            self.signal_states["west"] = SignalState.GREEN
        else:
            self.current_phase = SignalPhase.NORTH_SOUTH
            # Set east-west to red and north-south to green
            self.signal_states["east"] = SignalState.RED
            self.signal_states["west"] = SignalState.RED
            self.signal_states["north"] = SignalState.GREEN
            self.signal_states["south"] = SignalState.GREEN
            
        self.phase_start_time = time.time()
        self.yellow_start_time = None
    
    def get_recommendations(self) -> List[Dict[str, str]]:
        """
        Generate traffic recommendations based on current conditions.
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Check for high congestion
        for direction, level in self.congestion_levels.items():
            if level == "high":
                # Recommend alternative routes
                alt_routes = self.alternative_routes[direction]
                recommendations.append({
                    "type": "congestion",
                    "message": f"High congestion on {direction} lane",
                    "severity": "high",
                    "alternatives": f"Consider using {' or '.join(alt_routes)}"
                })
            elif level == "medium":
                recommendations.append({
                    "type": "warning",
                    "message": f"Moderate congestion on {direction} lane",
                    "severity": "medium"
                })
        
        # If no specific recommendations, provide general status
        if not recommendations:
            recommendations.append({
                "type": "info",
                "message": "Traffic flow is normal on all lanes",
                "severity": "low"
            })
        
        return recommendations
    
    def get_status(self) -> Dict:
        """
        Get current traffic system status.
        
        Returns:
            Dictionary containing current system status
        """
        return {
            "signals": {
                direction: {
                    "state": state.value,
                    "cars": self.car_counts[direction] + self.waiting_cars[direction],
                    "congestion": self.congestion_levels[direction],
                    "waiting": self.waiting_cars[direction]
                }
                for direction, state in self.signal_states.items()
            },
            "recommendations": self.get_recommendations()
        } 