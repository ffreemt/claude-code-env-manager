"""Test cases for EnvironmentProfile data model."""

import pytest
from datetime import datetime
from claude_env_manager.models import EnvironmentProfile


class TestEnvironmentProfile:
    """Test EnvironmentProfile data model."""

    def test_create_valid_profile(self):
        """Test creating a valid profile."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars,
            description="Test profile"
        )
        
        assert profile.name == "test-profile"
        assert profile.env == env_vars
        assert profile.description == "Test profile"
        assert isinstance(profile.created, datetime)
        assert isinstance(profile.modified, datetime)

    def test_profile_without_name(self):
        """Test profile without name raises error."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        with pytest.raises(ValueError, match="Profile name is required"):
            EnvironmentProfile(
                name="",
                env=env_vars
            )

    def test_profile_missing_required_vars(self):
        """Test profile missing required environment variables."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            # Missing ANTHROPIC_MODEL and ANTHROPIC_SMALL_FAST_MODEL
        }
        
        with pytest.raises(ValueError, match="Required environment variable.*is missing"):
            EnvironmentProfile(
                name="test-profile",
                env=env_vars
            )

    def test_profile_invalid_api_key(self):
        """Test profile with invalid API key format."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "invalid-key",  # Doesn't start with sk-
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        with pytest.raises(ValueError, match="API key must start with 'sk-'"):
            EnvironmentProfile(
                name="test-profile",
                env=env_vars
            )

    def test_profile_invalid_base_url(self):
        """Test profile with invalid base URL."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "invalid-url",  # Not HTTP/HTTPS
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        with pytest.raises(ValueError, match="Base URL must start with 'http://' or 'https://'"):
            EnvironmentProfile(
                name="test-profile",
                env=env_vars
            )

    def test_profile_any_base_url_accepted(self):
        """Test that any valid base URL is accepted."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://any-domain.com/api",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        # This should not raise an error
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars
        )
        
        assert profile.env["ANTHROPIC_BASE_URL"] == "https://any-domain.com/api"

    def test_profile_any_model_name_accepted(self):
        """Test that any model name format is accepted."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "zai-org/GLM-4.5",
            "ANTHROPIC_SMALL_FAST_MODEL": "gpt-4"
        }
        
        # This should not raise an error
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars
        )
        
        assert profile.env["ANTHROPIC_MODEL"] == "zai-org/GLM-4.5"
        assert profile.env["ANTHROPIC_SMALL_FAST_MODEL"] == "gpt-4"

    def test_profile_invalid_model_name_format(self):
        """Test profile with invalid model name format."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "invalid model@name",  # Contains invalid character @
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        with pytest.raises(ValueError, match="Invalid model name format"):
            EnvironmentProfile(
                name="test-profile",
                env=env_vars
            )

    def test_profile_to_dict(self):
        """Test converting profile to dictionary."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars,
            description="Test profile"
        )
        
        data = profile.to_dict()
        
        assert data["name"] == "test-profile"
        assert data["env"] == env_vars
        assert data["description"] == "Test profile"
        assert "created" in data
        assert "modified" in data

    def test_profile_from_dict(self):
        """Test creating profile from dictionary."""
        data = {
            "name": "test-profile",
            "env": {
                "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                "ANTHROPIC_API_KEY": "sk-ant-api03-test",
                "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
            },
            "description": "Test profile",
            "created": "2024-01-01T00:00:00",
            "modified": "2024-01-01T00:00:00"
        }
        
        profile = EnvironmentProfile.from_dict(data)
        
        assert profile.name == "test-profile"
        assert profile.env == data["env"]
        assert profile.description == "Test profile"
        assert isinstance(profile.created, datetime)
        assert isinstance(profile.modified, datetime)

    def test_update_env(self):
        """Test updating environment variables."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile = EnvironmentProfile(
            name="test-profile",
            env=env_vars
        )
        
        original_modified = profile.modified
        
        new_vars = {
            "ANTHROPIC_MODEL": "claude-3-opus-20240229",
            "NEW_VAR": "new-value"
        }
        
        profile.update_env(new_vars)
        
        assert profile.env["ANTHROPIC_MODEL"] == "claude-3-opus-20240229"
        assert profile.env["NEW_VAR"] == "new-value"
        assert profile.env["ANTHROPIC_API_KEY"] == "sk-ant-api03-test"  # Unchanged
        assert profile.modified > original_modified