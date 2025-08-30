# Claude Code Environment Manager

A modern Python TUI application for managing Claude Code environment configurations across multiple profiles, with seamless integration to `~/.claude/settings.json` and YAML-based profile management.

## Features

- **Profile Management**: Create, update, delete, and switch between environment profiles
- **TUI Interface**: Rich terminal interface with interactive profile selection
- **Validation**: Comprehensive validation for API keys, URLs, and model names
- **Integration**: Direct integration with Claude Code settings.json
- **Security**: Secure handling of API keys and sensitive configuration
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

```bash
# Install from source
git clone <repository-url>
cd claude-code-env-manager
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Using Installed CLI (Recommended)

1. **Initialize configuration**:
   ```bash
   claude-env-manager init
   ```

2. **Create a profile**:
   ```bash
   claude-env-manager create --interactive
   ```

3. **List profiles**:
   ```bash
   claude-env-manager list
   ```

4. **Apply a profile**:
   ```bash
   claude-env-manager apply development
   ```

### Option 2: Using Python Module (Development/Testing)

If you haven't installed the package or are working from source, you can run the application directly using Python's module syntax:

1. **Show help**:
   ```bash
   python -m src.claude_env_manager.main --help
   ```

2. **Initialize configuration**:
   ```bash
   python -m src.claude_env_manager.main init
   ```

3. **Create a profile**:
   ```bash
   python -m src.claude_env_manager.main create --interactive
   ```

4. **List profiles**:
   ```bash
   python -m src.claude_env_manager.main list
   ```

5. **Apply a profile**:
   ```bash
   python -m src.claude_env_manager.main apply development
   ```

6. **Show configuration**:
   ```bash
   python -m src.claude_env_manager.main config
   ```

7. **View profile details**:
   ```bash
   python -m src.claude_env_manager.main show development --format json
   ```

**Note**: When using the Python module syntax, you need to run the command from the project root directory where the `src/` directory is located.

## Commands

| Command | Description |
|---------|-------------|
| `list, ls` | List all environment profiles |
| `create, new` | Create a new environment profile |
| `update, edit` | Update an existing profile |
| `delete, rm` | Delete an environment profile |
| `apply, use` | Apply a profile to Claude Code settings |
| `show, get` | Show profile details |
| `current` | Show current active profile |
| `config` | Show configuration information |
| `init` | Initialize configuration files |

## Configuration

The tool manages two main configuration files:

1. **Profile Configuration** (`~/.claude/claude-profiles.yml`):
   ```yaml
   profiles:
     - name: "development"
       env:
         ANTHROPIC_BASE_URL: "https://api.anthropic.com"
         ANTHROPIC_API_KEY: "sk-ant-api03-..."
         ANTHROPIC_MODEL: "claude-3-5-sonnet-20241022"
         ANTHROPIC_SMALL_FAST_MODEL: "claude-3-haiku-20240307"
       description: "Development environment"
       created: "2024-01-01T00:00:00Z"
       modified: "2024-01-01T00:00:00Z"
   
   default_profile: "development"
   ```

2. **Claude Code Settings** (`~/.claude/settings.json`):
   ```json
   {
     "env": {
       "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
       "ANTHROPIC_API_KEY": "sk-ant-api03-...",
       "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
       "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
     },
     "permissions": {
       "allow": [],
       "deny": []
     },
     "statusLine": {
       "type": "command",
       "command": "~/.claude/ccline/ccline",
       "padding": 0
     },
     "$schema": "https://json.schemastore.org/claude-code-settings.json"
   }
   ```

## Examples

### Using Installed CLI

#### Interactive Profile Creation
```bash
claude-env-manager create --interactive
```

#### Apply Profile with Confirmation
```bash
claude-env-manager apply production
```

#### View Profile Details
```bash
claude-env-manager show development --format json
```

#### Update Profile
```bash
claude-env-manager update development --api-key sk-ant-api03-new-key
```

### Using Python Module (Development/Testing)

#### Show Help and Available Commands
```bash
python -m src.claude_env_manager.main --help
```

#### Initialize Configuration
```bash
python -m src.claude_env_manager.main init
```

#### Interactive Profile Creation
```bash
python -m src.claude_env_manager.main create --interactive
```

#### List Profiles in Different Formats
```bash
python -m src.claude_env_manager.main list --format table
python -m src.claude_env_manager.main list --format json
python -m src.claude_env_manager.main list --format yaml
```

#### Create Profile Non-interactively
```bash
python -m src.claude_env_manager.main create \
  --name "development" \
  --base-url "https://api.anthropic.com" \
  --api-key "sk-ant-api03-your-key" \
  --model "claude-3-5-sonnet-20241022" \
  --fast-model "claude-3-haiku-20240307" \
  --description "Development environment"
```

#### Apply Profile with Force (Skip Confirmation)
```bash
python -m src.claude_env_manager.main apply development --force
```

#### Show Profile Details
```bash
python -m src.claude_env_manager.main show development
python -m src.claude_env_manager.main show development --format json
```

#### Update Profile
```bash
python -m src.claude_env_manager.main update development --api-key sk-ant-api03-new-key
```

#### Delete Profile with Force
```bash
python -m src.claude_env_manager.main delete old-profile --force
```

#### Set Default Profile
```bash
python -m src.claude_env_manager.main default development
```

#### Show Current Active Profile
```bash
python -m src.claude_env_manager.main current
```

#### Show Configuration Information
```bash
python -m src.claude_env_manager.main config
python -m src.claude_env_manager.main config --verbose
```

#### View Profile Interactively
```bash
python -m src.claude_env_manager.main show
# This will show an interactive profile selector
```

## Environment Variables

- `CLAUDE_ENV_MANAGER_CONFIG`: Path to custom configuration file
- `CLAUDE_ENV_MANAGER_SETTINGS`: Path to custom settings file

## Development

### Setup Development Environment
```bash
# Clone repository
git clone <repository-url>
cd claude-code-env-manager

# Install development dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .

# Run tests
pytest

# Run linting
black src/
isort src/
flake8 src/
mypy src/
```

### Project Structure
```
claude-code-env-manager/
├── src/claude_env_manager/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── api.py               # Core API classes
│   ├── models.py            # Data models
│   ├── cli/                 # CLI components
│   │   ├── commands.py      # Command implementations
│   │   └── interface.py     # TUI interface components
│   ├── utils/
│   │   ├── config.py        # Configuration management
│   │   ├── validation.py    # Input validation
│   │   └── io.py            # File I/O utilities
│   └── exceptions.py        # Custom exceptions
├── tests/                   # Test suite
├── config/                  # Default configurations
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

## Architecture

The application follows a three-layer architecture:

1. **TUI Layer**: CLI interface with Rich components for user interaction
2. **Business Logic Layer**: Core API for profile management and validation
3. **Data Access Layer**: File I/O operations for YAML and JSON handling

## Security

- API keys are validated for format and stored securely
- Configuration files are created with appropriate permissions
- Backup files are created before modifying settings
- Input validation prevents injection attacks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub issue tracker.