"""TUI interface components for Claude Code Environment Manager."""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import yaml
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.prompt import Confirm, Prompt
from rich.style import Style
from rich.table import Table
from rich.theme import Theme

from ..models import EnvironmentProfile

# Custom theme for consistent styling
custom_theme = Theme(
    {
        "success": "green",
        "error": "bold red",
        "warning": "yellow",
        "info": "cyan",
        "primary": "blue",
        "secondary": "magenta",
        "accent": "bold cyan",
        "muted": "dim",
        "highlight": "reverse",
    }
)

console = Console(theme=custom_theme)


def list_profiles_tui(
    profiles: List[EnvironmentProfile],
    verbose: bool = False,
    default_profile: Optional[str] = None,
) -> None:
    """Display profiles in a table format with enhanced styling."""
    if not profiles:
        show_empty_state("No profiles found", "Use 'create' to add your first profile.")
        return

    # Create header with summary
    header_content = (
        f"[bold primary]Environment Profiles[/bold primary] ({len(profiles)} total)"
    )
    if default_profile:
        header_content += f" • [success]Default: {default_profile}[/success]"

    console.print(Panel(header_content, box=box.ROUNDED, border_style="primary"))

    # Create table
    table = Table(box=box.ROUNDED, expand=True)

    # Add columns with better styling
    table.add_column("Name", style="accent", no_wrap=True, width=15)
    table.add_column("Base URL", style="info", width=35)
    table.add_column("Model", style="secondary", width=25)
    if verbose:
        table.add_column("Fast Model", style="warning", width=20)
        table.add_column("API Key", style="error", width=20)
    table.add_column("Description", style="muted", width=30)
    table.add_column("Default", style="success", justify="center", width=8)

    # Sort profiles by name and default status
    sorted_profiles = sorted(
        profiles,
        key=lambda p: (
            0 if p.name == default_profile else 1,  # Default profile first
            p.name.lower(),  # Then alphabetical
        ),
    )

    # Add rows with enhanced styling
    for profile in sorted_profiles:
        # Truncate values for display
        base_url = profile.env.get("ANTHROPIC_BASE_URL", "")
        if len(base_url) > 35:
            base_url = base_url[:32] + "..."

        model = profile.env.get("ANTHROPIC_MODEL", "")
        if len(model) > 25:
            model = model[:22] + "..."

        description = profile.description or ""
        if len(description) > 30:
            description = description[:27] + "..."

        # Determine row styling based on profile status
        name_style = "bold accent" if profile.name == default_profile else "accent"

        # Build row
        row = [f"[{name_style}]{profile.name}[/]", base_url, model]

        if verbose:
            fast_model = profile.env.get("ANTHROPIC_SMALL_FAST_MODEL", "")
            if len(fast_model) > 20:
                fast_model = fast_model[:17] + "..."

            api_key = profile.env.get("ANTHROPIC_API_KEY", "")
            if api_key and api_key.startswith("sk-"):
                # Show masked API key
                api_key = "sk-" + "•" * 8 + "..."
            else:
                api_key = "[error]Not set[/error]"

            row.extend([fast_model, api_key])

        row.append(description)

        # Add default marker with enhanced styling
        is_default = default_profile == profile.name
        if is_default:
            row.append("[bold success]✓[/]")
        else:
            row.append("")

        table.add_row(*row)

    console.print(table)

    # Add footer with action hints
    footer_content = "[dim]Use 'show <name>' for details • 'apply <name>' to activate • 'create' to add new[/dim]"
    console.print(Panel(footer_content, box=box.ROUNDED, border_style="muted"))


