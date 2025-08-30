"""Configuration utilities for Claude Code Environment Manager."""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from ..exceptions import ConfigurationError


def get_default_config_path() -> Path:
    """Get the default configuration file path."""
    home = Path.home()
    return home / ".claude" / "claude-profiles.yml"


def get_default_settings_path() -> Path:
    """Get the default Claude Code settings file path."""
    home = Path.home()
    return home / ".claude" / "settings.json"


def get_config_path_from_env() -> Optional[Path]:
    """Get configuration file path from environment variable."""
    config_path = os.environ.get('CLAUDE_ENV_MANAGER_CONFIG')
    if config_path:
        return Path(config_path)
    return None


def get_settings_path_from_env() -> Optional[Path]:
    """Get settings file path from environment variable."""
    settings_path = os.environ.get('CLAUDE_ENV_MANAGER_SETTINGS')
    if settings_path:
        return Path(settings_path)
    return None


def resolve_config_path(config_path: Optional[str] = None) -> Path:
    """Resolve the configuration file path."""
    if config_path:
        return Path(config_path)
    
    # Check environment variable
    env_path = get_config_path_from_env()
    if env_path:
        return env_path
    
    # Use default
    return get_default_config_path()


def resolve_settings_path(settings_path: Optional[str] = None) -> Path:
    """Resolve the settings file path."""
    if settings_path:
        return Path(settings_path)
    
    # Check environment variable
    env_path = get_settings_path_from_env()
    if env_path:
        return env_path
    
    # Use default
    return get_default_settings_path()


def ensure_config_directory(config_path: Path) -> None:
    """Ensure the configuration directory exists."""
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)


def ensure_settings_directory(settings_path: Path) -> None:
    """Ensure the settings directory exists."""
    settings_dir = settings_path.parent
    settings_dir.mkdir(parents=True, exist_ok=True)


def get_user_home_dir() -> Path:
    """Get the user's home directory."""
    return Path.home()


def get_claude_config_dir() -> Path:
    """Get the Claude Code configuration directory."""
    return Path.home() / ".claude"


def is_claude_installed() -> bool:
    """Check if Claude Code is installed."""
    claude_dir = get_claude_config_dir()
    settings_file = claude_dir / "settings.json"
    return settings_file.exists()


def get_default_env_vars() -> Dict[str, str]:
    """Get default environment variables."""
    return {
        "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
        "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
        "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307",
        "ANTHROPIC_API_KEY": ""  # Will be filled by user
    }


def get_default_permissions() -> Dict[str, list]:
    """Get default permissions structure."""
    return {
        "allow": [],
        "deny": []
    }


def get_default_status_line() -> Dict[str, Any]:
    """Get default status line configuration."""
    # Platform-specific command path
    home = Path.home()
    if os.name == 'nt':  # Windows
        command = str(home / ".claude" / "ccline" / "ccline.exe")
    else:  # Unix-like
        command = str(home / ".claude" / "ccline" / "ccline")
    
    return {
        "type": "command",
        "command": command,
        "padding": 0
    }


def create_default_config() -> Dict[str, Any]:
    """Create a default configuration structure."""
    return {
        "profiles": [
            {
                "name": "development",
                "env": {
                    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                    "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                    "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307",
                    "ANTHROPIC_API_KEY": "sk-ant-api03-..."
                },
                "description": "Development environment",
                "created": "2024-01-01T00:00:00Z",
                "modified": "2024-01-01T00:00:00Z"
            }
        ],
        "default_profile": "development"
    }


def create_default_settings() -> Dict[str, Any]:
    """Create a default Claude Code settings structure."""
    return {
        "env": get_default_env_vars(),
        "permissions": get_default_permissions(),
        "statusLine": get_default_status_line(),
        "$schema": "https://json.schemastore.org/claude-code-settings.json"
    }


def validate_environment_setup() -> bool:
    """Validate that the environment is properly set up."""
    try:
        # Check if Claude Code is installed
        if not is_claude_installed():
            return False
        
        # Check if we can write to the config directory
        claude_dir = get_claude_config_dir()
        if not os.access(claude_dir, os.W_OK):
            return False
        
        return True
    
    except Exception:
        return False


def get_required_python_version() -> tuple:
    """Get the required Python version."""
    return (3, 11)


def check_python_version() -> bool:
    """Check if the current Python version meets requirements."""
    import sys
    current_version = sys.version_info[:2]
    required_version = get_required_python_version()
    
    return current_version >= required_version


def get_system_info() -> Dict[str, str]:
    """Get system information for debugging."""
    import sys
    import platform
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "system": platform.system(),
        "architecture": platform.machine(),
        "home_directory": str(Path.home()),
        "claude_config_dir": str(get_claude_config_dir()),
        "claude_installed": str(is_claude_installed())
    }