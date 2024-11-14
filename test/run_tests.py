import os
import sys
import unittest
from pathlib import Path

# Set up the Python path
ROOT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(ROOT_DIR))

# Discover and run tests
loader = unittest.TestLoader()
start_dir = os.path.join(ROOT_DIR, 'test')
suite = loader.discover(start_dir, pattern='test_*.py')

runner = unittest.TextTestRunner()
runner.run(suite) 