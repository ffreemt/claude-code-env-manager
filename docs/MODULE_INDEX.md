# Claude Code Environment Manager - Module Index

## 📋 Module Overview

This document provides a comprehensive, cross-referenced index of all modules in the Claude Code Environment Manager project. Each module includes detailed documentation, key functions, dependencies, and relationships with other modules.

## 🔗 Quick Navigation

### Core Modules
- [api.py](#api-py) - Core API and business logic
- [models.py](#models-py) - Data models and validation
- [exceptions.py](#exceptions-py) - Custom exceptions
- [main.py](#main-py) - CLI entry point

### CLI Components
- [cli/commands.py](#clicommandspy) - CLI command implementations
- [cli/interface.py](#cliinterfacepy) - TUI interface components
- [rich_cli.py](#rich_cli-py) - Rich CLI utilities

### Utility Modules
- [utils/config.py](#utilsconfigpy) - Configuration management
- [utils/validation.py](#utilsvalidationpy) - Input validation
- [utils/io.py](#utilsio-py) - File I/O operations

---

## 📖 Module Documentation

### api.py

**File**: `src/claude_env_manager/api.py`  
**Purpose**: Core API class and business logic implementation  
**Coverage**: 91% ✅  
**Lines**: 175  

#### Overview
The `api.py` module contains the main `ClaudeEnvManager` class which provides the primary interface for managing Claude Code environment configurations. It handles profile management, settings integration, and business logic validation.

#### Key Classes
- **ClaudeEnvManager**: Main API class for environment management

#### Key Functions
```python
# Configuration Management
def load_config() -> ProfileConfig
def save_config(config: ProfileConfig) -> None
def clear_cache() -> None

# Profile Management
def list_profiles() -> List[EnvironmentProfile]
def get_profile(name: str) -> EnvironmentProfile
def create_profile(name: str, env_vars: Dict[str, str], description: str = None) -> EnvironmentProfile
def update_profile(name: str, env_vars: Dict[str, str], description: str = None) -> EnvironmentProfile
def delete_profile(name: str) -> bool
def apply_profile(name: str) -> bool

# Profile State
def get_current_profile() -> Optional[str]
def get_default_profile() -> Optional[str]
def set_default_profile(name: str) -> None
def validate_profile(name: str) -> bool

# Settings Management
def load_settings() -> ClaudeSettings
def get_current_settings() -> Dict[str, Any]

# Utility Methods
def get_config_path() -> str
def get_settings_path() -> str
```

#### Dependencies
- **Internal**: models.py, exceptions.py, utils/io.py, utils/validation.py
- **External**: yaml, json, pathlib, typing, datetime

#### Usage Examples
```python
from claude_env_manager.api import ClaudeEnvManager

# Initialize manager
manager = ClaudeEnvManager()

# Create and manage profiles
profile = manager.create_profile(
    name="development",
    env_vars={
        "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
        "ANTHROPIC_API_KEY": "sk-ant-api03-test",
        "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
        "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
    }
)

# Apply profile
manager.apply_profile("development")
```

#### Related Modules
- [models.py](#models-py) - Data models used by API
- [utils/io.py](#utilsio-py) - File I/O operations
- [utils/validation.py](#utilsvalidationpy) - Validation functions

---

### models.py

**File**: `src/claude_env_manager/models.py`  
**Purpose**: Data models and validation rules  
**Coverage**: 100% ✅  
**Lines**: 113  

#### Overview
The `models.py` module defines the core data structures used throughout the application, including environment profiles, configuration containers, and settings models. All models include built-in validation and serialization capabilities.

#### Key Classes
- **EnvironmentProfile**: Environment profile data model with validation
- **ProfileConfig**: Configuration container for profiles
- **ClaudeSettings**: Claude Code settings model

#### Key Functions
```python
# EnvironmentProfile
def to_dict() -> Dict[str, Any]
def from_dict(data: Dict[str, Any]) -> EnvironmentProfile
def update_env(new_vars: Dict[str, str]) -> None

# ProfileConfig
def to_dict() -> Dict[str, Any]
def from_dict(data: Dict[str, Any]) -> ProfileConfig

# ClaudeSettings
def to_dict() -> Dict[str, Any]
def from_dict(data: Dict[str, Any]) -> ClaudeSettings
def update_env(new_vars: Dict[str, str]) -> None
```

#### Dependencies
- **Internal**: exceptions.py (via validation)
- **External**: dataclasses, datetime, typing, json, re, pathlib

#### Data Validation
- **Profile Names**: Non-empty, alphanumeric with hyphens/underscores
- **API Keys**: Must start with "sk-" prefix
- **Base URLs**: Must use http:// or https:// protocol
- **Model Names**: Must be valid model name formats
- **Environment Variables**: Required fields validation

#### Usage Examples
```python
from claude_env_manager.models import EnvironmentProfile, ProfileConfig

# Create profile
profile = EnvironmentProfile(
    name="development",
    env={
        "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
        "ANTHROPIC_API_KEY": "sk-ant-api03-test",
        "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
        "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
    },
    description="Development environment"
)

# Create configuration
config = ProfileConfig(
    profiles=[profile],
    default_profile="development"
)
```

#### Related Modules
- [api.py](#api-py) - Uses models for data structures
- [utils/validation.py](#utilsvalidationpy) - Validation logic

---

### exceptions.py

**File**: `src/claude_env_manager/exceptions.py`  
**Purpose**: Custom exception classes  
**Coverage**: 100% ✅  
**Lines**: 16  

#### Overview
The `exceptions.py` module defines a hierarchical exception structure for error handling throughout the application. All custom exceptions inherit from the base `ClaudeEnvManagerError` class.

#### Key Classes
- **ClaudeEnvManagerError**: Base exception class
- **ProfileNotFoundError**: Profile not found errors
- **ProfileExistsError**: Profile already exists errors
- **InvalidProfileError**: Profile validation errors
- **SettingsFileError**: Settings file operation errors
- **ConfigurationError**: Configuration management errors
- **ValidationError**: Input validation errors
- **FileOperationError**: File operation errors

#### Exception Hierarchy
```
ClaudeEnvManagerError (base)
├── ProfileNotFoundError
├── ProfileExistsError
├── InvalidProfileError
├── SettingsFileError
├── ConfigurationError
├── ValidationError
└── FileOperationError
```

#### Usage Examples
```python
from claude_env_manager.exceptions import ProfileNotFoundError, ValidationError

try:
    # Profile operation that might fail
    profile = manager.get_profile("nonexistent")
except ProfileNotFoundError:
    print("Profile not found")
except ValidationError as e:
    print(f"Validation error: {e}")
```

#### Related Modules
- [api.py](#api-py) - Raises and handles exceptions
- [utils/validation.py](#utilsvalidationpy) - Validation errors

---

### main.py

**File**: `src/claude_env_manager/main.py`  
**Purpose**: CLI entry point and command routing  
**Coverage**: 0% ❌  
**Lines**: 28  

#### Overview
The `main.py` module serves as the entry point for the CLI application. It sets up the Click framework, registers commands, and provides the main execution function.

#### Key Functions
```python
def main() -> None  # Main entry point
def cli() -> None   # CLI group setup
```

#### Dependencies
- **Internal**: cli/commands.py
- **External**: click

#### Command Structure
```bash
claude-env-manager --help
# Shows main help and available commands

claude-env-manager list
# List all profiles

claude-env-manager create --interactive
# Create profile interactively
```

#### Related Modules
- [cli/commands.py](#clicommandspy) - Command implementations
- [rich_cli.py](#rich_cli-py) - CLI utilities

---

### cli/commands.py

**File**: `src/claude_env_manager/cli/commands.py`  
**Purpose**: CLI command implementations  
**Coverage**: 0% ❌  
**Lines**: 294  

#### Overview
The `cli/commands.py` module contains the implementations of all CLI commands. It handles user input, argument parsing, and coordination with the core API.

#### Key Functions
```python
# Profile Management Commands
def list_profiles(ctx, format, verbose)
def create_profile(ctx, name, interactive, api_key, base_url, model, fast_model, description)
def update_profile(ctx, name, api_key, base_url, model, fast_model, description)
def delete_profile(ctx, name, force)
def apply_profile(ctx, name, backup, dry_run)

# Profile Information Commands
def show_profile(ctx, name, format)
def current_profile(ctx)
def get_default_profile(ctx)
def set_default_profile(ctx, name)

# Configuration Commands
def show_config(ctx)
def init_config(ctx, force)

# Utility Commands
def validate_profiles(ctx, name)
def export_profiles(ctx, format, output)
def import_profiles(ctx, input_file, format, merge)
```

#### Dependencies
- **Internal**: api.py, cli/interface.py, models.py
- **External**: click, rich, pathlib

#### Command Categories
- **Profile Management**: create, update, delete, list, apply
- **Profile Information**: show, current, default
- **Configuration**: config, init
- **Utilities**: validate, export, import

#### Usage Examples
```python
# In CLI usage:
claude-env-manager create --name development --interactive
claude-env-manager apply production --backup
claude-env-manager list --format json
```

#### Related Modules
- [api.py](#api-py) - Core API operations
- [cli/interface.py](#cliinterfacepy) - TUI components
- [rich_cli.py](#rich_cli-py) - Rich utilities

---

### cli/interface.py

**File**: `src/claude_env_manager/cli/interface.py`  
**Purpose**: TUI interface components  
**Coverage**: 0% ❌  
**Lines**: 307  

#### Overview
The `cli/interface.py` module provides terminal user interface components using the Rich library. It handles interactive forms, profile selection, and visual feedback.

#### Key Functions
```python
# Interactive Forms
def interactive_profile_form(ctx, existing_profile=None)
def interactive_profile_selection(ctx, allow_create=True)
def interactive_settings_form(ctx, current_settings=None)

# Display Components
def show_profile_table(profiles, verbose=False)
def show_profile_details(profile, format="table")
def show_settings_table(settings)
def show_success_message(message)
def show_warning_message(message)
def show_error_message(message)

# Progress and Status
def show_progress_bar(description, total=100)
def show_status_message(message, status="info")

# Confirmation Dialogs
def confirm_action(message, default=False)
def confirm_deletion(profile_name)
def confirm_profile_apply(profile_name, current_settings)
```

#### Dependencies
- **Internal**: cli/commands.py, models.py
- **External**: rich, click

#### UI Components
- **Forms**: Interactive data entry forms
- **Tables**: Rich table displays for profiles and settings
- **Progress**: Progress bars and status indicators
- **Dialogs**: Confirmation and input dialogs

#### Usage Examples
```python
# Interactive profile creation
profile_data = interactive_profile_form(ctx)

# Profile selection
selected = interactive_profile_selection(ctx)

# Display profile table
show_profile_table(profiles, verbose=True)
```

#### Related Modules
- [cli/commands.py](#clicommandspy) - Uses interface components
- [rich_cli.py](#rich_cli-py) - Rich utilities

---

### rich_cli.py

**File**: `src/claude_env_manager/rich_cli.py`  
**Purpose**: Rich CLI utilities  
**Coverage**: 0% ❌  
**Lines**: 35  

#### Overview
The `rich_cli.py` module provides utility functions for working with the Rich library, including console styling, table formatting, and progress indicators.

#### Key Functions
```python
def create_console(theme=None)
def create_table(title, columns, data=None)
def create_progress_bar(total, description="")
def format_success(text)
def format_warning(text)
def format_error(text)
def format_info(text)
def print_banner(text)
def print_section_header(text)
```

#### Dependencies
- **External**: rich

#### Utility Categories
- **Console**: Rich console management
- **Tables**: Table creation and formatting
- **Progress**: Progress bars and indicators
- **Styling**: Text formatting and styling

#### Usage Examples
```python
from claude_env_manager.rich_cli import create_console, create_table

console = create_console()
table = create_table("Profiles", ["Name", "Description"], profiles)
console.print(table)
```

#### Related Modules
- [cli/interface.py](#cliinterfacepy) - Uses Rich utilities
- [cli/commands.py](#clicommandspy) - CLI styling

---

### utils/config.py

**File**: `src/claude_env_manager/utils/config.py`  
**Purpose**: Configuration management utilities  
**Coverage**: 29% 🟡  
**Lines**: 83  

#### Overview
The `utils/config.py` module provides utilities for configuration file management, including YAML parsing, configuration validation, and path resolution.

#### Key Functions
```python
# Configuration Loading
def load_yaml_config(file_path: Path) -> Dict[str, Any]
def save_yaml_config(data: Dict[str, Any], file_path: Path) -> None

# Configuration Validation
def validate_config_structure(config: Dict[str, Any]) -> bool
def validate_profile_config(profile: Dict[str, Any]) -> bool

# Path Management
def get_default_config_path() -> Path
def get_default_settings_path() -> Path
def ensure_config_directory(path: Path) -> None

# Configuration Migration
def migrate_config_format(config: Dict[str, Any]) -> Dict[str, Any]
def backup_config_file(file_path: Path) -> Path
```

#### Dependencies
- **Internal**: exceptions.py, utils/io.py
- **External**: yaml, pathlib

#### Configuration Formats
- **YAML**: Primary configuration format
- **JSON**: Settings file format
- **Environment Variables**: Configuration overrides

#### Usage Examples
```python
from claude_env_manager.utils.config import load_yaml_config, save_yaml_config

# Load configuration
config = load_yaml_config(Path("config.yml"))

# Save configuration
save_yaml_config(config_data, Path("config.yml"))
```

#### Related Modules
- [api.py](#api-py) - Uses configuration utilities
- [utils/io.py](#utilsio-py) - File I/O operations

---

### utils/validation.py

**File**: `src/claude_env_manager/utils/validation.py`  
**Purpose**: Input validation utilities  
**Coverage**: 36% 🟡  
**Lines**: 125  

#### Overview
The `utils/validation.py` module provides comprehensive input validation functions for profile names, environment variables, API keys, and other user inputs.

#### Key Functions
```python
# Profile Validation
def validate_profile_name(name: str) -> bool
def validate_profile_description(description: str) -> bool

# Environment Variable Validation
def validate_environment_vars(env_vars: Dict[str, str]) -> bool
def validate_api_key_format(api_key: str) -> bool
def validate_base_url_format(base_url: str) -> bool
def validate_model_name_format(model_name: str) -> bool

# General Validation
def validate_required_fields(data: Dict[str, Any], required: List[str]) -> bool
def validate_url_format(url: str) -> bool
def validate_file_path(path: str) -> bool

# Sanitization
def sanitize_profile_name(name: str) -> str
def sanitize_input(input_str: str) -> str
```

#### Dependencies
- **Internal**: exceptions.py
- **External**: re, typing, pathlib

#### Validation Rules
- **Profile Names**: Alphanumeric, hyphens, underscores, 3-50 characters
- **API Keys**: Must start with "sk-", valid character set
- **Base URLs**: Must use http:// or https://, valid URL format
- **Model Names**: Valid model name patterns, no special characters
- **Environment Variables**: Required field validation

#### Usage Examples
```python
from claude_env_manager.utils.validation import (
    validate_profile_name,
    validate_api_key_format,
    validate_environment_vars
)

# Validate profile name
if validate_profile_name("development"):
    print("Valid profile name")

# Validate API key
if validate_api_key_format("sk-ant-api03-test"):
    print("Valid API key")

# Validate environment variables
if validate_environment_vars(env_vars):
    print("Valid environment variables")
```

#### Related Modules
- [models.py](#models-py) - Uses validation in model validation
- [api.py](#api-py) - Uses validation for profile operations

---

### utils/io.py

**File**: `src/claude_env_manager/utils/io.py`  
**Purpose**: File I/O operations utilities  
**Coverage**: 29% 🟡  
**Lines**: 65  

#### Overview
The `utils/io.py` module provides safe file I/O operations, backup creation, and error handling for file operations throughout the application.

#### Key Functions
```python
# File Operations
def safe_read_file(file_path: Path) -> Optional[str]
def safe_write_file(file_path: Path, content: str) -> bool
def safe_read_json(file_path: Path) -> Optional[Dict[str, Any]]
def safe_write_json(file_path: Path, data: Dict[str, Any]) -> bool

# Backup Operations
def create_backup(file_path: Path) -> Optional[Path]
def restore_backup(backup_path: Path, target_path: Path) -> bool
def list_backups(file_path: Path) -> List[Path]

# File Management
def ensure_directory_exists(path: Path) -> bool
def get_file_size(file_path: Path) -> int
def file_exists(file_path: Path) -> bool
def remove_file(file_path: Path) -> bool

# Path Operations
def get_relative_path(path: Path, base_path: Path) -> Path
def normalize_path(path: str) -> Path
```

#### Dependencies
- **Internal**: exceptions.py
- **External**: json, pathlib, datetime, shutil

#### File Operations
- **Safe Reading**: Handles file not found, permission errors
- **Safe Writing**: Atomic writes with error handling
- **Backup Creation**: Timestamped backup files
- **Directory Management**: Directory creation and validation

#### Usage Examples
```python
from claude_env_manager.utils.io import (
    safe_read_file,
    safe_write_file,
    create_backup
)

# Read file safely
content = safe_read_file(Path("config.yml"))

# Write file safely
success = safe_write_file(Path("config.yml"), content)

# Create backup
backup_path = create_backup(Path("settings.json"))
```

#### Related Modules
- [api.py](#api-py) - Uses file I/O for configuration
- [utils/config.py](#utilsconfigpy) - Uses file I/O for config management

---

## 🔗 Cross-Reference Matrix

### Module Dependencies

| Module | api.py | models.py | exceptions.py | main.py | cli/commands.py | cli/interface.py | rich_cli.py | utils/config.py | utils/validation.py | utils/io.py |
|--------|--------|-----------|---------------|---------|-----------------|------------------|-------------|-----------------|-------------------|-------------|
| **api.py** | - | ✅ | ✅ | - | - | - | - | ✅ | ✅ | ✅ |
| **models.py** | - | - | ✅ | - | - | - | - | - | ✅ | - |
| **exceptions.py** | - | - | - | - | - | - | - | - | ✅ | ✅ |
| **main.py** | - | - | - | - | ✅ | - | ✅ | - | - | - |
| **cli/commands.py** | ✅ | ✅ | ✅ | - | - | ✅ | ✅ | - | ✅ | - |
| **cli/interface.py** | - | ✅ | - | - | - | - | ✅ | - | - | - |
| **rich_cli.py** | - | - | - | - | - | - | - | - | - | - |
| **utils/config.py** | - | - | ✅ | - | - | - | - | - | - | ✅ |
| **utils/validation.py** | - | - | ✅ | - | - | - | - | - | - | - |
| **utils/io.py** | - | - | ✅ | - | - | - | - | - | - | - |

### Test Coverage by Module

| Module | Coverage | Status | Test Count |
|--------|----------|---------|------------|
| **api.py** | 91% | ✅ Excellent | 30 |
| **models.py** | 100% | ✅ Perfect | 11 |
| **exceptions.py** | 100% | ✅ Perfect | N/A |
| **main.py** | 0% | ❌ No Tests | 0 |
| **cli/commands.py** | 0% | ❌ No Tests | 0 |
| **cli/interface.py** | 0% | ❌ No Tests | 0 |
| **rich_cli.py** | 0% | ❌ No Tests | 0 |
| **utils/config.py** | 29% | 🟡 Needs Work | N/A |
| **utils/validation.py** | 36% | 🟡 Needs Work | N/A |
| **utils/io.py** | 29% | 🟡 Needs Work | N/A |

### Function Categories by Module

| Module | Data Models | Business Logic | CLI/UI | I/O Operations | Validation | Utilities |
|--------|------------|----------------|---------|----------------|------------|-----------|
| **api.py** | - | ✅ | - | - | ✅ | ✅ |
| **models.py** | ✅ | ✅ | - | - | ✅ | - |
| **exceptions.py** | - | - | - | - | - | ✅ |
| **main.py** | - | - | ✅ | - | - | - |
| **cli/commands.py** | - | ✅ | ✅ | - | ✅ | - |
| **cli/interface.py** | - | - | ✅ | - | - | ✅ |
| **rich_cli.py** | - | - | ✅ | - | - | ✅ |
| **utils/config.py** | - | - | - | ✅ | ✅ | ✅ |
| **utils/validation.py** | - | - | - | - | ✅ | ✅ |
| **utils/io.py** | - | - | - | ✅ | - | ✅ |

---

## 🎯 Development Guidelines

### Adding New Modules

1. **Module Creation**: Create new modules in appropriate directories
2. **Dependencies**: Minimize cross-module dependencies
3. **Documentation**: Add comprehensive docstrings and examples
4. **Testing**: Write comprehensive tests for new functionality
5. **Integration**: Update cross-reference matrix and documentation

### Module Responsibilities

- **Core Modules**: Business logic, data models, and core functionality
- **CLI Modules**: User interface and command handling
- **Utility Modules**: Shared functionality and helper functions
- **External Dependencies**: Minimize and document external dependencies

### Testing Requirements

- **Core Modules**: Target 90%+ test coverage
- **CLI Modules**: Target 80%+ test coverage
- **Utility Modules**: Target 70%+ test coverage
- **Integration Tests**: Test cross-module interactions

---

*Module Index generated: 2025-08-30*