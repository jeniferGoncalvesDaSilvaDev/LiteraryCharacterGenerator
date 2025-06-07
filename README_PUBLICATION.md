# Publication Setup Guide

This guide covers setting up automated publication to PyPI and GitHub Pages deployment for the Multiverse Character Generator.

## PyPI Publication Setup

### 1. Create PyPI Account and API Tokens

1. Create accounts on:
   - [PyPI](https://pypi.org/account/register/)
   - [Test PyPI](https://test.pypi.org/account/register/)

2. Generate API tokens:
   - PyPI: Account Settings → API Tokens → Add API Token
   - Test PyPI: Account Settings → API Tokens → Add API Token

### 2. Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
PYPI_API_TOKEN=pypi-your-production-token-here
TEST_PYPI_API_TOKEN=pypi-your-test-token-here
```

### 3. Manual Publication Commands

For manual publishing:

```bash
# Install build tools
pip install build twine wheel

# Build package
python -m build

# Check package
twine check dist/*

# Publish to Test PyPI
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*
```

### 4. Version Management

Update version in `pyproject.toml`:
```toml
[project]
version = "1.0.1"  # Increment for new releases
```

Create git tags for releases:
```bash
git tag v1.0.1
git push origin v1.0.1
```

## GitHub Pages Documentation Setup

### 1. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: GitHub Actions
3. The workflow will automatically deploy on pushes to main branch

### 2. Configure Repository Settings

Update these URLs in `pyproject.toml` and documentation:
```toml
[project.urls]
Homepage = "https://github.com/YOUR-USERNAME/multiverse-character-generator"
Documentation = "https://YOUR-USERNAME.github.io/multiverse-character-generator"
Repository = "https://github.com/YOUR-USERNAME/multiverse-character-generator.git"
```

### 3. Manual Documentation Deployment

To deploy documentation manually:

```bash
cd docs-site
npm install
npm run build
npm run export

# Deploy with gh-pages (optional)
npm install -g gh-pages
gh-pages -d out
```

## Automated Workflows

The repository includes three automated workflows:

### 1. Test Workflow (`.github/workflows/test.yml`)
- Runs on every push and pull request
- Tests across Python 3.8-3.11
- Executes structure and unit tests

### 2. PyPI Publication (`.github/workflows/publish-pypi.yml`)
- Triggers on version tags (`v*`)
- Publishes to Test PyPI for tags
- Publishes to PyPI for releases

### 3. Documentation Deployment (`.github/workflows/deploy-docs.yml`)
- Triggers on pushes to main branch
- Builds and deploys React documentation site
- Deploys to GitHub Pages

## Release Process

1. **Update Version**: Increment version in `pyproject.toml`
2. **Update Changelog**: Add new version entry to `CHANGELOG.md`
3. **Commit Changes**: `git commit -am "Release v1.0.1"`
4. **Create Tag**: `git tag v1.0.1`
5. **Push**: `git push origin main --tags`
6. **Create Release**: Use GitHub releases to create official release

## Package Structure

The package is configured with:

- **Entry Point**: `multiverse-gen` CLI command
- **Dependencies**: Automatically managed via pyproject.toml
- **Optional Dependencies**: `dev`, `docs`, `web` extras
- **Python Support**: 3.8-3.12
- **License**: MIT

## Troubleshooting

### Build Issues
- Ensure all dependencies are in `pyproject.toml`
- Check MANIFEST.in includes all necessary files
- Verify Python version compatibility

### Publication Issues
- Verify API tokens are correct and have upload permissions
- Check package name availability on PyPI
- Ensure version number hasn't been used before

### Documentation Issues
- Verify Node.js 18+ is available in CI
- Check Next.js build configuration
- Ensure GitHub Pages is enabled in repository settings

## Security Considerations

- Never commit API tokens to repository
- Use GitHub secrets for sensitive data
- Regularly rotate API tokens
- Monitor package downloads and usage

## Monitoring

After publication, monitor:
- PyPI download statistics
- GitHub Pages analytics
- Repository stars and issues
- Documentation site traffic