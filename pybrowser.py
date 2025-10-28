#!/usr/bin/env python3
"""
PyBrowser - A Fully Functional Python Web Browser

Main launcher script for the PyBrowser application.

Usage:
    python pybrowser.py [url]

Features:
    - Full HTML5, CSS3, and JavaScript support
    - Multi-tab browsing
    - History and bookmarks management
    - Developer tools with console and inspector
    - Network monitoring and downloads
    - Incognito mode
    - Security features (HTTPS enforcement, CSP)
    - Storage APIs (LocalStorage, SessionStorage, Cookies)
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from browser import BrowserMainWindow


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("PyBrowser")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PyBrowser")

    # Create main window
    window = BrowserMainWindow("PyBrowser")

    # Load initial URL if provided
    if len(sys.argv) > 1:
        url = sys.argv[1]
        # Get the first tab and load the URL
        tab = window.tabs.get_current_tab()
        if tab:
            tab.load(url)

    # Show window
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
