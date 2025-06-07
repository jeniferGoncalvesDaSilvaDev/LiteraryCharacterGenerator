"""
Basic usage examples for the Multiverse Character Generator library.

This example demonstrates the most common use cases for generating
fictional characters across different universes.
"""

import os
from multiverse_character_generator import MultiverseCharacterGenerator
from multiverse_character_generator.exceptions import (
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError
)


def main():
    """Demonstrate basic usage of the character generator."""
    print("🌟 Multiverse Character Generator - Basic Usage Examples")
    print("=" * 60)
    
    # Initialize the generator
    print("\n1. Initializing Character Generator...")
    try:
        generator = MultiverseCharacterGenerator(
            model_name="gpt2-medium",  # Use medium model for better quality
            use_gpu=None  # Auto-detect GPU
        )
        print("✅ Generator initialized successfully!")
        
        # Display model information
        model_info = generator.get_model_info()
        print(f"   Model: {model_info['model_name']}")
        print(f"   Device: {model_info['device']}")
        print(f"   Using GPU: {model_info['using_gpu']}")
        
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return
    
    # List available universes
    print("\n2. Available Universes:")
    universes = generator.list_universes()
    for i, universe in enumerate(universes, 1):
        print(f"   {i}. {universe.title()}")
    
    # Show universe requirements
    print("\n3. Universe Requirements:")
    for universe in universes[:3]:  # Show first 3 for brevity
        try:
            info = generator.get_universe_info(universe)
            print(f"\n   {universe.title()}:")
            print(f"   Required: {', '.join(info['inputs'])}")
            print(f"   Examples: {', '.join(info['exemplos'])}")
        except Exception as e:
            print(f"   ❌ Error getting info for {universe}: {e}")
    
    # Example 1: Fantasy Character
    print("\n4. Example 1: Generating a Fantasy Character")
    print("-" * 40)
    try:
        fantasy_character = generator.generate_character(
            universe="fantasia",
            details=["Halfling", "Rogue", "Chaotic Neutral", "Riverside Town"],
            max_length=300
        )
        print("✅ Fantasy character generated!")
        print("\n📖 Character Description:")
        print("-" * 25)
        print(fantasy_character.character)
        
    except (InvalidUniverseError, InvalidDetailsError, GenerationError) as e:
        print(f"❌ Error generating fantasy character: {e}")
    
    # Example 2: Sci-Fi Character with Quick Generation
    print("\n5. Example 2: Quick Sci-Fi Character Generation")
    print("-" * 45)
    try:
        scifi_character = generator.quick_generate(
            universe="sci-fi",
            max_length=250,
            temperature=0.9  # More creative
        )
        print("✅ Sci-Fi character generated using examples!")
        print("\n📖 Character Description:")
        print("-" * 25)
        print(scifi_character.character)
        
    except Exception as e:
        print(f"❌ Error generating sci-fi character: {e}")
    
    # Example 3: Cyberpunk Character with File Saving
    print("\n6. Example 3: Cyberpunk Character (Saved to File)")
    print("-" * 48)
    try:
        cyberpunk_character = generator.generate_character(
            universe="cyberpunk",
            details=[
                "Optical Enhancement Mk-III",
                "Street Samurai Gang",
                "Corporate Infiltration",
                "Neo-Tokyo District 9"
            ],
            save_to_file=True,
            output_dir="./generated_characters"
        )
        print("✅ Cyberpunk character generated and saved!")
        print(f"📁 Saved to: {cyberpunk_character.filename}")
        print("\n📖 Character Description:")
        print("-" * 25)
        print(cyberpunk_character.character[:500] + "..." if len(cyberpunk_character.character) > 500 else cyberpunk_character.character)
        
    except Exception as e:
        print(f"❌ Error generating cyberpunk character: {e}")
    
    # Example 4: Multiple Characters
    print("\n7. Example 4: Generating Multiple Characters")
    print("-" * 42)
    
    character_requests = [
        ("anime", ["Magical Girl", "Healing Powers", "Lost Memory", "Save Friends"]),
        ("marvel", ["Cosmic Energy", "X-Men", "Anti-Hero", "Space Station"]),
        ("terror", ["Librarian", "Fear of Mirrors", "Ancient Tome", "Abandoned Library"])
    ]
    
    generated_characters = []
    
    for universe, details in character_requests:
        try:
            print(f"\n   📝 Generating {universe.title()} character...")
            character = generator.generate_character(
                universe=universe,
                details=details,
                max_length=200
            )
            generated_characters.append((universe, character))
            print(f"   ✅ {universe.title()} character generated!")
            
        except Exception as e:
            print(f"   ❌ Failed to generate {universe} character: {e}")
    
    # Display all generated characters
    print(f"\n📚 Generated {len(generated_characters)} characters:")
    for i, (universe, character) in enumerate(generated_characters, 1):
        print(f"\n{i}. {universe.title()} Character:")
        print("-" * 20)
        # Show first 200 characters
        preview = character.character[:200] + "..." if len(character.character) > 200 else character.character
        print(preview)
    
    # Example 5: Error Handling
    print("\n8. Example 5: Error Handling")
    print("-" * 30)
    
    # Invalid universe
    try:
        generator.generate_character("invalid_universe", ["detail1", "detail2"])
    except InvalidUniverseError as e:
        print(f"✅ Caught expected error - Invalid Universe: {e}")
    
    # Invalid details count
    try:
        generator.generate_character("fantasia", ["Only", "Two"])  # Needs 4 details
    except InvalidDetailsError as e:
        print(f"✅ Caught expected error - Invalid Details: {e}")
    
    # Example 6: Custom Parameters
    print("\n9. Example 6: Custom Generation Parameters")
    print("-" * 42)
    try:
        custom_character = generator.generate_character(
            universe="anime",
            details=["Shounen Hero", "Fire Magic", "Village Destroyed", "Defeat Demon King"],
            max_length=400,        # Longer description
            temperature=0.7,       # Less random
            top_p=0.9,            # Focused sampling
            repetition_penalty=1.3 # Avoid repetition
        )
        print("✅ Character generated with custom parameters!")
        print("\n📖 Character Description:")
        print("-" * 25)
        print(custom_character.character)
        
    except Exception as e:
        print(f"❌ Error with custom parameters: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Basic usage examples completed!")
    print("\nNext steps:")
    print("- Try the async_usage.py example for asynchronous generation")
    print("- Check custom_parameters.py for advanced parameter tuning")
    print("- Explore different universes and character combinations")


if __name__ == "__main__":
    main()
