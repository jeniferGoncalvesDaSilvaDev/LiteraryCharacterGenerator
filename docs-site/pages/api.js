import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { tomorrow } from 'react-syntax-highlighter/dist/cjs/styles/prism'
import Link from 'next/link'

export default function ApiReference() {
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
        <h1 style={{ color: 'var(--dark-bg)', marginBottom: '2rem' }}>API Reference</h1>

        <section className="section">
          <h2 className="section-title">MultiverseCharacterGenerator</h2>
          
          <div className="card">
            <h3 className="card-title">Constructor</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`MultiverseCharacterGenerator(
    model_name: str = "gpt2-medium",
    use_gpu: Optional[bool] = None,
    cache_dir: Optional[str] = None
)`}
            </SyntaxHighlighter>
            
            <h4>Parameters:</h4>
            <ul>
              <li><strong>model_name</strong> (str): GPT-2 model variant ("gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl")</li>
              <li><strong>use_gpu</strong> (bool, optional): Force GPU usage. None for auto-detection</li>
              <li><strong>cache_dir</strong> (str, optional): Directory to cache model files</li>
            </ul>
          </div>

          <div className="card">
            <h3 className="card-title">generate_character()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`generate_character(
    universe: str,
    details: List[str],
    max_length: int = 350,
    temperature: float = 0.85,
    top_p: float = 0.92,
    repetition_penalty: float = 1.2,
    save_to_file: bool = False,
    output_dir: Optional[str] = None
) -> GeneratedCharacter`}
            </SyntaxHighlighter>
            
            <p>Generate a character with custom details.</p>
            
            <h4>Parameters:</h4>
            <ul>
              <li><strong>universe</strong> (str): Target universe ("fantasy", "sci-fi", "horror", "cyberpunk", "anime", "marvel")</li>
              <li><strong>details</strong> (List[str]): Character details matching universe requirements</li>
              <li><strong>max_length</strong> (int): Maximum text length (50-1000)</li>
              <li><strong>temperature</strong> (float): Sampling temperature (0.0-1.0)</li>
              <li><strong>top_p</strong> (float): Nucleus sampling parameter (0.0-1.0)</li>
              <li><strong>repetition_penalty</strong> (float): Repetition penalty (1.0-2.0)</li>
              <li><strong>save_to_file</strong> (bool): Whether to save character to file</li>
              <li><strong>output_dir</strong> (str, optional): Output directory for files</li>
            </ul>
            
            <h4>Returns:</h4>
            <p><strong>GeneratedCharacter:</strong> Object containing character text and optional filename</p>
            
            <h4>Raises:</h4>
            <ul>
              <li><strong>InvalidUniverseError:</strong> If universe is not supported</li>
              <li><strong>InvalidDetailsError:</strong> If details don't match universe requirements</li>
              <li><strong>GenerationError:</strong> If character generation fails</li>
            </ul>
          </div>

          <div className="card">
            <h3 className="card-title">quick_generate()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`quick_generate(
    universe: str,
    max_length: int = 350,
    temperature: float = 0.85,
    top_p: float = 0.92,
    repetition_penalty: float = 1.2,
    save_to_file: bool = False,
    output_dir: Optional[str] = None
) -> GeneratedCharacter`}
            </SyntaxHighlighter>
            
            <p>Generate a character using predefined examples for the universe.</p>
            
            <h4>Parameters:</h4>
            <p>Same as generate_character() except no details parameter required.</p>
          </div>

          <div className="card">
            <h3 className="card-title">generate_character_async()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`async generate_character_async(
    universe: str,
    details: List[str],
    max_length: int = 350,
    temperature: float = 0.85,
    top_p: float = 0.92,
    repetition_penalty: float = 1.2,
    save_to_file: bool = False,
    output_dir: Optional[str] = None
) -> GeneratedCharacter`}
            </SyntaxHighlighter>
            
            <p>Asynchronous version of generate_character().</p>
          </div>

          <div className="card">
            <h3 className="card-title">quick_generate_async()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`async quick_generate_async(
    universe: str,
    max_length: int = 350,
    temperature: float = 0.85,
    top_p: float = 0.92,
    repetition_penalty: float = 1.2,
    save_to_file: bool = False,
    output_dir: Optional[str] = None
) -> GeneratedCharacter`}
            </SyntaxHighlighter>
            
            <p>Asynchronous version of quick_generate().</p>
          </div>

          <div className="card">
            <h3 className="card-title">get_universe_info()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`get_universe_info(universe: str) -> Dict[str, List[str]]`}
            </SyntaxHighlighter>
            
            <p>Get information about a specific universe.</p>
            
            <h4>Returns:</h4>
            <p>Dictionary with 'inputs' and 'exemplos' keys containing required fields and example values.</p>
          </div>

          <div className="card">
            <h3 className="card-title">list_universes()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`list_universes() -> List[str]`}
            </SyntaxHighlighter>
            
            <p>Get a list of all available universes.</p>
            
            <h4>Returns:</h4>
            <p>List of universe names: ["fantasy", "sci-fi", "horror", "cyberpunk", "anime", "marvel"]</p>
          </div>

          <div className="card">
            <h3 className="card-title">get_model_info()</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`get_model_info() -> Dict[str, Union[str, bool]]`}
            </SyntaxHighlighter>
            
            <p>Get information about the loaded model.</p>
            
            <h4>Returns:</h4>
            <p>Dictionary with model name, GPU usage status, cache directory, and device information.</p>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Data Models</h2>
          
          <div className="card">
            <h3 className="card-title">GeneratedCharacter</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`class GeneratedCharacter(BaseModel):
    character: str          # The generated character text
    filename: Optional[str] # Filename if saved to file`}
            </SyntaxHighlighter>
            
            <p>Model representing a generated character with validation.</p>
          </div>

          <div className="card">
            <h3 className="card-title">CharacterDetails</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`class CharacterDetails(BaseModel):
    details: List[str]  # Character details (1-10 items)
    universe: str       # Target universe`}
            </SyntaxHighlighter>
            
            <p>Model for validating character generation input.</p>
          </div>

          <div className="card">
            <h3 className="card-title">GenerationConfig</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`class GenerationConfig(BaseModel):
    max_length: int = 350              # Text length (50-1000)
    temperature: float = 0.85          # Creativity (0.0-1.0)
    top_p: float = 0.92               # Vocabulary diversity (0.0-1.0)
    repetition_penalty: float = 1.2   # Repetition control (1.0-2.0)
    save_to_file: bool = False        # Auto-save option
    output_dir: Optional[str] = None  # Save directory`}
            </SyntaxHighlighter>
            
            <p>Model for generation parameter configuration with validation.</p>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Exceptions</h2>
          
          <div className="grid grid-2">
            <div className="card">
              <h3 className="card-title">InvalidUniverseError</h3>
              <p>Raised when an invalid universe is specified.</p>
              
              <h4>Attributes:</h4>
              <ul>
                <li><strong>universe:</strong> The invalid universe name</li>
                <li><strong>available_universes:</strong> List of valid universes</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">InvalidDetailsError</h3>
              <p>Raised when character details don't match universe requirements.</p>
              
              <h4>Attributes:</h4>
              <ul>
                <li><strong>universe:</strong> Target universe</li>
                <li><strong>expected_count:</strong> Required number of details</li>
                <li><strong>actual_count:</strong> Provided number of details</li>
                <li><strong>required_fields:</strong> List of required fields</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">GenerationError</h3>
              <p>Raised when character generation fails.</p>
              
              <h4>Attributes:</h4>
              <ul>
                <li><strong>cause:</strong> Original exception that caused the failure</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">ModelInitializationError</h3>
              <p>Raised when model initialization fails.</p>
              
              <h4>Attributes:</h4>
              <ul>
                <li><strong>model_name:</strong> Name of the model that failed to load</li>
                <li><strong>cause:</strong> Original exception</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">FileOperationError</h3>
              <p>Raised when file operations fail.</p>
              
              <h4>Attributes:</h4>
              <ul>
                <li><strong>filepath:</strong> Path of the file operation</li>
                <li><strong>operation:</strong> Type of operation (save/load)</li>
                <li><strong>cause:</strong> Original exception</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">ValidationError</h3>
              <p>Raised when input validation fails.</p>
              
              <h4>Attributes:</h4>
              <ul>
                <li><strong>field:</strong> Name of the invalid field</li>
                <li><strong>value:</strong> Invalid value provided</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Universe Specifications</h2>
          
          <div className="grid grid-2">
            <div className="card">
              <h3 className="card-title">Fantasy</h3>
              <ul>
                <li><strong>Field 1:</strong> Race (Elf, Dwarf, Human, Halfling, Orc)</li>
                <li><strong>Field 2:</strong> Class (Warrior, Mage, Rogue, Cleric, Paladin)</li>
                <li><strong>Field 3:</strong> Alignment (Lawful Good, Chaotic Evil, etc.)</li>
                <li><strong>Field 4:</strong> Kingdom (Rivendell, Gondor, Moria, etc.)</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">Sci-Fi</h3>
              <ul>
                <li><strong>Field 1:</strong> Species (Human, Android, Alien, Cyborg)</li>
                <li><strong>Field 2:</strong> Profession (Pilot, Engineer, Diplomat, Soldier)</li>
                <li><strong>Field 3:</strong> Affiliation (Federation, Empire, Rebels, Mercenary)</li>
                <li><strong>Field 4:</strong> Planet (Earth, Mars, Tatooine, Coruscant)</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">Horror</h3>
              <ul>
                <li><strong>Field 1:</strong> Occupation (Detective, Doctor, Student, Writer)</li>
                <li><strong>Field 2:</strong> Phobia (Heights, Darkness, Spiders, Crowds)</li>
                <li><strong>Field 3:</strong> Cursed Relic (Locket, Mirror, Book, Doll)</li>
                <li><strong>Field 4:</strong> Haunted Location (Asylum, Cemetery, Mansion)</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">Cyberpunk</h3>
              <ul>
                <li><strong>Field 1:</strong> Implants (Neural, Cybernetic Arm, Eye Enhancement)</li>
                <li><strong>Field 2:</strong> Affiliation (Corp, Gang, Independent, Government)</li>
                <li><strong>Field 3:</strong> Specialization (Hacker, Netrunner, Street Samurai)</li>
                <li><strong>Field 4:</strong> District (Neo-Tokyo, Night City, Sector 7)</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">Anime</h3>
              <ul>
                <li><strong>Field 1:</strong> Type (Protagonist, Rival, Mentor, Anti-hero)</li>
                <li><strong>Field 2:</strong> Unique Ability (Time Control, Telekinesis, etc.)</li>
                <li><strong>Field 3:</strong> Backstory (Lost Memory, Tragic Past, etc.)</li>
                <li><strong>Field 4:</strong> Goal (Save World, Find Truth, Become Strong)</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="card-title">Marvel</h3>
              <ul>
                <li><strong>Field 1:</strong> Power Origin (Mutation, Technology, Magic, Cosmic)</li>
                <li><strong>Field 2:</strong> Affiliation (Avengers, X-Men, SHIELD, Independent)</li>
                <li><strong>Field 3:</strong> Archetype (Hero, Villain, Anti-hero, Vigilante)</li>
                <li><strong>Field 4:</strong> Location (New York, Wakanda, Asgard, Space)</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Usage Examples</h2>
          
          <div className="card">
            <h3 className="card-title">Complete Example</h3>
            <SyntaxHighlighter language="python" style={tomorrow}>
{`from multiverse_character_generator import (
    MultiverseCharacterGenerator,
    InvalidUniverseError,
    InvalidDetailsError
)
import asyncio

# Initialize generator
generator = MultiverseCharacterGenerator(
    model_name="gpt2-medium",
    use_gpu=True,
    cache_dir="./models"
)

# Check available universes
print("Available universes:", generator.list_universes())

# Get universe information
fantasy_info = generator.get_universe_info("fantasy")
print("Fantasy fields:", fantasy_info['inputs'])

try:
    # Generate custom character
    character = generator.generate_character(
        universe="fantasy",
        details=["Elf", "Ranger", "Chaotic Good", "Rivendell"],
        max_length=400,
        temperature=0.9,
        save_to_file=True,
        output_dir="./characters"
    )
    
    print("Generated character:")
    print(character.character)
    print(f"Saved to: {character.filename}")
    
    # Quick generation
    quick_char = generator.quick_generate("sci-fi")
    print("\\nQuick character:")
    print(quick_char.character)
    
    # Async generation
    async def generate_multiple():
        tasks = [
            generator.generate_character_async("horror", 
                ["Detective", "Darkness", "Cursed Mirror", "Abandoned Hospital"]),
            generator.quick_generate_async("cyberpunk"),
            generator.quick_generate_async("anime")
        ]
        return await asyncio.gather(*tasks)
    
    characters = asyncio.run(generate_multiple())
    print(f"\\nGenerated {len(characters)} characters asynchronously")
    
    # Model information
    model_info = generator.get_model_info()
    print(f"\\nModel: {model_info['model_name']}")
    print(f"Using GPU: {model_info['using_gpu']}")
    print(f"Device: {model_info['device']}")
    
except InvalidUniverseError as e:
    print(f"Invalid universe: {e.universe}")
    print(f"Available: {e.available_universes}")
    
except InvalidDetailsError as e:
    print(f"Invalid details for {e.universe}")
    print(f"Expected {e.expected_count} details, got {e.actual_count}")
    print(f"Required fields: {e.required_fields}")
    
except Exception as e:
    print(f"Error: {e}")`}
            </SyntaxHighlighter>
          </div>
        </section>

        <div style={{ marginTop: '3rem', padding: '2rem', background: '#f8fafc', borderRadius: '0.5rem' }}>
          <h2 style={{ color: 'var(--dark-bg)', marginBottom: '1rem' }}>Related Documentation</h2>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <Link href="/tutorial" className="btn btn-primary">
              Complete Tutorial
            </Link>
            <Link href="/examples" className="btn btn-secondary">
              Advanced Examples
            </Link>
            <Link href="/" className="btn btn-secondary">
              Back to Home
            </Link>
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