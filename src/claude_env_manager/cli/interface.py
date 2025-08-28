"""TUI interface components for Claude Code Environment Manager."""

from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.align import Align
from rich import box
import json
import yaml

from ..models import EnvironmentProfile
from ..exceptions import ValidationError


console = Console()


def list_profiles_tui(profiles: List[EnvironmentProfile], verbose: bool = False) -> None:
    """Display profiles in a table format."""
    if not profiles:
        console.print("[yellow]No profiles found.[/yellow]")
        return
    
    # Create table
    table = Table(title="Environment Profiles", box=box.ROUNDED)
    
    # Add columns
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Base URL", style="green")
    table.add_column("Model", style="blue")
    if verbose:
        table.add_column("Fast Model", style="magenta")
        table.add_column("API Key", style="red")
    table.add_column("Description", style="yellow")
    table.add_column("Default", style="bold", justify="center")
    
    # Add rows
    default_profile = None
    for profile in profiles:
        # Get default profile (first one marked as default)
        if hasattr(profile, 'is_default') and profile.is_default:
            default_profile = profile.name
        
        # Truncate values for display
        base_url = profile.env.get("ANTHROPIC_BASE_URL", "")
        if len(base_url) > 30:
            base_url = base_url[:27] + "..."
        
        model = profile.env.get("ANTHROPIC_MODEL", "")
        if len(model) > 20:
            model = model[:17] + "..."
        
        description = profile.description or ""
        if len(description) > 30:
            description = description[:27] + "..."
        
        # Build row
        row = [
            f"[bold]{profile.name}[/bold]",
            base_url,
            model
        ]
        
        if verbose:
            fast_model = profile.env.get("ANTHROPIC_SMALL_FAST_MODEL", "")
            if len(fast_model) > 20:
                fast_model = fast_model[:17] + "..."
            
            api_key = profile.env.get("ANTHROPIC_API_KEY", "")
            if api_key:
                # Show only first 10 characters of API key
                api_key = api_key[:10] + "..."
            else:
                api_key = "[red]Not set[/red]"
            
            row.extend([fast_model, api_key])
        
        row.append(description)
        
        # Add default marker
        is_default = default_profile == profile.name
        row.append("✓" if is_default else "")
        
        table.add_row(*row)
    
    console.print(table)


