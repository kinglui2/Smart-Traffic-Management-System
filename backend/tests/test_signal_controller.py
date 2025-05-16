"""
Test file for the traffic signal controller module.
"""
import pytest
import time
from src.traffic_control.signal_controller import SignalController, SignalState

def test_controller_initialization():
    """Test signal controller initialization."""
    controller = SignalController()
    assert controller.current_state == SignalState.RED
    assert controller.min_green_time == 30
    assert controller.max_green_time == 120
    assert controller.yellow_time == 3
    assert controller.red_time == 5

def test_traffic_data_update():
    """Test updating traffic data."""
    controller = SignalController()
    
    # Update traffic data for a lane
    controller.update_traffic_data("lane1", 5, 10.0)
    assert controller.car_counts["lane1"] == 5
    assert controller.wait_times["lane1"] == 10.0

def test_green_time_calculation():
    """Test green time calculation based on traffic conditions."""
    controller = SignalController()
    
    # Test with no traffic
    assert controller.calculate_green_time("lane1") == controller.min_green_time
    
    # Test with moderate traffic
    controller.update_traffic_data("lane1", 10, 20.0)
    green_time = controller.calculate_green_time("lane1")
    assert green_time > controller.min_green_time
    assert green_time <= controller.max_green_time
    
    # Test with heavy traffic
    controller.update_traffic_data("lane1", 50, 60.0)
    green_time = controller.calculate_green_time("lane1")
    assert green_time == controller.max_green_time

def test_state_transition():
    """Test signal state transitions."""
    controller = SignalController()
    
    # Start with red
    assert controller.current_state == SignalState.RED
    
    # Add traffic data
    controller.update_traffic_data("lane1", 5, 10.0)
    
    # Set to green
    controller.set_state(SignalState.GREEN)
    assert controller.current_state == SignalState.GREEN
    
    # Wait for green to expire
    time.sleep(controller.state_duration + 0.1)
    new_state = controller.update_state()
    assert new_state == SignalState.YELLOW
    
    # Set to yellow
    controller.set_state(SignalState.YELLOW)
    assert controller.current_state == SignalState.YELLOW
    
    # Wait for yellow to expire
    time.sleep(controller.yellow_time + 0.1)
    new_state = controller.update_state()
    assert new_state == SignalState.RED

def test_priority_lane_selection():
    """Test selection of highest priority lane."""
    controller = SignalController()
    
    # Add traffic data for multiple lanes
    controller.update_traffic_data("lane1", 5, 10.0)
    controller.update_traffic_data("lane2", 10, 20.0)
    controller.update_traffic_data("lane3", 3, 5.0)
    
    # Lane 2 should have highest priority
    assert controller.get_highest_priority_lane() == "lane2"
    
    # Clear traffic data
    controller.car_counts.clear()
    controller.wait_times.clear()
    assert controller.get_highest_priority_lane() is None

def test_current_state_info():
    """Test getting current state information."""
    controller = SignalController()
    
    # Add traffic data
    controller.update_traffic_data("lane1", 5, 10.0)
    
    # Get state info
    state_info = controller.get_current_state()
    assert state_info['state'] == SignalState.RED.value
    assert 'elapsed_time' in state_info
    assert 'total_duration' in state_info
    assert state_info['car_counts'] == {"lane1": 5}
    assert state_info['wait_times'] == {"lane1": 10.0} 