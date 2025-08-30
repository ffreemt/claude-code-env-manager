"""Test cases for ClaudeEnvManager API."""

import pytest
import json
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from datetime import datetime

from claude_env_manager.api import ClaudeEnvManager
from claude_env_manager.models import EnvironmentProfile, ProfileConfig, ClaudeSettings
from claude_env_manager.exceptions import (
    ProfileNotFoundError,
    ProfileExistsError,
    InvalidProfileError,
    SettingsFileError,
    ConfigurationError
)


class TestClaudeEnvManager:
    """Test ClaudeEnvManager API class."""

    def test_init_with_default_paths(self):
        """Test initialization with default paths."""
        manager = ClaudeEnvManager()
        
        assert manager.config_file.name == "claude-profiles.yml"
        assert manager.settings_file.name == "settings.json"
        assert manager._config_cache is None
        assert manager._settings_cache is None

    def test_init_with_custom_paths(self):
        """Test initialization with custom paths."""
        config_path = "/custom/config.yml"
        settings_path = "/custom/settings.json"
        
        manager = ClaudeEnvManager(config_path, settings_path)
        
        # Use os.path.normpath to handle platform-specific path separators
        import os
        expected_config_path = os.path.normpath(config_path)
        expected_settings_path = os.path.normpath(settings_path)
        
        assert str(manager.config_file) == expected_config_path
        assert str(manager.settings_file) == expected_settings_path

    @patch('claude_env_manager.api.safe_read_file')
    @patch('claude_env_manager.api.yaml.safe_load')
    def test_load_config_existing_file(self, mock_yaml_load, mock_read_file):
        """Test loading configuration from existing file."""
        # Setup mocks
        mock_read_file.return_value = "yaml_content"
        mock_yaml_load.return_value = {
            "profiles": [
                {
                    "name": "test-profile",
                    "env": {
                        "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                        "ANTHROPIC_API_KEY": "sk-ant-api03-test",
                        "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                        "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
                    },
                    "description": "Test profile",
                    "created": "2024-01-01T00:00:00Z",
                    "modified": "2024-01-01T00:00:00Z"
                }
            ],
            "default_profile": "test-profile"
        }
        
        manager = ClaudeEnvManager()
        config = manager.load_config()
        
        assert len(config.profiles) == 1
        assert config.profiles[0].name == "test-profile"
        assert config.default_profile == "test-profile"
        assert manager._config_cache == config

    @patch('claude_env_manager.api.safe_read_file')
    def test_load_config_nonexistent_file(self, mock_read_file):
        """Test loading configuration when file doesn't exist."""
        mock_read_file.return_value = None
        
        with patch.object(Path, 'exists', return_value=False):
            manager = ClaudeEnvManager()
            config = manager.load_config()
            
            assert len(config.profiles) == 0
            assert config.default_profile is None

    @patch('claude_env_manager.api.safe_read_file')
    @patch('claude_env_manager.api.yaml.safe_load')
    def test_load_config_invalid_yaml(self, mock_yaml_load, mock_read_file):
        """Test loading configuration with invalid YAML."""
        mock_read_file.return_value = "invalid_yaml"
        mock_yaml_load.side_effect = yaml.YAMLError("Invalid YAML")
        
        manager = ClaudeEnvManager()
        
        with pytest.raises(ConfigurationError, match="Invalid YAML format"):
            manager.load_config()

    @patch('claude_env_manager.api.safe_write_file')
    def test_save_config(self, mock_write_file):
        """Test saving configuration."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile], default_profile="test-profile")
        
        manager = ClaudeEnvManager()
        manager.save_config(config)
        
        mock_write_file.assert_called_once()
        assert manager._config_cache == config

    @patch('claude_env_manager.api.safe_read_file')
    @patch('claude_env_manager.api.json.loads')
    def test_load_settings(self, mock_json_loads, mock_read_file):
        """Test loading settings."""
        mock_read_file.return_value = json.dumps({
            "env": {
                "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                "ANTHROPIC_API_KEY": "sk-ant-api03-test",
                "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
            },
            "permissions": {"allow": [], "deny": []},
            "statusLine": {
                "type": "command",
                "command": "/path/to/ccline",
                "padding": 0
            },
            "$schema": "https://json.schemastore.org/claude-code-settings.json"
        })
        
        mock_json_loads.return_value = {
            "env": {
                "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                "ANTHROPIC_API_KEY": "sk-ant-api03-test",
                "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
            },
            "permissions": {"allow": [], "deny": []},
            "statusLine": {
                "type": "command",
                "command": "/path/to/ccline",
                "padding": 0
            },
            "$schema": "https://json.schemastore.org/claude-code-settings.json"
        }
        
        with patch.object(Path, 'exists', return_value=True):
            manager = ClaudeEnvManager()
            settings = manager.load_settings()
            
            assert settings.env["ANTHROPIC_BASE_URL"] == "https://api.anthropic.com"
            assert manager._settings_cache == settings

    def test_load_settings_nonexistent_file(self):
        """Test loading settings when file doesn't exist."""
        with patch.object(Path, 'exists', return_value=False):
            manager = ClaudeEnvManager()
            
            with pytest.raises(SettingsFileError, match="Settings file not found"):
                manager.load_settings()

    def test_list_profiles(self):
        """Test listing profiles."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        profiles = manager.list_profiles()
        
        assert len(profiles) == 1
        assert profiles[0].name == "test-profile"

    def test_get_profile_existing(self):
        """Test getting existing profile."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        retrieved = manager.get_profile("test-profile")
        
        assert retrieved == profile

    def test_get_profile_nonexistent(self):
        """Test getting non-existent profile."""
        manager = ClaudeEnvManager()
        manager._config_cache = ProfileConfig()
        
        with pytest.raises(ProfileNotFoundError, match="Profile 'non-existent' not found"):
            manager.get_profile("non-existent")

    def test_create_profile_success(self):
        """Test creating profile successfully."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        config = ProfileConfig()
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        with patch.object(manager, 'save_config') as mock_save:
            profile = manager.create_profile("test-profile", env_vars, "Test description")
            
            assert profile.name == "test-profile"
            assert profile.env == env_vars
            assert profile.description == "Test description"
            mock_save.assert_called_once()

    def test_create_profile_already_exists(self):
        """Test creating profile that already exists."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        existing_profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[existing_profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        with pytest.raises(ProfileExistsError, match="Profile 'test-profile' already exists"):
            manager.create_profile("test-profile", env_vars)

    def test_update_profile_success(self):
        """Test updating profile successfully."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        new_env_vars = {"ANTHROPIC_MODEL": "claude-3-opus-20240229"}
        
        with patch.object(manager, 'save_config') as mock_save:
            updated = manager.update_profile("test-profile", new_env_vars, "Updated description")
            
            assert updated.env["ANTHROPIC_MODEL"] == "claude-3-opus-20240229"
            assert updated.description == "Updated description"
            mock_save.assert_called_once()

    def test_update_profile_nonexistent(self):
        """Test updating non-existent profile."""
        manager = ClaudeEnvManager()
        manager._config_cache = ProfileConfig()
        
        with pytest.raises(ProfileNotFoundError, match="Profile 'non-existent' not found"):
            manager.update_profile("non-existent", {"ANTHROPIC_MODEL": "new-model"})

    def test_delete_profile_success(self):
        """Test deleting profile successfully."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile], default_profile="test-profile")
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        with patch.object(manager, 'save_config') as mock_save:
            result = manager.delete_profile("test-profile")
            
            assert result is True
            mock_save.assert_called_once()

    def test_delete_profile_nonexistent(self):
        """Test deleting non-existent profile."""
        manager = ClaudeEnvManager()
        manager._config_cache = ProfileConfig()
        
        with pytest.raises(ProfileNotFoundError, match="Profile 'non-existent' not found"):
            manager.delete_profile("non-existent")

    @patch('claude_env_manager.api.create_backup')
    @patch('claude_env_manager.api.safe_write_file')
    def test_apply_profile_success(self, mock_write_file, mock_backup):
        """Test applying profile successfully."""
        # Setup profile
        profile_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=profile_env)
        config = ProfileConfig(profiles=[profile])
        
        # Setup settings
        settings_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-old",
            "ANTHROPIC_MODEL": "claude-3-haiku-20240307",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307",
            "OTHER_VAR": "other_value"
        }
        
        settings = ClaudeSettings(
            env=settings_env,
            permissions={"allow": [], "deny": []},
            status_line={"type": "command", "command": "/path/to/ccline", "padding": 0}
        )
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        manager._settings_cache = settings
        
        result = manager.apply_profile("test-profile")
        
        assert result is True
        # Check that non-Anthropic variables are preserved
        assert settings.env["OTHER_VAR"] == "other_value"
        # Check that Anthropic variables are updated
        assert settings.env["ANTHROPIC_MODEL"] == "claude-3-5-sonnet-20241022"

    def test_get_current_profile(self):
        """Test getting current profile."""
        # Setup profile
        profile_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=profile_env)
        config = ProfileConfig(profiles=[profile])
        
        # Setup settings with matching model
        settings_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        settings = ClaudeSettings(
            env=settings_env,
            permissions={"allow": [], "deny": []},
            status_line={"type": "command", "command": "/path/to/ccline", "padding": 0}
        )
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        manager._settings_cache = settings
        
        current = manager.get_current_profile()
        
        assert current == "test-profile"

    def test_get_current_profile_no_match(self):
        """Test getting current profile when no match found."""
        # Setup profile
        profile_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=profile_env)
        config = ProfileConfig(profiles=[profile])
        
        # Setup settings with different model
        settings_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-opus-20240229",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        settings = ClaudeSettings(
            env=settings_env,
            permissions={"allow": [], "deny": []},
            status_line={"type": "command", "command": "/path/to/ccline", "padding": 0}
        )
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        manager._settings_cache = settings
        
        current = manager.get_current_profile()
        
        assert current is None

    def test_get_default_profile(self):
        """Test getting default profile."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars
        )
        config = ProfileConfig(profiles=[profile], default_profile="test-profile")
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        default = manager.get_default_profile()
        
        assert default == "test-profile"

    def test_set_default_profile(self):
        """Test setting default profile."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars
        )
        config = ProfileConfig(profiles=[profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        with patch.object(manager, 'save_config') as mock_save:
            manager.set_default_profile("test-profile")
            
            assert config.default_profile == "test-profile"
            mock_save.assert_called_once()

    def test_set_default_profile_nonexistent(self):
        """Test setting default profile to non-existent profile."""
        manager = ClaudeEnvManager()
        manager._config_cache = ProfileConfig()
        
        with pytest.raises(ProfileNotFoundError, match="Profile 'non-existent' not found"):
            manager.set_default_profile("non-existent")

    def test_get_current_settings(self):
        """Test getting current settings as dictionary."""
        settings_env = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        settings = ClaudeSettings(
            env=settings_env,
            permissions={"allow": [], "deny": []},
            status_line={"type": "command", "command": "/path/to/ccline", "padding": 0}
        )
        
        manager = ClaudeEnvManager()
        manager._settings_cache = settings
        
        current_settings = manager.get_current_settings()
        
        assert current_settings["env"] == settings_env
        assert current_settings["$schema"] == "https://json.schemastore.org/claude-code-settings.json"

    def test_get_current_settings_error(self):
        """Test getting current settings when error occurs."""
        manager = ClaudeEnvManager()
        
        # Mock load_settings to raise an exception
        with patch.object(manager, 'load_settings', side_effect=SettingsFileError("Error")):
            current_settings = manager.get_current_settings()
            
            assert current_settings == {}

    def test_validate_profile_valid(self):
        """Test validating valid profile."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        result = manager.validate_profile("test-profile")
        
        assert result is True

    def test_validate_profile_invalid(self):
        """Test validating invalid profile."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(name="test-profile", env=env_vars)
        config = ProfileConfig(profiles=[profile])
        
        manager = ClaudeEnvManager()
        manager._config_cache = config
        
        result = manager.validate_profile("non-existent")
        
        assert result is False

    def test_clear_cache(self):
        """Test clearing cache."""
        manager = ClaudeEnvManager()
        manager._config_cache = "cached_config"
        manager._settings_cache = "cached_settings"
        
        manager.clear_cache()
        
        assert manager._config_cache is None
        assert manager._settings_cache is None

    def test_get_config_path(self):
        """Test getting config file path."""
        config_path = "/custom/config.yml"
        manager = ClaudeEnvManager(config_path)
        
        # Use os.path.normpath to handle platform-specific path separators
        import os
        expected_config_path = os.path.normpath(config_path)
        
        assert manager.get_config_path() == expected_config_path

    def test_get_settings_path(self):
        """Test getting settings file path."""
        settings_path = "/custom/settings.json"
        manager = ClaudeEnvManager(None, settings_path)
        
        # Use os.path.normpath to handle platform-specific path separators
        import os
        expected_settings_path = os.path.normpath(settings_path)
        
        assert manager.get_settings_path() == expected_settings_path