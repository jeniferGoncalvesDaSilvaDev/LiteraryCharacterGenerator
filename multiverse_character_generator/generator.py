"""
Core character generation functionality using GPT-2.
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Union
import torch
import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

from .models import CharacterDetails, GeneratedCharacter
from .universes import get_universes, create_prompt
from .exceptions import InvalidUniverseError, InvalidDetailsError, GenerationError
from .utils import setup_logging, save_character_to_file

# Setup logging
logger = logging.getLogger(__name__)


class MultiverseCharacterGenerator:
    """
    Main class for generating fictional characters across multiple universes.
    
    This class handles model initialization, character generation, and provides
    both synchronous and asynchronous interfaces.
    """
    
    def __init__(
        self,
        model_name: str = "gpt2-medium",
        use_gpu: bool = None,
        cache_dir: Optional[str] = None
    ):
        """
        Initialize the character generator.
        
        Args:
            model_name: Name of the GPT-2 model to use
            use_gpu: Whether to use GPU if available. None for auto-detect
            cache_dir: Directory to cache model files
        """
        self.model_name = model_name
        self.use_gpu = use_gpu if use_gpu is not None else torch.cuda.is_available()
        self.cache_dir = cache_dir
        
        # Initialize components
        self._setup_nltk()
        self._initialize_model()
        
        # Load universe configurations
        self.universes = get_universes()
        
        logger.info(f"MultiverseCharacterGenerator initialized with model: {model_name}")
    
    def _setup_nltk(self) -> None:
        """Download required NLTK data."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
    
    def _initialize_model(self) -> None:
        """Initialize the GPT-2 model and tokenizer."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            # Initialize text generation pipeline
            device = 0 if self.use_gpu else -1
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=device
            )
            
            logger.info("Model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise GenerationError(f"Model initialization failed: {str(e)}")
    
    def generate_character(
        self,
        universe: str,
        details: List[str],
        max_length: int = 350,
        temperature: float = 0.85,
        top_p: float = 0.92,
        repetition_penalty: float = 1.2,
        save_to_file: bool = False,
        output_dir: Optional[str] = None
    ) -> GeneratedCharacter:
        """
        Generate a character with custom details.
        
        Args:
            universe: The fictional universe (e.g., 'fantasy', 'sci-fi')
            details: List of character details matching universe requirements
            max_length: Maximum length of generated text
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            repetition_penalty: Penalty for repetition
            save_to_file: Whether to save the character to a file
            output_dir: Directory to save files (defaults to current directory)
            
        Returns:
            GeneratedCharacter object with character text and optional filename
            
        Raises:
            InvalidUniverseError: If universe is not supported
            InvalidDetailsError: If details don't match universe requirements
            GenerationError: If character generation fails
        """
        # Validate universe
        if universe not in self.universes:
            raise InvalidUniverseError(
                f"Invalid universe '{universe}'. "
                f"Available universes: {', '.join(self.universes.keys())}"
            )
        
        # Validate details
        expected_fields = len(self.universes[universe]["inputs"])
        if len(details) != expected_fields:
            raise InvalidDetailsError(
                f"Expected {expected_fields} details for universe '{universe}'. "
                f"Received {len(details)}. "
                f"Required fields: {', '.join(self.universes[universe]['inputs'])}"
            )
        
        # Generate character
        try:
            prompt = create_prompt(universe, details)
            character_text = self._generate_text(
                prompt=prompt,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty
            )
            
            # Save to file if requested
            filename = None
            if save_to_file:
                filename = save_character_to_file(
                    character_text=character_text,
                    universe=universe,
                    details=details,
                    output_dir=output_dir
                )
            
            logger.info(f"Successfully generated character for universe: {universe}")
            return GeneratedCharacter(character=character_text, filename=filename)
            
        except Exception as e:
            logger.error(f"Character generation failed: {str(e)}")
            raise GenerationError(f"Failed to generate character: {str(e)}")
    
    def quick_generate(
        self,
        universe: str,
        max_length: int = 350,
        temperature: float = 0.85,
        top_p: float = 0.92,
        repetition_penalty: float = 1.2,
        save_to_file: bool = False,
        output_dir: Optional[str] = None
    ) -> GeneratedCharacter:
        """
        Generate a character using predefined examples for the universe.
        
        Args:
            universe: The fictional universe
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            repetition_penalty: Penalty for repetition
            save_to_file: Whether to save the character to a file
            output_dir: Directory to save files
            
        Returns:
            GeneratedCharacter object
            
        Raises:
            InvalidUniverseError: If universe is not supported
            GenerationError: If character generation fails
        """
        if universe not in self.universes:
            raise InvalidUniverseError(
                f"Invalid universe '{universe}'. "
                f"Available universes: {', '.join(self.universes.keys())}"
            )
        
        examples = self.universes[universe]["exemplos"]
        return self.generate_character(
            universe=universe,
            details=examples,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            save_to_file=save_to_file,
            output_dir=output_dir
        )
    
    async def generate_character_async(
        self,
        universe: str,
        details: List[str],
        max_length: int = 350,
        temperature: float = 0.85,
        top_p: float = 0.92,
        repetition_penalty: float = 1.2,
        save_to_file: bool = False,
        output_dir: Optional[str] = None
    ) -> GeneratedCharacter:
        """
        Asynchronous version of generate_character.
        
        Args:
            Same as generate_character
            
        Returns:
            GeneratedCharacter object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.generate_character,
            universe,
            details,
            max_length,
            temperature,
            top_p,
            repetition_penalty,
            save_to_file,
            output_dir
        )
    
    async def quick_generate_async(
        self,
        universe: str,
        max_length: int = 350,
        temperature: float = 0.85,
        top_p: float = 0.92,
        repetition_penalty: float = 1.2,
        save_to_file: bool = False,
        output_dir: Optional[str] = None
    ) -> GeneratedCharacter:
        """
        Asynchronous version of quick_generate.
        
        Args:
            Same as quick_generate
            
        Returns:
            GeneratedCharacter object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.quick_generate,
            universe,
            max_length,
            temperature,
            top_p,
            repetition_penalty,
            save_to_file,
            output_dir
        )
    
    def _generate_text(
        self,
        prompt: str,
        max_length: int,
        temperature: float,
        top_p: float,
        repetition_penalty: float
    ) -> str:
        """
        Internal method to generate text using the model.
        
        Args:
            prompt: Input prompt for generation
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            repetition_penalty: Penalty for repetition
            
        Returns:
            Generated character text
        """
        try:
            output = self.generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=1,
                repetition_penalty=repetition_penalty,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            return output[0]['generated_text']
            
        except Exception as e:
            raise GenerationError(f"Text generation failed: {str(e)}")
    
    def get_universe_info(self, universe: str) -> Dict[str, List[str]]:
        """
        Get information about a specific universe.
        
        Args:
            universe: Name of the universe
            
        Returns:
            Dictionary with inputs and examples for the universe
            
        Raises:
            InvalidUniverseError: If universe is not supported
        """
        if universe not in self.universes:
            raise InvalidUniverseError(
                f"Invalid universe '{universe}'. "
                f"Available universes: {', '.join(self.universes.keys())}"
            )
        
        return self.universes[universe]
    
    def list_universes(self) -> List[str]:
        """
        Get a list of all available universes.
        
        Returns:
            List of universe names
        """
        return list(self.universes.keys())
    
    def get_model_info(self) -> Dict[str, Union[str, bool]]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "using_gpu": self.use_gpu,
            "cache_dir": self.cache_dir,
            "device": str(next(self.model.parameters()).device)
        }
