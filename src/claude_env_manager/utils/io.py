"""File I/O utilities for Claude Code Environment Manager."""

import shutil
from pathlib import Path
from typing import Optional
from .exceptions import FileOperationError


def safe_read_file(file_path: Path) -> Optional[str]:
    """Safely read a file and return its contents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        raise FileOperationError(f"Failed to read file {file_path}: {e}")


def safe_write_file(file_path: Path, content: str) -> None:
    """Safely write content to a file."""
    try:
        # Create parent directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to temporary file first
        temp_file = file_path.with_suffix(file_path.suffix + '.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Replace the original file
        temp_file.replace(file_path)
        
    except Exception as e:
        raise FileOperationError(f"Failed to write file {file_path}: {e}")


def create_backup(file_path: Path, backup_suffix: str = '.backup') -> Path:
    """Create a backup of the specified file."""
    try:
        if not file_path.exists():
            return file_path
        
        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
        shutil.copy2(file_path, backup_path)
        
        return backup_path
    
    except Exception as e:
        raise FileOperationError(f"Failed to create backup for {file_path}: {e}")


def restore_from_backup(file_path: Path, backup_suffix: str = '.backup') -> bool:
    """Restore a file from backup."""
    try:
        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
        
        if not backup_path.exists():
            return False
        
        shutil.copy2(backup_path, file_path)
        backup_path.unlink()  # Remove backup after restore
        
        return True
    
    except Exception as e:
        raise FileOperationError(f"Failed to restore backup for {file_path}: {e}")


def ensure_directory_exists(dir_path: Path) -> None:
    """Ensure a directory exists, creating it if necessary."""
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise FileOperationError(f"Failed to create directory {dir_path}: {e}")


def get_file_permissions(file_path: Path) -> Optional[int]:
    """Get file permissions."""
    try:
        return file_path.stat().st_mode
    except Exception:
        return None


def set_file_permissions(file_path: Path, permissions: int) -> None:
    """Set file permissions."""
    try:
        file_path.chmod(permissions)
    except Exception as e:
        raise FileOperationError(f"Failed to set permissions for {file_path}: {e}")


def is_file_writable(file_path: Path) -> bool:
    """Check if a file is writable."""
    try:
        return file_path.exists() and file_path.stat().st_mode & 0o200
    except Exception:
        return False


def get_file_size(file_path: Path) -> Optional[int]:
    """Get file size in bytes."""
    try:
        return file_path.stat().st_size
    except Exception:
        return None