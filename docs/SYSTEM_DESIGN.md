# Claude Code Environment Manager - System Design

## Overview
A modern Python TUI application for managing Claude Code environment configurations across multiple profiles, with seamless integration to `~/.claude/settings.json` and YAML-based profile management.

## System Architecture

### High-Level Components
```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Env Manager                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   TUI Layer     │  │  Business Logic │  │  Data Access    │ │
│  │                 │  │     Layer       │  │     Layer       │ │
│  │ • CLI Interface │  │ • Profile Mgmt  │  │ • JSON Handler  │ │
│  │ • Rich UI       │  │ • Validation    │  │ • YAML Handler  │ │
│  │ • Event System  │  │ • Config Sync   │  │ • File I/O      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. TUI Layer (Presentation)
- **CLI Interface**: Argument parsing and command routing
- **Rich UI Components**: Interactive terminal interface
- **Event System**: User interaction handling

#### 2. Business Logic Layer (Core)
- **Profile Management**: CRUD operations for environment profiles
- **Validation**: Input validation and error handling
- **Configuration Sync**: Bi-directional sync between YAML and JSON

#### 3. Data Access Layer (Persistence)
- **JSON Handler**: Read/write `~/.claude/settings.json`
- **YAML Handler**: Read/write profile configuration files
- **File I/O**: Safe file operations with backup/restore

## Data Models

### 1. Environment Profile (YAML Structure)
```yaml
# claude-profiles.yml
profiles:
  - name: "development"
    env:
      ANTHROPIC_BASE_URL: "https://api.anthropic.com"
      ANTHROPIC_API_KEY: "sk-dev-..."
      ANTHROPIC_MODEL: "claude-3-5-sonnet-20241022"
      ANTHROPIC_SMALL_FAST_MODEL: "claude-3-haiku-20240307"
    description: "Development environment"
    created: "2024-01-01T00:00:00Z"
    modified: "2024-01-01T00:00:00Z"

  - name: "production"
    env:
      ANTHROPIC_BASE_URL: "https://api.anthropic.com"
      ANTHROPIC_API_KEY: "sk-prod-..."
      ANTHROPIC_MODEL: "claude-3-5-sonnet-20241022"
      ANTHROPIC_SMALL_FAST_MODEL: "claude-3-haiku-20240307"
    description: "Production environment"
    created: "2024-01-01T00:00:00Z"
    modified: "2024-01-01T00:00:00Z"

default_profile: "development"
```

### 2. Settings JSON Structure
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_API_KEY": "sk-...",
    "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
  },
  "permissions": {
    "allow": [],
    "deny": []
  },
  "statusLine": {
    "type": "command",
    "command": "%USERPROFILE%/.claude/ccline/ccline.exe",
    "padding": 0
  },
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

## API Specification

### 1. Core API Class

```python
class ClaudeEnvManager:
    """Main API for managing Claude Code environment configurations."""
    
    def __init__(self, config_file: str = None):
        """Initialize with optional config file path."""
        
    def load_profiles(self) -> List[EnvironmentProfile]:
        """Load all profiles from YAML configuration."""
        
    def save_profiles(self, profiles: List[EnvironmentProfile]) -> None:
        """Save profiles to YAML configuration."""
        
    def create_profile(self, name: str, env_vars: Dict[str, str], 
                      description: str = None) -> EnvironmentProfile:
        """Create a new environment profile."""
        
    def update_profile(self, name: str, env_vars: Dict[str, str] = None, 
                      description: str = None) -> EnvironmentProfile:
        """Update an existing environment profile."""
        
    def delete_profile(self, name: str) -> bool:
        """Delete an environment profile."""
        
    def get_profile(self, name: str) -> EnvironmentProfile:
        """Get a specific profile by name."""
        
    def apply_profile(self, name: str) -> bool:
        """Apply profile to Claude Code settings.json."""
        
    def get_current_settings(self) -> Dict[str, Any]:
        """Get current Claude Code settings."""
        
    def set_default_profile(self, name: str) -> None:
        """Set the default profile."""
```

### 2. Data Model Classes

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class EnvironmentProfile:
    """Environment profile data model."""
    name: str
    env: Dict[str, str]
    description: Optional[str] = None
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

@dataclass
class ClaudeSettings:
    """Claude Code settings data model."""
    env: Dict[str, str]
    permissions: Dict[str, List[str]]
    status_line: Dict[str, Any]
    schema: str = "https://json.schemastore.org/claude-code-settings.json"
```

## TUI Interface Design

### 1. CLI Command Structure
```
claude-env-manager <command> [options]

Commands:
  list, ls          List all environment profiles
  create, new       Create a new environment profile
  update, edit      Update an existing profile
  delete, rm        Delete an environment profile
  apply, use        Apply a profile to Claude Code
  show, get         Show profile details
  current           Show current active profile
  config            Show configuration info
  init              Initialize configuration

Options:
  --config FILE     Configuration file path
  --verbose, -v     Verbose output
  --quiet, -q       Quiet mode
  --help, -h        Show help
  --version, -V     Show version
```

### 2. TUI Component Design

