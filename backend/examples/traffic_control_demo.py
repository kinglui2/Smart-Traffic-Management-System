"""
Demo script for the traffic signal control system.
"""
import time
from src.traffic_control import TrafficSignalController, SignalState

def print_signal_states(states):
    """Print the current signal states in a readable format."""
    for lane, state in states.items():
        color = {
            SignalState.RED: '\033[91m',    # Red
            SignalState.YELLOW: '\033[93m',  # Yellow
            SignalState.GREEN: '\033[92m'    # Green
        }[state]
        reset = '\033[0m'
        print(f"{lane}: {color}{state.value}{reset}")
    print()

def main():
    # Initialize the controller with four lanes
    lanes = ["North", "South", "East", "West"]
    controller = TrafficSignalController(lanes)
    
    # Simulate traffic for 2 minutes
    print("Starting traffic simulation...")
    simulation_time = 0.0
    update_interval = 1.0  # Update every second
    
    try:
        while simulation_time < 120.0:  # 2 minutes
            # Update car counts (simulated)
            for lane in lanes:
                # Simulate varying traffic conditions
                if simulation_time < 30.0:
                    controller.update_car_count(lane, 5)  # Light traffic
                elif simulation_time < 60.0:
                    controller.update_car_count(lane, 15)  # Heavy traffic
                else:
                    controller.update_car_count(lane, 8)  # Moderate traffic
            
            # Update the controller
            controller.update(update_interval)
            
            # Print current states
            print(f"\nTime: {simulation_time:.1f}s")
            print_signal_states(controller.get_signal_states())
            
            # Print any recommendations
            recommendations = controller.get_recommendations()
            if recommendations:
                print("Traffic Recommendations:")
                for rec in recommendations:
                    print(f"- {rec}")
                print()
            
            # Wait for the next update
            time.sleep(update_interval)
            simulation_time += update_interval
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == '__main__':
    main() 