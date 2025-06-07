"""
Pydantic models for data validation and type safety.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class CharacterDetails(BaseModel):
    """
    Model for character generation input details.
    """
    details: List[str] = Field(
        ...,
        description="List of character details matching universe requirements",
        min_items=1,
        max_items=10
    )
    universe: str = Field(
        ...,
        description="The fictional universe for character generation"
    )
    
    @validator('universe')
    def universe_must_be_lowercase(cls, v):
        """Ensure universe name is lowercase for consistency."""
        return v.lower()
    
    @validator('details')
    def details_must_not_be_empty(cls, v):
        """Ensure all details are non-empty strings."""
        for detail in v:
            if not detail or not detail.strip():
                raise ValueError("Character details cannot be empty")
        return [detail.strip() for detail in v]


class GeneratedCharacter(BaseModel):
    """
    Model for generated character output.
    """
    character: str = Field(
        ...,
        description="The generated character text"
    )
    filename: Optional[str] = Field(
        None,
        description="Filename if character was saved to file"
    )
    
    @validator('character')
    def character_must_not_be_empty(cls, v):
        """Ensure generated character is not empty."""
        if not v or not v.strip():
            raise ValueError("Generated character cannot be empty")
        return v


class UniverseInfo(BaseModel):
    """
    Model for universe configuration information.
    """
    inputs: List[str] = Field(
        ...,
        description="Required input fields for this universe"
    )
    exemplos: List[str] = Field(
        ...,
        description="Example values for quick generation"
    )
    
    @validator('inputs', 'exemplos')
    def lists_must_not_be_empty(cls, v):
        """Ensure lists are not empty."""
        if not v:
            raise ValueError("Universe configuration lists cannot be empty")
        return v


class GenerationConfig(BaseModel):
    """
    Model for text generation configuration parameters.
    """
    max_length: int = Field(
        350,
        description="Maximum length of generated text",
        ge=50,
        le=1000
    )
    temperature: float = Field(
        0.85,
        description="Sampling temperature (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )
    top_p: float = Field(
        0.92,
        description="Nucleus sampling parameter",
        ge=0.0,
        le=1.0
    )
    repetition_penalty: float = Field(
        1.2,
        description="Penalty for repetition",
        ge=1.0,
        le=2.0
    )
    save_to_file: bool = Field(
        False,
        description="Whether to save generated character to file"
    )
    output_dir: Optional[str] = Field(
        None,
        description="Directory to save files"
    )


class ModelInfo(BaseModel):
    """
    Model for information about the loaded model.
    """
    model_name: str = Field(
        ...,
        description="Name of the GPT-2 model"
    )
    using_gpu: bool = Field(
        ...,
        description="Whether GPU is being used"
    )
    cache_dir: Optional[str] = Field(
        None,
        description="Model cache directory"
    )
    device: str = Field(
        ...,
        description="Device the model is running on"
    )


class BatchGenerationRequest(BaseModel):
    """
    Model for batch character generation requests.
    """
    requests: List[CharacterDetails] = Field(
        ...,
        description="List of character generation requests",
        min_items=1,
        max_items=10
    )
    config: Optional[GenerationConfig] = Field(
        None,
        description="Generation configuration to apply to all requests"
    )


class BatchGenerationResponse(BaseModel):
    """
    Model for batch character generation responses.
    """
    characters: List[GeneratedCharacter] = Field(
        ...,
        description="List of generated characters"
    )
    success_count: int = Field(
        ...,
        description="Number of successful generations"
    )
    error_count: int = Field(
        ...,
        description="Number of failed generations"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="List of error messages for failed generations"
    )
