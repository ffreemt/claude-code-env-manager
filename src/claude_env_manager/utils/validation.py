"""Validation utilities for Claude Code Environment Manager."""

import re
from typing import Dict, Any
from urllib.parse import urlparse
from ..exceptions import ValidationError


def validate_profile_name(name: str) -> None:
    """Validate profile name."""
    if not name:
        raise ValidationError("Profile name is required")
    
    if len(name) > 50:
        raise ValidationError("Profile name must be 50 characters or less")
    
    # Only allow alphanumeric characters, hyphens, and underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise ValidationError("Profile name can only contain letters, numbers, hyphens, and underscores")
    
    # Cannot start or end with hyphen or underscore
    if name.startswith(('-', '_')) or name.endswith(('-', '_')):
        raise ValidationError("Profile name cannot start or end with hyphen or underscore")


def validate_environment_vars(env_vars: Dict[str, str], partial: bool = False) -> None:
    """Validate environment variables."""
    if not env_vars:
        raise ValidationError("Environment variables are required")
    
    # For partial updates, only validate the provided variables
    if partial:
        for var, value in env_vars.items():
            if not value:
                raise ValidationError(f"Environment variable '{var}' cannot be empty")
            # Validate specific variables if they are provided
            if var == "ANTHROPIC_API_KEY":
                validate_api_key(value)
            elif var == "ANTHROPIC_BASE_URL":
                validate_base_url(value)
            elif var in ("ANTHROPIC_MODEL", "ANTHROPIC_SMALL_FAST_MODEL"):
                validate_model_name(value)
    else:
        # For full profile creation, validate all required variables
        required_vars = [
            "ANTHROPIC_BASE_URL",
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_MODEL",
            "ANTHROPIC_SMALL_FAST_MODEL"
        ]
        
        # Check required variables
        for var in required_vars:
            if var not in env_vars:
                raise ValidationError(f"Required environment variable '{var}' is missing")
            if not env_vars[var]:
                raise ValidationError(f"Environment variable '{var}' cannot be empty")
        
        # Validate specific variables
        validate_api_key(env_vars.get("ANTHROPIC_API_KEY", ""))
        validate_base_url(env_vars.get("ANTHROPIC_BASE_URL", ""))
        validate_model_name(env_vars.get("ANTHROPIC_MODEL", ""))
        validate_model_name(env_vars.get("ANTHROPIC_SMALL_FAST_MODEL", ""))


def validate_api_key(api_key: str) -> None:
    """Validate Anthropic API key format."""
    if not api_key:
        raise ValidationError("API key is required")
    
    if not api_key.startswith("sk-"):
        raise ValidationError("API key must start with 'sk-'")
    
    # Relaxed length check for development and testing
    # Production API keys are typically 100+ characters, but allow shorter for testing
    if len(api_key) < 5:
        raise ValidationError("API key appears to be too short (minimum 5 characters)")


def validate_base_url(url: str) -> None:
    """Validate base URL."""
    if not url:
        raise ValidationError("Base URL is required")
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError("Base URL must be a valid URL")
        
        if parsed.scheme not in ('http', 'https'):
            raise ValidationError("Base URL must use HTTP or HTTPS protocol")
        
        # Accept any valid base URL
        # Note: Removed restriction to anthropic.com or localhost only
    
    except Exception as e:
        if "must be a valid URL" in str(e):
            raise ValidationError("Base URL must be a valid URL")
        raise ValidationError(f"Invalid base URL: {e}")


def validate_model_name(model: str) -> None:
    """Validate model name."""
    if not model:
        raise ValidationError("Model name is required")
    
    # Accept any model name (including those with slashes like zai-org/GLM-4.5)
    # Basic validation: should contain at least one character and can include slashes, dots, hyphens, underscores
    # Exclude special characters like @, #, etc.
    if not re.match(r'^[a-zA-Z0-9_.\-/]+$', model):
        raise ValidationError("Invalid model name format")


def validate_description(description: str) -> None:
    """Validate profile description."""
    if description is None:
        return
    
    if len(description) > 500:
        raise ValidationError("Description must be 500 characters or less")


def validate_config_data(data: Dict[str, Any]) -> None:
    """Validate configuration data structure."""
    if not isinstance(data, dict):
        raise ValidationError("Configuration must be a dictionary")
    
    if 'profiles' in data:
        if not isinstance(data['profiles'], list):
            raise ValidationError("Profiles must be a list")
        
        for profile in data['profiles']:
            if not isinstance(profile, dict):
                raise ValidationError("Each profile must be a dictionary")
            
            if 'name' not in profile:
                raise ValidationError("Profile must have a name")
            
            if 'env' not in profile:
                raise ValidationError("Profile must have environment variables")
            
            if not isinstance(profile['env'], dict):
                raise ValidationError("Environment variables must be a dictionary")
    
    if 'default_profile' in data and data['default_profile']:
        if not isinstance(data['default_profile'], str):
            raise ValidationError("Default profile must be a string")


def validate_settings_data(data: Dict[str, Any]) -> None:
    """Validate settings data structure."""
    if not isinstance(data, dict):
        raise ValidationError("Settings must be a dictionary")
    
    if 'env' not in data:
        raise ValidationError("Settings must have environment variables")
    
    if not isinstance(data['env'], dict):
        raise ValidationError("Environment variables must be a dictionary")
    
    if 'permissions' not in data:
        raise ValidationError("Settings must have permissions")
    
    if not isinstance(data['permissions'], dict):
        raise ValidationError("Permissions must be a dictionary")
    
    if 'statusLine' not in data:
        raise ValidationError("Settings must have status line configuration")
    
    if not isinstance(data['statusLine'], dict):
        raise ValidationError("Status line must be a dictionary")


def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe."""
    if not filename:
        return False
    
    # Check for unsafe characters
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    if any(char in filename for char in unsafe_chars):
        return False
    
    # Check for reserved filenames
    reserved_names = ['con', 'prn', 'aux', 'nul'] + [f'com{i}' for i in range(1, 10)] + [f'lpt{i}' for i in range(1, 10)]
    if filename.lower() in reserved_names:
        return False
    
    return True


def sanitize_string(value: str, max_length: int = None) -> str:
    """Sanitize string input."""
    if not value:
        return ""
    
    # Remove null bytes and control characters
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    
    # Strip whitespace
    value = value.strip()
    
    # Truncate if max length specified
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_boolean(value: Any) -> bool:
    """Validate and convert to boolean."""
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ('true', 'yes', '1', 'on')
    
    if isinstance(value, (int, float)):
        return bool(value)
    
    return False