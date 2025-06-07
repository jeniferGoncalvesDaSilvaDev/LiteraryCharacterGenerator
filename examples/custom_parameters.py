"""
Custom parameters examples for the Multiverse Character Generator library.

This example demonstrates how to fine-tune generation parameters for
different types of characters and use cases.
"""

import os
import tempfile
from multiverse_character_generator import MultiverseCharacterGenerator
from multiverse_character_generator.exceptions import MultiverseGeneratorError


def demonstrate_temperature_effects(generator: MultiverseCharacterGenerator) -> None:
    """Show how temperature affects character generation creativity."""
    print("1. Temperature Effects on Character Generation")
    print("-" * 45)
    
    universe = "anime"
    details = ["Mecha Pilot", "Psychic Powers", "Colony Destroyed", "Fight Aliens"]
    
    temperatures = [0.3, 0.7, 1.0]
    temperature_descriptions = {
        0.3: "Conservative (More predictable, focused)",
        0.7: "Balanced (Good mix of creativity and coherence)", 
        1.0: "Creative (More random and diverse)"
    }
    
    for temp in temperatures:
        print(f"\n📊 Temperature: {temp} - {temperature_descriptions[temp]}")
        print("-" * 35)
        
        try:
            character = generator.generate_character(
                universe=universe,
                details=details,
                temperature=temp,
                max_length=200
            )
            
            # Show first 150 characters
            preview = character.character[:150] + "..." if len(character.character) > 150 else character.character
            print(preview)
            
        except MultiverseGeneratorError as e:
            print(f"❌ Error with temperature {temp}: {e}")


def demonstrate_length_control(generator: MultiverseCharacterGenerator) -> None:
    """Show how max_length affects character descriptions."""
    print("\n2. Length Control for Different Use Cases")
    print("-" * 42)
    
    universe = "cyberpunk"
    details = ["Bionic Eyes", "Corporate Spy", "Data Theft", "Neon District"]
    
    length_configs = [
        (100, "Brief Summary"),
        (250, "Standard Description"),
        (500, "Detailed Profile")
    ]
    
    for max_len, description in length_configs:
        print(f"\n📏 {description} (max_length={max_len}):")
        print("-" * 30)
        
        try:
            character = generator.generate_character(
                universe=universe,
                details=details,
                max_length=max_len,
                temperature=0.8
            )
            
            print(f"Generated length: {len(character.character)} characters")
            print("Content:")
            print(character.character)
            
        except MultiverseGeneratorError as e:
            print(f"❌ Error with length {max_len}: {e}")


def demonstrate_sampling_parameters(generator: MultiverseCharacterGenerator) -> None:
    """Show effects of top_p and repetition_penalty."""
    print("\n3. Advanced Sampling Parameters")
    print("-" * 32)
    
    universe = "marvel"
    details = ["Magnetic Powers", "Brotherhood", "Anti-Hero", "Industrial City"]
    
    sampling_configs = [
        {"top_p": 0.7, "repetition_penalty": 1.0, "description": "Focused, may repeat"},
        {"top_p": 0.95, "repetition_penalty": 1.2, "description": "Diverse, less repetition"},
        {"top_p": 1.0, "repetition_penalty": 1.5, "description": "Very diverse, avoid repetition"}
    ]
    
    for config in sampling_configs:
        print(f"\n🎯 Config: top_p={config['top_p']}, repetition_penalty={config['repetition_penalty']}")
        print(f"   {config['description']}")
        print("-" * 40)
        
        try:
            character = generator.generate_character(
                universe=universe,
                details=details,
                top_p=config["top_p"],
                repetition_penalty=config["repetition_penalty"],
                max_length=250,
                temperature=0.8
            )
            
            preview = character.character[:200] + "..." if len(character.character) > 200 else character.character
            print(preview)
            
        except MultiverseGeneratorError as e:
            print(f"❌ Error with sampling config: {e}")


