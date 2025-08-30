# Claude Code Environment Manager - API Reference

## 📖 Overview

The Claude Code Environment Manager API provides a comprehensive interface for managing Claude Code environment configurations through Python. This document covers all public APIs, data models, and usage examples.

## 🏗️ Core Classes

### ClaudeEnvManager

The main API class for managing Claude Code environment configurations.

```python
from claude_env_manager.api import ClaudeEnvManager

# Initialize with default paths
manager = ClaudeEnvManager()

# Initialize with custom paths
manager = ClaudeEnvManager(
    config_file="/path/to/config.yml",
    settings_file="/path/to/settings.json"
)
```

#### Constructor

```python
def __init__(self, config_file: str = None, settings_file: str = None)
```

**Parameters:**
- `config_file` (str, optional): Path to profile configuration file. Defaults to `~/.claude/claude-profiles.yml`
- `settings_file` (str, optional): Path to Claude Code settings file. Defaults to `~/.claude/settings.json`

#### Configuration Management

##### load_config()

```python
def load_config(self) -> ProfileConfig
```

Load configuration from YAML file. Returns cached configuration if available.

**Returns:** `ProfileConfig` - Loaded configuration object

**Raises:**
- `ConfigurationError`: Invalid YAML format or configuration structure
- `FileOperationError`: File access or read errors

**Example:**
```python
try:
    config = manager.load_config()
    print(f"Loaded {len(config.profiles)} profiles")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

##### save_config()

```python
def save_config(self, config: ProfileConfig) -> None
```

Save configuration to YAML file.

**Parameters:**
- `config` (ProfileConfig): Configuration object to save

**Raises:**
- `FileOperationError`: File write or permission errors

**Example:**
```python
config = manager.load_config()
config.default_profile = "development"
manager.save_config(config)
```

##### clear_cache()

```python
def clear_cache(self) -> None
```

Clear internal configuration and settings cache.

**Example:**
```python
manager.clear_cache()  # Force reload from disk
```

#### Profile Management

##### list_profiles()

```python
def list_profiles(self) -> List[EnvironmentProfile]
```

Get list of all environment profiles.

**Returns:** `List[EnvironmentProfile]` - List of profile objects

**Example:**
```python
profiles = manager.list_profiles()
for profile in profiles:
    print(f"{profile.name}: {profile.description}")
```

##### get_profile()

```python
def get_profile(self, name: str) -> EnvironmentProfile
```

Get a specific profile by name.

**Parameters:**
- `name` (str): Profile name to retrieve

**Returns:** `EnvironmentProfile` - Requested profile object

**Raises:**
- `ProfileNotFoundError`: Profile with given name not found

**Example:**
```python
try:
    profile = manager.get_profile("development")
    print(f"Profile model: {profile.env['ANTHROPIC_MODEL']}")
except ProfileNotFoundError:
    print("Profile not found")
```

##### create_profile()

```python
def create_profile(
    self, 
    name: str, 
    env_vars: Dict[str, str], 
    description: str = None
) -> EnvironmentProfile
```

Create a new environment profile.

**Parameters:**
- `name` (str): Profile name
- `env_vars` (Dict[str, str]): Environment variables dictionary
- `description` (str, optional): Profile description

**Returns:** `EnvironmentProfile` - Created profile object

**Raises:**
- `ProfileExistsError`: Profile with name already exists
- `InvalidProfileError`: Invalid profile data or validation failure

**Example:**
```python
env_vars = {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_API_KEY": "sk-ant-api03-test",
    "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
}

profile = manager.create_profile(
    name="development",
    env_vars=env_vars,
    description="Development environment"
)
```

##### update_profile()

```python
def update_profile(
    self, 
    name: str, 
    env_vars: Dict[str, str], 
    description: str = None
) -> EnvironmentProfile
```

Update an existing environment profile.

**Parameters:**
- `name` (str): Profile name to update
- `env_vars` (Dict[str, str]): Updated environment variables
- `description` (str, optional): Updated description

**Returns:** `EnvironmentProfile` - Updated profile object

**Raises:**
- `ProfileNotFoundError`: Profile not found
- `InvalidProfileError`: Invalid profile data

**Example:**
```python
updated = manager.update_profile(
    name="development",
    env_vars={"ANTHROPIC_MODEL": "claude-3-opus-20240229"},
    description="Updated development environment"
)
```

##### delete_profile()

```python
def delete_profile(self, name: str) -> bool
```

Delete an environment profile.

**Parameters:**
- `name` (str): Profile name to delete

**Returns:** `bool` - True if profile was deleted, False if not found

**Raises:**
- `ProfileNotFoundError`: Profile not found

**Example:**
```python
if manager.delete_profile("old-profile"):
    print("Profile deleted successfully")
