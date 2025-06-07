"""
Asynchronous usage examples for the Multiverse Character Generator library.

This example demonstrates how to use the async methods for concurrent
character generation and batch processing.
"""

import asyncio
import time
from typing import List, Tuple
from multiverse_character_generator import MultiverseCharacterGenerator
from multiverse_character_generator.models import GeneratedCharacter
from multiverse_character_generator.exceptions import MultiverseGeneratorError


async def generate_single_character_async(generator: MultiverseCharacterGenerator) -> None:
    """Example 1: Basic async character generation."""
    print("1. Basic Async Character Generation")
    print("-" * 35)
    
    try:
        start_time = time.time()
        
        character = await generator.generate_character_async(
            universe="fantasia",
            details=["Dragon", "Sorcerer", "Lawful Evil", "Volcanic Lair"],
            max_length=250
        )
        
        end_time = time.time()
        
        print(f"✅ Character generated in {end_time - start_time:.2f} seconds")
        print("\n📖 Generated Character:")
        print(character.character[:300] + "..." if len(character.character) > 300 else character.character)
        
    except MultiverseGeneratorError as e:
        print(f"❌ Error: {e}")


async def quick_generate_async(generator: MultiverseCharacterGenerator) -> None:
    """Example 2: Quick async generation."""
    print("\n2. Quick Async Generation")
    print("-" * 25)
    
    try:
        start_time = time.time()
        
        character = await generator.quick_generate_async(
            universe="cyberpunk",
            temperature=0.8
        )
        
        end_time = time.time()
        
        print(f"✅ Quick character generated in {end_time - start_time:.2f} seconds")
        print("\n📖 Generated Character:")
        print(character.character[:300] + "..." if len(character.character) > 300 else character.character)
        
    except MultiverseGeneratorError as e:
        print(f"❌ Error: {e}")


async def concurrent_generation(generator: MultiverseCharacterGenerator) -> None:
    """Example 3: Concurrent character generation."""
    print("\n3. Concurrent Character Generation")
    print("-" * 35)
    
    # Define multiple character requests
    requests = [
        ("sci-fi", ["Alien", "Engineer", "Rebel Fleet", "Asteroid Base"]),
        ("anime", ["Ninja", "Shadow Magic", "Clan Betrayed", "Seek Revenge"]),
        ("terror", ["Doctor", "Agoraphobia", "Medical Journal", "Asylum"]),
        ("marvel", ["Spider Powers", "Avengers", "Vigilante", "Queens"])
    ]
    
    try:
        start_time = time.time()
        
        # Create coroutines for concurrent execution
        tasks = [
            generator.generate_character_async(
                universe=universe,
                details=details,
                max_length=200
            )
            for universe, details in requests
        ]
        
        # Execute all tasks concurrently
        characters = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        
        print(f"✅ Generated {len(requests)} characters concurrently in {end_time - start_time:.2f} seconds")
        
        # Display results
        for i, (request, result) in enumerate(zip(requests, characters)):
            universe, details = request
            if isinstance(result, Exception):
                print(f"\n❌ {universe.title()} generation failed: {result}")
            else:
                print(f"\n📖 {i+1}. {universe.title()} Character:")
                preview = result.character[:150] + "..." if len(result.character) > 150 else result.character
                print(preview)
        
    except Exception as e:
        print(f"❌ Concurrent generation error: {e}")


async def batch_processing_with_rate_limiting(generator: MultiverseCharacterGenerator) -> None:
    """Example 4: Batch processing with rate limiting."""
    print("\n4. Batch Processing with Rate Limiting")
    print("-" * 40)
    
    # Large batch of character requests
    batch_requests = [
        ("fantasia", ["Orc", "Warrior", "Chaotic Evil", "Dark Mountains"]),
        ("sci-fi", ["Robot", "Medic", "Space Navy", "Medical Ship"]),
        ("cyberpunk", ["Neural Implant", "Data Courier", "Freelancer", "Underground"]),
        ("anime", ["Samurai", "Wind Technique", "Honor Lost", "Restore Name"]),
        ("terror", ["Photographer", "Nyctophobia", "Cursed Camera", "Darkroom"]),
        ("marvel", ["Telekinesis", "X-Force", "Mutant", "School"])
    ]
    
    async def generate_with_delay(universe: str, details: List[str], delay: float) -> Tuple[str, GeneratedCharacter]:
        """Generate character with artificial delay for rate limiting."""
        await asyncio.sleep(delay)
        character = await generator.generate_character_async(
            universe=universe,
            details=details,
            max_length=150
        )
        return universe, character
    
    try:
        start_time = time.time()
        
        # Create tasks with staggered delays (rate limiting)
        tasks = [
            generate_with_delay(universe, details, i * 0.5)  # 0.5 second intervals
            for i, (universe, details) in enumerate(batch_requests)
        ]
        
        # Process in batches of 3
        batch_size = 3
        results = []
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_results)
            
            print(f"   Completed batch {i//batch_size + 1}/{(len(tasks) + batch_size - 1)//batch_size}")
        
        end_time = time.time()
        
        print(f"\n✅ Processed {len(batch_requests)} characters in {end_time - start_time:.2f} seconds")
        
        # Count successful generations
        successful = sum(1 for result in results if not isinstance(result, Exception))
        print(f"📊 Success rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Batch processing error: {e}")


