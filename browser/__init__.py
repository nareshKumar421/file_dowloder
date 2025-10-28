"""
PyBrowser - A Fully Functional Python Web Browser

A complete web browser implementation featuring:
- Full HTML5, CSS3, and JavaScript support via QtWebEngine
- Multi-tab browsing
- History and bookmarks management
- Developer tools
- Network inspection
- Security features (HTTPS enforcement, CSP)
- Storage APIs (LocalStorage, SessionStorage, Cookies)
"""

__version__ = "1.0.0"
__author__ = "PyBrowser Team"
__license__ = "MIT"

from .core.engine import BrowserEngine
from .ui.main_window import BrowserMainWindow

__all__ = ['BrowserEngine', 'BrowserMainWindow']
