# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the `claude-code-env-manager` project - a specialized environment management system for Claude Code development workflows. The project is currently in initial setup phase and ready for development.

## Project Structure

```
claude-code-env-manager/
├── src/                    # Source code files (to be created)
├── tests/                  # Test files (to be created) 
├── docs/                   # Documentation (to be created)
├── config/                 # Configuration files (to be created)
├── scripts/                # Utility scripts (to be created)
├── assets/                 # Static assets (to be created)
└── CLAUDE.md              # This guidance file
```

## Development Setup

This project is currently empty. To start development:

1. **Initialize the project structure** based on the chosen technology stack
2. **Set up version control** with `git init`
3. **Choose your programming language** and appropriate build tools
4. **Configure the environment** management system as per project requirements

## Architecture Context

This project appears to be an environment manager for Claude Code, suggesting it may involve:
- Environment configuration and management
- Development workflow automation
- Toolchain integration and setup
- Project template generation
- Configuration file management

## Directory Guidelines

### src/ - Source Code
- Primary implementation code for the environment management system
- Consider modular architecture: core/, config/, cli/, api/, utils/
- Follow language-specific conventions for the chosen technology stack

### tests/ - Test Files
- Mirror the src/ directory structure for comprehensive testing
- Include unit tests, integration tests, and end-to-end tests
- Test environment setup and configuration scenarios

### config/ - Configuration
- Default environment configurations
- Template files for different development environments
- Settings for the environment management system itself
- Use JSON/YAML for structured configuration data

### scripts/ - Automation
- Build and deployment scripts
- Environment setup automation
- CLI tools and utilities
- Development workflow scripts

### docs/ - Documentation
- API documentation for the environment management system
- User guides and setup instructions
- Development workflow documentation
- Configuration reference guides

## Build and Development Commands

No build commands are currently configured. Based on the environment management nature of this project, consider setting up:

```bash
# Development commands (to be implemented)
# Build: npm run build or python -m build
# Test: npm test or pytest
# Lint: npm run lint or flake8
# Start: npm run dev or python -m env_manager
# Setup: scripts/setup-env.sh
```

## Technology Stack Considerations

Given this is an environment management project, consider:
- **Python**: Excellent for system administration, configuration management, and CLI tools
- **Node.js**: Good for cross-platform CLI tools and configuration management
- **Go**: Suitable for high-performance system tools and binaries
- **Rust**: Ideal for safe, high-performance system utilities

## Configuration Management

The project will likely need to handle:
- Environment variable management
- Configuration file generation and templating
- Development environment setup automation
- Toolchain configuration management
- Cross-platform compatibility considerations

## Git Configuration

This project currently lacks git initialization. When setting up version control:
- Initialize with `git init`
- Create a comprehensive `.gitignore` file (reference the one in `../try1/.gitignore`)
- Consider using a conventional commit message format
- Set up appropriate branches for development workflow

## Notes

This is a new project in the setup phase. The initial development should focus on:
1. Defining the core requirements and scope
2. Choosing the appropriate technology stack
3. Setting up the basic project structure
4. Implementing the fundamental environment management features
5. Creating comprehensive tests and documentation