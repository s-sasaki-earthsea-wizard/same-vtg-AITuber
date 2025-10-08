"""
Pytest configuration and shared fixtures for same-vtg-AITuber tests.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(override=True)
