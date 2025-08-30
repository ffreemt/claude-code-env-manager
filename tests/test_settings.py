"""Test cases for ClaudeSettings data model."""

import pytest
from claude_env_manager.models import ClaudeSettings


class TestClaudeSettings:
    """Test ClaudeSettings data model."""

    def test_create_valid_settings(self):
        """Test creating valid settings."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        permissions = {
            "allow": ["file:read"],
            "deny": ["network:write"]
        }
        
        status_line = {
            "type": "command",
            "command": "/path/to/ccline",
            "padding": 0
        }
        
        settings = ClaudeSettings(
            env=env_vars,
            permissions=permissions,
            status_line=status_line
        )
        
        assert settings.env == env_vars
        assert settings.permissions == permissions
        assert settings.status_line == status_line
        assert settings.schema == "https://json.schemastore.org/claude-code-settings.json"

    def test_settings_without_env(self):
        """Test settings without environment variables raises error."""
        permissions = {
            "allow": [],
            "deny": []
        }
        
        status_line = {
            "type": "command",
            "command": "/path/to/ccline",
            "padding": 0
        }
        
        with pytest.raises(ValueError, match="Environment variables are required"):
            ClaudeSettings(
                env={},
                permissions=permissions,
                status_line=status_line
            )

    def test_settings_without_permissions(self):
        """Test settings without permissions raises error."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        status_line = {
            "type": "command",
            "command": "/path/to/ccline",
            "padding": 0
        }
        
        with pytest.raises(ValueError, match="Permissions dictionary must contain.*allow.*deny"):
            ClaudeSettings(
                env=env_vars,
                permissions={},
                status_line=status_line
            )

    def test_settings_without_status_line_type(self):
        """Test settings without status line type raises error."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        permissions = {
            "allow": [],
            "deny": []
        }
        
        status_line = {
            "command": "/path/to/ccline",
            "padding": 0
            # Missing "type"
        }
        
        with pytest.raises(ValueError, match="Status line must have a 'type' field"):
            ClaudeSettings(
                env=env_vars,
                permissions=permissions,
                status_line=status_line
            )

    def test_settings_to_dict(self):
        """Test converting settings to dictionary."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        permissions = {
            "allow": ["file:read"],
            "deny": ["network:write"]
        }
        
        status_line = {
            "type": "command",
            "command": "/path/to/ccline",
            "padding": 0
        }
        
        settings = ClaudeSettings(
            env=env_vars,
            permissions=permissions,
            status_line=status_line
        )
        
        data = settings.to_dict()
        
        assert data["env"] == env_vars
        assert data["permissions"] == permissions
        assert data["statusLine"] == status_line
        assert data["$schema"] == "https://json.schemastore.org/claude-code-settings.json"

    def test_settings_from_dict(self):
        """Test creating settings from dictionary."""
        data = {
            "env": {
                "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                "ANTHROPIC_API_KEY": "sk-ant-api03-test",
                "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
            },
            "permissions": {
                "allow": ["file:read"],
                "deny": ["network:write"]
            },
            "statusLine": {
                "type": "command",
                "command": "/path/to/ccline",
                "padding": 0
            },
            "$schema": "https://json.schemastore.org/claude-code-settings.json"
        }
        
        settings = ClaudeSettings.from_dict(data)
        
        assert settings.env == data["env"]
        assert settings.permissions == data["permissions"]
        assert settings.status_line == data["statusLine"]
        assert settings.schema == data["$schema"]

    def test_settings_from_dict_with_schema_field(self):
        """Test creating settings from dictionary with schema field."""
        data = {
            "env": {
                "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
                "ANTHROPIC_API_KEY": "sk-ant-api03-test",
                "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
                "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
            },
            "permissions": {
                "allow": [],
                "deny": []
            },
            "statusLine": {
                "type": "command",
                "command": "/path/to/ccline",
                "padding": 0
            },
            "$schema": "https://json.schemastore.org/claude-code-settings.json"
        }
        
        settings = ClaudeSettings.from_dict(data)
        
        assert settings.schema == data["$schema"]

    def test_update_env(self):
        """Test updating environment variables."""
        env_vars = {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_API_KEY": "sk-ant-api03-test",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "ANTHROPIC_SMALL_FAST_MODEL": "claude-3-haiku-20240307"
        }
        
        settings = ClaudeSettings(
            env=env_vars,
            permissions={"allow": [], "deny": []},
            status_line={"type": "command", "command": "/path/to/ccline", "padding": 0}
        )
        
        new_vars = {
            "ANTHROPIC_MODEL": "claude-3-opus-20240229",
            "NEW_VAR": "new-value"
        }
        
        settings.update_env(new_vars)
        
        assert settings.env["ANTHROPIC_MODEL"] == "claude-3-opus-20240229"
        assert settings.env["NEW_VAR"] == "new-value"
        assert settings.env["ANTHROPIC_API_KEY"] == "sk-ant-api03-test"  # Unchanged