"""Custom exceptions for Claude Code Environment Manager."""


class ClaudeEnvManagerError(Exception):
    """Base exception for ClaudeEnvManager."""
    pass


class ProfileNotFoundError(ClaudeEnvManagerError):
    """Raised when a profile is not found."""
    pass


class ProfileExistsError(ClaudeEnvManagerError):
    """Raised when trying to create a profile that already exists."""
    pass


class InvalidProfileError(ClaudeEnvManagerError):
    """Raised when profile validation fails."""
    pass


class SettingsFileError(ClaudeEnvManagerError):
    """Raised when there's an error with the settings file."""
    pass


class ConfigurationError(ClaudeEnvManagerError):
    """Raised when there's a configuration error."""
    pass


class ValidationError(ClaudeEnvManagerError):
    """Raised when validation fails."""
    pass


class FileOperationError(ClaudeEnvManagerError):
    """Raised when file operations fail."""
    pass