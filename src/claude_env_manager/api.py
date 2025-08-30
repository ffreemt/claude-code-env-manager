"""Core API classes for Claude Code Environment Manager."""

import json
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import EnvironmentProfile, ClaudeSettings, ProfileConfig
from .exceptions import (
    ProfileNotFoundError,
    ProfileExistsError,
    InvalidProfileError,
    SettingsFileError,
    ConfigurationError,
    FileOperationError
)
from .utils.io import safe_read_file, safe_write_file, create_backup
from .utils.validation import validate_profile_name, validate_environment_vars


class ClaudeEnvManager:
    """Main API for managing Claude Code environment configurations."""

    def __init__(self, config_file: str = None, settings_file: str = None):
        """Initialize with optional config file paths."""
        self.config_file = Path(config_file) if config_file else self._get_default_config_path()
        self.settings_file = Path(settings_file) if settings_file else self._get_default_settings_path()
        self._config_cache = None
        self._settings_cache = None

    def _get_default_config_path(self) -> Path:
        """Get default configuration file path."""
        home = Path.home()
        return home / ".claude" / "claude-profiles.yml"

    def _get_default_settings_path(self) -> Path:
        """Get default Claude Code settings file path."""
        home = Path.home()
        return home / ".claude" / "settings.json"

    def load_config(self) -> ProfileConfig:
        """Load configuration from YAML file."""
        if self._config_cache:
            return self._config_cache

        try:
            if not self.config_file.exists():
                # Create default config if it doesn't exist
                config = ProfileConfig()
                self.save_config(config)
                return config

            data = safe_read_file(self.config_file)
            if not data:
                return ProfileConfig()

            config_dict = yaml.safe_load(data)
            if config_dict:
                self._config_cache = ProfileConfig.from_dict(config_dict)
            else:
                self._config_cache = ProfileConfig()
            
            return self._config_cache
        
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML format in {self.config_file}: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def save_config(self, config: ProfileConfig) -> None:
        """Save configuration to YAML file."""
        try:
            # Ensure parent directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = config.to_dict()
            yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
            
            safe_write_file(self.config_file, yaml_str)
            self._config_cache = config
        
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")

    def load_settings(self) -> ClaudeSettings:
        """Load Claude Code settings from JSON file."""
        if self._settings_cache:
            return self._settings_cache

        try:
            if not self.settings_file.exists():
                raise SettingsFileError(f"Settings file not found: {self.settings_file}")

            data = safe_read_file(self.settings_file)
            if not data:
                raise SettingsFileError(f"Settings file is empty: {self.settings_file}")

            settings_dict = json.loads(data)
            self._settings_cache = ClaudeSettings.from_dict(settings_dict)
            return self._settings_cache
        
        except json.JSONDecodeError as e:
            raise SettingsFileError(f"Invalid JSON format in {self.settings_file}: {e}")
        except Exception as e:
            raise SettingsFileError(f"Failed to load settings: {e}")

    def save_settings(self, settings: ClaudeSettings) -> None:
        """Save Claude Code settings to JSON file."""
        try:
            # Create backup before modifying
            create_backup(self.settings_file)
            
            data = settings.to_dict()
            json_str = json.dumps(data, indent=2)
            
            safe_write_file(self.settings_file, json_str)
            self._settings_cache = settings
        
        except Exception as e:
            raise SettingsFileError(f"Failed to save settings: {e}")

    def list_profiles(self) -> List[EnvironmentProfile]:
        """List all environment profiles."""
        config = self.load_config()
        return config.profiles.copy()

    def get_profile(self, name: str) -> EnvironmentProfile:
        """Get a specific profile by name."""
        config = self.load_config()
        profile = config.get_profile(name)
        if not profile:
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        return profile

    def create_profile(self, name: str, env_vars: Dict[str, str], 
                      description: str = None) -> EnvironmentProfile:
        """Create a new environment profile."""
        # Validate profile name
        validate_profile_name(name)
        
        # Validate environment variables
        validate_environment_vars(env_vars)
        
        # Check if profile already exists
        config = self.load_config()
        if config.get_profile(name):
            raise ProfileExistsError(f"Profile '{name}' already exists")
        
        # Create and validate profile
        try:
            profile = EnvironmentProfile(
                name=name,
                env=env_vars,
                description=description
            )
        except ValueError as e:
            raise InvalidProfileError(f"Invalid profile data: {e}")
        
        # Add to config
        config.add_profile(profile)
        
        # If this is the first profile, set as default
        if len(config.profiles) == 1:
            config.default_profile = name
        
        # Save config
        self.save_config(config)
        
        return profile

    def update_profile(self, name: str, env_vars: Dict[str, str] = None, 
                      description: str = None) -> EnvironmentProfile:
        """Update an existing environment profile."""
        config = self.load_config()
        profile = config.get_profile(name)
        if not profile:
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        
        # Update environment variables if provided
        if env_vars:
            validate_environment_vars(env_vars, partial=True)
            profile.update_env(env_vars)
        
        # Update description if provided
        if description is not None:
            profile.description = description
        
        # Save config
        self.save_config(config)
        
        return profile

    def delete_profile(self, name: str) -> bool:
        """Delete an environment profile."""
        config = self.load_config()
        
        if not config.get_profile(name):
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        
        removed = config.remove_profile(name)
        if removed:
            self.save_config(config)
        
        return removed

    def apply_profile(self, name: str) -> bool:
        """Apply a profile to Claude Code settings."""
        try:
            # Get the profile
            profile = self.get_profile(name)
            
            # Load current settings
            settings = self.load_settings()
            
            # Update environment variables
            new_env = profile.env.copy()
            
            # Preserve any non-Anthropic environment variables
            for key, value in settings.env.items():
                if not key.startswith("ANTHROPIC_"):
                    new_env[key] = value
            
            # Set API_TIMEOUT_MS to 600000 if not specified in profile
            if "API_TIMEOUT_MS" not in new_env:
                new_env["API_TIMEOUT_MS"] = "600000"
            
            # Update settings
            settings.env = new_env
            
            # Save settings
            self.save_settings(settings)
            
            # Set as default profile
            config = self.load_config()
            config.default_profile = name
            self.save_config(config)
            
            return True
        
        except Exception as e:
            raise SettingsFileError(f"Failed to apply profile '{name}': {e}")

    def get_current_profile(self) -> Optional[str]:
        """Get the name of the current active profile."""
        try:
            settings = self.load_settings()
            config = self.load_config()
            
            # Find profile with matching environment variables
            for profile in config.profiles:
                # Check if ANTHROPIC_MODEL matches (good enough indicator)
                if (profile.env.get("ANTHROPIC_MODEL") == 
                    settings.env.get("ANTHROPIC_MODEL")):
                    return profile.name
            
            return None
        
        except Exception:
            return None

    def get_default_profile(self) -> Optional[str]:
        """Get the default profile name."""
        config = self.load_config()
        return config.default_profile

    def set_default_profile(self, name: str) -> None:
        """Set the default profile."""
        config = self.load_config()
        
        if not config.get_profile(name):
            raise ProfileNotFoundError(f"Profile '{name}' not found")
        
        config.default_profile = name
        self.save_config(config)

    def get_current_settings(self) -> Dict[str, Any]:
        """Get current Claude Code settings as dictionary."""
        try:
            settings = self.load_settings()
            return settings.to_dict()
        except SettingsFileError:
            return {}

    def validate_profile(self, name: str) -> bool:
        """Validate a profile."""
        try:
            profile = self.get_profile(name)
            # The profile's __post_init__ method handles validation
            return True
        except (ProfileNotFoundError, ValueError):
            return False

    def clear_cache(self) -> None:
        """Clear internal cache."""
        self._config_cache = None
        self._settings_cache = None

    def get_config_path(self) -> str:
        """Get the configuration file path."""
        return str(self.config_file)

    def get_settings_path(self) -> str:
        """Get the settings file path."""
        return str(self.settings_file)