def demonstrate_universe_optimized_parameters(generator: MultiverseCharacterGenerator) -> None:
    """Show optimized parameters for different universes."""
    print("\n4. Universe-Optimized Parameters")
    print("-" * 33)
    
    # Optimized parameters for each universe type
    universe_configs = {
        "fantasia": {
            "temperature": 0.8,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "max_length": 350,
            "rationale": "Fantasy benefits from creative but coherent worldbuilding"
        },
        "sci-fi": {
            "temperature": 0.7,
            "top_p": 0.85,
            "repetition_penalty": 1.3,
            "max_length": 400,
            "rationale": "Sci-fi needs technical coherence with creative elements"
        },
        "terror": {
            "temperature": 0.9,
            "top_p": 0.95,
            "repetition_penalty": 1.1,
            "max_length": 300,
            "rationale": "Horror thrives on unpredictability and atmosphere"
        },
        "cyberpunk": {
            "temperature": 0.85,
            "top_p": 0.92,
            "repetition_penalty": 1.4,
            "max_length": 320,
            "rationale": "Cyberpunk needs gritty detail without repetitive jargon"
        }
    }
    
    # Sample details for each universe
    sample_details = {
        "fantasia": ["Half-Orc", "Paladin", "Lawful Good", "Sacred Grove"],
        "sci-fi": ["Synthetic", "Archaeologist", "Independent", "Ancient Ship"],
        "terror": ["Curator", "Trypophobia", "Ritual Mask", "Underground Museum"],
        "cyberpunk": ["Spinal Jack", "Info Broker", "Shadow Network", "Data Haven"]
    }
    
    for universe, config in universe_configs.items():
        print(f"\n🎮 {universe.title()} Universe Optimization:")
        print(f"   Rationale: {config['rationale']}")
        print(f"   Parameters: temp={config['temperature']}, top_p={config['top_p']}, "
              f"rep_penalty={config['repetition_penalty']}, max_len={config['max_length']}")
        print("-" * 50)
        
        try:
            character = generator.generate_character(
                universe=universe,
                details=sample_details[universe],
                temperature=config["temperature"],
                top_p=config["top_p"],
                repetition_penalty=config["repetition_penalty"],
                max_length=config["max_length"]
            )
            
            preview = character.character[:250] + "..." if len(character.character) > 250 else character.character
            print(preview)
            
        except MultiverseGeneratorError as e:
            print(f"❌ Error with {universe} optimization: {e}")


def demonstrate_file_output_options(generator: MultiverseCharacterGenerator) -> None:
    """Show different file output configurations."""
    print("\n5. File Output and Organization")
    print("-" * 30)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Using temporary directory: {temp_dir}")
        
        # Create organized subdirectories
        universe_dirs = {
            "fantasy_characters": ("fantasia", ["Tiefling", "Bard", "Chaotic Neutral", "Tavern"]),
            "space_opera": ("sci-fi", ["Alien", "Diplomat", "Galactic Union", "Space Station"]),
            "horror_collection": ("terror", ["Priest", "Cleithrophobia", "Holy Relic", "Sealed Crypt"])
        }
        
        for subdir, (universe, details) in universe_dirs.items():
            output_path = os.path.join(temp_dir, subdir)
            os.makedirs(output_path, exist_ok=True)
            
            print(f"\n📝 Generating {universe} character in {subdir}/")
            
            try:
                character = generator.generate_character(
                    universe=universe,
                    details=details,
                    max_length=300,
                    temperature=0.8,
                    save_to_file=True,
                    output_dir=output_path
                )
                
                print(f"✅ Saved to: {character.filename}")
                
                # Show file size
                if character.filename and os.path.exists(character.filename):
                    file_size = os.path.getsize(character.filename)
                    print(f"   File size: {file_size} bytes")
                
            except MultiverseGeneratorError as e:
                print(f"❌ Error saving {universe} character: {e}")


