#!/usr/bin/env python3
"""
Main Entry Point for Insider-trades repository.
Run `python main.py --help` for available subcommands.
"""

import sys
from src.cli import main

if __name__ == "__main__":
    sys.exit(main())
