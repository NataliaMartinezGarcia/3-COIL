import sys
import os

# Get the project root directory (the parent directory of 'tests')
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the root directory to the Python path
sys.path.append(root_dir)