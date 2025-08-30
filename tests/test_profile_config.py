"""Test cases for ProfileConfig data model."""

import pytest
from claude_env_manager.models import EnvironmentProfile, ProfileConfig


class TestProfileConfig:
    """Test ProfileConfig data model."""

    def test_create_empty_config(self):
        """Test creating empty config."""
        config = ProfileConfig()
        
        assert config.profiles == []
        assert config.default_profile is None

    def test_create_config_with_profiles(self):
        """Test creating config with profiles."""
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
        
        config = ProfileConfig(
            profiles=[profile],
            default_profile="test-profile"
        )
        
        assert len(config.profiles) == 1
        assert config.profiles[0] == profile
        assert config.default_profile == "test-profile"

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
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
        
        config = ProfileConfig(
            profiles=[profile],
            default_profile="test-profile"
        )
        
        data = config.to_dict()
        
        assert "profiles" in data
        assert len(data["profiles"]) == 1
        assert data["profiles"][0]["name"] == "test-profile"
        assert data["default_profile"] == "test-profile"

    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        data = {
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
                    "created": "2024-01-01T00:00:00",
                    "modified": "2024-01-01T00:00:00"
                }
            ],
            "default_profile": "test-profile"
        }
        
        config = ProfileConfig.from_dict(data)
        
        assert len(config.profiles) == 1
        assert config.profiles[0].name == "test-profile"
        assert config.default_profile == "test-profile"

    def test_config_from_dict_without_profiles(self):
        """Test creating config from dictionary without profiles."""
        data = {
            "default_profile": "test-profile"
        }
        
        config = ProfileConfig.from_dict(data)
        
        assert config.profiles == []
        assert config.default_profile == "test-profile"

    def test_config_from_dict_without_default(self):
        """Test creating config from dictionary without default profile."""
        data = {
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
                    "created": "2024-01-01T00:00:00",
                    "modified": "2024-01-01T00:00:00"
                }
            ]
        }
        
        config = ProfileConfig.from_dict(data)
        
        assert len(config.profiles) == 1
        assert config.default_profile is None

    def test_get_profile(self):
        """Test getting profile by name."""
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
        
        config = ProfileConfig(profiles=[profile])
        
        # Test existing profile
        found = config.get_profile("test-profile")
        assert found == profile
        
        # Test non-existing profile
        not_found = config.get_profile("non-existent")
        assert not_found is None

    def test_add_profile(self):
        """Test adding profile to config."""
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
        
        config = ProfileConfig()
        config.add_profile(profile)
        
        assert len(config.profiles) == 1
        assert config.profiles[0] == profile

    def test_add_duplicate_profile(self):
        """Test adding duplicate profile raises error."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile1 = EnvironmentProfile(
            name="test-profile",
            env=env_vars,
            description="Test profile"
        )
        
        profile2 = EnvironmentProfile(
            name="test-profile",  # Same name
            env=env_vars,
            description="Another test profile"
        )
        
        config = ProfileConfig()
        config.add_profile(profile1)
        
        with pytest.raises(ValueError, match="Profile 'test-profile' already exists"):
            config.add_profile(profile2)

    def test_remove_profile(self):
        """Test removing profile from config."""
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
        
        config = ProfileConfig(
            profiles=[profile],
            default_profile="test-profile"
        )
        
        # Remove existing profile
        removed = config.remove_profile("test-profile")
        assert removed is True
        assert len(config.profiles) == 0
        assert config.default_profile is None  # Default cleared

    def test_remove_nonexistent_profile(self):
        """Test removing non-existent profile."""
        config = ProfileConfig()
        
        removed = config.remove_profile("non-existent")
        assert removed is False

    def test_remove_default_profile_with_others(self):
        """Test removing default profile when other profiles exist."""
        env_vars1 = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test-1",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        env_vars2 = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test-2",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        profile1 = EnvironmentProfile(name="profile1", env=env_vars1)
        profile2 = EnvironmentProfile(name="profile2", env=env_vars2)
        
        config = ProfileConfig(
            profiles=[profile1, profile2],
            default_profile="profile1"
        )
        
        # Remove default profile
        removed = config.remove_profile("profile1")
        assert removed is True
        assert len(config.profiles) == 1
        assert config.default_profile == "profile2"  # Default set to remaining profile

    def test_update_profile(self):
        """Test updating profile."""
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
        
        config = ProfileConfig(profiles=[profile])
        
        # Update environment variables
        new_env_vars = {
            "ANTHROPIC_MODEL": "claude-3-opus-20240229",
            "NEW_VAR": "new-value"
        }
        
        updated = config.update_profile("test-profile", env=new_env_vars)
        
        assert updated is not None
        assert updated.env["ANTHROPIC_MODEL"] == "claude-3-opus-20240229"
        assert updated.env["NEW_VAR"] == "new-value"
        assert updated.env["ANTHROPIC_API_KEY"] == "sk-ant-api03-test"  # Unchanged

    def test_update_profile_description(self):
        """Test updating profile description."""
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
        
        config = ProfileConfig(profiles=[profile])
        
        # Update description
        updated = config.update_profile("test-profile", description="Updated description")
        
        assert updated is not None
        assert updated.description == "Updated description"

    def test_update_nonexistent_profile(self):
        """Test updating non-existent profile."""
        config = ProfileConfig()
        
        updated = config.update_profile("non-existent", description="New description")
        assert updated is None

    def test_update_profile_no_changes(self):
        """Test updating profile with no changes."""
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
        
        config = ProfileConfig(profiles=[profile])
        
        # Update with no changes
        updated = config.update_profile("test-profile")
        
        assert updated is not None
        assert updated.description == "Test profile"  # Unchanged