#### Profile Selection Interface
```
┌─────────────────────────────────────────────────────────────────┐
│                 Select Environment Profile                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   📁 Development Environment                                   │
│      Base URL: https://api.anthropic.com                        │
│      Model: claude-3-5-sonnet-20241022                          │
│      Fast Model: claude-3-haiku-20240307                        │
│                                                                 │
│   📁 Production Environment                                    │
│      Base URL: https://api.anthropic.com                        │
│      Model: claude-3-5-sonnet-20241022                          │
│      Fast Model: claude-3-haiku-20240307                        │
│                                                                 │
│   📁 Local Testing                                             │
│      Base URL: http://localhost:8056                           │
│      Model: claude-3-haiku-20240307                            │
│      Fast Model: claude-3-haiku-20240307                        │
│                                                                 │
│                                                                 │
│   [Enter] Select  [e] Edit  [n] New  [d] Delete  [q] Quit       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Profile Creation/Edit Interface
```
┌─────────────────────────────────────────────────────────────────┐
│                   Create/Edit Profile                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Profile Name: [my-new-profile      ]                          │
│   Description:  [For local development]                          │
│                                                                 │
│   Environment Variables:                                        │
│                                                                 │
│   ANTHROPIC_BASE_URL: [https://api.anthropic.com       ]       │
│   ANTHROPIC_API_KEY:   [sk-ant-api03-...             ]       │
│   ANTHROPIC_MODEL:     [claude-3-5-sonnet-20241022  ]       │
│   ANTHROPIC_FAST_MODEL:[claude-3-haiku-20240307     ]       │
│                                                                 │
│                                                                 │
│   [Save] [Cancel] [Validate] [Test Connection]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core Dependencies
- **Python 3.11+**: Base language with modern type hints
- **click**: CLI framework for command-line interface
- **rich**: Rich text and beautiful formatting for the TUI
- **PyYAML**: YAML file parsing and generation
- **pydantic**: Data validation and serialization
- **pathlib**: Modern path handling (cross-platform)

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Optional Dependencies
- **textual**: Advanced TUI framework (if richer interface needed)
- **python-dotenv**: Environment variable loading
- **requests**: HTTP testing for API connections

## File Structure

```
claude-code-env-manager/
├── src/
│   ├── claude_env_manager/
│   │   ├── __init__.py
│   │   ├── main.py              # CLI entry point
│   │   ├── api.py               # Core API classes
│   │   ├── models.py            # Data models
│   │   ├── cli/                 # CLI components
│   │   │   ├── __init__.py
│   │   │   ├── commands.py      # Command implementations
│   │   │   └── interface.py     # TUI interface components
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Configuration management
│   │   │   ├── validation.py    # Input validation
│   │   │   └── io.py            # File I/O utilities
│   │   └── exceptions.py        # Custom exceptions
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_models.py
│   ├── test_cli.py
│   └── test_utils.py
├── config/
│   ├── claude-profiles.yml     # Default profiles config
│   └── settings-schema.json    # Claude settings schema
├── scripts/
│   ├── install.sh              # Installation script
│   └── setup-dev.sh            # Development setup
├── docs/
│   ├── README.md              # User documentation
│   ├── API.md                 # API documentation
│   └── DEVELOPMENT.md         # Developer guide
├── pyproject.toml             # Project configuration
├── requirements.txt           # Dependencies
├── requirements-dev.txt       # Development dependencies
├── .gitignore               # Git ignore rules
└── README.md                # Project readme
```

## Key Design Decisions

### 1. Configuration Management
- **YAML for Profiles**: Human-readable, commentable configuration format
- **JSON for Settings**: Maintain compatibility with Claude Code format
- **Dual Sync**: Bi-directional synchronization between YAML profiles and JSON settings

### 2. Validation Strategy
- **Pydantic Models**: Type validation and serialization
- **Environment Variable Validation**: Validate API keys and URLs
- **Schema Validation**: JSON schema validation for settings file

### 3. Error Handling
- **Custom Exceptions**: Clear, actionable error messages
- **Graceful Degradation**: Continue operating with partial functionality
- **User-Friendly Messages**: Clear guidance for resolution

### 4. Performance Considerations
- **Lazy Loading**: Load profiles only when needed
- **Caching**: In-memory caching for frequent operations
- **Minimal I/O**: Reduce file operations to essential ones

## Security Considerations

### 1. API Key Protection
- **Secure Storage**: Encrypt sensitive data in configuration files
- **Environment Variables**: Support reading sensitive data from environment
- **Access Control**: Restrict file permissions to user-only

### 2. File Operations
- **Atomic Updates**: Write to temporary files, then rename
- **Backup Creation**: Automatic backups before modifications
- **Validation**: Validate syntax before applying changes

### 3. Input Validation
- **Sanitization**: Validate all user inputs
- **URL Validation**: Ensure base URLs are properly formatted
- **API Key Format**: Validate API key formats (e.g., "sk-ant-*")

## Future Extensibility

### 1. Plugin Architecture
- **Profile Sources**: Support multiple profile sources (Git, S3, etc.)
- **Validation Plugins**: Custom validation rules
- **UI Themes**: Multiple TUI themes and layouts

### 2. Integration Points
- **CI/CD Integration**: Environment management in pipelines
- **Cloud Providers**: Direct integration with cloud services
- **Template Engine**: Profile templating and generation

### 3. Advanced Features
- **Profile Versioning**: Track changes over time
- **Team Sharing**: Collaborative profile management
- **Analytics**: Usage statistics and optimization

## Implementation Phases

### Phase 1: Core Functionality
- [ ] Basic CLI structure with click
- [ ] YAML profile management
- [ ] JSON settings manipulation
- [ ] Create/Read/Update/Delete profile operations

### Phase 2: TUI Interface
- [ ] Rich-based TUI components
- [ ] Interactive profile selection
- [ ] Profile creation/editing interface
- [ ] Real-time validation and feedback

### Phase 3: Advanced Features
- [ ] Profile testing and validation
- [ ] Backup and restore functionality
- [ ] Import/export capabilities
- [ ] Configuration templates

### Phase 4: Polish and Optimization
- [ ] Performance optimization
- [ ] Enhanced error handling
- [ ] Documentation and examples
- [ ] Testing and quality assurance

This design provides a comprehensive foundation for a fast, delightful, and maintainable Claude Code environment management tool.