def show_profile_details_tui(
    profile: EnvironmentProfile, format: str = "table"
) -> None:
    """Show detailed profile information with enhanced display."""
    if format == "json":
        console.print_json(data=profile.to_dict())
        return

    if format == "yaml":
        yaml_str = yaml.dump(profile.to_dict(), default_flow_style=False)
        console.print(
            Panel(
                yaml_str,
                title=f"Profile: {profile.name}",
                box=box.ROUNDED,
                border_style="primary",
            )
        )
        return

    # Enhanced table format with better organization
    console.print(
        Panel(
            f"[bold primary]Profile Details: {profile.name}[/bold primary]",
            box=box.ROUNDED,
            border_style="primary",
        )
    )

    # Create metadata table
    meta_table = Table(box=box.ROUNDED, expand=True)
    meta_table.add_column("Property", style="accent", width=15)
    meta_table.add_column("Value", style="info", width=50)

    # Add profile metadata
    meta_table.add_row("[bold]Name[/bold]", f"[bold]{profile.name}[/bold]")
    meta_table.add_row(
        "Description", profile.description or "[dim]No description[/dim]"
    )
    meta_table.add_row("Created", profile.created.strftime("%Y-%m-%d %H:%M:%S"))
    meta_table.add_row("Modified", profile.modified.strftime("%Y-%m-%d %H:%M:%S"))

    console.print(meta_table)

    # Create environment variables table
    console.print()  # Spacing
    console.print(
        Panel(
            "[bold secondary]Environment Variables[/bold secondary]",
            box=box.ROUNDED,
            border_style="secondary",
        )
    )

    env_table = Table(box=box.ROUNDED, expand=True)
    env_table.add_column("Variable", style="warning", width=25)
    env_table.add_column("Value", style="info", width=45)

    # Group environment variables for better organization
    env_vars = {
        "Authentication": ["ANTHROPIC_API_KEY"],
        "Configuration": [
            "ANTHROPIC_BASE_URL",
            "ANTHROPIC_MODEL",
            "ANTHROPIC_SMALL_FAST_MODEL",
        ],
    }

    # Add environment variables by category
    for category, keys in env_vars.items():
        if category == "Authentication":
            env_table.add_row(f"[bold {category.lower()}]{category}[/bold]", "")
            for key in keys:
                if key in profile.env:
                    value = profile.env[key]
                    if value and value.startswith("sk-"):
                        display_value = "sk-" + "•" * 12 + "..."
                    else:
                        display_value = "[error]Invalid format[/error]"
                    display_key = (
                        key.replace("ANTHROPIC_", "").replace("_", " ").title()
                    )
                    env_table.add_row(
                        f"[{category.lower()}]{display_key}[/]", display_value
                    )
        elif category == "Configuration":
            env_table.add_row(f"[bold {category.lower()}]{category}[/bold]", "")
            for key in keys:
                if key in profile.env:
                    value = profile.env[key]
                    display_key = (
                        key.replace("ANTHROPIC_", "").replace("_", " ").title()
                    )
                    env_table.add_row(f"[{category.lower()}]{display_key}[/]", value)

    # Add any additional environment variables
    additional_vars = [
        k for k in profile.env.keys() if k not in sum(env_vars.values(), [])
    ]
    if additional_vars:
        env_table.add_row("[bold info]Additional[/bold]", "")
        for key in additional_vars:
            value = profile.env[key]
            display_key = key.replace("ANTHROPIC_", "").replace("_", " ").title()
            env_table.add_row(f"[info]{display_key}[/]", value)

    console.print(env_table)

    # Add validation status
    console.print()  # Spacing
    try:
        profile.__post_init__()  # This will raise ValueError if invalid
        validation_status = "[success]✓ Valid[/success]"
    except ValueError as e:
        validation_status = f"[error]✗ Invalid: {e}[/error]"

    console.print(
        Panel(
            f"Validation Status: {validation_status}",
            box=box.ROUNDED,
            border_style="success" if "Valid" in validation_status else "error",
        )
    )


def select_profile_tui(manager) -> Optional[EnvironmentProfile]:
    """Interactive profile selection with enhanced UI."""
    profiles = manager.list_profiles()

    if not profiles:
        show_empty_state(
            "No profiles available", "Use 'create' to add a profile first."
        )
        return None

    # Create header
    console.print(
        Panel(
            "[bold primary]Select Profile[/bold primary]",
            box=box.ROUNDED,
            border_style="primary",
        )
    )

    # Create selection table with better styling
    table = Table(box=box.ROUNDED, expand=True)
    table.add_column("#", style="accent", justify="right", width=3)
    table.add_column("Name", style="accent", width=15)
    table.add_column("Base URL", style="info", width=30)
    table.add_column("Model", style="secondary", width=20)
    table.add_column("Description", style="muted", width=25)

    # Get default profile for highlighting
    default_profile = manager.get_default_profile()

    # Add profiles to table
    for i, profile in enumerate(profiles):
        base_url = profile.env.get("ANTHROPIC_BASE_URL", "")
        if len(base_url) > 30:
            base_url = base_url[:27] + "..."

        model = profile.env.get("ANTHROPIC_MODEL", "")
        if len(model) > 18:
            model = model[:15] + "..."

        description = profile.description or ""
        if len(description) > 25:
            description = description[:22] + "..."

        # Highlight default profile
        name_style = "bold accent" if profile.name == default_profile else "accent"

        table.add_row(
            str(i + 1), f"[{name_style}]{profile.name}[/]", base_url, model, description
        )

    console.print(table)

    # Add footer with instructions
    footer_content = (
        "[dim]Enter number to select • 'q' to quit • 'c' to create new profile[/dim]"
    )
    console.print(Panel(footer_content, box=box.ROUNDED, border_style="muted"))

    # Get user selection with enhanced error handling
    while True:
        try:
            choices = [str(i + 1) for i in range(len(profiles))] + ["q", "c"]
            choice = Prompt.ask(
                "[primary]Select profile[/primary]", choices=choices, show_choices=False
            )

            if choice.lower() == "q":
                show_info_tui("Selection cancelled.")
                return None

            if choice.lower() == "c":
                console.print()
                show_info_tui("Creating new profile...")
                return create_profile_tui()

            index = int(choice) - 1
            if 0 <= index < len(profiles):
                selected_profile = profiles[index]
                show_success_tui(f"Selected profile: {selected_profile.name}")
                return selected_profile

        except (ValueError, KeyboardInterrupt):
            show_error_tui("Invalid selection. Please try again.")
            time.sleep(1)  # Brief pause for better UX
            continue


