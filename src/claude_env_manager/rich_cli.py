#!/usr/bin/env python3
"""
Claude Environment Manager - Rich CLI Interface
Intensive Learning Path - Day 1 Implementation
"""

import argparse
import sys
from rich.console import Console
from rich.table import Table

def create_parser():
    """Create argument parser with subcommands"""
    parser = argparse.ArgumentParser(
        description="""
[bold green]Claude Environment Manager[/]

[bold]Manage your Claude Code configurations with style.[/]

[bold]Examples:[/]
  claude-env list                    # List all environments
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command - our first command
    list_parser = subparsers.add_parser('list', help='List all environments')
    
    return parser

def cmd_list(args, console: Console):
    """Handle the list command with beautiful Rich table"""
    # Create a Rich table
    table = Table(title="🌐 Claude Environments")
    
    # Add columns with styling
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Base URL", style="green")
    table.add_column("Status", style="magenta")
    
    # Sample environments for Day 1
    environments = [
        {"name": "production", "url": "https://api.anthropic.com", "status": "✓ Active"},
        {"name": "development", "url": "https://api.anthropic.com", "status": "● Testing"},  
        {"name": "staging", "url": "https://api.anthropic.com", "status": "◉ Staging"}
    ]
    
    # Add rows with colored status
    for env in environments:
        if "✓ Active" in env["status"]:
            status_style = "[green]✓ Active[/]"
        elif "● Testing" in env["status"]:
            status_style = "[yellow]● Testing[/]"
        elif "◉ Staging" in env["status"]:
            status_style = "[blue]◉ Staging[/]"
        else:
            status_style = env["status"]
            
        table.add_row(
            env["name"],
            env["url"],
            status_style
        )
    
    console.print(table)

def main():
    """Main entry point for the CLI"""
    parser = create_parser()
    args = parser.parse_args()
    
    console = Console()
    
    if args.command == 'list':
        cmd_list(args, console)
    else:
        console.print("[bold red]Error:[/] Please specify a command")
        console.print("Use [yellow]--help[/] for available commands")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()