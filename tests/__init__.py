"""Test suite for Claude Code Environment Manager."""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json
import yaml
import tempfile
import shutil
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from claude_env_manager.models import EnvironmentProfile, ClaudeSettings, ProfileConfig
from claude_env_manager.api import ClaudeEnvManager
from claude_env_manager.exceptions import (
    ProfileNotFoundError,
    ProfileExistsError,
    InvalidProfileError,
    SettingsFileError,
    ConfigurationError,
    ValidationError
)
from claude_env_manager.utils.io import (
    safe_read_file,
    safe_write_file,
    create_backup,
    restore_from_backup
)
from claude_env_manager.utils.validation import (
    validate_profile_name,
    validate_environment_vars,
    validate_api_key,
    validate_base_url,
    validate_model_name
)