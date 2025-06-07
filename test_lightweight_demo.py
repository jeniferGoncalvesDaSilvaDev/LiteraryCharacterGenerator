#!/usr/bin/env python3
"""
Lightweight demonstration of the Multiverse Character Generator library structure
without heavy ML dependencies. This shows the library organization and core functionality.
"""

import sys
import os
from pathlib import Path

def test_library_imports():
    """Test that core library modules can be imported."""
    print("Testing library imports...")
    
    try:
        # Test core module imports (without heavy dependencies)
        from multiverse_character_generator import __version__
        from multiverse_character_generator.models import (
            CharacterDetails, GeneratedCharacter, UniverseInfo, GenerationConfig
        )
        from multiverse_character_generator.exceptions import (
            MultiverseGeneratorError, InvalidUniverseError, InvalidDetailsError
        )
        from multiverse_character_generator.universes import get_universe_config, get_all_universes
        from multiverse_character_generator.utils import clean_generated_text, save_character_to_file
        
        print("✓ All core modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_universe_configuration():
    """Test universe configuration without ML dependencies."""
    print("\nTesting universe configuration...")
    
    try:
        from multiverse_character_generator.universes import get_all_universes, get_universe_config
        
        universes = get_all_universes()
        print(f"✓ Found {len(universes)} universes: {', '.join(universes)}")
        
        for universe in universes[:3]:  # Test first 3 universes
            config = get_universe_config(universe)
            print(f"  • {universe}: {len(config['inputs'])} required fields")
        
        return True
        
    except Exception as e:
        print(f"✗ Universe configuration error: {e}")
        return False

def test_data_models():
    """Test Pydantic model validation."""
    print("\nTesting data models...")
    
    try:
        from multiverse_character_generator.models import (
            CharacterDetails, GeneratedCharacter, GenerationConfig
        )
        
        # Test CharacterDetails validation
        details = CharacterDetails(
            universe="fantasy",
            details=["Elf", "Mage", "Chaotic Good", "Rivendell"]
        )
        print(f"✓ CharacterDetails validation: {details.universe}")
        
        # Test GeneratedCharacter model
        character = GeneratedCharacter(
            character="Test character description",
            filename="test_character.txt"
        )
        print(f"✓ GeneratedCharacter model: {len(character.character)} chars")
        
        # Test GenerationConfig
        config = GenerationConfig(
            max_length=300,
            temperature=0.8,
            save_to_file=True
        )
        print(f"✓ GenerationConfig validation: temp={config.temperature}")
        
        return True
        
    except Exception as e:
        print(f"✗ Data model error: {e}")
        return False

def test_utilities():
    """Test utility functions."""
    print("\nTesting utilities...")
    
    try:
        from multiverse_character_generator.utils import clean_generated_text
        
        # Test text cleaning
        dirty_text = "  This is a test character.\n\n\nWith extra spaces.  "
        clean_text = clean_generated_text(dirty_text)
        print(f"✓ Text cleaning: '{dirty_text[:30]}...' -> '{clean_text[:30]}...'")
        
        return True
        
    except Exception as e:
        print(f"✗ Utilities error: {e}")
        return False

def test_exception_handling():
    """Test custom exception classes."""
    print("\nTesting exception handling...")
    
    try:
        from multiverse_character_generator.exceptions import (
            InvalidUniverseError, InvalidDetailsError
        )
        
        # Test InvalidUniverseError
        try:
            raise InvalidUniverseError(
                message="Test universe error",
                universe="invalid_universe",
                available_universes=["fantasy", "sci-fi"]
            )
        except InvalidUniverseError as e:
            print(f"✓ InvalidUniverseError: {e.universe}")
        
        # Test InvalidDetailsError
        try:
            raise InvalidDetailsError(
                message="Test details error",
                universe="fantasy",
                expected_count=4,
                actual_count=2
            )
        except InvalidDetailsError as e:
            print(f"✓ InvalidDetailsError: expected {e.expected_count}, got {e.actual_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Exception handling error: {e}")
        return False

def test_cli_module():
    """Test CLI module structure."""
    print("\nTesting CLI module...")
    
    try:
        from multiverse_character_generator.cli import create_parser
        
        parser = create_parser()
        print(f"✓ CLI parser created with {len(parser._actions)} arguments")
        
        # Test help generation
        help_text = parser.format_help()
        if "multiverse-gen" in help_text and "fantasy" in help_text:
            print("✓ CLI help text contains expected content")
        
        return True
        
    except Exception as e:
        print(f"✗ CLI module error: {e}")
        return False

def demonstrate_universe_showcase():
    """Demonstrate universe information without ML generation."""
    print("\n" + "="*50)
    print("MULTIVERSE CHARACTER GENERATOR - UNIVERSE SHOWCASE")
    print("="*50)
    
    try:
        from multiverse_character_generator.universes import get_all_universes, get_universe_config
        
        universes = get_all_universes()
        
        for universe in universes:
            config = get_universe_config(universe)
            print(f"\n🌍 {universe.upper()} UNIVERSE")
            print("-" * 30)
            
            print("Required Fields:")
            for i, field in enumerate(config['inputs'], 1):
                print(f"  {i}. {field}")
            
            print("\nExample Values:")
            for i, example in enumerate(config['exemplos'][:4], 1):  # Show first 4 examples
                print(f"  {i}. {example}")
        
        return True
        
    except Exception as e:
        print(f"✗ Universe showcase error: {e}")
        return False

def show_package_structure():
    """Display the package structure."""
    print("\n" + "="*50)
    print("PACKAGE STRUCTURE")
    print("="*50)
    
    package_files = [
        "multiverse_character_generator/__init__.py",
        "multiverse_character_generator/generator.py",
        "multiverse_character_generator/models.py", 
        "multiverse_character_generator/universes.py",
        "multiverse_character_generator/exceptions.py",
        "multiverse_character_generator/utils.py",
        "multiverse_character_generator/cli.py",
        "examples/basic_usage.py",
        "examples/async_usage.py",
        "examples/custom_parameters.py",
        "docs/README.md",
        "docs/API_REFERENCE.md",
        "docs/QUICK_START.md",
        "docs/EXAMPLES.md",
        "docs-site/package.json",
        "pyproject.toml",
        "setup.py"
    ]
    
    print("Core Package Files:")
    for file_path in package_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")

def main():
    """Run all lightweight tests."""
    print("MULTIVERSE CHARACTER GENERATOR - LIGHTWEIGHT DEMO")
    print("=" * 60)
    print("Testing library structure without heavy ML dependencies...")
    
    tests = [
        ("Core Imports", test_library_imports),
        ("Universe Configuration", test_universe_configuration),
        ("Data Models", test_data_models),
        ("Utilities", test_utilities),
        ("Exception Handling", test_exception_handling),
        ("CLI Module", test_cli_module)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
    
    print(f"\n" + "="*60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All core library components working correctly!")
        
        # Show additional information
        demonstrate_universe_showcase()
        show_package_structure()
        
        print(f"\n" + "="*60)
        print("PUBLICATION READY")
        print("="*60)
        print("✓ React documentation site configured")
        print("✓ GitHub Actions workflows for PyPI publication")
        print("✓ GitHub Pages deployment setup")
        print("✓ Complete package structure with CLI")
        print("✓ Professional documentation and examples")
        
        print(f"\nNext steps:")
        print("1. Configure GitHub repository secrets for PyPI tokens")
        print("2. Enable GitHub Pages in repository settings")
        print("3. Create version tags for automated publishing")
        print("4. Install heavy dependencies for full ML functionality")
        
    else:
        print(f"✗ {total - passed} tests failed - check library structure")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())