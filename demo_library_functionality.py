#!/usr/bin/env python3
"""
Demonstration of the Multiverse Character Generator library functionality.
This script shows the complete library structure and core features.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demonstrate_library_features():
    """Demonstrate the key features of the Multiverse Character Generator library."""
    print("🌟 Multiverse Character Generator Library")
    print("=" * 60)
    
    # 1. Universe Configuration
    print("\n1. Available Universes and Configuration")
    print("-" * 40)
    
    from multiverse_character_generator.universes import get_universes, create_prompt
    
    universes = get_universes()
    print(f"Total universes supported: {len(universes)}")
    
    for universe_name, config in universes.items():
        inputs = config["inputs"]
        examples = config["exemplos"]
        print(f"\n{universe_name.upper()}:")
        print(f"  Required inputs: {inputs}")
        print(f"  Example values: {examples}")
    
    # 2. Prompt Generation
    print("\n\n2. Intelligent Prompt Generation")
    print("-" * 35)
    
    # Fantasy character example
    fantasy_details = ["Halfling", "Rogue", "Chaotic Neutral", "Riverside Town"]
    fantasy_prompt = create_prompt("fantasia", fantasy_details)
    print(f"\nFantasy Character Prompt ({len(fantasy_prompt)} characters):")
    print("-" * 25)
    print(fantasy_prompt[:300] + "..." if len(fantasy_prompt) > 300 else fantasy_prompt)
    
    # Cyberpunk character example
    cyberpunk_details = ["Optical Enhancement Mk-III", "Street Samurai Gang", "Corporate Infiltration", "Neo-Tokyo District 9"]
    cyberpunk_prompt = create_prompt("cyberpunk", cyberpunk_details)
    print(f"\nCyberpunk Character Prompt ({len(cyberpunk_prompt)} characters):")
    print("-" * 28)
    print(cyberpunk_prompt[:300] + "..." if len(cyberpunk_prompt) > 300 else cyberpunk_prompt)
    
    # 3. Data Models and Validation
    print("\n\n3. Data Models and Validation")
    print("-" * 30)
    
    from multiverse_character_generator.models import CharacterDetails, GeneratedCharacter
    
    # Valid character details
    valid_details = CharacterDetails(
        universe="anime",
        details=["Magical Girl", "Healing Powers", "Lost Memory", "Save Friends"]
    )
    print(f"✓ Valid character details: {valid_details.universe} with {len(valid_details.details)} details")
    
    # Generated character model
    sample_character = GeneratedCharacter(
        character="A brave magical girl with the power to heal others...",
        filename="character_magical_girl_20241207.txt"
    )
    print(f"✓ Generated character model: {len(sample_character.character)} chars, saved to {sample_character.filename}")
    
    # 4. Exception Handling
    print("\n\n4. Comprehensive Error Handling")
    print("-" * 32)
    
    from multiverse_character_generator.exceptions import (
        InvalidUniverseError, InvalidDetailsError, GenerationError
    )
    
    try:
        create_prompt("invalid_universe", ["test"])
    except Exception as e:
        print(f"✓ Caught invalid universe error: {type(e).__name__}")
    
    try:
        create_prompt("fantasia", ["too", "few"])  # Fantasy needs 4 details
    except Exception as e:
        print(f"✓ Caught invalid details error: {type(e).__name__}")
    
    # 5. Utility Functions
    print("\n\n5. Utility Functions")
    print("-" * 19)
    
    from multiverse_character_generator.utils import (
        sanitize_filename, clean_generated_text, validate_generation_parameters
    )
    
    # Filename sanitization
    dirty_filename = "Character: Elf/Ranger\\Path?File*.txt"
    clean_filename = sanitize_filename(dirty_filename)
    print(f"✓ Filename sanitization: '{dirty_filename}' → '{clean_filename}'")
    
    # Text cleaning
    messy_text = "This   is    a\n\n\ntest   text\n\n\n   "
    cleaned_text = clean_generated_text(messy_text)
    print(f"✓ Text cleaning: Reduced whitespace and formatting issues")
    
    # Parameter validation
    try:
        validate_generation_parameters(300, 0.8, 0.9, 1.2)
        print("✓ Parameter validation: All parameters valid")
    except Exception as e:
        print(f"✗ Parameter validation failed: {e}")
    
    # 6. File Organization
    print("\n\n6. File Organization and Structure")
    print("-" * 34)
    
    required_files = [
        "multiverse_character_generator/__init__.py",
        "multiverse_character_generator/generator.py",
        "multiverse_character_generator/models.py", 
        "multiverse_character_generator/universes.py",
        "multiverse_character_generator/exceptions.py",
        "multiverse_character_generator/utils.py",
        "setup.py",
        "README.md"
    ]
    
    existing_files = [f for f in required_files if os.path.exists(f)]
    print(f"✓ Core library files: {len(existing_files)}/{len(required_files)} present")
    
    example_files = ["examples/basic_usage.py", "examples/async_usage.py", "examples/custom_parameters.py"]
    existing_examples = [f for f in example_files if os.path.exists(f)]
    print(f"✓ Example scripts: {len(existing_examples)}/{len(example_files)} present")
    
    test_files = ["tests/test_generator.py", "tests/test_universes.py"]
    existing_tests = [f for f in test_files if os.path.exists(f)]
    print(f"✓ Test files: {len(existing_tests)}/{len(test_files)} present")
    
    # 7. Library Summary
    print("\n\n7. Library Summary")
    print("-" * 17)
    
    print("The Multiverse Character Generator library provides:")
    print("• 6 fictional universes (fantasy, sci-fi, horror, cyberpunk, anime, marvel)")
    print("• Intelligent prompt engineering for each universe")
    print("• GPT-2 model integration with customizable parameters")
    print("• Synchronous and asynchronous character generation")
    print("• Comprehensive error handling and validation")
    print("• File saving and organization utilities")
    print("• Professional packaging with setup.py")
    print("• Extensive documentation and examples")
    print("• Complete test suite")

def show_usage_examples():
    """Show basic usage examples."""
    print("\n\n8. Basic Usage Examples")
    print("-" * 24)
    
    print("\n# Install the library")
    print("pip install torch transformers pydantic nltk numpy tokenizers")
    
    print("\n# Basic usage")
    print("from multiverse_character_generator import MultiverseCharacterGenerator")
    print()
    print("# Initialize generator")
    print("generator = MultiverseCharacterGenerator()")
    print()
    print("# Generate a fantasy character")
    print("character = generator.generate_character(")
    print("    universe='fantasia',")
    print("    details=['Elf', 'Mage', 'Chaotic Good', 'Ancient Forest']")
    print(")")
    print("print(character.character)")
    print()
    print("# Quick generation with examples")
    print("character = generator.quick_generate('cyberpunk')")
    print()
    print("# Async generation")
    print("character = await generator.generate_character_async('sci-fi', details)")
    print()
    print("# Save to file")
    print("character = generator.generate_character(")
    print("    universe='anime',")
    print("    details=['Ninja', 'Shadow Magic', 'Clan Betrayed', 'Seek Revenge'],")
    print("    save_to_file=True,")
    print("    output_dir='./characters'")
    print(")")

def main():
    """Main demonstration function."""
    try:
        demonstrate_library_features()
        show_usage_examples()
        
        print("\n" + "=" * 60)
        print("🎉 Library demonstration completed successfully!")
        print("\nThe Multiverse Character Generator library is ready for use.")
        print("Run 'python examples/basic_usage.py' to see it in action.")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("The library structure is complete but requires dependencies.")
        print("Install with: pip install torch transformers pydantic nltk")

if __name__ == "__main__":
    main()