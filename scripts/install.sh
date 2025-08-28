#!/bin/bash

# Installation script for Claude Code Environment Manager

set -e

echo "Installing Claude Code Environment Manager..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.11 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install dependencies
echo "Installing dependencies..."
pip install -e .

echo "✅ Installation completed successfully!"

# Initialize configuration if it doesn't exist
if [ ! -f "$HOME/.claude/claude-profiles.yml" ]; then
    echo "Initializing configuration..."
    claude-env-manager init
fi

echo ""
echo "🎉 Claude Code Environment Manager is ready!"
echo ""
echo "Quick start:"
echo "  claude-env-manager list              # List all profiles"
echo "  claude-env-manager create --interactive  # Create a new profile"
echo "  claude-env-manager apply development  # Apply a profile"
echo "  claude-env-manager --help             # Show all commands"
echo ""