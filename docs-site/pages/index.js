import Link from 'next/link'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { tomorrow } from 'react-syntax-highlighter/dist/cjs/styles/prism'

export default function Home() {
  const installCode = `pip install multiverse-character-generator`
  
  const quickStartCode = `from multiverse_character_generator import MultiverseCharacterGenerator

# Initialize the generator
generator = MultiverseCharacterGenerator()

# Generate a fantasy character
character = generator.quick_generate("fantasy")
print(character.character)

# Generate with custom details
character = generator.generate_character(
    universe="sci-fi",
    details=["Human", "Pilot", "Rebel Alliance", "Tatooine"]
)
print(character.character)`

  const universes = [
    {
      name: "Fantasy",
      key: "fantasy",
      description: "Medieval fantasy with magic, dragons, and epic adventures",
      fields: ["Race", "Class", "Alignment", "Kingdom"]
    },
    {
      name: "Sci-Fi",
      key: "sci-fi", 
      description: "Space exploration, alien worlds, and advanced technology",
      fields: ["Species", "Profession", "Affiliation", "Planet"]
    },
    {
      name: "Horror",
      key: "horror",
      description: "Cosmic horror, supernatural entities, and psychological terror",
      fields: ["Occupation", "Phobia", "Cursed Relic", "Haunted Location"]
    },
    {
      name: "Cyberpunk",
      key: "cyberpunk",
      description: "Dystopian future with cybernetic implants and corporate control",
      fields: ["Implants", "Affiliation", "Specialization", "District"]
    },
    {
      name: "Anime",
      key: "anime",
      description: "Japanese animation style with unique abilities and storylines",
      fields: ["Type", "Unique Ability", "Backstory", "Goal"]
    },
    {
      name: "Marvel",
      key: "marvel",
      description: "Superhero universe with powers, teams, and epic battles",
      fields: ["Power Origin", "Affiliation", "Archetype", "Location"]
    }
  ]

  return (
    <>
      <header className="header">
        <div className="container">
          <nav className="nav">
            <h1>Multiverse Character Generator</h1>
            <ul className="nav-links">
              <li><Link href="/" className="nav-link">Home</Link></li>
              <li><Link href="/tutorial" className="nav-link">Tutorial</Link></li>
              <li><Link href="/api" className="nav-link">API</Link></li>
              <li><Link href="/examples" className="nav-link">Examples</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <section className="hero">
        <div className="container">
          <h1>Generate Characters Across Multiple Universes</h1>
          <p>Create compelling fictional characters using GPT-2 for fantasy, sci-fi, horror, cyberpunk, anime, and Marvel universes</p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link href="/tutorial" className="btn btn-primary">Get Started</Link>
            <a href="https://github.com/your-username/multiverse-character-generator" className="btn btn-secondary">View on GitHub</a>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2 className="section-title">Quick Installation</h2>
          <div className="grid grid-2">
            <div className="card">
              <h3 className="card-title">Install via pip</h3>
              <SyntaxHighlighter language="bash" style={tomorrow}>
                {installCode}
              </SyntaxHighlighter>
              <p className="card-text">
                Install the library with all dependencies using pip. Requires Python 3.8 or higher.
              </p>
            </div>
            <div className="card">
              <h3 className="card-title">Quick Start Example</h3>
              <SyntaxHighlighter language="python" style={tomorrow}>
                {quickStartCode}
              </SyntaxHighlighter>
              <p className="card-text">
                Generate your first character in just a few lines of code.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="section" style={{ background: '#f8fafc' }}>
        <div className="container">
          <h2 className="section-title">Supported Universes</h2>
          <div className="universe-grid">
            {universes.map((universe) => (
              <div key={universe.key} className={`universe-card ${universe.key}`}>
                <h3 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>{universe.name}</h3>
                <p style={{ marginBottom: '1.5rem', opacity: 0.9 }}>{universe.description}</p>
                <div>
                  <strong>Required Fields:</strong>
                  <ul style={{ listStyle: 'none', padding: 0, margin: '0.5rem 0' }}>
                    {universe.fields.map((field) => (
                      <li key={field} style={{ margin: '0.25rem 0' }}>• {field}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2 className="section-title">Key Features</h2>
          <div className="grid grid-3">
            <div className="card">
              <h3 className="card-title">🎯 Multiple Universes</h3>
              <p className="card-text">
                Support for 6 different fictional universes with specific character archetypes and requirements.
              </p>
            </div>
            <div className="card">
              <h3 className="card-title">⚡ Async Support</h3>
              <p className="card-text">
                Generate multiple characters concurrently with built-in async methods for better performance.
              </p>
            </div>
            <div className="card">
              <h3 className="card-title">🔧 Customizable</h3>
              <p className="card-text">
                Fine-tune generation parameters like temperature, top_p, and repetition penalty.
              </p>
            </div>
            <div className="card">
              <h3 className="card-title">💾 Auto-Save</h3>
              <p className="card-text">
                Automatically save generated characters to files with customizable output directories.
              </p>
            </div>
            <div className="card">
              <h3 className="card-title">✅ Validation</h3>
              <p className="card-text">
                Built-in input validation using Pydantic models ensures data integrity and type safety.
              </p>
            </div>
            <div className="card">
              <h3 className="card-title">🚀 GPU Acceleration</h3>
              <p className="card-text">
                Automatic GPU detection and usage when available for faster character generation.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="section" style={{ background: '#f8fafc' }}>
        <div className="container">
          <h2 className="section-title">Get Started Now</h2>
          <div className="grid grid-2">
            <div className="card">
              <h3 className="card-title">📚 Complete Tutorial</h3>
              <p className="card-text">
                Learn how to use the library with step-by-step examples, from basic usage to advanced integrations.
              </p>
              <Link href="/tutorial" className="btn btn-primary" style={{ marginTop: '1rem' }}>
                Start Tutorial
              </Link>
            </div>
            <div className="card">
              <h3 className="card-title">📖 API Reference</h3>
              <p className="card-text">
                Detailed documentation of all classes, methods, and parameters with comprehensive examples.
              </p>
              <Link href="/api" className="btn btn-primary" style={{ marginTop: '1rem' }}>
                View API Docs
              </Link>
            </div>
          </div>
        </div>
      </section>

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