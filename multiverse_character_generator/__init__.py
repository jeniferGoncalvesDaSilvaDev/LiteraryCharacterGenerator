"""
Multiverse Character Generator Library

A Python library for generating fictional characters across multiple universes using GPT-2.
"""

from .generator import MultiverseCharacterGenerator
from .models import CharacterDetails, GeneratedCharacter, UniverseInfo
from .exceptions import (
    MultiverseGeneratorError,
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError
)
from .universes import get_universes, get_universe_info

__version__ = "1.0.0"
__author__ = "Multiverse Character Generator Team"
__email__ = "contact@multiversegen.com"

__all__ = [
    "MultiverseCharacterGenerator",
    "CharacterDetails",
    "GeneratedCharacter", 
    "UniverseInfo",
    "MultiverseGeneratorError",
    "InvalidUniverseError",
    "InvalidDetailsError",
    "GenerationError",
    "get_universes",
    "get_universe_info"
]