```

##### apply_profile()

```python
def apply_profile(self, name: str) -> bool
```

Apply a profile to Claude Code settings.

**Parameters:**
- `name` (str): Profile name to apply

**Returns:** `bool` - True if profile was applied successfully

**Raises:**
- `ProfileNotFoundError`: Profile not found
- `SettingsFileError`: Settings file access or write errors

**Example:**
```python
try:
    success = manager.apply_profile("production")
    if success:
        print("Profile applied successfully")
except ProfileNotFoundError:
    print("Profile not found")
```

#### Profile State Management

##### get_current_profile()

```python
def get_current_profile(self) -> Optional[str]
```

Get the currently active profile name by comparing with settings.

**Returns:** `Optional[str]` - Current profile name or None if no match

**Example:**
```python
current = manager.get_current_profile()
if current:
    print(f"Active profile: {current}")
else:
    print("No active profile found")
```

##### get_default_profile()

```python
def get_default_profile(self) -> Optional[str]
```

Get the default profile name from configuration.

**Returns:** `Optional[str]` - Default profile name or None if not set

**Example:**
```python
default = manager.get_default_profile()
if default:
    print(f"Default profile: {default}")
```

##### set_default_profile()

```python
def set_default_profile(self, name: str) -> None
```

Set the default profile.

**Parameters:**
- `name` (str): Profile name to set as default

**Raises:**
- `ProfileNotFoundError`: Profile not found

**Example:**
```python
manager.set_default_profile("development")
```

##### validate_profile()

```python
def validate_profile(self, name: str) -> bool
```

Validate a profile's configuration.

**Parameters:**
- `name` (str): Profile name to validate

**Returns:** `bool` - True if profile is valid

**Example:**
```python
if manager.validate_profile("development"):
    print("Profile is valid")
else:
    print("Profile has validation errors")
```

#### Settings Management

##### load_settings()

```python
def load_settings(self) -> ClaudeSettings
```

Load Claude Code settings from JSON file.

**Returns:** `ClaudeSettings` - Loaded settings object

**Raises:**
- `SettingsFileError`: Settings file access or parse errors

**Example:**
```python
try:
    settings = manager.load_settings()
    print(f"Current model: {settings.env['ANTHROPIC_MODEL']}")
except SettingsFileError:
    print("Could not load settings")
```

##### get_current_settings()

```python
def get_current_settings(self) -> Dict[str, Any]
```

Get current settings as dictionary.

**Returns:** `Dict[str, Any]` - Settings dictionary or empty dict on error

**Example:**
```python
settings = manager.get_current_settings()
if settings:
    print(f"Base URL: {settings.get('env', {}).get('ANTHROPIC_BASE_URL')}")
```

#### Utility Methods

##### get_config_path()

```python
def get_config_path(self) -> str
```

Get the configuration file path.

**Returns:** `str` - Absolute path to configuration file

**Example:**
```python
config_path = manager.get_config_path()
print(f"Config file: {config_path}")
```

##### get_settings_path()

```python
def get_settings_path(self) -> str
```

Get the settings file path.

**Returns:** `str` - Absolute path to settings file

**Example:**
```python
settings_path = manager.get_settings_path()
print(f"Settings file: {settings_path}")
```

## 📊 Data Models

### EnvironmentProfile

Data model for environment profiles.

```python
@dataclass
class EnvironmentProfile:
    name: str
    env: Dict[str, str]
    description: Optional[str] = None
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
```

#### Methods

##### to_dict()

```python
def to_dict(self) -> Dict[str, Any]
```

Convert profile to dictionary.

**Returns:** `Dict[str, Any]` - Profile dictionary representation

##### from_dict()

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> EnvironmentProfile
```

Create profile from dictionary.

**Parameters:**
- `data` (Dict[str, Any]): Profile dictionary

**Returns:** `EnvironmentProfile` - Profile instance

##### update_env()

```python
def update_env(self, new_vars: Dict[str, str]) -> None
```

Update environment variables.

**Parameters:**
- `new_vars` (Dict[str, str]): New environment variables to merge

### ProfileConfig

Configuration model for profile management.

```python
@dataclass
class ProfileConfig:
    profiles: List[EnvironmentProfile] = field(default_factory=list)
    default_profile: Optional[str] = None
```

#### Methods

##### to_dict()

```python
def to_dict(self) -> Dict[str, Any]
```

Convert configuration to dictionary.

##### from_dict()

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> ProfileConfig
```

Create configuration from dictionary.

### ClaudeSettings

Settings model for Claude Code configuration.

```python
@dataclass
class ClaudeSettings:
    env: Dict[str, str]
    permissions: Dict[str, List[str]]
    status_line: Dict[str, Any]
    schema: str = "https://json.schemastore.org/claude-code-settings.json"
```

#### Methods

##### to_dict()

```python
def to_dict(self) -> Dict[str, Any]
```

Convert settings to dictionary.

##### from_dict()

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> ClaudeSettings
```

Create settings from dictionary.

##### update_env()

```python
def update_env(self, new_vars: Dict[str, str]) -> None
```

