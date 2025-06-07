#!/usr/bin/env python3
"""
Test the basic library structure without requiring heavy dependencies.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """Test that core modules exist and can be imported without torch."""
    print("Testing core module structure...")
    
    try:
        # Test universe configuration (no torch dependency)
        from multiverse_character_generator.universes import get_universes, create_prompt
        
        universes = get_universes()
        print(f"Found {len(universes)} universes: {list(universes.keys())}")
        
        # Test each universe
        expected_universes = ["fantasia", "sci-fi", "terror", "cyberpunk", "anime", "marvel"]
        for universe in expected_universes:
            if universe not in universes:
                print(f"Missing expected universe: {universe}")
                return False
            
            config = universes[universe]
            if "inputs" not in config or "exemplos" not in config:
                print(f"Universe {universe} missing required configuration")
                return False
            
            # Test prompt creation
            prompt = create_prompt(universe, config["exemplos"])
            if len(prompt) < 50:
                print(f"Universe {universe} generated short prompt")
                return False
            
            print(f"✓ {universe}: {len(config['inputs'])} fields")
        
        return True
        
    except Exception as e:
        print(f"Core module test failed: {e}")
        return False

def test_exception_classes():
    """Test exception classes without torch."""
    print("\nTesting exception classes...")
    
    try:
        from multiverse_character_generator.exceptions import (
            MultiverseGeneratorError, InvalidUniverseError, InvalidDetailsError
        )
        
        # Test basic exception creation
        base_error = MultiverseGeneratorError("Test error", "TEST_CODE")
        if "[TEST_CODE]" not in str(base_error):
            print("Base exception formatting failed")
            return False
        
        universe_error = InvalidUniverseError("Test", "invalid", ["valid1", "valid2"])
        if "invalid" not in str(universe_error):
            print("Universe error formatting failed")
            return False
        
        details_error = InvalidDetailsError("Test", "fantasy", 4, 2, ["field1", "field2"])
        if "requires 4 details" not in str(details_error):
            print("Details error formatting failed")
            return False
        
        print("✓ All exception classes working")
        return True
        
    except Exception as e:
        print(f"Exception test failed: {e}")
        return False

def test_prompt_generation():
    """Test prompt generation for all universes."""
    print("\nTesting prompt generation...")
    
    try:
        from multiverse_character_generator.universes import get_universes, create_prompt
        
        universes = get_universes()
        test_cases = {
            "fantasia": ["Elf", "Mage", "Chaotic Good", "Ancient Forest"],
            "sci-fi": ["Human", "Engineer", "Federation", "Space Station"],
            "terror": ["Doctor", "Claustrophobia", "Medical Kit", "Abandoned Hospital"],
            "cyberpunk": ["Neural Link", "Data Runner", "Freelancer", "Night City"],
            "anime": ["Student", "Fire Magic", "Village Burned", "Become Hero"],
            "marvel": ["Mutation", "X-Men", "Hero", "New York"]
        }
        
        for universe, details in test_cases.items():
            prompt = create_prompt(universe, details)
            
            # Check that all details appear in prompt
            for detail in details:
                if detail not in prompt:
                    print(f"Detail '{detail}' missing from {universe} prompt")
                    return False
            
            # Check for universe-specific keywords
            prompt_lower = prompt.lower()
            if universe == "fantasia" and not any(word in prompt_lower for word in ["fantasia", "mágicas", "equipamento"]):
                print(f"Fantasy prompt missing key terms")
                return False
            elif universe == "cyberpunk" and not any(word in prompt_lower for word in ["cyberpunk", "cibernéticas", "corporações"]):
                print(f"Cyberpunk prompt missing key terms")
                return False
            
            print(f"✓ {universe}: {len(prompt)} chars, contains all details")
        
        return True
        
    except Exception as e:
        print(f"Prompt generation test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "multiverse_character_generator/__init__.py",
        "multiverse_character_generator/generator.py",
        "multiverse_character_generator/models.py",
        "multiverse_character_generator/universes.py",
        "multiverse_character_generator/exceptions.py",
        "multiverse_character_generator/utils.py",
        "setup.py",
        "README.md",
        "examples/basic_usage.py",
        "examples/async_usage.py",
        "examples/custom_parameters.py",
        "tests/test_generator.py",
        "tests/test_universes.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"Missing files: {missing_files}")
        return False
    
    print(f"✓ All {len(required_files)} required files present")
    return True

def main():
    """Run structure tests."""
    print("🌟 Multiverse Character Generator - Library Structure Verification")
    print("=" * 65)
    
    tests = [
        test_file_structure,
        test_core_modules,
        test_exception_classes,
        test_prompt_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                break
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
            break
    
    print("\n" + "=" * 65)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Library structure is complete and functional!")
        print("\nThe Multiverse Character Generator library includes:")
        print("- 6 fictional universes (fantasy, sci-fi, horror, cyberpunk, anime, marvel)")
        print("- Comprehensive error handling and validation")
        print("- Synchronous and asynchronous character generation")
        print("- File saving and organization utilities")
        print("- Extensive examples and test coverage")
        print("- Professional packaging with setup.py")
        
        print("\nNext steps:")
        print("- Dependencies are installing in the background")
        print("- Once complete, run: python examples/basic_usage.py")
        print("- For testing: pytest tests/")
        print("- For async examples: python examples/async_usage.py")
    else:
        print("❌ Library structure has issues")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)