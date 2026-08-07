"""
Pytest configuration and root path setup.
"""

import os
import sys

# Ensure repository root is on sys.path for importing 'src'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
