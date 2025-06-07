#!/usr/bin/env python3
"""
Quick test script to verify the Multiverse Character Generator library functionality.
This script tests the core features without requiring heavy model downloads.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all library modules can be imported."""
    print("Testing library imports...")
    
    try:
        from multiverse_character_generator import MultiverseCharacterGenerator
        from multiverse_character_generator.models import CharacterDetails, GeneratedCharacter
        from multiverse_character_generator.exceptions import InvalidUniverseError
        from multiverse_character_generator.universes import get_universes, create_prompt
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_universe_configuration():
    """Test universe configuration and prompt generation."""
    print("\nTesting universe configuration...")
    
    try:
        from multiverse_character_generator.universes import get_universes, create_prompt
        
        # Test getting all universes
        universes = get_universes()
        print(f"✅ Found {len(universes)} universes: {list(universes.keys())}")
        
        # Test each universe configuration
        for universe_name, config in universes.items():
            if "inputs" not in config or "exemplos" not in config:
                print(f"❌ Universe {universe_name} missing required configuration")
                return False
            
            inputs = config["inputs"]
            examples = config["exemplos"]
            
            if len(inputs) != len(examples):
                print(f"❌ Universe {universe_name} has mismatched inputs/examples")
                return False
            
            # Test prompt creation with examples
            try:
                prompt = create_prompt(universe_name, examples)
                if len(prompt) < 50:
                    print(f"❌ Universe {universe_name} generated very short prompt")
                    return False
                print(f"✅ {universe_name}: {len(inputs)} fields, prompt length: {len(prompt)}")
            except Exception as e:
                print(f"❌ Failed to create prompt for {universe_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Universe configuration test failed: {e}")
        return False

def test_models():
    """Test Pydantic model validation."""
    print("\nTesting data models...")
    
    try:
        from multiverse_character_generator.models import CharacterDetails, GeneratedCharacter
        
        # Test CharacterDetails model
        valid_details = CharacterDetails(
            universe="fantasia",
            details=["Elf", "Ranger", "Chaotic Good", "Forest"]
        )
        print(f"✅ CharacterDetails model: {valid_details.universe}")
        
        # Test GeneratedCharacter model
        valid_character = GeneratedCharacter(
            character="A brave elf ranger from the mystical forest...",
            filename=None
        )
        print(f"✅ GeneratedCharacter model: {len(valid_character.character)} chars")
        
        # Test validation errors
        try:
            invalid_details = CharacterDetails(
                universe="fantasia",
                details=[]  # Empty details should fail
            )
            print("❌ Should have failed validation for empty details")
            return False
        except Exception:
            print("✅ Correctly rejected empty details")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_exceptions():
    """Test custom exception classes."""
    print("\nTesting exception handling...")
    
    try:
        from multiverse_character_generator.exceptions import (
            InvalidUniverseError, InvalidDetailsError, GenerationError
        )
        
        # Test exception creation and string representation
        universe_error = InvalidUniverseError(
            "Test error", 
            universe="invalid", 
            available_universes=["fantasia", "sci-fi"]
        )
        print(f"✅ InvalidUniverseError: {universe_error}")
        
        details_error = InvalidDetailsError(
            "Test error",
            universe="fantasia",
            expected_count=4,
            actual_count=2
        )
        print(f"✅ InvalidDetailsError: {details_error}")
        
        gen_error = GenerationError("Test generation error")
        print(f"✅ GenerationError: {gen_error}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception test failed: {e}")
        return False

def test_utilities():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from multiverse_character_generator.utils import (
            sanitize_filename, validate_generation_parameters, clean_generated_text
        )
        
        # Test filename sanitization
        sanitized = sanitize_filename("Test Character: Elf/Ranger\\Path?")
        expected_chars = set("Test_Character__Elf_Ranger_Path_")
        if not all(c in expected_chars or c.isalnum() or c == '_' for c in sanitized):
            print(f"❌ Filename sanitization failed: {sanitized}")
            return False
        print(f"✅ Filename sanitization: '{sanitized}'")
        
        # Test parameter validation (should not raise errors)
        validate_generation_parameters(
            max_length=300,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.2
        )
        print("✅ Parameter validation passed")
        
        # Test text cleaning
        messy_text = "This   is    a\n\n\ntest   text\n\n\n   "
        cleaned = clean_generated_text(messy_text)
        if "   " in cleaned or "\n\n\n" in cleaned:
            print(f"❌ Text cleaning failed: '{cleaned}'")
            return False
        print("✅ Text cleaning passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🌟 Multiverse Character Generator - Library Structure Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_universe_configuration,
        test_models,
        test_exceptions,
        test_utilities
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All library structure tests passed!")
        print("\nThe library is properly structured and ready for use.")
        print("Next steps:")
        print("- Install dependencies: pip install torch transformers pydantic nltk")
        print("- Run examples: python examples/basic_usage.py")
        print("- Run tests: pytest tests/")
    else:
        print("❌ Some tests failed. Please review the library structure.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)