def demonstrate_parameter_validation(generator: MultiverseCharacterGenerator) -> None:
    """Show parameter validation and error handling."""
    print("\n6. Parameter Validation Examples")
    print("-" * 32)
    
    universe = "anime"
    details = ["Sword Master", "Lightning Style", "Master Killed", "Seek Truth"]
    
    # Test invalid parameter ranges
    invalid_params = [
        {"temperature": -0.1, "description": "Negative temperature"},
        {"temperature": 1.5, "description": "Temperature too high"},
        {"max_length": 10, "description": "Length too short"},
        {"max_length": 2000, "description": "Length too long"},
        {"top_p": 1.5, "description": "top_p too high"},
        {"repetition_penalty": 0.5, "description": "Repetition penalty too low"}
    ]
    
    for params in invalid_params:
        description = params.pop("description")
        print(f"\n🧪 Testing: {description}")
        
        try:
            character = generator.generate_character(
                universe=universe,
                details=details,
                **params
            )
            print(f"⚠️  Unexpectedly succeeded: {character.character[:50]}...")
            
        except Exception as e:
            print(f"✅ Correctly caught error: {type(e).__name__}: {e}")


def demonstrate_performance_tuning(generator: MultiverseCharacterGenerator) -> None:
    """Show performance considerations for different parameters."""
    print("\n7. Performance Tuning Considerations")
    print("-" * 36)
    
    universe = "cyberpunk"
    details = ["Cyber Deck", "Hacker Collective", "ICE Breaking", "Virtual Space"]
    
    # Performance-focused configurations
    perf_configs = [
        {
            "name": "Speed Optimized",
            "params": {"max_length": 150, "temperature": 0.5, "top_p": 0.8},
            "description": "Faster generation, more predictable output"
        },
        {
            "name": "Quality Optimized", 
            "params": {"max_length": 400, "temperature": 0.85, "top_p": 0.95},
            "description": "Higher quality, longer generation time"
        },
        {
            "name": "Balanced",
            "params": {"max_length": 250, "temperature": 0.75, "top_p": 0.9},
            "description": "Good balance of speed and quality"
        }
    ]
    
    import time
    
    for config in perf_configs:
        print(f"\n⚡ {config['name']} Configuration:")
        print(f"   {config['description']}")
        print(f"   Parameters: {config['params']}")
        
        try:
            start_time = time.time()
            
            character = generator.generate_character(
                universe=universe,
                details=details,
                **config["params"]
            )
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            print(f"   ⏱️  Generation time: {generation_time:.2f} seconds")
            print(f"   📏 Output length: {len(character.character)} characters")
            
            # Calculate efficiency metric (chars per second)
            efficiency = len(character.character) / generation_time if generation_time > 0 else 0
            print(f"   📊 Efficiency: {efficiency:.1f} chars/second")
            
        except MultiverseGeneratorError as e:
            print(f"❌ Error with {config['name']} config: {e}")


def main():
    """Main function demonstrating all parameter customization examples."""
    print("🌟 Multiverse Character Generator - Custom Parameters Examples")
    print("=" * 65)
    
    # Initialize generator
    print("\nInitializing Character Generator...")
    try:
        generator = MultiverseCharacterGenerator(
            model_name="gpt2",  # Use base model for consistent demos
            use_gpu=False       # Disable GPU for consistent performance metrics
        )
        print("✅ Generator initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return
    
    # Run all parameter demonstration examples
    demonstrate_temperature_effects(generator)
    demonstrate_length_control(generator)
    demonstrate_sampling_parameters(generator)
    demonstrate_universe_optimized_parameters(generator)
    demonstrate_file_output_options(generator)
    demonstrate_parameter_validation(generator)
    demonstrate_performance_tuning(generator)
    
    print("\n" + "=" * 65)
    print("🎉 Custom parameters examples completed!")
    print("\nKey insights:")
    print("- Temperature controls creativity vs coherence")
    print("- Length affects detail level and generation time")
    print("- top_p and repetition_penalty fine-tune output quality")
    print("- Different universes benefit from different parameter sets")
    print("- File organization helps manage generated content")
    print("- Performance can be optimized based on use case requirements")


if __name__ == "__main__":
    main()