def create_profile_tui() -> Optional[EnvironmentProfile]:
    """Interactive profile creation."""
    console.print(
        Panel.fit("[bold green]Create New Profile[/bold green]", box=box.ROUNDED)
    )

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
            "[cyan]ANTHROPIC_BASE_URL[/cyan]", default="https://api.anthropic.com"
        )

        api_key = Prompt.ask("[cyan]ANTHROPIC_API_KEY[/cyan]")

        model = Prompt.ask(
            "[cyan]ANTHROPIC_MODEL[/cyan]", default="claude-3-5-sonnet-20241022"
        )

        fast_model = Prompt.ask(
            "[cyan]ANTHROPIC_SMALL_FAST_MODEL[/cyan]", default="claude-3-haiku-20240307"
        )

        # Create environment variables dictionary
        env_vars = {
            "ANTHROPIC_BASE_URL": base_url,
            "ANTHROPIC_API_KEY": api_key,
            "ANTHROPIC_MODEL": model,
            "ANTHROPIC_SMALL_FAST_MODEL": fast_model,
        }

        # Create profile
        from ..models import EnvironmentProfile

        profile = EnvironmentProfile(
            name=name, env=env_vars, description=description or None
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

        console.print(
            Panel.fit(
                f"[bold blue]Edit Profile: {profile.name}[/bold blue]", box=box.ROUNDED
            )
        )

        # Show current values
        console.print("\n[bold]Current values:[/bold]")
        show_profile_details_tui(profile)

        # Get new values
        console.print("\n[bold]Edit values (leave blank to keep current):[/bold]")

        # Get description
        new_description = Prompt.ask(
            "[cyan]Description[/cyan]", default=profile.description or ""
        )

        # Get environment variables
        console.print("\n[bold]Environment Variables:[/bold]")

        new_base_url = Prompt.ask(
            "[cyan]ANTHROPIC_BASE_URL[/cyan]",
            default=profile.env.get("ANTHROPIC_BASE_URL", ""),
        )

        new_api_key = Prompt.ask(
            "[cyan]ANTHROPIC_API_KEY[/cyan]",
            default=profile.env.get("ANTHROPIC_API_KEY", ""),
        )

        new_model = Prompt.ask(
            "[cyan]ANTHROPIC_MODEL[/cyan]",
            default=profile.env.get("ANTHROPIC_MODEL", ""),
        )

        new_fast_model = Prompt.ask(
            "[cyan]ANTHROPIC_SMALL_FAST_MODEL[/cyan]",
            default=profile.env.get("ANTHROPIC_SMALL_FAST_MODEL", ""),
        )

        # Create updated environment variables
        new_env_vars = {
            "ANTHROPIC_BASE_URL": new_base_url,
            "ANTHROPIC_API_KEY": new_api_key,
            "ANTHROPIC_MODEL": new_model,
            "ANTHROPIC_SMALL_FAST_MODEL": new_fast_model,
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


def show_empty_state(title: str, message: str) -> None:
    """Show empty state with helpful message."""
    empty_panel = Panel(
        f"[bold warning]{title}[/bold warning]\n\n[dim]{message}[/dim]",
        box=box.ROUNDED,
        border_style="warning",
        title="Empty",
    )
    console.print(empty_panel)


def confirm_action_tui(message: str) -> bool:
    """Confirm an action with user."""
    return Confirm.ask(f"[error]{message}[/error]")


def show_success_tui(message: str) -> None:
    """Show success message."""
    console.print(f"[success]✅ {message}[/success]")


def show_error_tui(message: str, suggestion: str = "") -> None:
    """Show error message with optional suggestion."""
    error_content = f"[error]❌ {message}[/error]"
    if suggestion:
        error_content += f"\n[dim]💡 {suggestion}[/dim]"
    console.print(Panel(error_content, box=box.ROUNDED, border_style="error"))


def show_warning_tui(message: str) -> None:
    """Show warning message."""
    console.print(f"[warning]⚠️  {message}[/warning]")


def show_info_tui(message: str) -> None:
    """Show info message."""
    console.print(f"[info]ℹ️  {message}[/info]")


def progress_tui(message: str, current: int, total: int) -> None:
    """Show progress message."""
    percentage = (current / total) * 100
    progress_content = f"[info]⏳ {message}[/info] • [primary]{percentage:.1f}%[/primary] ([success]{current}/{total}[/success])"
    console.print(Panel(progress_content, box=box.ROUNDED, border_style="info"))


def loading_tui(message: str) -> None:
    """Show loading message with spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[bold blue]{message}...[/bold blue]", total=None)
        # Simulate some work - in real usage, this would be replaced with actual work
        time.sleep(0.1)


def show_progress_with_steps(message: str, steps: List[str]) -> None:
    """Show progress with multiple steps."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[bold primary]{message}[/bold primary]", total=len(steps)
        )

        for i, step in enumerate(steps):
            progress.update(
                task, advance=1, description=f"[bold blue]{step}[/bold blue]"
            )
            time.sleep(0.1)  # Simulate work


def show_operation_result(
    operation: str, success: bool, message: str = "", details: str = ""
) -> None:
    """Show operation result with consistent styling."""
    if success:
        status_icon = "[success]✅[/success]"
        status_style = "success"
        status_text = "Success"
    else:
        status_icon = "[error]❌[/error]"
        status_style = "error"
        status_text = "Failed"

    result_content = f"{status_icon} [bold]{operation}[/bold]: [bold {status_style}]{status_text}[/bold {status_style}]"

    if message:
        result_content += f"\n{message}"

    if details:
        result_content += f"\n[dim]{details}[/dim]"

    console.print(Panel(result_content, box=box.ROUNDED, border_style=status_style))


def show_banner() -> None:
    """Show application banner."""
    banner_text = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                          Claude Code Environment Manager                         ║
    ║                     Professional Environment Configuration Tool                     ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """

    # Get current time for dynamic content
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    banner_content = Panel(
        f"{banner_text}\n[dim]Started at {current_time}[/dim]",
        style="bold blue",
        box=box.ROUNDED,
        border_style="blue",
    )
    console.print(banner_content)


def show_help_tui() -> None:
    """Show comprehensive help information."""
    help_panel = Panel(
        "[bold blue]Claude Code Environment Manager[/bold blue]\n"
        "[dim]Manage Claude Code environment configurations with ease[/dim]",
        box=box.ROUNDED,
        border_style="blue",
    )
    console.print(help_panel)

    # Commands section
    console.print()
    console.print(
        Panel(
            "[bold cyan]Available Commands[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan",
        )
    )

    commands_table = Table(box=box.ROUNDED, expand=True)
    commands_table.add_column("Command", style="cyan", width=15)
    commands_table.add_column("Description", style="green", width=45)
    commands_table.add_column("Example", style="dim", width=30)

    commands = [
        ("list/ls", "List all environment profiles", "claude-env-manager list"),
        ("create", "Create a new environment profile", "claude-env-manager create -i"),
        ("update", "Update an existing profile", "claude-env-manager update dev -i"),
        ("delete", "Delete a profile", "claude-env-manager delete old"),
        ("apply", "Apply a profile to Claude Code", "claude-env-manager apply dev"),
        ("show", "Show profile details", "claude-env-manager show dev"),
        ("current", "Show current active profile", "claude-env-manager current"),
        ("default", "Set default profile", "claude-env-manager default dev"),
        ("config", "Show configuration info", "claude-env-manager config -v"),
        ("init", "Initialize configuration", "claude-env-manager init"),
    ]

    for cmd, desc, example in commands:
        commands_table.add_row(f"[cyan]{cmd}[/]", desc, f"[dim]{example}[/]")

    console.print(commands_table)

    # Options section
    console.print()
    console.print(
        Panel(
            "[bold yellow]Common Options[/bold yellow]",
            box=box.ROUNDED,
            border_style="yellow",
        )
    )

    options_table = Table(box=box.ROUNDED, expand=True)
    options_table.add_column("Option", style="cyan", width=20)
    options_table.add_column("Description", style="green", width=60)

    options = [
        ("-c, --config FILE", "Specify configuration file path"),
        ("-s, --settings FILE", "Specify settings file path"),
        ("-v, --verbose", "Enable verbose output"),
        ("-q, --quiet", "Quiet mode (minimal output)"),
        ("-i, --interactive", "Interactive mode"),
        ("-f, --format FORMAT", "Output format (table, json, yaml)"),
        ("-n, --name NAME", "Profile name"),
        ("-f, --force", "Force operation without confirmation"),
    ]

    for opt, desc in options:
        options_table.add_row(f"[cyan]{opt}[/]", desc)

    console.print(options_table)

    # Footer
    console.print()
    footer_content = (
        "[dim]Use 'claude-env-manager <command> --help' for detailed command help[/dim]"
    )
    console.print(Panel(footer_content, box=box.ROUNDED, border_style="muted"))
