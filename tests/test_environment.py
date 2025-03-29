"""
Test file to verify the environment setup.
"""
import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)
    print(f"Added {project_root} to Python path")


def test_imports():
    """Test if all required packages can be imported."""
    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"Error importing OpenCV: {e}")
        return False

    try:
        import numpy as np
        print(f"NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"Error importing NumPy: {e}")
        return False

    try:
        import tensorflow as tf
        print(f"TensorFlow version: {tf.__version__}")
    except ImportError as e:
        print(f"Error importing TensorFlow: {e}")
        return False

    try:
        from flask import Flask
        app = Flask(__name__)
        print("Flask imported successfully")
    except ImportError as e:
        print(f"Error importing Flask: {e}")
        return False

    print("\nAll required packages imported successfully!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        print("\nEnvironment setup failed. Please check the error messages above.")
        sys.exit(1) 