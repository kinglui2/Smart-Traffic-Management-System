"""
Entry point script to run the Smart Traffic Management System web interface.
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.web_interface.app import socketio, app

if __name__ == '__main__':
    print("Starting Smart Traffic Management System web interface...")
    print("Access the dashboard at http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 