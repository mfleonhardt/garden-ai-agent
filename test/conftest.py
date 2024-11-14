import sys
from pathlib import Path

# Get the absolute path to the project root
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Add project root and api directory to Python path
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / 'api'))

# Optional: Print paths for debugging
print(f"Python path: {sys.path}") 