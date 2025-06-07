#!/usr/bin/env python3
"""
Command-line interface for the Multiverse Character Generator.
"""

import argparse
import asyncio
import sys
from typing import List, Optional
from pathlib import Path

from .generator import MultiverseCharacterGenerator
from .exceptions import (
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError,
    MultiverseGeneratorError
)


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="multiverse-gen",
        description="Generate fictional characters across multiple universes using GPT-2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick generation
  multiverse-gen fantasy
  multiverse-gen sci-fi --temperature 0.9
  
  # Custom character details
  multiverse-gen fantasy --details "Elf" "Mage" "Chaotic Good" "Rivendell"
  
  # Save to file
  multiverse-gen cyberpunk --save --output-dir ./characters
  
  # List available universes
  multiverse-gen --list-universes
  
  # Get universe information
  multiverse-gen --universe-info fantasy
        """
    )
    
    parser.add_argument(
        "universe",
        nargs="?",
        help="Target universe (fantasy, sci-fi, horror, cyberpunk, anime, marvel)"
    )
    
    parser.add_argument(
        "--details",
        nargs="+",
        help="Character details matching universe requirements"
    )
    
    parser.add_argument(
        "--max-length",
        type=int,
        default=350,
        help="Maximum length of generated text (default: 350)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.85,
        help="Sampling temperature (0.0-1.0, default: 0.85)"
    )
    
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.92,
        help="Nucleus sampling parameter (0.0-1.0, default: 0.92)"
    )
    
    parser.add_argument(
        "--repetition-penalty",
        type=float,
        default=1.2,
        help="Repetition penalty (1.0-2.0, default: 1.2)"
    )
    
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save generated character to file"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save files (default: current directory)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gpt2-medium",
        choices=["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"],
        help="GPT-2 model to use (default: gpt2-medium)"
    )
    
    parser.add_argument(
        "--no-gpu",
        action="store_true",
        help="Disable GPU usage"
    )
    
    parser.add_argument(
        "--cache-dir",
        type=str,
        help="Directory to cache model files"
    )
    
    parser.add_argument(
        "--list-universes",
        action="store_true",
        help="List all available universes"
    )
    
    parser.add_argument(
        "--universe-info",
        type=str,
        metavar="UNIVERSE",
        help="Show information about a specific universe"
    )
    
    parser.add_argument(
        "--batch",
        type=str,
        help="Path to JSON file with batch generation requests"
    )
    
    parser.add_argument(
        "--async",
        action="store_true",
        dest="use_async",
        help="Use async generation (useful for batch processing)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser


def print_universe_list(generator: MultiverseCharacterGenerator) -> None:
    """Print list of available universes."""
    universes = generator.list_universes()
    print("Available Universes:")
    print("===================")
    for universe in universes:
        print(f"  • {universe}")
    print(f"\nTotal: {len(universes)} universes")


def print_universe_info(generator: MultiverseCharacterGenerator, universe: str) -> None:
    """Print detailed information about a universe."""
    try:
        info = generator.get_universe_info(universe)
        print(f"Universe: {universe.title()}")
        print("=" * (len(universe) + 10))
        
        print("\nRequired Fields:")
        for i, field in enumerate(info['inputs'], 1):
            print(f"  {i}. {field}")
        
        print("\nExample Values:")
        for i, example in enumerate(info['exemplos'], 1):
            print(f"  {i}. {example}")
            
    except InvalidUniverseError as e:
        print(f"Error: {e}")
        print(f"Available universes: {', '.join(e.available_universes)}")


def load_batch_requests(file_path: str) -> List[dict]:
    """Load batch generation requests from JSON file."""
    import json
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and 'requests' in data:
            return data['requests']
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid batch file format")
            
    except Exception as e:
        print(f"Error loading batch file: {e}")
        sys.exit(1)


async def process_batch_requests(
    generator: MultiverseCharacterGenerator,
    requests: List[dict],
    args: argparse.Namespace
) -> None:
    """Process batch generation requests."""
    print(f"Processing {len(requests)} batch requests...")
    
    tasks = []
    for i, req in enumerate(requests):
        universe = req.get('universe')
        details = req.get('details')
        
        if not universe:
            print(f"Warning: Request {i+1} missing universe, skipping")
            continue
        
        params = {
            'max_length': req.get('max_length', args.max_length),
            'temperature': req.get('temperature', args.temperature),
            'top_p': req.get('top_p', args.top_p),
            'repetition_penalty': req.get('repetition_penalty', args.repetition_penalty),
            'save_to_file': req.get('save_to_file', args.save),
            'output_dir': req.get('output_dir', args.output_dir)
        }
        
        if details:
            task = generator.generate_character_async(
                universe=universe,
                details=details,
                **params
            )
        else:
            task = generator.quick_generate_async(
                universe=universe,
                **params
            )
        
        tasks.append((i+1, task))
    
    # Execute batch requests
    results = []
    for i, task in tasks:
        try:
            result = await task
            results.append((i, result, None))
            if args.verbose:
                print(f"✓ Request {i} completed")
        except Exception as e:
            results.append((i, None, e))
            print(f"✗ Request {i} failed: {e}")
    
    # Summary
    successful = len([r for r in results if r[2] is None])
    failed = len(results) - successful
    
    print(f"\nBatch Generation Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(results)}")


async def generate_character_async(
    generator: MultiverseCharacterGenerator,
    args: argparse.Namespace
) -> None:
    """Generate a single character asynchronously."""
    params = {
        'max_length': args.max_length,
        'temperature': args.temperature,
        'top_p': args.top_p,
        'repetition_penalty': args.repetition_penalty,
        'save_to_file': args.save,
        'output_dir': args.output_dir
    }
    
    try:
        if args.details:
            character = await generator.generate_character_async(
                universe=args.universe,
                details=args.details,
                **params
            )
        else:
            character = await generator.quick_generate_async(
                universe=args.universe,
                **params
            )
        
        print(f"Generated Character ({args.universe}):")
        print("=" * 40)
        print(character.character)
        
        if character.filename:
            print(f"\n✓ Saved to: {character.filename}")
            
    except MultiverseGeneratorError as e:
        print(f"Error: {e}")
        sys.exit(1)


def generate_character_sync(
    generator: MultiverseCharacterGenerator,
    args: argparse.Namespace
) -> None:
    """Generate a single character synchronously."""
    params = {
        'max_length': args.max_length,
        'temperature': args.temperature,
        'top_p': args.top_p,
        'repetition_penalty': args.repetition_penalty,
        'save_to_file': args.save,
        'output_dir': args.output_dir
    }
    
    try:
        if args.details:
            character = generator.generate_character(
                universe=args.universe,
                details=args.details,
                **params
            )
        else:
            character = generator.quick_generate(
                universe=args.universe,
                **params
            )
        
        print(f"Generated Character ({args.universe}):")
        print("=" * 40)
        print(character.character)
        
        if character.filename:
            print(f"\n✓ Saved to: {character.filename}")
            
    except MultiverseGeneratorError as e:
        print(f"Error: {e}")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle info commands
    if args.list_universes or args.universe_info:
        try:
            generator = MultiverseCharacterGenerator(
                model_name=args.model,
                use_gpu=not args.no_gpu,
                cache_dir=args.cache_dir
            )
            
            if args.list_universes:
                print_universe_list(generator)
            elif args.universe_info:
                print_universe_info(generator, args.universe_info)
                
        except Exception as e:
            print(f"Error initializing generator: {e}")
            sys.exit(1)
        
        return
    
    # Validate required arguments
    if not args.universe and not args.batch:
        parser.error("Either universe or --batch is required")
    
    # Initialize generator
    if args.verbose:
        print("Initializing character generator...")
    
    try:
        generator = MultiverseCharacterGenerator(
            model_name=args.model,
            use_gpu=not args.no_gpu,
            cache_dir=args.cache_dir
        )
        
        if args.verbose:
            model_info = generator.get_model_info()
            print(f"Model: {model_info['model_name']}")
            print(f"Device: {model_info['device']}")
            print(f"GPU: {model_info['using_gpu']}")
            
    except Exception as e:
        print(f"Error initializing generator: {e}")
        sys.exit(1)
    
    # Process requests
    try:
        if args.batch:
            # Batch processing
            requests = load_batch_requests(args.batch)
            asyncio.run(process_batch_requests(generator, requests, args))
            
        elif args.use_async:
            # Single async generation
            asyncio.run(generate_character_async(generator, args))
            
        else:
            # Single sync generation
            generate_character_sync(generator, args)
            
    except KeyboardInterrupt:
        print("\n\nGeneration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()