def show_profile_details_tui(profile: EnvironmentProfile, format: str = 'table') -> None:
    """Show detailed profile information."""
    if format == 'json':
        console.print_json(data=profile.to_dict())
        return
    
    if format == 'yaml':
        yaml_str = yaml.dump(profile.to_dict(), default_flow_style=False)
        console.print(Panel(yaml_str, title=f"Profile: {profile.name}", box=box.ROUNDED))
        return
    
    # Table format
    table = Table(title=f"Profile Details: {profile.name}", box=box.ROUNDED)
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    
    # Add profile metadata
    table.add_row("Name", f"[bold]{profile.name}[/bold]")
    table.add_row("Description", profile.description or "[dim]No description[/dim]")
    table.add_row("Created", profile.created.strftime("%Y-%m-%d %H:%M:%S"))
    table.add_row("Modified", profile.modified.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Add environment variables
    table.add_row("", "")  # Empty row for separation
    table.add_row("[bold]Environment Variables[/bold]", "")
    
    for key, value in profile.env.items():
        # Format key for display
        display_key = key.replace("ANTHROPIC_", "")
        display_key = display_key.replace("_", " ").title()
        
        # Format value for display
        if "API_KEY" in key:
            # Show only first 10 characters of API key
            if value and value.startswith("sk-"):
                display_value = value[:10] + "..."
            else:
                display_value = "[red]Invalid format[/red]"
        elif "BASE_URL" in key:
            display_value = value
        else:
            display_value = value
        
        table.add_row(f"[green]{display_key}[/green]", display_value)
    
    console.print(table)


def select_profile_tui(manager) -> Optional[EnvironmentProfile]:
    """Interactive profile selection."""
    profiles = manager.list_profiles()
    
    if not profiles:
        console.print("[yellow]No profiles available for selection.[/yellow]")
        return None
    
    # Create selection table
    table = Table(title="Select Profile", box=box.ROUNDED)
    table.add_column("Index", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Base URL", style="blue")
    table.add_column("Model", style="magenta")
    table.add_column("Description", style="yellow")
    
    # Add profiles to table
    for i, profile in enumerate(profiles):
        base_url = profile.env.get("ANTHROPIC_BASE_URL", "")
        if len(base_url) > 25:
            base_url = base_url[:22] + "..."
        
        model = profile.env.get("ANTHROPIC_MODEL", "")
        if len(model) > 15:
            model = model[:12] + "..."
        
        description = profile.description or ""
        if len(description) > 20:
            description = description[:17] + "..."
        
        table.add_row(str(i + 1), profile.name, base_url, model, description)
    
    console.print(table)
    
    # Get user selection
    while True:
        try:
            choice = Prompt.ask(
                "Enter profile number (or 'q' to quit)",
                choices=[str(i + 1) for i in range(len(profiles))] + ['q']
            )
            
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(profiles):
                return profiles[index]
            
        except (ValueError, KeyboardInterrupt):
            console.print("[red]Invalid selection. Please try again.[/red]")
            continue


def create_profile_tui() -> Optional[EnvironmentProfile]:
    """Interactive profile creation."""
    console.print(Panel.fit("[bold green]Create New Profile[/bold green]", box=box.ROUNDED))
    
    try:
        # Get profile name
        name = Prompt.ask("[cyan]Profile name[/cyan]")
        if not name:
            console.print("[red]Profile name is required.[/red]")
            return None
        
        # Get description
        description = Prompt.ask("[cyan]Description (optional)[/cyan]", default="")
        
        # Get environment variables
        console.print("\n[bold]Environment Variables:[/bold]")
        
        base_url = Prompt.ask(
            "[cyan]ANTHROPIC_BASE_URL[/cyan]",
            default="https://api.anthropic.com"
        )
        
        api_key = Prompt.ask("[cyan]ANTHROPIC_API_KEY[/cyan]")
        
        model = Prompt.ask(
            "[cyan]ANTHROPIC_MODEL[/cyan]",
            default="claude-3-5-sonnet-20241022"
        )
        
        fast_model = Prompt.ask(
            "[cyan]ANTHROPIC_SMALL_FAST_MODEL[/cyan]",
            default="claude-3-haiku-20240307"
        )
        
        # Create environment variables dictionary
        env_vars = {
            "ANTHROPIC_BASE_URL": base_url,
            "ANTHROPIC_API_KEY": api_key,
            "ANTHROPIC_MODEL": model,
            "ANTHROPIC_SMALL_FAST_MODEL": fast_model
        }
        
        # Create profile
        from ..models import EnvironmentProfile
        profile = EnvironmentProfile(
            name=name,
            env=env_vars,
            description=description or None
        )
        
        # Validate profile
        profile.__post_init__()  # This will raise ValueError if invalid
        
        # Show summary
        console.print("\n[bold green]Profile Summary:[/bold green]")
        show_profile_details_tui(profile)
        
        # Confirm creation
        if Confirm.ask("\n[cyan]Create this profile?[/cyan]"):
            return profile
        else:
            console.print("[yellow]Profile creation cancelled.[/yellow]")
            return None
    
    except ValueError as e:
        console.print(f"[red]Validation error: {e}[/red]")
        return None
    except KeyboardInterrupt:
        console.print("\n[yellow]Profile creation cancelled.[/yellow]")
        return None


def edit_profile_tui(manager, profile_name: str) -> Optional[EnvironmentProfile]:
    """Interactive profile editing."""
    try:
        # Get existing profile
        profile = manager.get_profile(profile_name)
        
        console.print(Panel.fit(f"[bold blue]Edit Profile: {profile.name}[/bold blue]", box=box.ROUNDED))
        
        # Show current values
        console.print("\n[bold]Current values:[/bold]")
        show_profile_details_tui(profile)
        
        # Get new values
        console.print("\n[bold]Edit values (leave blank to keep current):[/bold]")
        
        # Get description
        new_description = Prompt.ask(
            "[cyan]Description[/cyan]",
            default=profile.description or ""
        )
        
        # Get environment variables
        console.print("\n[bold]Environment Variables:[/bold]")
        
        new_base_url = Prompt.ask(
            "[cyan]ANTHROPIC_BASE_URL[/cyan]",
            default=profile.env.get("ANTHROPIC_BASE_URL", "")
        )
        
        new_api_key = Prompt.ask(
            "[cyan]ANTHROPIC_API_KEY[/cyan]",
            default=profile.env.get("ANTHROPIC_API_KEY", "")
        )
        
        new_model = Prompt.ask(
            "[cyan]ANTHROPIC_MODEL[/cyan]",
            default=profile.env.get("ANTHROPIC_MODEL", "")
        )
        
        new_fast_model = Prompt.ask(
            "[cyan]ANTHROPIC_SMALL_FAST_MODEL[/cyan]",
            default=profile.env.get("ANTHROPIC_SMALL_FAST_MODEL", "")
        )
        
        # Create updated environment variables
        new_env_vars = {
            "ANTHROPIC_BASE_URL": new_base_url,
            "ANTHROPIC_API_KEY": new_api_key,
            "ANTHROPIC_MODEL": new_model,
            "ANTHROPIC_SMALL_FAST_MODEL": new_fast_model
        }
        
        # Check if anything changed
        env_changed = new_env_vars != profile.env
        desc_changed = new_description != (profile.description or "")
        
        if not env_changed and not desc_changed:
            console.print("[yellow]No changes made.[/yellow]")
            return None
        
        # Update profile
        updated_profile = profile
        
        if env_changed:
            updated_profile.update_env(new_env_vars)
        
        if desc_changed:
            updated_profile.description = new_description or None
        
        # Validate updated profile
        updated_profile.__post_init__()  # This will raise ValueError if invalid
        
        # Show summary
        console.print("\n[bold green]Updated Profile:[/bold green]")
        show_profile_details_tui(updated_profile)
        
        # Confirm update
        if Confirm.ask("\n[cyan]Apply these changes?[/cyan]"):
            return updated_profile
        else:
            console.print("[yellow]Profile update cancelled.[/yellow]")
            return None
    
    except ValueError as e:
        console.print(f"[red]Validation error: {e}[/red]")
        return None
    except KeyboardInterrupt:
        console.print("\n[yellow]Profile update cancelled.[/yellow]")
        return None


def confirm_action_tui(message: str) -> bool:
    """Confirm an action with user."""
    return Confirm.ask(f"[red]{message}[/red]")


def show_success_tui(message: str) -> None:
    """Show success message."""
    console.print(f"[bold green]✅ {message}[/bold green]")


def show_error_tui(message: str) -> None:
    """Show error message."""
    console.print(f"[bold red]❌ {message}[/bold red]")


def show_warning_tui(message: str) -> None:
    """Show warning message."""
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")


def show_info_tui(message: str) -> None:
    """Show info message."""
    console.print(f"[bold blue]ℹ️  {message}[/bold blue]")


def progress_tui(message: str, current: int, total: int) -> None:
    """Show progress message."""
    percentage = (current / total) * 100
    console.print(f"[blue]⏳ {message}[/blue] - {percentage:.1f}% ({current}/{total})")


def loading_tui(message: str) -> None:
    """Show loading message."""
    with console.status(f"[bold blue]{message}...[/bold blue]") as status:
        # This would be used in a context where we're actually doing work
        # For now, just show a simple message
        console.print(f"[bold blue]{message}...[/bold blue]")


def show_banner() -> None:
    """Show application banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                         Claude Code Environment Manager                          ║
    ║                            Manage Claude Code with ease                         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue", box=box.ROUNDED))


def show_help_tui() -> None:
    """Show help information."""
    help_text = """
    [bold green]Available Commands:[/bold green]
    
    [cyan]list[/cyan]        - List all environment profiles
    [cyan]create[/cyan]      - Create a new environment profile
    [cyan]update[/cyan]      - Update an existing profile
    [cyan]delete[/cyan]      - Delete a profile
    [cyan]apply[/cyan]       - Apply a profile to Claude Code
    [cyan]show[/cyan]        - Show profile details
    [cyan]current[/cyan]     - Show current active profile
    [cyan]default[/cyan]     - Set default profile
    [cyan]config[/cyan]      - Show configuration info
    [cyan]init[/cyan]        - Initialize configuration
    
    [bold green]Examples:[/bold green]
    
    • List all profiles: [yellow]claude-env-manager list[/yellow]
    • Create new profile: [yellow]claude-env-manager create --interactive[/yellow]
    • Apply profile: [yellow]claude-env-manager apply development[/yellow]
    • Show profile details: [yellow]claude-env-manager show development[/yellow]
    """
    
    console.print(Panel(help_text, title="Help", box=box.ROUNDED))