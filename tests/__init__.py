"""
Test suite for the Multiverse Character Generator library.
"""

import os
import sys
import logging

# Add the parent directory to sys.path to import the library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure logging for tests
logging.basicConfig(
    level=logging.WARNING,  # Reduce noise during testing
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Test configuration
TEST_CONFIG = {
    "model_name": "gpt2",  # Use smaller model for faster tests
    "max_length": 100,     # Shorter text for faster generation
    "use_gpu": False,      # Disable GPU for consistent testing
    "cache_dir": None      # Use default cache
}

# Test data
SAMPLE_UNIVERSES = [
    "fantasia",
    "sci-fi", 
    "terror",
    "cyberpunk",
    "anime",
    "marvel"
]

SAMPLE_DETAILS = {
    "fantasia": ["Elf", "Ranger", "Chaotic Good", "Silverwood Forest"],
    "sci-fi": ["Human", "Pilot", "Earth Alliance", "Mars Station"],
    "terror": ["Teacher", "Fear of Dark", "Antique Music Box", "Old School"],
    "cyberpunk": ["Neural Interface", "Arasaka Corp", "Data Thief", "Night City"],
    "anime": ["Ninja", "Shadow Clone", "Orphaned", "Become Strongest"],
    "marvel": ["Gamma Radiation", "Avengers", "Hero", "New York"]
}

# Utility functions for tests
def get_test_generator():
    """Get a configured generator instance for testing."""
    from multiverse_character_generator import MultiverseCharacterGenerator
    return MultiverseCharacterGenerator(**TEST_CONFIG)

def get_sample_details(universe: str):
    """Get sample details for a given universe."""
    return SAMPLE_DETAILS.get(universe, [])

def is_valid_character_text(text: str) -> bool:
    """Check if generated text looks like valid character description."""
    return (
        isinstance(text, str) and
        len(text.strip()) > 10 and
        not text.strip().startswith("Error") and
        not text.strip().startswith("Failed")
    )
