"""
Utility functions for the Multiverse Character Generator library.
"""

import os
import logging
import re
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from .exceptions import FileOperationError


def setup_logging(
    level: str = "INFO",
    format_string: str = None,
    log_file: str = None
) -> logging.Logger:
    """
    Set up logging configuration for the library.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        log_file: Optional file to write logs to
        
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[
            logging.StreamHandler(),
            *([logging.FileHandler(log_file)] if log_file else [])
        ]
    )
    
    return logging.getLogger("multiverse_character_generator")


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """
    Sanitize a string to be safe for use as a filename.
    
    Args:
        filename: Raw filename string
        max_length: Maximum length for the filename
        
    Returns:
        Sanitized filename string
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove extra whitespace and replace with underscores
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    
    # Remove leading/trailing periods and underscores
    sanitized = sanitized.strip('._')
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('._')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "character"
    
    return sanitized


def save_character_to_file(
    character_text: str,
    universe: str,
    details: List[str],
    output_dir: Optional[str] = None
) -> str:
    """
    Save generated character text to a file.
    
    Args:
        character_text: The generated character text
        universe: The universe the character belongs to
        details: Character details used for generation
        output_dir: Directory to save the file (defaults to current directory)
        
    Returns:
        Path to the saved file
        
    Raises:
        FileOperationError: If file saving fails
    """
    try:
        # Create output directory if it doesn't exist
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        else:
            output_dir = "."
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        detail_string = "_".join(details[:2]) if len(details) >= 2 else details[0] if details else "character"
        filename_base = f"{universe}_{sanitize_filename(detail_string)}_{timestamp}"
        filename = f"{filename_base}.txt"
        
        # Full file path
        filepath = os.path.join(output_dir, filename)
        
        # Write character to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Generated Character - {universe.title()} Universe\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generation Details:\n")
            f.write(f"- Universe: {universe}\n")
            f.write(f"- Details: {', '.join(details)}\n")
            f.write(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Character Description:\n")
            f.write("-" * 20 + "\n")
            f.write(character_text)
        
        return filepath
        
    except Exception as e:
        raise FileOperationError(
            f"Failed to save character to file",
            filepath=filepath if 'filepath' in locals() else None,
            operation="save",
            cause=e
        )


def load_character_from_file(filepath: str) -> str:
    """
    Load character text from a file.
    
    Args:
        filepath: Path to the character file
        
    Returns:
        Character text content
        
    Raises:
        FileOperationError: If file loading fails
    """
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        return content
        
    except Exception as e:
        raise FileOperationError(
            f"Failed to load character from file",
            filepath=filepath,
            operation="load",
            cause=e
        )


def validate_generation_parameters(
    max_length: int,
    temperature: float,
    top_p: float,
    repetition_penalty: float
) -> None:
    """
    Validate text generation parameters.
    
    Args:
        max_length: Maximum length of generated text
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        repetition_penalty: Repetition penalty
        
    Raises:
        ValueError: If any parameter is invalid
    """
    if not isinstance(max_length, int) or max_length < 50 or max_length > 1000:
        raise ValueError("max_length must be an integer between 50 and 1000")
    
    if not isinstance(temperature, (int, float)) or temperature < 0.0 or temperature > 1.0:
        raise ValueError("temperature must be a number between 0.0 and 1.0")
    
    if not isinstance(top_p, (int, float)) or top_p < 0.0 or top_p > 1.0:
        raise ValueError("top_p must be a number between 0.0 and 1.0")
    
    if not isinstance(repetition_penalty, (int, float)) or repetition_penalty < 1.0 or repetition_penalty > 2.0:
        raise ValueError("repetition_penalty must be a number between 1.0 and 2.0")


def format_character_output(
    character_text: str,
    universe: str,
    details: List[str],
    include_metadata: bool = True
) -> str:
    """
    Format character output with consistent styling.
    
    Args:
        character_text: The generated character text
        universe: The universe the character belongs to
        details: Character details used for generation
        include_metadata: Whether to include generation metadata
        
    Returns:
        Formatted character text
    """
    formatted_text = ""
    
    if include_metadata:
        formatted_text += f"🌟 {universe.title()} Character\n"
        formatted_text += "=" * 50 + "\n\n"
        formatted_text += f"📋 Generation Details:\n"
        for i, detail in enumerate(details, 1):
            formatted_text += f"  {i}. {detail}\n"
        formatted_text += "\n"
        formatted_text += "📖 Character Description:\n"
        formatted_text += "-" * 30 + "\n"
    
    formatted_text += character_text
    
    return formatted_text


def get_system_info() -> dict:
    """
    Get system information relevant to the library.
    
    Returns:
        Dictionary with system information
    """
    import platform
    import sys
    import torch
    
    return {
        "platform": platform.platform(),
        "python_version": sys.version,
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
    }


def estimate_generation_time(
    max_length: int,
    use_gpu: bool = False
) -> float:
    """
    Estimate character generation time based on parameters.
    
    Args:
        max_length: Maximum length of text to generate
        use_gpu: Whether GPU acceleration is being used
        
    Returns:
        Estimated generation time in seconds
    """
    # Base time estimation (rough approximation)
    base_time_per_token = 0.1 if not use_gpu else 0.05  # seconds
    estimated_tokens = max_length * 0.75  # Rough token count estimation
    
    return estimated_tokens * base_time_per_token


def clean_generated_text(text: str) -> str:
    """
    Clean and post-process generated text.
    
    Args:
        text: Raw generated text
        
    Returns:
        Cleaned text
    """
    # Remove excessive newlines
    cleaned = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove trailing whitespace from lines
    lines = [line.rstrip() for line in cleaned.split('\n')]
    cleaned = '\n'.join(lines)
    
    # Remove excessive spaces
    cleaned = re.sub(r' {3,}', '  ', cleaned)
    
    # Trim leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned
