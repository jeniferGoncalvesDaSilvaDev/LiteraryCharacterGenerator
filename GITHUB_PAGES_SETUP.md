# GitHub Pages Setup Guide

## Your Documentation Site URL

Once deployed, your Character Generator documentation will be available at:

```
https://jenifergoncalvesdasilvadev.github.io/character_generator
```

## Setup Steps

### 1. Repository Settings
1. Go to your repository: `https://github.com/jeniferGoncalvesDaSilvaDev/character_generator`
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**

### 2. Enable GitHub Actions
The repository includes automated workflows that will:
- Build and deploy documentation automatically when you push code
- Publish to PyPI when you create version tags

### 3. Required Repository Secrets (for PyPI publishing)
To enable automatic PyPI publishing, add these secrets in Settings → Secrets and variables → Actions:

```
PYPI_API_TOKEN - Your PyPI API token
TEST_PYPI_API_TOKEN - Your TestPyPI API token (optional)
```

### 4. First Deployment
After enabling GitHub Pages:
1. Push this code to your repository
2. The GitHub Actions workflow will automatically run
3. Your documentation site will be built and deployed
4. Visit the URL above to see your live documentation

## Documentation Site Features

Your site will include:
- Professional landing page with universe showcases
- Interactive tutorial with step-by-step examples
- Complete API reference documentation
- Advanced integration examples for web frameworks
- Responsive design with syntax highlighting

## PyPI Publication

To publish your library to PyPI:
1. Create a new release with a version tag (e.g., `v1.0.0`)
2. The GitHub Action will automatically build and publish to PyPI
3. Users can then install with: `pip install character-generator`

## Local Development

To run the documentation site locally:
```bash
cd docs-site
npm install
npm run dev
```

The site will be available at `http://localhost:3000`

## File Structure

```
character_generator/
├── multiverse_character_generator/    # Main library code
├── docs-site/                        # React documentation site
├── examples/                         # Usage examples
├── docs/                            # Markdown documentation
├── .github/workflows/               # GitHub Actions
└── README.md                       # Project overview
```

## Next Steps

1. Push this code to your GitHub repository
2. Enable GitHub Pages in repository settings
3. Add PyPI API tokens to repository secrets
4. Create your first release to publish to PyPI