import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { tomorrow } from 'react-syntax-highlighter/dist/cjs/styles/prism'
import Link from 'next/link'

export default function Tutorial() {
  const [activeSection, setActiveSection] = useState('installation')

  const sections = [
    { id: 'installation', title: 'Installation' },
    { id: 'basic-usage', title: 'Basic Usage' },
    { id: 'universes', title: 'Understanding Universes' },
    { id: 'custom-details', title: 'Custom Character Details' },
    { id: 'parameters', title: 'Generation Parameters' },
    { id: 'async-usage', title: 'Async Generation' },
    { id: 'file-operations', title: 'File Operations' },
    { id: 'error-handling', title: 'Error Handling' },
    { id: 'performance', title: 'Performance Tips' },
    { id: 'web-integration', title: 'Web Framework Integration' }
  ]

  const codeExamples = {
    installation: `# Install the library
pip install multiverse-character-generator

# Or install from source
git clone https://github.com/your-username/multiverse-character-generator.git
cd multiverse-character-generator
pip install -e .`,

    basicUsage: `from multiverse_character_generator import MultiverseCharacterGenerator

# Initialize the generator
generator = MultiverseCharacterGenerator()

# Quick generation with predefined examples
character = generator.quick_generate("fantasy")
print(character.character)
print(f"Saved to: {character.filename}")`,

    customDetails: `# Generate a fantasy character with specific details
character = generator.generate_character(
    universe="fantasy",
    details=["Elf", "Ranger", "Chaotic Good", "Rivendell"]
)

# Generate a sci-fi character
character = generator.generate_character(
    universe="sci-fi",
    details=["Android", "Engineer", "Federation", "Earth"]
)

# Generate a cyberpunk character
character = generator.generate_character(
    universe="cyberpunk",
    details=["Neural Implants", "Shadow Corp", "Hacker", "Neo-Tokyo"]
)`,

    parameters: `# Customize generation parameters
character = generator.generate_character(
    universe="horror",
    details=["Detective", "Claustrophobia", "Cursed Locket", "Abandoned Asylum"],
    max_length=500,        # Longer description
    temperature=0.9,       # More creative
    top_p=0.95,           # More diverse vocabulary
    repetition_penalty=1.3, # Avoid repetition
    save_to_file=True,     # Save to file
    output_dir="./characters" # Custom directory
)`,

    asyncUsage: `import asyncio

async def generate_multiple_characters():
    generator = MultiverseCharacterGenerator()
    
    # Generate multiple characters concurrently
    tasks = [
        generator.generate_character_async("fantasy", ["Dwarf", "Warrior", "Lawful Good", "Moria"]),
        generator.generate_character_async("sci-fi", ["Alien", "Diplomat", "Galactic Union", "Proxima B"]),
        generator.generate_character_async("anime", ["Protagonist", "Time Control", "Lost Memory", "Save World"])
    ]
    
    characters = await asyncio.gather(*tasks)
    return characters

# Run the async function
characters = asyncio.run(generate_multiple_characters())`,

    errorHandling: `from multiverse_character_generator import (
    MultiverseCharacterGenerator,
    InvalidUniverseError,
    InvalidDetailsError,
    GenerationError
)

try:
    generator = MultiverseCharacterGenerator()
    
    # This will raise InvalidUniverseError
    character = generator.generate_character("invalid_universe", ["test"])
    
except InvalidUniverseError as e:
    print(f"Universe error: {e}")
    print(f"Available universes: {e.available_universes}")
    
except InvalidDetailsError as e:
    print(f"Details error: {e}")
    print(f"Expected {e.expected_count} details, got {e.actual_count}")
    
except GenerationError as e:
    print(f"Generation failed: {e}")`,

    webIntegration: `# Flask integration example
from flask import Flask, request, jsonify
from multiverse_character_generator import MultiverseCharacterGenerator

app = Flask(__name__)
generator = MultiverseCharacterGenerator()

@app.route('/generate', methods=['POST'])
def generate_character():
    data = request.json
    
    try:
        if 'details' in data:
            character = generator.generate_character(
                universe=data['universe'],
                details=data['details']
            )
        else:
            character = generator.quick_generate(data['universe'])
            
        return jsonify({
            'success': True,
            'character': character.character,
            'filename': character.filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# FastAPI integration example
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
generator = MultiverseCharacterGenerator()

class GenerationRequest(BaseModel):
    universe: str
    details: list = None

@app.post("/generate")
async def generate_character(request: GenerationRequest):
    try:
        if request.details:
            character = await generator.generate_character_async(
                universe=request.universe,
                details=request.details
            )
        else:
            character = await generator.quick_generate_async(request.universe)
            
        return {
            "character": character.character,
            "filename": character.filename
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))`
  }

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

      <div className="container" style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: '2rem', padding: '2rem 1rem' }}>
        <nav className="tutorial-nav">
          <h3 style={{ marginBottom: '1rem', color: 'var(--dark-bg)' }}>Tutorial Sections</h3>
          <ul>
            {sections.map((section) => (
              <li key={section.id}>
                <a
                  href={`#${section.id}`}
                  className={activeSection === section.id ? 'active' : ''}
                  onClick={(e) => {
                    e.preventDefault()
                    setActiveSection(section.id)
                    document.getElementById(section.id)?.scrollIntoView({ behavior: 'smooth' })
                  }}
                >
                  {section.title}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <main className="tutorial-content">
          <h1 style={{ color: 'var(--dark-bg)', marginBottom: '2rem' }}>Complete Tutorial</h1>

          <section id="installation">
            <h2>Installation</h2>
            <p>
              The Multiverse Character Generator requires Python 3.8 or higher. Install it using pip:
            </p>
            <SyntaxHighlighter language="bash" style={tomorrow}>
              {codeExamples.installation}
            </SyntaxHighlighter>
            <div className="alert alert-info">
              <strong>Note:</strong> The library will automatically download the GPT-2 model on first use. 
              This may take a few minutes depending on your internet connection.
            </div>
          </section>

          <section id="basic-usage">
            <h2>Basic Usage</h2>
            <p>
              Start generating characters with just a few lines of code. The <code className="inline-code">quick_generate</code> 
              method uses predefined examples for each universe:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
              {codeExamples.basicUsage}
            </SyntaxHighlighter>
            <p>
              This will generate a random fantasy character using the library's built-in examples and optionally save it to a file.
            </p>
          </section>

          <section id="universes">
            <h2>Understanding Universes</h2>
            <p>
              Each universe has specific requirements for character details. Here are the supported universes and their required fields:
            </p>
            
            <div className="grid grid-2" style={{ margin: '2rem 0' }}>
              <div className="card">
                <h3 className="card-title">Fantasy</h3>
                <ul>
                  <li><strong>Race:</strong> Elf, Dwarf, Human, Halfling, etc.</li>
                  <li><strong>Class:</strong> Warrior, Mage, Rogue, Cleric, etc.</li>
                  <li><strong>Alignment:</strong> Lawful Good, Chaotic Evil, etc.</li>
                  <li><strong>Kingdom:</strong> Rivendell, Gondor, Moria, etc.</li>
                </ul>
              </div>
              
              <div className="card">
                <h3 className="card-title">Sci-Fi</h3>
                <ul>
                  <li><strong>Species:</strong> Human, Android, Alien, Cyborg, etc.</li>
                  <li><strong>Profession:</strong> Pilot, Engineer, Diplomat, etc.</li>
                  <li><strong>Affiliation:</strong> Federation, Empire, Rebels, etc.</li>
                  <li><strong>Planet:</strong> Earth, Mars, Tatooine, etc.</li>
                </ul>
              </div>
              
              <div className="card">
                <h3 className="card-title">Horror</h3>
                <ul>
                  <li><strong>Occupation:</strong> Detective, Doctor, Student, etc.</li>
                  <li><strong>Phobia:</strong> Heights, Darkness, Spiders, etc.</li>
                  <li><strong>Cursed Relic:</strong> Locket, Mirror, Book, etc.</li>
                  <li><strong>Haunted Location:</strong> Asylum, Cemetery, etc.</li>
                </ul>
              </div>
              
              <div className="card">
                <h3 className="card-title">Cyberpunk</h3>
                <ul>
                  <li><strong>Implants:</strong> Neural, Cybernetic Arm, etc.</li>
                  <li><strong>Affiliation:</strong> Corp, Gang, Independent, etc.</li>
                  <li><strong>Specialization:</strong> Hacker, Netrunner, etc.</li>
                  <li><strong>District:</strong> Neo-Tokyo, Night City, etc.</li>
                </ul>
              </div>
            </div>
          </section>

          <section id="custom-details">
            <h2>Custom Character Details</h2>
            <p>
              For more control over character generation, provide specific details for each universe:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
              {codeExamples.customDetails}
            </SyntaxHighlighter>
            <div className="alert alert-warning">
              <strong>Important:</strong> Each universe requires exactly 4 details in the correct order. 
              Check the universe requirements above or use <code className="inline-code">generator.get_universe_info(universe)</code> 
              to see the required fields.
            </div>
          </section>

          <section id="parameters">
            <h2>Generation Parameters</h2>
            <p>
              Fine-tune the character generation process with various parameters:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
              {codeExamples.parameters}
            </SyntaxHighlighter>
            
            <h3>Parameter Explanation</h3>
            <ul>
              <li><strong>max_length:</strong> Controls the length of generated text (50-1000)</li>
              <li><strong>temperature:</strong> Higher values (0.8-1.0) make output more creative</li>
              <li><strong>top_p:</strong> Nucleus sampling parameter (0.9-0.98 recommended)</li>
              <li><strong>repetition_penalty:</strong> Reduces repetitive text (1.1-1.3 recommended)</li>
              <li><strong>save_to_file:</strong> Automatically save generated characters</li>
              <li><strong>output_dir:</strong> Directory for saved files</li>
            </ul>
          </section>

          <section id="async-usage">
            <h2>Async Generation</h2>
            <p>
              Generate multiple characters concurrently for better performance:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
              {codeExamples.asyncUsage}
            </SyntaxHighlighter>
            <div className="alert alert-success">
              <strong>Performance Tip:</strong> Async generation is particularly useful when creating multiple 
              characters or integrating with web frameworks that support async operations.
            </div>
          </section>

          <section id="file-operations">
            <h2>File Operations</h2>
            <p>
              The library can automatically save generated characters to files with timestamps and universe names:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`# Enable file saving
character = generator.generate_character(
    universe="fantasy",
    details=["Elf", "Mage", "Neutral Good", "Rivendell"],
    save_to_file=True,
    output_dir="./my_characters"
)

print(f"Character saved to: {character.filename}")

# Files are named: {universe}_{timestamp}.txt
# Example: fantasy_20241207_143052.txt`}
            </SyntaxHighlighter>
          </section>

          <section id="error-handling">
            <h2>Error Handling</h2>
            <p>
              The library provides specific exceptions for different error conditions:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
              {codeExamples.errorHandling}
            </SyntaxHighlighter>
            
            <h3>Exception Types</h3>
            <ul>
              <li><strong>InvalidUniverseError:</strong> Unknown universe specified</li>
              <li><strong>InvalidDetailsError:</strong> Wrong number or type of details</li>
              <li><strong>GenerationError:</strong> Model generation failure</li>
              <li><strong>ModelInitializationError:</strong> Model loading failure</li>
              <li><strong>FileOperationError:</strong> File save/load failure</li>
            </ul>
          </section>

          <section id="performance">
            <h2>Performance Tips</h2>
            
            <h3>GPU Acceleration</h3>
            <p>
              The library automatically detects and uses GPU when available. For better performance:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`# Force GPU usage (if available)
generator = MultiverseCharacterGenerator(use_gpu=True)

# Check if GPU is being used
model_info = generator.get_model_info()
print(f"Using GPU: {model_info['using_gpu']}")
print(f"Device: {model_info['device']}")`}
            </SyntaxHighlighter>

            <h3>Model Caching</h3>
            <p>
              Cache models for faster initialization:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`# Use custom cache directory
generator = MultiverseCharacterGenerator(
    model_name="gpt2-medium",
    cache_dir="./model_cache"
)`}
            </SyntaxHighlighter>

            <h3>Batch Processing</h3>
            <p>
              For generating many characters, use async methods:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`import asyncio
from typing import List

async def generate_character_batch(
    generator: MultiverseCharacterGenerator,
    requests: List[tuple]
) -> List[GeneratedCharacter]:
    """Generate multiple characters concurrently."""
    tasks = []
    
    for universe, details in requests:
        task = generator.generate_character_async(universe, details)
        tasks.append(task)
    
    return await asyncio.gather(*tasks)

# Usage
requests = [
    ("fantasy", ["Human", "Paladin", "Lawful Good", "Gondor"]),
    ("sci-fi", ["Android", "Pilot", "Rebellion", "Coruscant"]),
    ("horror", ["Student", "Darkness", "Diary", "Old Library"])
]

characters = asyncio.run(generate_character_batch(generator, requests))`}
            </SyntaxHighlighter>
          </section>

          <section id="web-integration">
            <h2>Web Framework Integration</h2>
            <p>
              Integrate the library with popular web frameworks:
            </p>
            <SyntaxHighlighter language="python" style={tomorrow}>
              {codeExamples.webIntegration}
            </SyntaxHighlighter>
            
            <div className="alert alert-info">
              <strong>Production Tips:</strong>
              <ul style={{ margin: '1rem 0', paddingLeft: '2rem' }}>
                <li>Initialize the generator once at startup, not per request</li>
                <li>Use async methods for better performance</li>
                <li>Implement proper error handling and logging</li>
                <li>Consider rate limiting for public APIs</li>
                <li>Cache frequently used characters</li>
              </ul>
            </div>
          </section>

          <div style={{ marginTop: '3rem', padding: '2rem', background: '#f8fafc', borderRadius: '0.5rem' }}>
            <h2 style={{ color: 'var(--dark-bg)', marginBottom: '1rem' }}>Next Steps</h2>
            <p style={{ marginBottom: '1.5rem' }}>
              Now that you've completed the tutorial, explore more advanced features:
            </p>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              <Link href="/api" className="btn btn-primary">
                API Reference
              </Link>
              <Link href="/examples" className="btn btn-secondary">
                Advanced Examples
              </Link>
              <a href="https://github.com/your-username/multiverse-character-generator" className="btn btn-secondary">
                GitHub Repository
              </a>
            </div>
          </div>
        </main>
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