"""
Test cases for the traffic signal control module.
"""
import unittest
from src.traffic_control.signal_controller import (
    TrafficSignalController,
    SignalState,
    LaneInfo
)
import pytest
import time
from src.traffic_control.controller import TrafficController, SignalPhase

class TestTrafficSignalController(unittest.TestCase):
    """Test cases for the TrafficSignalController class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lanes = ["North", "South", "East", "West"]
        self.controller = TrafficSignalController(self.lanes)
        
    def test_initialization(self):
        """Test if the controller initializes correctly."""
        self.assertEqual(len(self.controller.lanes), 4)
        self.assertEqual(len(self.controller.lane_info), 4)
        
        # First lane should be green, others red
        for i, lane in enumerate(self.lanes):
            self.assertIn(lane, self.controller.lane_info)
            info = self.controller.lane_info[lane]
            self.assertEqual(info.car_count, 0)
            expected_state = SignalState.GREEN if i == 0 else SignalState.RED
            self.assertEqual(info.signal_state, expected_state)
            self.assertEqual(info.wait_time, 0.0)
            self.assertEqual(info.congestion_level, 0.0)
    
    def test_update_car_count(self):
        """Test updating car counts for lanes."""
        self.controller.update_car_count("North", 10)
        self.assertEqual(self.controller.lane_info["North"].car_count, 10)
        self.assertEqual(self.controller.lane_info["North"].congestion_level, 0.5)
        
        # Test maximum congestion
        self.controller.update_car_count("South", 25)
        self.assertEqual(self.controller.lane_info["South"].car_count, 25)
        self.assertEqual(self.controller.lane_info["South"].congestion_level, 1.0)
    
    def test_calculate_green_time(self):
        """Test green time calculation based on congestion."""
        # Test base green time
        base_time = self.controller.calculate_green_time("North")
        self.assertEqual(base_time, 30.0)
        
        # Test increased green time with congestion
        self.controller.update_car_count("North", 15)
        increased_time = self.controller.calculate_green_time("North")
        self.assertGreater(increased_time, base_time)
    
    def test_signal_state_transitions(self):
        """Test traffic signal state transitions."""
        # Initial state should be green for first lane, red for others
        states = self.controller.get_signal_states()
        self.assertEqual(states["North"], SignalState.GREEN)
        for lane in ["South", "East", "West"]:
            self.assertEqual(states[lane], SignalState.RED)
        
        # Update time to trigger state changes
        self.controller.update(35.0)  # Move past green and yellow phases
        states = self.controller.get_signal_states()
        self.assertEqual(states["North"], SignalState.RED)
        
        # Update again to ensure next lane becomes green
        self.controller.update(0.1)  # Small update to trigger next lane
        states = self.controller.get_signal_states()
        self.assertEqual(states["South"], SignalState.GREEN)
    
    def test_recommendations(self):
        """Test traffic recommendations generation."""
        # No recommendations for low congestion
        recommendations = self.controller.get_recommendations()
        self.assertEqual(len(recommendations), 0)
        
        # Add high congestion to a lane
        self.controller.update_car_count("North", 15)  # 75% congestion
        recommendations = self.controller.get_recommendations()
        self.assertEqual(len(recommendations), 1)
        self.assertIn("North", recommendations[0])

@pytest.fixture
def controller():
    """Create a TrafficController instance for testing."""
    return TrafficController()

def test_initial_state(controller):
    """Test initial state of the traffic controller."""
    # Check signal states
    assert controller.signal_states["north"].value == SignalState.GREEN.value
    assert controller.signal_states["south"].value == SignalState.GREEN.value
    assert controller.signal_states["east"].value == SignalState.RED.value
    assert controller.signal_states["west"].value == SignalState.RED.value
    
    # Check other initial values
    assert controller.current_phase == SignalPhase.NORTH_SOUTH
    assert controller.car_counts["north"] == 0
    assert controller.congestion_levels["north"] == "low"

def test_update_car_counts(controller):
    """Test updating car counts and congestion levels."""
    new_counts = {
        "north": 12,
        "south": 8,
        "east": 3,
        "west": 6
    }
    controller.update_car_counts(new_counts)
    
    assert controller.car_counts["north"] == 12
    assert controller.congestion_levels["north"] == "high"
    assert controller.congestion_levels["south"] == "medium"
    assert controller.congestion_levels["east"] == "low"
    assert controller.congestion_levels["west"] == "medium"

def test_calculate_green_time(controller):
    """Test green time calculation based on traffic conditions."""
    # Set up some traffic
    controller.car_counts = {
        "north": 5,
        "south": 5,
        "east": 2,
        "west": 2
    }
    
    # Test north-south phase
    ns_time = controller.calculate_green_time(SignalPhase.NORTH_SOUTH)
    assert ns_time >= controller.min_green_time
    assert ns_time <= controller.max_green_time
    assert ns_time == 30 + (10 * 5)  # base + (total_cars * 5)
    
    # Test east-west phase
    ew_time = controller.calculate_green_time(SignalPhase.EAST_WEST)
    assert ew_time >= controller.min_green_time
    assert ew_time <= controller.max_green_time
    assert ew_time == 30 + (4 * 5)  # base + (total_cars * 5)

def test_signal_state_transition(controller):
    """Test signal state transitions."""
    # Force phase change by setting a short green time
    controller.min_green_time = 1
    controller.max_green_time = 1
    controller.yellow_time = 1
    
    # Initial state should be north-south green
    initial_states = controller.update_signal_states()
    assert initial_states["north"] == "GREEN"
    assert initial_states["south"] == "GREEN"
    assert initial_states["east"] == "RED"
    assert initial_states["west"] == "RED"
    
    # Wait for green phase to complete
    time.sleep(1.1)
    yellow_states = controller.update_signal_states()
    assert yellow_states["north"] == "YELLOW"
    assert yellow_states["south"] == "YELLOW"
    assert yellow_states["east"] == "RED"
    assert yellow_states["west"] == "RED"
    
    # Wait for yellow phase to complete
    time.sleep(1.1)
    final_states = controller.update_signal_states()
    assert final_states["north"] == "RED"
    assert final_states["south"] == "RED"
    assert final_states["east"] == "GREEN"
    assert final_states["west"] == "GREEN"

def test_recommendations(controller):
    """Test traffic recommendations generation."""
    # Test with high congestion
    controller.car_counts = {
        "north": 15,
        "south": 12,
        "east": 3,
        "west": 2
    }
    controller._update_congestion_levels()
    
    recommendations = controller.get_recommendations()
    assert len(recommendations) >= 2  # Should have at least 2 recommendations
    
    high_congestion_recs = [r for r in recommendations if r["severity"] == "high"]
    assert len(high_congestion_recs) == 2
    assert "alternatives" in high_congestion_recs[0]
    
    # Test with normal conditions
    controller.car_counts = {
        "north": 2,
        "south": 3,
        "east": 1,
        "west": 2
    }
    controller._update_congestion_levels()
    
    normal_recommendations = controller.get_recommendations()
    assert len(normal_recommendations) == 1
    assert normal_recommendations[0]["type"] == "info"
    assert normal_recommendations[0]["severity"] == "low"

def test_get_status(controller):
    """Test getting system status."""
    # Set up some traffic conditions
    controller.car_counts = {
        "north": 12,
        "south": 8,
        "east": 3,
        "west": 6
    }
    controller._update_congestion_levels()
    
    status = controller.get_status()
    
    assert "signals" in status
    assert "recommendations" in status
    assert len(status["signals"]) == 4
    
    north_status = status["signals"]["north"]
    assert "state" in north_status
    assert "cars" in north_status
    assert "congestion" in north_status
    assert north_status["cars"] == 12
    assert north_status["congestion"] == "high"

def test_invalid_inputs(controller):
    """Test handling of invalid inputs."""
    # Test with invalid car counts
    with pytest.raises(KeyError):
        controller.update_car_counts({"invalid_direction": 5})
    
    # Test with missing directions
    partial_counts = {"north": 5}
    controller.update_car_counts(partial_counts)
    assert controller.car_counts["east"] == 0  # Should preserve existing count

if __name__ == '__main__':
    unittest.main() 