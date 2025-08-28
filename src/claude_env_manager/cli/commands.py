"""CLI commands for Claude Code Environment Manager."""

import click
from pathlib import Path
from typing import Optional
import sys

from ..api import ClaudeEnvManager
from ..exceptions import (
    ProfileNotFoundError,
    ProfileExistsError,
    InvalidProfileError,
    SettingsFileError,
    ConfigurationError
)
from ..utils.validation import validate_environment_vars, validate_profile_name
from .interface import (
    list_profiles_tui,
    select_profile_tui,
    create_profile_tui,
    edit_profile_tui,
    show_profile_details_tui,
    confirm_action_tui
)


@click.group()
@click.option('--config', '-c', type=click.Path(), help='Configuration file path')
@click.option('--settings', '-s', type=click.Path(), help='Settings file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode')
@click.pass_context
def cli(ctx, config, settings, verbose, quiet):
    """Claude Code Environment Manager.
    
    Manage Claude Code environment configurations with ease.
    """
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['settings_path'] = settings
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    
    # Initialize the environment manager
    try:
        ctx.obj['manager'] = ClaudeEnvManager(config, settings)
    except Exception as e:
        click.echo(f"Error initializing environment manager: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), 
              default='table', help='Output format')
@click.pass_context
def list(ctx, format):
    """List all environment profiles."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    verbose = ctx.obj['verbose']
    
    try:
        profiles = manager.list_profiles()
        
        if not profiles:
            if not quiet:
                click.echo("No profiles found. Use 'create' to add a profile.")
            return
        
        if format == 'table':
            list_profiles_tui(profiles, verbose)
        elif format == 'json':
            import json
            data = [p.to_dict() for p in profiles]
            click.echo(json.dumps(data, indent=2))
        elif format == 'yaml':
            import yaml
            data = [p.to_dict() for p in profiles]
            click.echo(yaml.dump(data, default_flow_style=False))
    
    except Exception as e:
        click.echo(f"Error listing profiles: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', required=True, help='Profile name')
@click.option('--base-url', '-b', help='Anthropic base URL')
@click.option('--api-key', '-k', help='Anthropic API key')
@click.option('--model', '-m', help='Anthropic model')
@click.option('--fast-model', '-f', help='Anthropic fast model')
@click.option('--description', '-d', help='Profile description')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.pass_context
def create(ctx, name, base_url, api_key, model, fast_model, description, interactive):
    """Create a new environment profile."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        # Validate profile name
        validate_profile_name(name)
        
        if interactive:
            # Use TUI for interactive creation
            profile = create_profile_tui()
            if profile:
                manager.create_profile(
                    profile.name,
                    profile.env,
                    profile.description
                )
                if not quiet:
                    click.echo(f"✅ Profile '{profile.name}' created successfully.")
        else:
            # Check for required parameters
            if not all([base_url, api_key, model, fast_model]):
                click.echo("Error: --base-url, --api-key, --model, and --fast-model are required in non-interactive mode.", err=True)
                sys.exit(1)
            
            # Create environment variables dictionary
            env_vars = {
                "ANTHROPIC_BASE_URL": base_url,
                "ANTHROPIC_API_KEY": api_key,
                "ANTHROPIC_MODEL": model,
                "ANTHROPIC_SMALL_FAST_MODEL": fast_model
            }
            
            # Validate environment variables
            validate_environment_vars(env_vars)
            
            # Create profile
            manager.create_profile(name, env_vars, description)
            if not quiet:
                click.echo(f"✅ Profile '{name}' created successfully.")
    
    except ProfileExistsError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except (ValidationError, ValueError) as e:
        click.echo(f"Validation error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error creating profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', required=True, help='Profile name')
@click.option('--base-url', '-b', help='Anthropic base URL')
@click.option('--api-key', '-k', help='Anthropic API key')
@click.option('--model', '-m', help='Anthropic model')
@click.option('--fast-model', '-f', help='Anthropic fast model')
@click.option('--description', '-d', help='Profile description')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.pass_context
def update(ctx, name, base_url, api_key, model, fast_model, description, interactive):
    """Update an existing environment profile."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        if interactive:
            # Use TUI for interactive editing
            profile = edit_profile_tui(manager, name)
            if profile:
                manager.update_profile(name, profile.env, profile.description)
                if not quiet:
                    click.echo(f"✅ Profile '{name}' updated successfully.")
        else:
            # Build update parameters
            env_vars = {}
            if base_url:
                env_vars["ANTHROPIC_BASE_URL"] = base_url
            if api_key:
                env_vars["ANTHROPIC_API_KEY"] = api_key
            if model:
                env_vars["ANTHROPIC_MODEL"] = model
            if fast_model:
                env_vars["ANTHROPIC_SMALL_FAST_MODEL"] = fast_model
            
            # Update profile
            manager.update_profile(name, env_vars or None, description)
            if not quiet:
                click.echo(f"✅ Profile '{name}' updated successfully.")
    
    except ProfileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except (ValidationError, ValueError) as e:
        click.echo(f"Validation error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error updating profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', required=True, help='Profile name')
@click.option('--force', '-f', is_flag=True, help='Force deletion without confirmation')
@click.pass_context
def delete(ctx, name, force):
    """Delete an environment profile."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        # Check if profile exists
        try:
            manager.get_profile(name)
        except ProfileNotFoundError:
            click.echo(f"Error: Profile '{name}' not found.", err=True)
            sys.exit(1)
        
        # Confirm deletion unless forced
        if not force:
            if not confirm_action_tui(f"Delete profile '{name}'?"):
                if not quiet:
                    click.echo("Deletion cancelled.")
                return
        
        # Delete profile
        if manager.delete_profile(name):
            if not quiet:
                click.echo(f"✅ Profile '{name}' deleted successfully.")
        else:
            click.echo(f"Error: Failed to delete profile '{name}'.", err=True)
            sys.exit(1)
    
    except Exception as e:
        click.echo(f"Error deleting profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', required=True, help='Profile name')
@click.option('--force', '-f', is_flag=True, help='Force application without confirmation')
@click.pass_context
def apply(ctx, name, force):
    """Apply a profile to Claude Code settings."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        # Check if profile exists
        try:
            profile = manager.get_profile(name)
        except ProfileNotFoundError:
            click.echo(f"Error: Profile '{name}' not found.", err=True)
            sys.exit(1)
        
        # Confirm application unless forced
        if not force:
            if not confirm_action_tui(f"Apply profile '{name}' to Claude Code settings?"):
                if not quiet:
                    click.echo("Application cancelled.")
                return
        
        # Apply profile
        if manager.apply_profile(name):
            if not quiet:
                click.echo(f"✅ Profile '{name}' applied successfully.")
        else:
            click.echo(f"Error: Failed to apply profile '{name}'.", err=True)
            sys.exit(1)
    
    except SettingsFileError as e:
        click.echo(f"Settings file error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error applying profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', help='Profile name (if not specified, shows interactive selector)')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), 
              default='table', help='Output format')
@click.pass_context
def show(ctx, name, format):
    """Show profile details."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        if name:
            # Show specific profile
            profile = manager.get_profile(name)
            show_profile_details_tui(profile, format)
        else:
            # Interactive profile selection
            selected_profile = select_profile_tui(manager)
            if selected_profile:
                show_profile_details_tui(selected_profile, format)
            elif not quiet:
                click.echo("No profile selected.")
    
    except ProfileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error showing profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def current(ctx):
    """Show current active profile."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        current = manager.get_current_profile()
        if current:
            click.echo(f"Current profile: {current}")
        else:
            if not quiet:
                click.echo("No active profile found.")
    
    except Exception as e:
        click.echo(f"Error getting current profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', required=True, help='Profile name')
@click.pass_context
def default(ctx, name):
    """Set the default profile."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        # Check if profile exists
        try:
            manager.get_profile(name)
        except ProfileNotFoundError:
            click.echo(f"Error: Profile '{name}' not found.", err=True)
            sys.exit(1)
        
        # Set default profile
        manager.set_default_profile(name)
        if not quiet:
            click.echo(f"✅ Default profile set to '{name}'.")
    
    except Exception as e:
        click.echo(f"Error setting default profile: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def config(ctx):
    """Show configuration information."""
    manager = ctx.obj['manager']
    verbose = ctx.obj['verbose']
    
    try:
        click.echo("Configuration Information:")
        click.echo(f"  Config file: {manager.get_config_path()}")
        click.echo(f"  Settings file: {manager.get_settings_path()}")
        click.echo(f"  Claude Code installed: {Path(manager.get_settings_path()).exists()}")
        
        if verbose:
            profiles = manager.list_profiles()
            click.echo(f"  Total profiles: {len(profiles)}")
            
            default_profile = manager.get_default_profile()
            if default_profile:
                click.echo(f"  Default profile: {default_profile}")
            else:
                click.echo("  Default profile: None")
            
            current_profile = manager.get_current_profile()
            if current_profile:
                click.echo(f"  Current profile: {current_profile}")
            else:
                click.echo("  Current profile: None")
    
    except Exception as e:
        click.echo(f"Error showing configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--force', '-f', is_flag=True, help='Force initialization without confirmation')
@click.pass_context
def init(ctx, force):
    """Initialize configuration files."""
    manager = ctx.obj['manager']
    quiet = ctx.obj['quiet']
    
    try:
        # Check if already initialized
        config_path = Path(manager.get_config_path())
        if config_path.exists() and not force:
            if not confirm_action_tui("Configuration file already exists. Reinitialize?"):
                if not quiet:
                    click.echo("Initialization cancelled.")
                return
        
        # Create default configuration
        from ..models import ProfileConfig, EnvironmentProfile
        from ..utils.config import create_default_config, create_default_settings
        
        # Create profile config
        default_config_data = create_default_config()
        profile_config = ProfileConfig.from_dict(default_config_data)
        manager.save_config(profile_config)
        
        if not quiet:
            click.echo(f"✅ Configuration initialized at {manager.get_config_path()}")
            click.echo(f"✅ Default profile 'development' created")
            click.echo("Use 'claude-env-manager apply development' to apply the default profile.")
    
    except Exception as e:
        click.echo(f"Error initializing configuration: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()