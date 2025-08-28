#!/bin/bash

# Development setup script for Claude Code Environment Manager

set -e

echo "Setting up development environment for Claude Code Environment Manager..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.11 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install package in development mode
echo "Installing package in development mode..."
pip install -e .

# Set up pre-commit hooks (if available)
if command -v pre-commit &> /dev/null; then
    echo "Setting up pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installed"
fi

# Create test configuration
echo "Creating test configuration..."
mkdir -p tests/config
cp config/claude-profiles.yml tests/config/claude-profiles.yml

# Set up test environment
export CLAUDE_ENV_MANAGER_CONFIG=tests/config/claude-profiles.yml
export CLAUDE_ENV_MANAGER_SETTINGS=tests/config/settings.json

echo "✅ Development setup completed!"
echo ""
echo "Development commands:"
echo "  pytest                 # Run tests"
echo "  pytest --cov         # Run tests with coverage"
echo "  black .               # Format code"
echo "  isort .               # Sort imports"
echo "  flake8 .              # Lint code"
echo "  mypy .                # Type check"
echo ""
echo "To run the CLI:"
echo "  python -m claude_env_manager.main --help"