Update environment variables.

## 🚨 Exception Classes

### Base Exception

#### ClaudeEnvManagerError

Base exception class for all ClaudeEnvManager errors.

```python
class ClaudeEnvManagerError(Exception):
    pass
```

### Profile Management Errors

#### ProfileNotFoundError

Raised when a requested profile is not found.

```python
try:
    profile = manager.get_profile("nonexistent")
except ProfileNotFoundError as e:
    print(f"Profile not found: {e}")
```

#### ProfileExistsError

Raised when trying to create a profile that already exists.

```python
try:
    manager.create_profile("existing", env_vars)
except ProfileExistsError as e:
    print(f"Profile already exists: {e}")
```

#### InvalidProfileError

Raised when profile validation fails.

```python
try:
    manager.create_profile("invalid", invalid_env_vars)
except InvalidProfileError as e:
    print(f"Invalid profile: {e}")
```

### File Operation Errors

#### SettingsFileError

Raised when there's an error with the settings file.

```python
try:
    settings = manager.load_settings()
except SettingsFileError as e:
    print(f"Settings file error: {e}")
```

#### ConfigurationError

Raised when there's a configuration error.

```python
try:
    config = manager.load_config()
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

#### FileOperationError

Raised when file operations fail.

```python
try:
    manager.save_config(config)
except FileOperationError as e:
    print(f"File operation error: {e}")
```

### Validation Errors

#### ValidationError

Raised when validation fails.

```python
try:
    validate_profile_name("invalid@name")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## 💡 Usage Examples

### Basic Profile Management

```python
from claude_env_manager.api import ClaudeEnvManager

# Initialize manager
manager = ClaudeEnvManager()

# Create a development profile
dev_env = {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_API_KEY": "sk-ant-api03-dev-key",
    "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
}

manager.create_profile(
    name="development",
    env_vars=dev_env,
    description="Development environment"
)

# Create a production profile
prod_env = {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_API_KEY": "sk-ant-api03-prod-key",
    "ANTHROPIC_MODEL": "claude-3-opus-20240229",
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
}

manager.create_profile(
    name="production",
    env_vars=prod_env,
    description="Production environment"
)

# List all profiles
profiles = manager.list_profiles()
print(f"Available profiles: {[p.name for p in profiles]}")

# Set default profile
manager.set_default_profile("development")

# Apply development profile
manager.apply_profile("development")
```

### Profile Switching Workflow

```python
from claude_env_manager.api import ClaudeEnvManager

manager = ClaudeEnvManager()

def switch_environment(env_name):
    """Switch to a different environment profile."""
    try:
        # Check current profile
        current = manager.get_current_profile()
        if current == env_name:
            print(f"Already using {env_name} profile")
            return
        
        # Apply new profile
        success = manager.apply_profile(env_name)
        if success:
            print(f"Switched to {env_name} profile")
        else:
            print(f"Failed to switch to {env_name} profile")
            
    except ProfileNotFoundError:
        print(f"Profile {env_name} not found")
    except Exception as e:
        print(f"Error switching profile: {e}")

# Example usage
switch_environment("production")
```

### Profile Validation

```python
from claude_env_manager.api import ClaudeEnvManager

manager = ClaudeEnvManager()

def validate_all_profiles():
    """Validate all profiles in the configuration."""
    config = manager.load_config()
    
    print("Validating profiles...")
    for profile in config.profiles:
        try:
            # Re-create profile to trigger validation
            EnvironmentProfile(
                name=profile.name,
                env=profile.env,
                description=profile.description
            )
            print(f"✅ {profile.name}: Valid")
        except Exception as e:
            print(f"❌ {profile.name}: {e}")

validate_all_profiles()
```

### Custom Configuration Paths

```python
from claude_env_manager.api import ClaudeEnvManager
from pathlib import Path

# Use custom configuration paths
config_dir = Path.home() / ".custom-claude-config"
config_dir.mkdir(exist_ok=True)

manager = ClaudeEnvManager(
    config_file=str(config_dir / "profiles.yml"),
    settings_file=str(config_dir / "settings.json")
)

# Work with custom configuration
manager.create_profile(
    name="custom-profile",
    env_vars={
        "ANTHROPIC_BASE_URL": "https://custom.api.com",
        "ANTHROPIC_API_KEY": "sk-ant-api03-custom",
        "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
        "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
    }
)

print(f"Using config: {manager.get_config_path()}")
print(f"Using settings: {manager.get_settings_path()}")
```

## 🔗 Related Modules

- [models.py](../src/claude_env_manager/models.py) - Data model implementations
- [exceptions.py](../src/claude_env_manager/exceptions.py) - Exception definitions
- [utils/io.py](../src/claude_env_manager/utils/io.py) - File I/O utilities
- [utils/validation.py](../src/claude_env_manager/utils/validation.py) - Validation functions

*API Reference generated: 2025-08-30*