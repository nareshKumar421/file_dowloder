#!/usr/bin/env python3
"""
Simple launcher for the File Downloader GUI
"""

import sys
import subprocess

def check_dependencies():
    """Check if GUI dependencies are installed"""
    try:
        import customtkinter
        return True
    except ImportError:
        return False

def main():
    if not check_dependencies():
        print("=" * 60)
        print("GUI dependencies not installed!")
        print("=" * 60)
        print("\nPlease install GUI dependencies:")
        print("  pip install -r requirements-gui.txt")
        print("\nOr install customtkinter directly:")
        print("  pip install customtkinter")
        print("=" * 60)
        sys.exit(1)

    # Import and run GUI
    from downloader_gui import main as gui_main
    gui_main()

if __name__ == "__main__":
    main()
