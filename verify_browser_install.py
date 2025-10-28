#!/usr/bin/env python3
"""
Browser Installation Verification Script

Checks if all required dependencies for PyBrowser are installed.
"""

import sys

def check_module(module_name, package_name=None):
    """Check if a module can be imported."""
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("PyBrowser Installation Verification")
    print("=" * 60)
    print()

    all_ok = True

    # Check Python version
    print("Python Version:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.7+)")
        all_ok = False

    print()
    print("Required Packages:")

    # Check required packages
    checks = [
        ("PyQt6.QtCore", "PyQt6"),
        ("PyQt6.QtWidgets", "PyQt6"),
        ("PyQt6.QtWebEngineWidgets", "PyQt6-WebEngine"),
        ("PyQt6.QtWebEngineCore", "PyQt6-WebEngine"),
        ("requests", "requests"),
        ("bs4", "beautifulsoup4"),
        ("lxml", "lxml"),
        ("cssutils", "cssutils"),
        ("cryptography", "cryptography"),
    ]

    for module, package in checks:
        if not check_module(module, package):
            all_ok = False

    print()
    print("=" * 60)

    if all_ok:
        print("✓ All dependencies are installed!")
        print()
        print("You can now run the browser:")
        print("  python pybrowser.py")
        print()
        return 0
    else:
        print("✗ Some dependencies are missing!")
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements-browser.txt")
        print()
        print("Or install manually:")
        print("  pip install PyQt6 PyQt6-WebEngine requests beautifulsoup4 lxml cssutils cryptography")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
