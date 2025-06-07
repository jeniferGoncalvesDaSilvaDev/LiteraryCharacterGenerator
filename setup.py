"""
Setup configuration for the Multiverse Character Generator library.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read README.md file for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A Python library for generating fictional characters across multiple universes using GPT-2."

# Read version from __init__.py
def get_version():
    """Get version from package __init__.py."""
    version_file = os.path.join(os.path.dirname(__file__), 'multiverse_character_generator', '__init__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="character-generator",
    version=get_version(),
    author="Multiverse Character Generator Team",
    author_email="contact@multiversegen.com",
    description="A Python library for generating fictional characters across multiple universes using GPT-2",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/multiverse-character-generator/multiverse-character-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.9.0",
        "transformers>=4.20.0",
        "pydantic>=1.8.0",
        "nltk>=3.6",
        "numpy>=1.21.0",
        "tokenizers>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.17.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.17.0",
        ],
        "gpu": [
            "torch[cu118]>=1.9.0",  # CUDA 11.8 support
        ]
    },
    entry_points={
        "console_scripts": [
            "multiverse-generate=multiverse_character_generator.cli:main",
        ],
    },
    keywords=[
        "artificial intelligence",
        "natural language processing",
        "text generation",
        "gpt-2",
        "character generation",
        "creative writing",
        "storytelling",
        "fiction",
        "fantasy",
        "sci-fi",
        "cyberpunk",
        "anime",
        "marvel"
    ],
    project_urls={
        "Documentation": "https://multiverse-character-generator.readthedocs.io/",
        "Source": "https://github.com/multiverse-character-generator/multiverse-character-generator",
        "Tracker": "https://github.com/multiverse-character-generator/multiverse-character-generator/issues",
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    platforms=["any"],
)