async def error_handling_async(generator: MultiverseCharacterGenerator) -> None:
    """Example 5: Async error handling."""
    print("\n5. Async Error Handling")
    print("-" * 23)
    
    # Test various error conditions
    error_tests = [
        ("invalid_universe", ["detail1", "detail2"]),
        ("fantasia", ["too", "few"]),  # Fantasy needs 4 details
        ("sci-fi", [])  # Empty details
    ]
    
    for universe, details in error_tests:
        try:
            print(f"\n   Testing: {universe} with {len(details)} details")
            character = await generator.generate_character_async(universe, details)
            print(f"   ⚠️  Unexpected success: {character.character[:50]}...")
            
        except MultiverseGeneratorError as e:
            print(f"   ✅ Caught expected error: {type(e).__name__}")
            
        except Exception as e:
            print(f"   ❌ Unexpected error: {type(e).__name__}: {e}")


async def performance_comparison(generator: MultiverseCharacterGenerator) -> None:
    """Example 6: Performance comparison between sync and async."""
    print("\n6. Performance Comparison: Sync vs Async")
    print("-" * 40)
    
    requests = [
        ("fantasia", ["Elf", "Ranger", "Neutral Good", "Ancient Forest"]),
        ("sci-fi", ["Human", "Captain", "Federation", "Starship"]),
        ("anime", ["Student", "Teleportation", "Bullied", "Protect Others"])
    ]
    
    # Synchronous generation
    print("\n   📊 Synchronous Generation:")
    sync_start = time.time()
    sync_results = []
    
    for universe, details in requests:
        try:
            character = generator.generate_character(universe, details, max_length=100)
            sync_results.append(character)
        except Exception as e:
            print(f"      Sync error for {universe}: {e}")
    
    sync_end = time.time()
    sync_time = sync_end - sync_start
    print(f"   ⏱️  Sync time: {sync_time:.2f} seconds")
    
    # Asynchronous generation
    print("\n   📊 Asynchronous Generation:")
    async_start = time.time()
    
    try:
        tasks = [
            generator.generate_character_async(universe, details, max_length=100)
            for universe, details in requests
        ]
        async_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        async_end = time.time()
        async_time = async_end - async_start
        
        print(f"   ⏱️  Async time: {async_time:.2f} seconds")
        
        # Calculate performance improvement
        if sync_time > 0:
            improvement = ((sync_time - async_time) / sync_time) * 100
            print(f"   🚀 Performance improvement: {improvement:.1f}%")
        
        successful_async = sum(1 for result in async_results if not isinstance(result, Exception))
        print(f"   📈 Async success rate: {successful_async}/{len(requests)}")
        
    except Exception as e:
        print(f"   ❌ Async comparison error: {e}")


async def main():
    """Main async function demonstrating all examples."""
    print("🌟 Multiverse Character Generator - Async Usage Examples")
    print("=" * 60)
    
    # Initialize generator
    print("\nInitializing Character Generator...")
    try:
        generator = MultiverseCharacterGenerator(
            model_name="gpt2",  # Use smaller model for faster demos
            use_gpu=False       # Disable GPU for consistent timing
        )
        print("✅ Generator initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return
    
    # Run all async examples
    await generate_single_character_async(generator)
    await quick_generate_async(generator)
    await concurrent_generation(generator)
    await batch_processing_with_rate_limiting(generator)
    await error_handling_async(generator)
    await performance_comparison(generator)
    
    print("\n" + "=" * 60)
    print("🎉 Async usage examples completed!")
    print("\nKey takeaways:")
    print("- Use async methods for concurrent character generation")
    print("- Implement rate limiting for large batches")
    print("- Handle errors gracefully with proper exception catching")
    print("- Async can provide significant performance improvements")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
