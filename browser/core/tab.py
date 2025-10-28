"""
Browser Tab Implementation

Each tab contains a QtWebEngineView with full HTML5/CSS3/JavaScript support.
Handles page loading, navigation, events, and communication with the main window.
"""

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt6.QtCore import QUrl, pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class BrowserTab(QWidget):
    """
    Individual browser tab with web engine integration.

    Signals:
        url_changed: Emitted when the URL changes
        title_changed: Emitted when the page title changes
        loading_progress: Emitted during page load (0-100)
        loading_started: Emitted when page loading starts
        loading_finished: Emitted when page loading completes
        icon_changed: Emitted when the page icon changes
    """

    url_changed = pyqtSignal(QUrl)
    title_changed = pyqtSignal(str)
    loading_progress = pyqtSignal(int)
    loading_started = pyqtSignal()
    loading_finished = pyqtSignal(bool)
    icon_changed = pyqtSignal()

    def __init__(self, profile=None, parent=None):
        """
        Initialize a browser tab.

        Args:
            profile: QWebEngineProfile for this tab (for cookies, cache, etc.)
            parent: Parent widget
        """
        super().__init__(parent)

        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create web engine view
        if profile:
            self.web_view = QWebEngineView()
            page = QWebEnginePage(profile, self.web_view)
            self.web_view.setPage(page)
        else:
            self.web_view = QWebEngineView()

        self.layout.addWidget(self.web_view)

        # Configure web engine settings
        self._configure_settings()

        # Connect signals
        self._connect_signals()

        # History tracking
        self.history = []
        self.history_index = -1

    def _configure_settings(self):
        """Configure web engine settings for modern web support."""
        settings = self.web_view.settings()

        # Enable all modern web features
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)

        # Set default font sizes
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumFontSize, 10)

    def _connect_signals(self):
        """Connect web view signals to tab signals."""
        self.web_view.urlChanged.connect(self._on_url_changed)
        self.web_view.titleChanged.connect(self.title_changed.emit)
        self.web_view.loadProgress.connect(self.loading_progress.emit)
        self.web_view.loadStarted.connect(self.loading_started.emit)
        self.web_view.loadFinished.connect(self._on_load_finished)
        self.web_view.iconChanged.connect(self.icon_changed.emit)

    def _on_url_changed(self, url):
        """Handle URL change and update history."""
        self.url_changed.emit(url)

        # Update history
        if self.history_index < len(self.history) - 1:
            # Remove forward history if we navigate from middle of history
            self.history = self.history[:self.history_index + 1]

        self.history.append(url.toString())
        self.history_index = len(self.history) - 1

    def _on_load_finished(self, success):
        """Handle page load completion."""
        self.loading_finished.emit(success)

    def load(self, url):
        """
        Load a URL in this tab.

        Args:
            url: URL string or QUrl object
        """
        if isinstance(url, str):
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://', 'file://', 'about:')):
                url = 'https://' + url
            url = QUrl(url)

        self.web_view.load(url)

    def reload(self):
        """Reload the current page."""
        self.web_view.reload()

    def stop(self):
        """Stop loading the current page."""
        self.web_view.stop()

    def back(self):
        """Navigate back in history."""
        if self.can_go_back():
            self.web_view.back()

    def forward(self):
        """Navigate forward in history."""
        if self.can_go_forward():
            self.web_view.forward()

    def can_go_back(self):
        """Check if can navigate back."""
        return self.web_view.history().canGoBack()

    def can_go_forward(self):
        """Check if can navigate forward."""
        return self.web_view.history().canGoForward()

    def url(self):
        """Get current URL."""
        return self.web_view.url()

    def title(self):
        """Get current page title."""
        title = self.web_view.title()
        return title if title else "New Tab"

    def icon(self):
        """Get current page icon."""
        return self.web_view.icon()

    def is_loading(self):
        """Check if page is currently loading."""
        return self.web_view.isLoading()

    def execute_javascript(self, script, callback=None):
        """
        Execute JavaScript in the page context.

        Args:
            script: JavaScript code to execute
            callback: Optional callback for the result
        """
        if callback:
            self.web_view.page().runJavaScript(script, callback)
        else:
            self.web_view.page().runJavaScript(script)

    def zoom_in(self):
        """Zoom in."""
        current = self.web_view.zoomFactor()
        self.web_view.setZoomFactor(min(current + 0.1, 3.0))

    def zoom_out(self):
        """Zoom out."""
        current = self.web_view.zoomFactor()
        self.web_view.setZoomFactor(max(current - 0.1, 0.25))

    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.web_view.setZoomFactor(1.0)

    def find_text(self, text, case_sensitive=False):
        """
        Find text in the page.

        Args:
            text: Text to find
            case_sensitive: Whether search is case sensitive
        """
        flags = QWebEnginePage.FindFlag(0)
        if case_sensitive:
            flags = QWebEnginePage.FindFlag.FindCaseSensitively

        self.web_view.findText(text, flags)

    def get_html(self, callback):
        """
        Get the page HTML.

        Args:
            callback: Callback function to receive HTML
        """
        self.web_view.page().toHtml(callback)

    def get_selected_text(self):
        """Get currently selected text."""
        return self.web_view.selectedText()

    def page(self):
        """Get the QWebEnginePage instance."""
        return self.web_view.page()
