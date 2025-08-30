#!/usr/bin/env python3
"""
Simple entry point for Claude Environment Manager CLI
Usage: python ce.py list
"""

from src.claude_env_manager.rich_cli import main

if __name__ == "__main__":
    main()