"""Data models for Claude Code Environment Manager."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import re
from pathlib import Path


@dataclass
class EnvironmentProfile:
    """Environment profile data model."""
    name: str
    env: Dict[str, str]
    description: Optional[str] = None
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate profile data."""
        if not self.name:
            raise ValueError("Profile name is required")
        
        # Ensure required environment variables are present
        required_vars = [
            "ANTHROPIC_BASE_URL",
            "ANTHROPIC_API_KEY", 
            "ANTHROPIC_MODEL",
            "ANTHROPIC_SMALL_FAST_MODEL"
        ]
        
        for var in required_vars:
            if var not in self.env:
                raise ValueError(f"Required environment variable '{var}' is missing")
        
        # Validate API key format
        api_key = self.env.get("ANTHROPIC_API_KEY", "")
        if not api_key.startswith("sk-"):
            raise ValueError("API key must start with 'sk-'")
        
        # Validate URL format
        base_url = self.env.get("ANTHROPIC_BASE_URL", "")
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("Base URL must start with 'http://' or 'https://'")
        
        # Validate model names
        model = self.env.get("ANTHROPIC_MODEL", "")
        fast_model = self.env.get("ANTHROPIC_SMALL_FAST_MODEL", "")
        
        # Validate model names format
        for model_name in [model, fast_model]:
            if model_name and not re.match(r'^[a-zA-Z0-9_.\-/]+$', model_name):
                raise ValueError("Invalid model name format")

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for serialization."""
        return {
            "name": self.name,
            "env": self.env,
            "description": self.description,
            "created": self.created.isoformat(),
            "modified": self.modified.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnvironmentProfile":
        """Create profile from dictionary."""
        profile_data = data.copy()
        
        # Parse datetime fields
        if "created" in profile_data:
            profile_data["created"] = datetime.fromisoformat(profile_data["created"])
        if "modified" in profile_data:
            profile_data["modified"] = datetime.fromisoformat(profile_data["modified"])
        
        return cls(**profile_data)

    def update_env(self, env_vars: Dict[str, str]) -> None:
        """Update environment variables and mark as modified."""
        import time
        self.env.update(env_vars)
        # Ensure timestamp is different by adding a small delay if needed
        new_time = datetime.now()
        if new_time <= self.modified:
            time.sleep(0.001)  # 1ms delay
            self.modified = datetime.now()
        else:
            self.modified = new_time


@dataclass
class ClaudeSettings:
    """Claude Code settings data model."""
    env: Dict[str, str]
    permissions: Dict[str, List[str]]
    status_line: Dict[str, Any]
    schema: str = "https://json.schemastore.org/claude-code-settings.json"

    def __post_init__(self):
        """Validate settings data."""
        if not self.env:
            raise ValueError("Environment variables are required")
        
        if "allow" not in self.permissions or "deny" not in self.permissions:
            raise ValueError("Permissions dictionary must contain 'allow' and 'deny' keys")
        
        if "type" not in self.status_line:
            raise ValueError("Status line must have a 'type' field")

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary for JSON serialization."""
        return {
            "env": self.env,
            "permissions": self.permissions,
            "statusLine": self.status_line,
            "$schema": self.schema
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClaudeSettings":
        """Create settings from dictionary."""
        settings_data = data.copy()
        
        # Handle schema field
        if "$schema" in settings_data:
            settings_data["schema"] = settings_data.pop("$schema")
        
        # Handle statusLine field
        if "statusLine" in settings_data:
            settings_data["status_line"] = settings_data.pop("statusLine")
        
        return cls(**settings_data)

    def update_env(self, env_vars: Dict[str, str]) -> None:
        """Update environment variables."""
        self.env.update(env_vars)


@dataclass
class ProfileConfig:
    """Configuration file data model."""
    profiles: List[EnvironmentProfile] = field(default_factory=list)
    default_profile: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for YAML serialization."""
        return {
            "profiles": [profile.to_dict() for profile in self.profiles],
            "default_profile": self.default_profile
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProfileConfig":
        """Create config from dictionary."""
        profiles = []
        if "profiles" in data:
            profiles = [EnvironmentProfile.from_dict(p) for p in data["profiles"]]
        
        default_profile = data.get("default_profile")
        
        return cls(profiles=profiles, default_profile=default_profile)

    def get_profile(self, name: str) -> Optional[EnvironmentProfile]:
        """Get a profile by name."""
        for profile in self.profiles:
            if profile.name == name:
                return profile
        return None

    def add_profile(self, profile: EnvironmentProfile) -> None:
        """Add a new profile."""
        # Check if profile already exists
        if self.get_profile(profile.name):
            raise ValueError(f"Profile '{profile.name}' already exists")
        
        self.profiles.append(profile)

    def remove_profile(self, name: str) -> bool:
        """Remove a profile by name. Returns True if removed, False if not found."""
        for i, profile in enumerate(self.profiles):
            if profile.name == name:
                del self.profiles[i]
                # Update default profile if it was the removed one
                if self.default_profile == name:
                    self.default_profile = self.profiles[0].name if self.profiles else None
                return True
        return False

    def update_profile(self, name: str, **kwargs) -> Optional[EnvironmentProfile]:
        """Update a profile by name. Returns updated profile or None if not found."""
        profile = self.get_profile(name)
        if not profile:
            return None
        
        # Update fields
        if "env" in kwargs:
            profile.update_env(kwargs["env"])
        if "description" in kwargs:
            profile.description = kwargs["description"]
        
        return profile