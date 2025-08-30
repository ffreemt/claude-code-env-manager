"""Main entry point for Claude Code Environment Manager."""

import click
from pathlib import Path
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_env_manager.cli.commands import cli
from claude_env_manager.cli.interface import show_banner
from claude_env_manager.utils.config import check_python_version, validate_environment_setup
from claude_env_manager.exceptions import ConfigurationError


def main():
    """Main entry point for the CLI."""
    try:
        # Check Python version
        if not check_python_version():
            click.echo("Error: Python 3.11 or higher is required.", err=True)
            sys.exit(1)
        
        # Check environment setup
        if not validate_environment_setup():
            click.echo("Warning: Claude Code not found. Some features may not work.", err=True)
        
        # Show banner for interactive commands
        if len(sys.argv) > 1 and sys.argv[1] not in ['-h', '--help', '--version', '-V']:
            show_banner()
        
        # Run CLI
        cli()
    
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.")
        sys.exit(1)
    except ConfigurationError as e:
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()