"""
Tests for universe-related functionality.
"""

import pytest
from multiverse_character_generator.universes import (
    get_universes,
    get_universe_info,
    create_prompt,
    get_universe_templates
)
from . import SAMPLE_UNIVERSES, SAMPLE_DETAILS


class TestUniverses:
    """Test suite for universe functionality."""
    
    def test_get_universes(self):
        """Test getting all universes."""
        universes = get_universes()
        
        assert isinstance(universes, dict)
        assert len(universes) == len(SAMPLE_UNIVERSES)
        
        for universe_name in SAMPLE_UNIVERSES:
            assert universe_name in universes
            
            universe_config = universes[universe_name]
            assert isinstance(universe_config, dict)
            assert "inputs" in universe_config
            assert "exemplos" in universe_config
            assert isinstance(universe_config["inputs"], list)
            assert isinstance(universe_config["exemplos"], list)
            assert len(universe_config["inputs"]) > 0
            assert len(universe_config["exemplos"]) > 0
    
    def test_universe_input_output_consistency(self):
        """Test that inputs and examples have consistent lengths."""
        universes = get_universes()
        
        for universe_name, config in universes.items():
            inputs = config["inputs"]
            exemplos = config["exemplos"]
            
            assert len(inputs) == len(exemplos), (
                f"Universe '{universe_name}' has mismatched inputs ({len(inputs)}) "
                f"and examples ({len(exemplos)})"
            )
    
    def test_get_universe_info_valid(self):
        """Test getting info for valid universes."""
        for universe in SAMPLE_UNIVERSES:
            info = get_universe_info(universe)
            
            assert isinstance(info, dict)
            assert "inputs" in info
            assert "exemplos" in info
            assert len(info["inputs"]) > 0
            assert len(info["exemplos"]) > 0
    
    def test_get_universe_info_invalid(self):
        """Test getting info for invalid universe."""
        with pytest.raises(KeyError) as exc_info:
            get_universe_info("nonexistent_universe")
        
        assert "nonexistent_universe" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)
    
    def test_create_prompt_valid(self):
        """Test creating prompts for all valid universes."""
        for universe in SAMPLE_UNIVERSES:
            details = SAMPLE_DETAILS[universe]
            prompt = create_prompt(universe, details)
            
            assert isinstance(prompt, str)
            assert len(prompt) > 0
            
            # Check that all details are included in the prompt
            for detail in details:
                assert detail in prompt
            
            # Check that universe-specific keywords are present
            prompt_lower = prompt.lower()
            if universe == "fantasia":
                assert any(word in prompt_lower for word in ["fantasia", "fantasy", "mágicas", "equipamento"])
            elif universe == "sci-fi":
                assert any(word in prompt_lower for word in ["ficção científica", "tecnologia", "interestelares"])
            elif universe == "terror":
                assert any(word in prompt_lower for word in ["horror", "insanidade", "entidades"])
            elif universe == "cyberpunk":
                assert any(word in prompt_lower for word in ["cyberpunk", "cibernéticas", "megacorporações"])
            elif universe == "anime":
                assert any(word in prompt_lower for word in ["anime", "power-up", "nakama"])
            elif universe == "marvel":
                assert any(word in prompt_lower for word in ["marvel", "uniforme", "herói"])
    
    def test_create_prompt_invalid_universe(self):
        """Test creating prompt for invalid universe."""
        with pytest.raises(KeyError):
            create_prompt("invalid_universe", ["detail1", "detail2"])
    
    def test_create_prompt_wrong_detail_count(self):
        """Test creating prompt with wrong number of details."""
        universe = "fantasia"
        wrong_details = ["only", "two"]  # Fantasy needs 4 details
        
        with pytest.raises(ValueError) as exc_info:
            create_prompt(universe, wrong_details)
        
        assert "Expected 4 details" in str(exc_info.value)
        assert "got 2" in str(exc_info.value)
    
    def test_get_universe_templates(self):
        """Test getting universe templates."""
        templates = get_universe_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) == len(SAMPLE_UNIVERSES)
        
        for universe in SAMPLE_UNIVERSES:
            assert universe in templates
            template = templates[universe]
            assert isinstance(template, str)
            assert len(template) > 0
            
            # Check for placeholder formatting
            assert "{0}" in template
            
            # Count placeholders to match expected detail count
            universes = get_universes()
            expected_count = len(universes[universe]["inputs"])
            for i in range(expected_count):
                assert f"{{{i}}}" in template
    
    def test_template_formatting(self):
        """Test that templates format correctly with details."""
        templates = get_universe_templates()
        
        for universe in SAMPLE_UNIVERSES:
            template = templates[universe]
            details = SAMPLE_DETAILS[universe]
            
            try:
                formatted = template.format(*details)
                assert isinstance(formatted, str)
                assert len(formatted) > len(template)  # Should be longer after formatting
                
                # Original placeholders should be replaced
                for i in range(len(details)):
                    assert f"{{{i}}}" not in formatted
                
                # Details should be present in formatted text
                for detail in details:
                    assert detail in formatted
                    
            except (IndexError, KeyError) as e:
                pytest.fail(f"Template formatting failed for {universe}: {e}")
    
    def test_universe_specific_content(self):
        """Test that universe prompts contain appropriate content."""
        test_cases = [
            ("fantasia", ["magia", "equipamento", "segredo"]),
            ("sci-fi", ["tecnologia", "interestelares", "planeta"]),
            ("terror", ["insanidade", "entidades", "horror"]),
            ("cyberpunk", ["cibernéticas", "corporações", "netrunner"]),
            ("anime", ["transformação", "poder", "nakama"]),
            ("marvel", ["uniforme", "herói", "vilão"])
        ]
        
        for universe, expected_keywords in test_cases:
            details = SAMPLE_DETAILS[universe]
            prompt = create_prompt(universe, details)
            prompt_lower = prompt.lower()
            
            # At least one expected keyword should be present
            found_keywords = [kw for kw in expected_keywords if kw in prompt_lower]
            assert len(found_keywords) > 0, (
                f"Universe '{universe}' prompt should contain at least one of {expected_keywords}, "
                f"but none were found in: {prompt[:100]}..."
            )
    
    def test_prompt_structure(self):
        """Test that prompts have consistent structure."""
        for universe in SAMPLE_UNIVERSES:
            details = SAMPLE_DETAILS[universe]
            prompt = create_prompt(universe, details)
            
            # Should contain character details
            for detail in details:
                assert detail in prompt
            
            # Should contain formatting like colons and newlines
            assert ":" in prompt
            assert "\n" in prompt
            
            # Should be reasonably long (detailed prompt)
            assert len(prompt) > 100
    
    def test_detail_preservation(self):
        """Test that all provided details are preserved in prompts."""
        for universe in SAMPLE_UNIVERSES:
            details = SAMPLE_DETAILS[universe]
            prompt = create_prompt(universe, details)
            
            for i, detail in enumerate(details):
                assert detail in prompt, (
                    f"Detail '{detail}' (index {i}) not found in prompt for universe '{universe}'"
                )
    
    def test_prompt_uniqueness(self):
        """Test that different universes produce different prompts."""
        prompts = {}
        base_details = ["Test", "Character", "Details", "Here"]
        
        for universe in SAMPLE_UNIVERSES:
            # Use the correct number of details for each universe
            universes = get_universes()
            required_count = len(universes[universe]["inputs"])
            universe_details = base_details[:required_count]
            
            if len(universe_details) < required_count:
                # Pad with additional generic details if needed
                universe_details.extend([f"Extra{i}" for i in range(required_count - len(universe_details))])
            
            prompts[universe] = create_prompt(universe, universe_details)
        
        # All prompts should be different
        prompt_values = list(prompts.values())
        unique_prompts = set(prompt_values)
        
        assert len(unique_prompts) == len(prompt_values), (
            "All universe prompts should be unique"
        )
