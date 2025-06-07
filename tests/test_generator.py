"""
Tests for the MultiverseCharacterGenerator class.
"""

import pytest
import asyncio
import os
import tempfile
from unittest.mock import patch, MagicMock

from multiverse_character_generator import MultiverseCharacterGenerator
from multiverse_character_generator.exceptions import (
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError
)
from multiverse_character_generator.models import GeneratedCharacter

from . import TEST_CONFIG, SAMPLE_UNIVERSES, SAMPLE_DETAILS, get_test_generator, is_valid_character_text


class TestMultiverseCharacterGenerator:
    """Test suite for MultiverseCharacterGenerator."""
    
    @pytest.fixture
    def generator(self):
        """Fixture to provide a generator instance."""
        return get_test_generator()
    
    def test_initialization(self):
        """Test generator initialization."""
        generator = MultiverseCharacterGenerator(**TEST_CONFIG)
        
        assert generator.model_name == TEST_CONFIG["model_name"]
        assert generator.use_gpu == TEST_CONFIG["use_gpu"]
        assert hasattr(generator, 'model')
        assert hasattr(generator, 'tokenizer')
        assert hasattr(generator, 'generator')
        assert hasattr(generator, 'universes')
    
    def test_list_universes(self, generator):
        """Test universe listing."""
        universes = generator.list_universes()
        
        assert isinstance(universes, list)
        assert len(universes) == len(SAMPLE_UNIVERSES)
        for universe in SAMPLE_UNIVERSES:
            assert universe in universes
    
    def test_get_universe_info(self, generator):
        """Test getting universe information."""
        for universe in SAMPLE_UNIVERSES:
            info = generator.get_universe_info(universe)
            
            assert isinstance(info, dict)
            assert "inputs" in info
            assert "exemplos" in info
            assert isinstance(info["inputs"], list)
            assert isinstance(info["exemplos"], list)
            assert len(info["inputs"]) > 0
            assert len(info["exemplos"]) > 0
    
    def test_get_universe_info_invalid(self, generator):
        """Test getting info for invalid universe."""
        with pytest.raises(InvalidUniverseError):
            generator.get_universe_info("invalid_universe")
    
    def test_get_model_info(self, generator):
        """Test getting model information."""
        info = generator.get_model_info()
        
        assert isinstance(info, dict)
        assert "model_name" in info
        assert "using_gpu" in info
        assert "cache_dir" in info
        assert "device" in info
        assert info["model_name"] == TEST_CONFIG["model_name"]
    
    @pytest.mark.slow
    def test_generate_character_valid(self, generator):
        """Test character generation with valid inputs."""
        universe = "fantasia"
        details = SAMPLE_DETAILS[universe]
        
        result = generator.generate_character(universe, details)
        
        assert isinstance(result, GeneratedCharacter)
        assert isinstance(result.character, str)
        assert len(result.character.strip()) > 0
        assert result.filename is None  # No file saving by default
    
    @pytest.mark.slow
    def test_generate_character_all_universes(self, generator):
        """Test character generation for all universes."""
        for universe in SAMPLE_UNIVERSES:
            details = SAMPLE_DETAILS[universe]
            
            result = generator.generate_character(universe, details)
            
            assert isinstance(result, GeneratedCharacter)
            assert is_valid_character_text(result.character)
    
    def test_generate_character_invalid_universe(self, generator):
        """Test character generation with invalid universe."""
        with pytest.raises(InvalidUniverseError) as exc_info:
            generator.generate_character("invalid_universe", ["detail1", "detail2"])
        
        assert "invalid_universe" in str(exc_info.value)
        assert "Available universes:" in str(exc_info.value)
    
    def test_generate_character_invalid_details_count(self, generator):
        """Test character generation with wrong number of details."""
        universe = "fantasia"
        wrong_details = ["Only", "Two"]  # Fantasy needs 4 details
        
        with pytest.raises(InvalidDetailsError) as exc_info:
            generator.generate_character(universe, wrong_details)
        
        assert "Expected 4 details" in str(exc_info.value)
        assert "Received 2" in str(exc_info.value)
    
    @pytest.mark.slow
    def test_quick_generate(self, generator):
        """Test quick character generation."""
        for universe in SAMPLE_UNIVERSES:
            result = generator.quick_generate(universe)
            
            assert isinstance(result, GeneratedCharacter)
            assert is_valid_character_text(result.character)
    
    def test_quick_generate_invalid_universe(self, generator):
        """Test quick generation with invalid universe."""
        with pytest.raises(InvalidUniverseError):
            generator.quick_generate("invalid_universe")
    
    @pytest.mark.slow
    def test_generate_character_with_file_save(self, generator):
        """Test character generation with file saving."""
        with tempfile.TemporaryDirectory() as temp_dir:
            universe = "fantasia"
            details = SAMPLE_DETAILS[universe]
            
            result = generator.generate_character(
                universe,
                details,
                save_to_file=True,
                output_dir=temp_dir
            )
            
            assert isinstance(result, GeneratedCharacter)
            assert result.filename is not None
            assert os.path.exists(result.filename)
            
            # Check file content
            with open(result.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                assert universe in content
                assert result.character in content
    
    @pytest.mark.slow
    def test_custom_generation_parameters(self, generator):
        """Test character generation with custom parameters."""
        universe = "sci-fi"
        details = SAMPLE_DETAILS[universe]
        
        result = generator.generate_character(
            universe,
            details,
            max_length=150,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        assert isinstance(result, GeneratedCharacter)
        assert is_valid_character_text(result.character)
    
    @pytest.mark.asyncio
    async def test_generate_character_async(self, generator):
        """Test asynchronous character generation."""
        universe = "cyberpunk"
        details = SAMPLE_DETAILS[universe]
        
        result = await generator.generate_character_async(universe, details)
        
        assert isinstance(result, GeneratedCharacter)
        assert is_valid_character_text(result.character)
    
    @pytest.mark.asyncio
    async def test_quick_generate_async(self, generator):
        """Test asynchronous quick generation."""
        result = await generator.quick_generate_async("anime")
        
        assert isinstance(result, GeneratedCharacter)
        assert is_valid_character_text(result.character)
    
    @pytest.mark.asyncio
    async def test_async_error_handling(self, generator):
        """Test error handling in async methods."""
        with pytest.raises(InvalidUniverseError):
            await generator.generate_character_async("invalid", ["detail"])
    
    def test_parameter_validation(self, generator):
        """Test parameter validation."""
        universe = "marvel"
        details = SAMPLE_DETAILS[universe]
        
        # Test invalid max_length
        with pytest.raises(Exception):  # Should be caught by model validation
            generator.generate_character(universe, details, max_length=0)
        
        # Test invalid temperature  
        with pytest.raises(Exception):
            generator.generate_character(universe, details, temperature=2.0)
    
    @patch('multiverse_character_generator.generator.pipeline')
    def test_generation_error_handling(self, mock_pipeline, generator):
        """Test handling of generation errors."""
        # Mock pipeline to raise an exception
        mock_pipeline.return_value.side_effect = Exception("Model failed")
        
        with pytest.raises(GenerationError):
            generator.generate_character("fantasia", SAMPLE_DETAILS["fantasia"])
    
    def test_empty_details_validation(self, generator):
        """Test validation of empty details."""
        universe = "terror"
        empty_details = ["", "  ", "valid", "detail"]
        
        # This should be caught by the validation in the model or generator
        with pytest.raises((InvalidDetailsError, ValueError)):
            generator.generate_character(universe, empty_details)
    
    @pytest.mark.slow
    def test_multiple_generations_consistency(self, generator):
        """Test that multiple generations work consistently."""
        universe = "anime"
        details = SAMPLE_DETAILS[universe]
        
        results = []
        for _ in range(3):
            result = generator.generate_character(universe, details)
            results.append(result)
        
        # All should be valid GeneratedCharacter objects
        for result in results:
            assert isinstance(result, GeneratedCharacter)
            assert is_valid_character_text(result.character)
        
        # Results should be different (high probability with temperature > 0)
        character_texts = [r.character for r in results]
        assert len(set(character_texts)) > 1, "Generated characters should be different"
