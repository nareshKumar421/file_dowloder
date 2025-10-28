"""
Browser Engine Core

Manages the web engine configuration, profiles, and provides
the foundation for the browser's rendering capabilities.
"""

from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QObject, pyqtSignal
import os


class BrowserEngine(QObject):
    """
    Core browser engine managing profiles, settings, and web engine configuration.

    This class provides:
    - Profile management (default, incognito)
    - Global settings configuration
    - Download handling
    - User agent management
    - Cache and storage management
    """

    download_requested = pyqtSignal(object)  # QWebEngineDownloadRequest

    def __init__(self, app_name="PyBrowser", parent=None):
        """
        Initialize the browser engine.

        Args:
            app_name: Application name for storage paths
            parent: Parent QObject
        """
        super().__init__(parent)

        self.app_name = app_name

        # Create data directory
        self.data_dir = os.path.expanduser(f"~/.{app_name.lower()}")
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize profiles
        self.default_profile = self._create_default_profile()
        self.incognito_profile = self._create_incognito_profile()

        # Configure global settings
        self._configure_global_settings()

        # Connect download handler
        self.default_profile.downloadRequested.connect(self.download_requested.emit)
        self.incognito_profile.downloadRequested.connect(self.download_requested.emit)

    def _create_default_profile(self):
        """Create the default profile with persistent storage."""
        profile = QWebEngineProfile.defaultProfile()

        # Set storage paths
        profile.setPersistentStoragePath(os.path.join(self.data_dir, "storage"))
        profile.setCachePath(os.path.join(self.data_dir, "cache"))

        # Configure settings
        settings = profile.settings()
        self._configure_profile_settings(settings)

        # Set user agent
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 PyBrowser/1.0"
        )
        profile.setHttpUserAgent(user_agent)

        return profile

    def _create_incognito_profile(self):
        """Create an incognito profile with no persistent storage."""
        profile = QWebEngineProfile(self)
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)

        # Configure settings
        settings = profile.settings()
        self._configure_profile_settings(settings)

        # Set user agent
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 PyBrowser/1.0"
        )
        profile.setHttpUserAgent(user_agent)

        return profile

    def _configure_profile_settings(self, settings):
        """
        Configure settings for a profile.

        Args:
            settings: QWebEngineSettings instance
        """
        # JavaScript
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)

        # Storage
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)

        # Security
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)

        # Features
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PrintElementBackgrounds, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)

        # DNS prefetching
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)

        # Scrolling
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)

    def _configure_global_settings(self):
        """Configure global web engine settings."""
        settings = QWebEngineSettings.globalSettings()

        # Set default font
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, "Arial")
        settings.setFontFamily(QWebEngineSettings.FontFamily.SerifFont, "Times New Roman")
        settings.setFontFamily(QWebEngineSettings.FontFamily.SansSerifFont, "Arial")
        settings.setFontFamily(QWebEngineSettings.FontFamily.FixedFont, "Courier New")

        # Set font sizes
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFixedFontSize, 13)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumFontSize, 8)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumLogicalFontSize, 6)

    def get_default_profile(self):
        """Get the default profile."""
        return self.default_profile

    def get_incognito_profile(self):
        """Get the incognito profile."""
        return self.incognito_profile

    def clear_cache(self):
        """Clear the browser cache."""
        self.default_profile.clearHttpCache()

    def clear_cookies(self):
        """Clear all cookies."""
        self.default_profile.cookieStore().deleteAllCookies()

    def get_storage_path(self):
        """Get the browser storage path."""
        return self.data_dir

    def set_http_user_agent(self, user_agent, incognito=False):
        """
        Set custom user agent.

        Args:
            user_agent: User agent string
            incognito: Whether to set for incognito profile
        """
        if incognito:
            self.incognito_profile.setHttpUserAgent(user_agent)
        else:
            self.default_profile.setHttpUserAgent(user_agent)

    def get_http_user_agent(self, incognito=False):
        """
        Get current user agent.

        Args:
            incognito: Whether to get from incognito profile

        Returns:
            User agent string
        """
        if incognito:
            return self.incognito_profile.httpUserAgent()
        else:
            return self.default_profile.httpUserAgent()
