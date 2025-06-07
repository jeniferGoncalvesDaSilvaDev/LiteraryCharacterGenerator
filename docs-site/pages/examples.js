import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { tomorrow } from 'react-syntax-highlighter/dist/cjs/styles/prism'
import Link from 'next/link'

export default function Examples() {
  return (
    <>
      <header className="header">
        <div className="container">
          <nav className="nav">
            <Link href="/">
              <h1>Multiverse Character Generator</h1>
            </Link>
            <ul className="nav-links">
              <li><Link href="/" className="nav-link">Home</Link></li>
              <li><Link href="/tutorial" className="nav-link">Tutorial</Link></li>
              <li><Link href="/api" className="nav-link">API</Link></li>
              <li><Link href="/examples" className="nav-link">Examples</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <div className="container" style={{ padding: '2rem 1rem' }}>
        <h1 style={{ color: 'var(--dark-bg)', marginBottom: '2rem' }}>Advanced Examples</h1>

        <section className="section">
          <h2 className="section-title">Web Application Integration</h2>
          
          <div className="card">
            <h3 className="card-title">Flask REST API</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from multiverse_character_generator import (
    MultiverseCharacterGenerator,
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError
)
import asyncio
import logging

app = Flask(__name__)
CORS(app)

# Initialize generator once at startup
generator = MultiverseCharacterGenerator(
    model_name="gpt2-medium",
    use_gpu=True,
    cache_dir="./model_cache"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html', universes=generator.list_universes())

@app.route('/api/universes', methods=['GET'])
def get_universes():
    """Get all available universes with their requirements."""
    universes = {}
    for universe in generator.list_universes():
        universes[universe] = generator.get_universe_info(universe)
    return jsonify(universes)

@app.route('/api/generate', methods=['POST'])
def generate_character():
    """Generate a character with custom or quick generation."""
    try:
        data = request.get_json()
        
        if not data or 'universe' not in data:
            return jsonify({'error': 'Universe is required'}), 400
        
        universe = data['universe'].lower()
        details = data.get('details')
        
        # Generation parameters with defaults
        params = {
            'max_length': data.get('max_length', 350),
            'temperature': data.get('temperature', 0.85),
            'top_p': data.get('top_p', 0.92),
            'repetition_penalty': data.get('repetition_penalty', 1.2),
            'save_to_file': data.get('save_to_file', False),
            'output_dir': data.get('output_dir', './characters')
        }
        
        # Generate character
        if details and len(details) > 0:
            character = generator.generate_character(
                universe=universe,
                details=details,
                **params
            )
        else:
            character = generator.quick_generate(
                universe=universe,
                **params
            )
        
        logger.info(f"Generated character for universe: {universe}")
        
        return jsonify({
            'success': True,
            'character': character.character,
            'filename': character.filename,
            'universe': universe,
            'generation_params': params
        })
        
    except InvalidUniverseError as e:
        return jsonify({
            'error': f'Invalid universe: {e.universe}',
            'available_universes': e.available_universes
        }), 400
        
    except InvalidDetailsError as e:
        return jsonify({
            'error': f'Invalid details for {e.universe}',
            'expected_count': e.expected_count,
            'actual_count': e.actual_count,
            'required_fields': e.required_fields
        }), 400
        
    except GenerationError as e:
        logger.error(f"Generation error: {e}")
        return jsonify({'error': 'Character generation failed'}), 500
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/batch-generate', methods=['POST'])
def batch_generate():
    """Generate multiple characters concurrently."""
    try:
        data = request.get_json()
        requests = data.get('requests', [])
        
        if not requests:
            return jsonify({'error': 'No generation requests provided'}), 400
        
        if len(requests) > 10:
            return jsonify({'error': 'Maximum 10 concurrent requests allowed'}), 400
        
        async def generate_batch():
            tasks = []
            for req in requests:
                universe = req['universe']
                details = req.get('details')
                
                if details:
                    task = generator.generate_character_async(
                        universe=universe,
                        details=details,
                        max_length=req.get('max_length', 350),
                        temperature=req.get('temperature', 0.85)
                    )
                else:
                    task = generator.quick_generate_async(
                        universe=universe,
                        max_length=req.get('max_length', 350),
                        temperature=req.get('temperature', 0.85)
                    )
                
                tasks.append(task)
            
            return await asyncio.gather(*tasks, return_exceptions=True)
        
        # Run async batch generation
        results = asyncio.run(generate_batch())
        
        characters = []
        errors = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append({
                    'request_index': i,
                    'error': str(result)
                })
            else:
                characters.append({
                    'character': result.character,
                    'filename': result.filename,
                    'request_index': i
                })
        
        return jsonify({
            'success': True,
            'characters': characters,
            'errors': errors,
            'success_count': len(characters),
            'error_count': len(errors)
        })
        
    except Exception as e:
        logger.error(f"Batch generation error: {e}")
        return jsonify({'error': 'Batch generation failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)`}
            </SyntaxHighlighter>
          </div>

          <div className="card">
            <h3 className="card-title">FastAPI with Async Support</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from multiverse_character_generator import (
    MultiverseCharacterGenerator,
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError
)
import logging

app = FastAPI(
    title="Multiverse Character Generator API",
    description="Generate fictional characters across multiple universes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generator
generator = MultiverseCharacterGenerator(
    model_name="gpt2-medium",
    use_gpu=True
)

# Request/Response models
class GenerationRequest(BaseModel):
    universe: str = Field(..., description="Target universe")
    details: Optional[List[str]] = Field(None, description="Character details")
    max_length: int = Field(350, ge=50, le=1000, description="Maximum text length")
    temperature: float = Field(0.85, ge=0.0, le=1.0, description="Creativity level")
    top_p: float = Field(0.92, ge=0.0, le=1.0, description="Vocabulary diversity")
    repetition_penalty: float = Field(1.2, ge=1.0, le=2.0, description="Repetition control")
    save_to_file: bool = Field(False, description="Save to file")
    output_dir: Optional[str] = Field(None, description="Output directory")

class BatchGenerationRequest(BaseModel):
    requests: List[GenerationRequest] = Field(..., max_items=10)

class CharacterResponse(BaseModel):
    character: str
    filename: Optional[str]
    universe: str
    generation_params: Dict[str, Any]

class BatchResponse(BaseModel):
    characters: List[CharacterResponse]
    errors: List[Dict[str, Any]]
    success_count: int
    error_count: int

@app.get("/")
async def root():
    return {
        "message": "Multiverse Character Generator API",
        "version": "1.0.0",
        "universes": generator.list_universes(),
        "docs": "/docs"
    }

@app.get("/universes")
async def get_universes():
    """Get all available universes with their requirements."""
    universes = {}
    for universe in generator.list_universes():
        universes[universe] = generator.get_universe_info(universe)
    return universes

@app.post("/generate", response_model=CharacterResponse)
async def generate_character(request: GenerationRequest):
    """Generate a single character."""
    try:
        params = {
            'max_length': request.max_length,
            'temperature': request.temperature,
            'top_p': request.top_p,
            'repetition_penalty': request.repetition_penalty,
            'save_to_file': request.save_to_file,
            'output_dir': request.output_dir
        }
        
        if request.details:
            character = await generator.generate_character_async(
                universe=request.universe,
                details=request.details,
                **params
            )
        else:
            character = await generator.quick_generate_async(
                universe=request.universe,
                **params
            )
        
        return CharacterResponse(
            character=character.character,
            filename=character.filename,
            universe=request.universe,
            generation_params=params
        )
        
    except InvalidUniverseError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Invalid universe: {e.universe}",
                "available_universes": e.available_universes
            }
        )
    except InvalidDetailsError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Invalid details for {e.universe}",
                "expected_count": e.expected_count,
                "actual_count": e.actual_count,
                "required_fields": e.required_fields
            }
        )
    except GenerationError as e:
        raise HTTPException(status_code=500, detail={"error": "Generation failed"})

@app.post("/batch-generate", response_model=BatchResponse)
async def batch_generate(request: BatchGenerationRequest):
    """Generate multiple characters concurrently."""
    tasks = []
    
    for req in request.requests:
        if req.details:
            task = generator.generate_character_async(
                universe=req.universe,
                details=req.details,
                max_length=req.max_length,
                temperature=req.temperature,
                top_p=req.top_p,
                repetition_penalty=req.repetition_penalty
            )
        else:
            task = generator.quick_generate_async(
                universe=req.universe,
                max_length=req.max_length,
                temperature=req.temperature
            )
        
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    characters = []
    errors = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            errors.append({
                "request_index": i,
                "error": str(result)
            })
        else:
            characters.append(CharacterResponse(
                character=result.character,
                filename=result.filename,
                universe=request.requests[i].universe,
                generation_params={}
            ))
    
    return BatchResponse(
        characters=characters,
        errors=errors,
        success_count=len(characters),
        error_count=len(errors)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)`}
            </SyntaxHighlighter>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Gaming Applications</h2>
          
          <div className="card">
            <h3 className="card-title">RPG Character Generator System</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`import random
from typing import Dict, List, Tuple
from multiverse_character_generator import MultiverseCharacterGenerator
from dataclasses import dataclass

@dataclass
class RPGCharacter:
    name: str
    background: str
    stats: Dict[str, int]
    equipment: List[str]
    universe: str

class RPGCharacterSystem:
    def __init__(self):
        self.generator = MultiverseCharacterGenerator()
        
        # Character name lists by universe
        self.name_pools = {
            "fantasy": ["Aragorn", "Legolas", "Gimli", "Elara", "Thorin", "Galadriel"],
            "sci-fi": ["Zara", "Kai", "Nova", "Orion", "Luna", "Phoenix"],
            "cyberpunk": ["Ghost", "Neon", "Razor", "Chrome", "Pulse", "Viper"],
            "horror": ["Salem", "Raven", "Ash", "Shade", "Morrigan", "Dante"],
            "anime": ["Akira", "Yuki", "Hana", "Rei", "Sora", "Kira"],
            "marvel": ["Stormbreaker", "Quantum", "Echo", "Vortex", "Nexus", "Phoenix"]
        }
        
        # Equipment by universe
        self.equipment_pools = {
            "fantasy": ["Enchanted Sword", "Magic Staff", "Healing Potion", "Shield"],
            "sci-fi": ["Plasma Rifle", "Energy Shield", "Med Kit", "Jetpack"],
            "cyberpunk": ["Neural Implant", "Smart Gun", "Hacking Deck", "Armor Plating"],
            "horror": ["Blessed Amulet", "Silver Dagger", "Holy Water", "Protective Ward"],
            "anime": ["Mystic Blade", "Spirit Orb", "Transformation Device", "Sacred Scroll"],
            "marvel": ["Vibranium Shield", "Arc Reactor", "Web Shooters", "Utility Belt"]
        }
    
    def generate_stats(self, universe: str) -> Dict[str, int]:
        """Generate random stats based on universe."""
        if universe == "fantasy":
            return {
                "Strength": random.randint(8, 18),
                "Dexterity": random.randint(8, 18),
                "Intelligence": random.randint(8, 18),
                "Wisdom": random.randint(8, 18),
                "Constitution": random.randint(8, 18),
                "Charisma": random.randint(8, 18)
            }
        elif universe == "sci-fi":
            return {
                "Technology": random.randint(10, 20),
                "Combat": random.randint(8, 18),
                "Diplomacy": random.randint(8, 18),
                "Science": random.randint(10, 20),
                "Piloting": random.randint(8, 18)
            }
        elif universe == "cyberpunk":
            return {
                "Hacking": random.randint(10, 20),
                "Combat": random.randint(8, 18),
                "Stealth": random.randint(10, 18),
                "Technology": random.randint(12, 20),
                "Street Smarts": random.randint(10, 18)
            }
        # Add more universe-specific stats...
        else:
            return {"Power": random.randint(10, 20), "Skill": random.randint(8, 18)}
    
    def create_full_character(self, universe: str, custom_details: List[str] = None) -> RPGCharacter:
        """Create a complete RPG character with stats and equipment."""
        
        # Generate character background
        if custom_details:
            character_data = self.generator.generate_character(
                universe=universe,
                details=custom_details,
                temperature=0.8,
                max_length=300
            )
        else:
            character_data = self.generator.quick_generate(
                universe=universe,
                temperature=0.8,
                max_length=300
            )
        
        # Generate name, stats, and equipment
        name = random.choice(self.name_pools.get(universe, ["Unknown"]))
        stats = self.generate_stats(universe)
        equipment = random.sample(
            self.equipment_pools.get(universe, ["Basic Equipment"]), 
            k=min(3, len(self.equipment_pools.get(universe, [])))
        )
        
        return RPGCharacter(
            name=name,
            background=character_data.character,
            stats=stats,
            equipment=equipment,
            universe=universe
        )
    
    def create_party(self, universe: str, party_size: int = 4) -> List[RPGCharacter]:
        """Create a balanced party of characters."""
        party = []
        
        # Define roles for balanced party
        if universe == "fantasy":
            roles = [
                ["Human", "Warrior", "Lawful Good", "Gondor"],
                ["Elf", "Mage", "Chaotic Good", "Rivendell"],
                ["Dwarf", "Cleric", "Lawful Good", "Moria"],
                ["Halfling", "Rogue", "Chaotic Neutral", "Shire"]
            ]
        elif universe == "sci-fi":
            roles = [
                ["Human", "Captain", "Federation", "Earth"],
                ["Android", "Engineer", "Federation", "Mars"],
                ["Alien", "Diplomat", "Alliance", "Proxima B"],
                ["Cyborg", "Pilot", "Independent", "Station Alpha"]
            ]
        # Add more universe-specific party compositions...
        
        for i in range(min(party_size, len(roles) if 'roles' in locals() else party_size)):
            if 'roles' in locals() and i < len(roles):
                character = self.create_full_character(universe, roles[i])
            else:
                character = self.create_full_character(universe)
            party.append(character)
        
        return party
    
    def export_character_sheet(self, character: RPGCharacter) -> str:
        """Export character as formatted character sheet."""
        sheet = f"""
========================================
CHARACTER SHEET - {character.universe.upper()}
========================================

NAME: {character.name}
UNIVERSE: {character.universe}

BACKGROUND:
{character.background}

STATISTICS:
"""
        for stat, value in character.stats.items():
            sheet += f"  {stat}: {value}\\n"
        
        sheet += f"\\nEQUIPMENT:\\n"
        for item in character.equipment:
            sheet += f"  • {item}\\n"
        
        sheet += "\\n========================================"
        return sheet

# Usage example
def main():
    rpg_system = RPGCharacterSystem()
    
    # Create a single character
    character = rpg_system.create_full_character("fantasy")
    print(rpg_system.export_character_sheet(character))
    
    # Create a balanced party
    party = rpg_system.create_party("sci-fi", 4)
    print(f"\\nGenerated party of {len(party)} characters:")
    for char in party:
        print(f"- {char.name} ({char.universe})")

if __name__ == "__main__":
    main()`}
            </SyntaxHighlighter>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Creative Writing Tools</h2>
          
          <div className="card">
            <h3 className="card-title">Story Generator with Character Integration</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`import asyncio
from typing import List, Dict, Any
from multiverse_character_generator import MultiverseCharacterGenerator

class StoryGenerator:
    def __init__(self):
        self.generator = MultiverseCharacterGenerator()
        
        # Story templates by universe
        self.story_templates = {
            "fantasy": [
                "The ancient prophecy speaks of {character_count} heroes who must {quest_goal}.",
                "In the realm of {setting}, {character_count} unlikely allies discover {mystery}.",
                "When darkness threatens {setting}, {character_count} champions rise to {quest_goal}."
            ],
            "sci-fi": [
                "The year is 2387, and {character_count} crew members aboard {setting} face {crisis}.",
                "On the distant planet {setting}, {character_count} colonists uncover {mystery}.",
                "When alien forces threaten {setting}, {character_count} unlikely heroes must {quest_goal}."
            ],
            "horror": [
                "In the cursed town of {setting}, {character_count} survivors confront {horror_element}.",
                "The old mansion holds {mystery}, and {character_count} investigators dare to uncover the truth.",
                "When {horror_element} awakens in {setting}, {character_count} souls fight for survival."
            ]
        }
        
        # Story elements by universe
        self.story_elements = {
            "fantasy": {
                "quest_goals": ["unite the kingdoms", "defeat the ancient evil", "find the lost artifact"],
                "mysteries": ["a forgotten magic", "the secret of the old gods", "a portal to other realms"],
                "settings": ["Eldoria", "the Forbidden Forest", "the Crystal Caves"]
            },
            "sci-fi": {
                "quest_goals": ["save the galaxy", "prevent the AI uprising", "find the lost colony"],
                "mysteries": ["an alien artifact", "the secret of faster-than-light travel", "a time anomaly"],
                "crises": ["system failure", "alien invasion", "space-time rift"],
                "settings": ["the starship Endeavor", "Mars Colony Beta", "Station Omega"]
            },
            "horror": {
                "horror_elements": ["the ancient curse", "the vengeful spirit", "the eldritch horror"],
                "mysteries": ["the family secret", "the forbidden ritual", "the sealed chamber"],
                "settings": ["Ravenshollow", "the Blackwood Estate", "St. Mary's Asylum"]
            }
        }
    
    async def generate_story_with_characters(
        self, 
        universe: str, 
        character_count: int = 3,
        story_length: int = 500
    ) -> Dict[str, Any]:
        """Generate a complete story with characters."""
        
        # Generate characters concurrently
        character_tasks = [
            self.generator.quick_generate_async(
                universe=universe,
                max_length=200,
                temperature=0.8
            ) for _ in range(character_count)
        ]
        
        characters = await asyncio.gather(*character_tasks)
        
        # Select story template and elements
        import random
        template = random.choice(self.story_templates.get(universe, []))
        elements = self.story_elements.get(universe, {})
        
        # Generate story context
        story_context = {}
        for key, values in elements.items():
            if values:
                story_context[key] = random.choice(values)
        
        story_context['character_count'] = character_count
        
        # Create story outline
        story_intro = template.format(**story_context)
        
        # Generate detailed story
        story_prompt = f"{story_intro}\\n\\nThe characters in this story are:\\n"
        for i, char in enumerate(characters, 1):
            story_prompt += f"Character {i}: {char.character[:100]}...\\n"
        
        story_prompt += "\\nContinue this story with these characters:"
        
        # Generate main story
        story_result = await self.generator._generate_text(
            prompt=story_prompt,
            max_length=story_length,
            temperature=0.85,
            top_p=0.92,
            repetition_penalty=1.2
        )
        
        return {
            "universe": universe,
            "story_intro": story_intro,
            "characters": [char.character for char in characters],
            "full_story": story_result,
            "story_elements": story_context
        }
    
    def format_story_output(self, story_data: Dict[str, Any]) -> str:
        """Format story for readable output."""
        output = f"""
========================================
GENERATED STORY - {story_data['universe'].upper()}
========================================

{story_data['story_intro']}

CHARACTERS:
"""
        for i, character in enumerate(story_data['characters'], 1):
            output += f"\\n{i}. {character}\\n"
        
        output += f"""
STORY:
{story_data['full_story']}

========================================
Story Elements Used: {story_data['story_elements']}
========================================
"""
        return output

# Advanced writing assistant
class WritingAssistant:
    def __init__(self):
        self.story_gen = StoryGenerator()
        self.generator = MultiverseCharacterGenerator()
    
    async def generate_writing_prompt(self, universe: str, prompt_type: str = "character") -> str:
        """Generate writing prompts with characters."""
        
        if prompt_type == "character":
            character = await self.generator.quick_generate_async(
                universe=universe,
                temperature=0.9,
                max_length=150
            )
            
            prompts = [
                f"Write about what happens when {character.character[:50]}... faces their greatest fear.",
                f"Describe a typical day in the life of {character.character[:50]}...",
                f"What secret is {character.character[:50]}... hiding from their companions?"
            ]
            
            import random
            return random.choice(prompts)
        
        elif prompt_type == "conflict":
            char1 = await self.generator.quick_generate_async(universe, temperature=0.8)
            char2 = await self.generator.quick_generate_async(universe, temperature=0.8)
            
            return f"Write a scene where these two characters meet:\\n\\nCharacter A: {char1.character[:100]}...\\n\\nCharacter B: {char2.character[:100]}...\\n\\nWhat conflict arises between them?"
        
        elif prompt_type == "world-building":
            setting_char = await self.generator.quick_generate_async(universe, temperature=0.7)
            return f"Using this character as inspiration: {setting_char.character[:100]}..., describe the world they inhabit. What makes this place unique?"
    
    async def character_development_exercise(self, universe: str) -> Dict[str, str]:
        """Generate character development exercises."""
        character = await self.generator.quick_generate_async(
            universe=universe,
            temperature=0.8,
            max_length=200
        )
        
        exercises = {
            "backstory": f"Expand on this character's past: {character.character}",
            "dialogue": f"Write a conversation where this character reveals something important about themselves: {character.character[:100]}...",
            "internal_conflict": f"What internal struggle does this character face? {character.character[:100]}...",
            "character_arc": f"How does this character change throughout their story? {character.character[:100]}...",
            "relationships": f"Describe this character's relationship with their closest ally and their greatest enemy: {character.character[:100]}..."
        }
        
        return exercises

# Usage example
async def main():
    story_gen = StoryGenerator()
    writing_assistant = WritingAssistant()
    
    # Generate a complete story
    story = await story_gen.generate_story_with_characters("fantasy", 3, 400)
    print(story_gen.format_story_output(story))
    
    # Generate writing prompts
    prompt = await writing_assistant.generate_writing_prompt("sci-fi", "character")
    print(f"\\nWriting Prompt: {prompt}")
    
    # Character development exercises
    exercises = await writing_assistant.character_development_exercise("horror")
    print("\\nCharacter Development Exercises:")
    for exercise_type, exercise in exercises.items():
        print(f"\\n{exercise_type.title()}: {exercise}")

if __name__ == "__main__":
    asyncio.run(main())`}
            </SyntaxHighlighter>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Performance and Optimization</h2>
          
          <div className="card">
            <h3 className="card-title">Caching and Performance System</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`import asyncio
import hashlib
import json
import pickle
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from multiverse_character_generator import MultiverseCharacterGenerator

class PerformanceOptimizedGenerator:
    def __init__(self, cache_dir: str = "./character_cache"):
        self.generator = MultiverseCharacterGenerator(
            model_name="gpt2-medium",
            use_gpu=True,
            cache_dir="./model_cache"
        )
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # In-memory cache for frequently used results
        self.memory_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "disk_hits": 0,
            "generations": 0
        }
        
        # Performance tracking
        self.generation_times = []
        self.batch_sizes = []
    
    def _generate_cache_key(self, universe: str, details: List[str] = None, **params) -> str:
        """Generate a unique cache key for the request."""
        cache_data = {
            "universe": universe,
            "details": details,
            "params": {k: v for k, v in params.items() if k in [
                'max_length', 'temperature', 'top_p', 'repetition_penalty'
            ]}
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _load_from_disk_cache(self, cache_key: str) -> Optional[Any]:
        """Load result from disk cache."""
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                # Check if cache is still fresh (24 hours)
                if time.time() - cached_data['timestamp'] < 86400:
                    self.cache_stats["disk_hits"] += 1
                    return cached_data['result']
                else:
                    cache_file.unlink()  # Remove expired cache
            except Exception:
                pass
        
        return None
    
    def _save_to_disk_cache(self, cache_key: str, result: Any) -> None:
        """Save result to disk cache."""
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        cached_data = {
            'result': result,
            'timestamp': time.time()
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cached_data, f)
        except Exception:
            pass  # Fail silently if caching doesn't work
    
    async def generate_character_cached(
        self,
        universe: str,
        details: List[str] = None,
        use_cache: bool = True,
        **params
    ) -> Any:
        """Generate character with caching support."""
        
        if use_cache:
            cache_key = self._generate_cache_key(universe, details, **params)
            
            # Check memory cache first
            if cache_key in self.memory_cache:
                self.cache_stats["hits"] += 1
                return self.memory_cache[cache_key]
            
            # Check disk cache
            cached_result = self._load_from_disk_cache(cache_key)
            if cached_result:
                self.memory_cache[cache_key] = cached_result
                return cached_result
        
        # Generate new character
        start_time = time.time()
        
        if details:
            result = await self.generator.generate_character_async(
                universe=universe,
                details=details,
                **params
            )
        else:
            result = await self.generator.quick_generate_async(
                universe=universe,
                **params
            )
        
        generation_time = time.time() - start_time
        self.generation_times.append(generation_time)
        self.cache_stats["generations"] += 1
        self.cache_stats["misses"] += 1
        
        # Cache the result
        if use_cache:
            cache_key = self._generate_cache_key(universe, details, **params)
            self.memory_cache[cache_key] = result
            self._save_to_disk_cache(cache_key, result)
        
        return result
    
    async def batch_generate_optimized(
        self,
        requests: List[Dict[str, Any]],
        max_concurrent: int = 5,
        use_cache: bool = True
    ) -> List[Any]:
        """Optimized batch generation with concurrency control."""
        
        start_time = time.time()
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def generate_with_semaphore(request):
            async with semaphore:
                return await self.generate_character_cached(
                    universe=request['universe'],
                    details=request.get('details'),
                    use_cache=use_cache,
                    **{k: v for k, v in request.items() if k not in ['universe', 'details']}
                )
        
        tasks = [generate_with_semaphore(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        batch_time = time.time() - start_time
        self.batch_sizes.append(len(requests))
        
        print(f"Batch of {len(requests)} completed in {batch_time:.2f}s")
        return results
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get detailed performance statistics."""
        cache_hit_rate = (
            self.cache_stats["hits"] / 
            (self.cache_stats["hits"] + self.cache_stats["misses"])
            if (self.cache_stats["hits"] + self.cache_stats["misses"]) > 0 else 0
        )
        
        avg_generation_time = (
            sum(self.generation_times) / len(self.generation_times)
            if self.generation_times else 0
        )
        
        return {
            "cache_stats": self.cache_stats,
            "cache_hit_rate": f"{cache_hit_rate:.2%}",
            "average_generation_time": f"{avg_generation_time:.2f}s",
            "total_generations": len(self.generation_times),
            "memory_cache_size": len(self.memory_cache),
            "disk_cache_files": len(list(self.cache_dir.glob("*.pkl")))
        }
    
    def clear_cache(self, memory_only: bool = False) -> None:
        """Clear the cache."""
        self.memory_cache.clear()
        
        if not memory_only:
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
    
    def pregenerate_common_characters(self, universes: List[str], count_per_universe: int = 10) -> None:
        """Pre-generate common characters for better response times."""
        
        async def pregenerate():
            tasks = []
            
            for universe in universes:
                for _ in range(count_per_universe):
                    tasks.append(
                        self.generate_character_cached(
                            universe=universe,
                            use_cache=True,
                            temperature=0.85
                        )
                    )
            
            await asyncio.gather(*tasks)
            print(f"Pre-generated {len(tasks)} characters")
        
        asyncio.run(pregenerate())

# Load testing utility
class LoadTester:
    def __init__(self, generator: PerformanceOptimizedGenerator):
        self.generator = generator
    
    async def run_load_test(
        self,
        concurrent_users: int = 10,
        requests_per_user: int = 5,
        universes: List[str] = None
    ) -> Dict[str, Any]:
        """Simulate concurrent load on the generator."""
        
        if not universes:
            universes = ["fantasy", "sci-fi", "horror"]
        
        start_time = time.time()
        
        async def simulate_user():
            user_start = time.time()
            results = []
            
            for _ in range(requests_per_user):
                universe = random.choice(universes)
                try:
                    result = await self.generator.generate_character_cached(
                        universe=universe,
                        temperature=random.uniform(0.7, 0.9),
                        max_length=random.randint(200, 400)
                    )
                    results.append(True)
                except Exception as e:
                    results.append(False)
                
                # Random delay between requests
                await asyncio.sleep(random.uniform(0.1, 0.5))
            
            user_time = time.time() - user_start
            return {
                "success_rate": sum(results) / len(results),
                "total_time": user_time,
                "requests": len(results)
            }
        
        # Run concurrent users
        user_tasks = [simulate_user() for _ in range(concurrent_users)]
        user_results = await asyncio.gather(*user_tasks)
        
        total_time = time.time() - start_time
        
        # Calculate statistics
        total_requests = sum(r["requests"] for r in user_results)
        avg_success_rate = sum(r["success_rate"] for r in user_results) / len(user_results)
        requests_per_second = total_requests / total_time
        
        return {
            "concurrent_users": concurrent_users,
            "total_requests": total_requests,
            "total_time": f"{total_time:.2f}s",
            "requests_per_second": f"{requests_per_second:.2f}",
            "average_success_rate": f"{avg_success_rate:.2%}",
            "performance_stats": self.generator.get_performance_stats()
        }

# Usage example
async def main():
    import random
    
    # Initialize optimized generator
    opt_gen = PerformanceOptimizedGenerator()
    
    # Pre-generate some common characters
    print("Pre-generating common characters...")
    opt_gen.pregenerate_common_characters(["fantasy", "sci-fi"], 5)
    
    # Test caching performance
    print("\\nTesting cache performance...")
    
    # Generate same character multiple times (should hit cache)
    for i in range(3):
        start = time.time()
        char = await opt_gen.generate_character_cached(
            universe="fantasy",
            details=["Elf", "Mage", "Chaotic Good", "Rivendell"]
        )
        end = time.time()
        print(f"Generation {i+1}: {end-start:.3f}s")
    
    # Performance statistics
    stats = opt_gen.get_performance_stats()
    print(f"\\nPerformance Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Load testing
    print("\\nRunning load test...")
    load_tester = LoadTester(opt_gen)
    load_results = await load_tester.run_load_test(
        concurrent_users=5,
        requests_per_user=3
    )
    
    print("Load Test Results:")
    for key, value in load_results.items():
        if key != "performance_stats":
            print(f"  {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())`}
            </SyntaxHighlighter>
          </div>
        </section>

        <div style={{ marginTop: '3rem', padding: '2rem', background: '#f8fafc', borderRadius: '0.5rem' }}>
          <h2 style={{ color: 'var(--dark-bg)', marginBottom: '1rem' }}>More Resources</h2>
          <p style={{ marginBottom: '1.5rem' }}>
            These examples demonstrate advanced usage patterns for the Multiverse Character Generator. 
            Explore the complete API documentation and tutorial for more implementation details.
          </p>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <Link href="/api" className="btn btn-primary">
              API Reference
            </Link>
            <Link href="/tutorial" className="btn btn-secondary">
              Complete Tutorial
            </Link>
            <a href="https://github.com/your-username/multiverse-character-generator" className="btn btn-secondary">
              GitHub Repository
            </a>
          </div>
        </div>
      </div>

      <footer className="footer">
        <div className="container">
          <div className="footer-links">
            <a href="https://github.com/your-username/multiverse-character-generator" className="footer-link">GitHub</a>
            <a href="https://pypi.org/project/multiverse-character-generator/" className="footer-link">PyPI</a>
            <Link href="/tutorial" className="footer-link">Documentation</Link>
          </div>
          <p>&copy; 2024 Multiverse Character Generator. Licensed under MIT License.</p>
        </div>
      </footer>
    </>
  )
}