"""
Browser Main Window

The main browser window integrating all components:
- Tabs management
- Navigation bar
- Browser engine
- History and bookmarks
- Developer tools
- Network management
- Storage
- Security
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QMessageBox,
    QDialog, QListWidget, QDialogButtonBox, QLabel,
    QInputDialog, QFileDialog, QSplitter
)
from PyQt6.QtCore import Qt, QUrl, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence, QIcon

from browser.core.engine import BrowserEngine
from browser.core.tab import BrowserTab
from browser.core.history import HistoryManager
from browser.core.bookmarks import BookmarksManager
from browser.ui.navigation_bar import NavigationBar
from browser.ui.tabs_widget import BrowserTabWidget
from browser.network.network_manager import NetworkManager
from browser.storage.storage_manager import StorageManager
from browser.security.security_manager import SecurityManager
from browser.devtools.devtools_panel import DevToolsPanel


class BrowserMainWindow(QMainWindow):
    """
    Main browser window.

    This is the primary browser interface that integrates all components.
    """

    def __init__(self, app_name="PyBrowser"):
        """
        Initialize the main browser window.

        Args:
            app_name: Application name
        """
        super().__init__()

        self.app_name = app_name
        self.setWindowTitle(app_name)
        self.resize(1200, 800)

        # Initialize browser engine
        self.engine = BrowserEngine(app_name, self)

        # Initialize managers
        storage_path = self.engine.get_storage_path()
        self.history_manager = HistoryManager(storage_path, self)
        self.bookmarks_manager = BookmarksManager(storage_path, self)
        self.network_manager = NetworkManager(
            self.engine.get_default_profile(),
            storage_path,
            self
        )
        self.storage_manager = StorageManager(storage_path, self)
        self.security_manager = SecurityManager(self)

        # Developer tools
        self.devtools = None
        self.devtools_visible = False

        # Home page
        self.home_url = "https://www.google.com"

        # Create UI
        self._create_ui()
        self._create_menu_bar()
        self._connect_signals()

        # Create initial tab
        self.add_new_tab(self.home_url)

        # Apply stylesheet
        self._apply_stylesheet()

    def _create_ui(self):
        """Create the main UI."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Navigation bar
        self.nav_bar = NavigationBar(self)
        layout.addWidget(self.nav_bar)

        # Tabs widget
        self.tabs = BrowserTabWidget(self)
        layout.addWidget(self.tabs)

        # Status bar
        self.statusBar().showMessage("Ready")

    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        new_window_action = QAction("New Window", self)
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        new_window_action.triggered.connect(self._new_window)
        file_menu.addAction(new_window_action)

        new_incognito_action = QAction("New Incognito Tab", self)
        new_incognito_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_incognito_action.triggered.connect(self._new_incognito_tab)
        file_menu.addAction(new_incognito_action)

        file_menu.addSeparator()

        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_action.triggered.connect(self.tabs.close_current_tab)
        file_menu.addAction(close_tab_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        find_action = QAction("Find...", self)
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self._find_in_page)
        edit_menu.addAction(find_action)

        # View menu
        view_menu = menubar.addMenu("View")

        reload_action = QAction("Reload", self)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.triggered.connect(self._reload_current_tab)
        view_menu.addAction(reload_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self._zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self._zoom_out)
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self._reset_zoom)
        view_menu.addAction(reset_zoom_action)

        view_menu.addSeparator()

        fullscreen_action = QAction("Full Screen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # History menu
        history_menu = menubar.addMenu("History")

        show_history_action = QAction("Show History", self)
        show_history_action.setShortcut(QKeySequence("Ctrl+H"))
        show_history_action.triggered.connect(self._show_history)
        history_menu.addAction(show_history_action)

        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self._clear_history)
        history_menu.addAction(clear_history_action)

        # Bookmarks menu
        bookmarks_menu = menubar.addMenu("Bookmarks")

        bookmark_page_action = QAction("Bookmark This Page", self)
        bookmark_page_action.setShortcut(QKeySequence("Ctrl+D"))
        bookmark_page_action.triggered.connect(self._bookmark_current_page)
        bookmarks_menu.addAction(bookmark_page_action)

        show_bookmarks_action = QAction("Show Bookmarks", self)
        show_bookmarks_action.setShortcut(QKeySequence("Ctrl+Shift+B"))
        show_bookmarks_action.triggered.connect(self._show_bookmarks)
        bookmarks_menu.addAction(show_bookmarks_action)

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        devtools_action = QAction("Developer Tools", self)
        devtools_action.setShortcut(QKeySequence("F12"))
        devtools_action.triggered.connect(self._toggle_devtools)
        tools_menu.addAction(devtools_action)

        tools_menu.addSeparator()

        downloads_action = QAction("Downloads", self)
        downloads_action.setShortcut(QKeySequence("Ctrl+J"))
        downloads_action.triggered.connect(self._show_downloads)
        tools_menu.addAction(downloads_action)

        tools_menu.addSeparator()

        clear_cache_action = QAction("Clear Cache", self)
        clear_cache_action.triggered.connect(self._clear_cache)
        tools_menu.addAction(clear_cache_action)

        clear_cookies_action = QAction("Clear Cookies", self)
        clear_cookies_action.triggered.connect(self._clear_cookies)
        tools_menu.addAction(clear_cookies_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _connect_signals(self):
        """Connect all signals."""
        # Navigation bar signals
        self.nav_bar.navigate_home.connect(self._navigate_home)
        self.nav_bar.navigate_back.connect(self._navigate_back)
        self.nav_bar.navigate_forward.connect(self._navigate_forward)
        self.nav_bar.reload.connect(self._reload_current_tab)
        self.nav_bar.stop.connect(self._stop_loading)
        self.nav_bar.url_submitted.connect(self._on_url_submitted)
        self.nav_bar.bookmark_added.connect(self._bookmark_current_page)
        self.nav_bar.new_tab.connect(lambda: self.add_new_tab())
        self.nav_bar.new_incognito_tab.connect(self._new_incognito_tab)
        self.nav_bar.toggle_devtools.connect(self._toggle_devtools)

        # Tabs signals
        self.tabs.tab_changed.connect(self._on_tab_changed)
        self.tabs.tab_close_requested.connect(self._on_tab_close_requested)
        self.tabs.new_tab_requested.connect(lambda: self.add_new_tab())

        # Network manager signals
        self.network_manager.download_started.connect(self._on_download_started)
        self.network_manager.download_finished.connect(self._on_download_finished)

    def add_new_tab(self, url=None, incognito=False):
        """
        Add a new browser tab.

        Args:
            url: Initial URL to load
            incognito: Whether to use incognito mode
        """
        # Create tab
        profile = (self.engine.get_incognito_profile() if incognito
                  else self.engine.get_default_profile())

        tab = BrowserTab(profile, self)

        # Connect tab signals
        tab.url_changed.connect(lambda url: self._on_tab_url_changed(tab, url))
        tab.title_changed.connect(lambda title: self._on_tab_title_changed(tab, title))
        tab.loading_started.connect(lambda: self._on_tab_loading_started(tab))
        tab.loading_finished.connect(lambda success: self._on_tab_loading_finished(tab, success))
        tab.loading_progress.connect(lambda progress: self._on_tab_loading_progress(tab, progress))

        # Connect console messages to devtools
        tab.page().javaScriptConsoleMessage = self._on_console_message

        # Add tab to tabs widget
        title = "New Tab" + (" (Incognito)" if incognito else "")
        index = self.tabs.add_tab(tab, title)
        self.tabs.setCurrentIndex(index)

        # Load URL
        if url:
            tab.load(url)
        else:
            tab.load(self.home_url)

        return tab

    def _on_tab_changed(self, index):
        """Handle tab change."""
        tab = self.tabs.get_current_tab()
        if tab:
            # Update navigation bar
            self.nav_bar.set_url(tab.url())
            self.nav_bar.set_back_enabled(tab.can_go_back())
            self.nav_bar.set_forward_enabled(tab.can_go_forward())
            self.nav_bar.set_loading_state(tab.is_loading())

            # Update window title
            self.setWindowTitle(f"{tab.title()} - {self.app_name}")

    def _on_tab_close_requested(self, index):
        """Handle tab close request."""
        self.tabs.remove_tab(index)

        # Close window if no tabs left
        if self.tabs.count() == 0:
            self.close()

    def _on_tab_url_changed(self, tab, url):
        """Handle tab URL change."""
        # Only update if this is the current tab
        if tab == self.tabs.get_current_tab():
            self.nav_bar.set_url(url)
            self.nav_bar.set_back_enabled(tab.can_go_back())
            self.nav_bar.set_forward_enabled(tab.can_go_forward())

        # Add to history (only for non-incognito tabs)
        url_str = url.toString()
        if url_str and not url_str.startswith(('about:', 'chrome:')):
            self.history_manager.add_entry(url_str, tab.title())

    def _on_tab_title_changed(self, tab, title):
        """Handle tab title change."""
        # Only update window title if this is the current tab
        if tab == self.tabs.get_current_tab():
            self.setWindowTitle(f"{title} - {self.app_name}")

    def _on_tab_loading_started(self, tab):
        """Handle tab loading start."""
        if tab == self.tabs.get_current_tab():
            self.nav_bar.set_loading_state(True)
            self.statusBar().showMessage("Loading...")

    def _on_tab_loading_finished(self, tab, success):
        """Handle tab loading finish."""
        if tab == self.tabs.get_current_tab():
            self.nav_bar.set_loading_state(False)
            if success:
                self.statusBar().showMessage("Ready", 2000)
            else:
                self.statusBar().showMessage("Failed to load page", 3000)

    def _on_tab_loading_progress(self, tab, progress):
        """Handle tab loading progress."""
        if tab == self.tabs.get_current_tab():
            self.nav_bar.set_progress(progress)

    def _on_url_submitted(self, url):
        """Handle URL submission."""
        tab = self.tabs.get_current_tab()
        if tab:
            # Validate URL with security manager
            is_valid, error_msg = self.security_manager.validate_url(url)

            if not is_valid:
                QMessageBox.warning(self, "Security Warning", error_msg)
                return

            tab.load(url)

    def _navigate_home(self):
        """Navigate to home page."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.load(self.home_url)

    def _navigate_back(self):
        """Navigate back."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.back()

    def _navigate_forward(self):
        """Navigate forward."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.forward()

    def _reload_current_tab(self):
        """Reload current tab."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.reload()

    def _stop_loading(self):
        """Stop loading current tab."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.stop()

    def _zoom_in(self):
        """Zoom in current tab."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.zoom_in()

    def _zoom_out(self):
        """Zoom out current tab."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.zoom_out()

    def _reset_zoom(self):
        """Reset zoom in current tab."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.reset_zoom()

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _new_window(self):
        """Open a new browser window."""
        new_window = BrowserMainWindow(self.app_name)
        new_window.show()

    def _new_incognito_tab(self):
        """Open a new incognito tab."""
        self.add_new_tab(incognito=True)

    def _bookmark_current_page(self):
        """Bookmark the current page."""
        tab = self.tabs.get_current_tab()
        if tab:
            url = tab.url().toString()
            title = tab.title()

            if self.bookmarks_manager.is_bookmarked(url):
                QMessageBox.information(self, "Bookmark", "This page is already bookmarked.")
            else:
                self.bookmarks_manager.add_bookmark(url, title)
                QMessageBox.information(self, "Bookmark Added", f"Bookmarked: {title}")

    def _show_history(self):
        """Show history dialog."""
        dialog = HistoryDialog(self.history_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            url = dialog.get_selected_url()
            if url:
                tab = self.tabs.get_current_tab()
                if tab:
                    tab.load(url)

    def _clear_history(self):
        """Clear browsing history."""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all browsing history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.history_manager.clear_history()
            QMessageBox.information(self, "History Cleared", "Browsing history has been cleared.")

    def _show_bookmarks(self):
        """Show bookmarks dialog."""
        dialog = BookmarksDialog(self.bookmarks_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            url = dialog.get_selected_url()
            if url:
                tab = self.tabs.get_current_tab()
                if tab:
                    tab.load(url)

    def _toggle_devtools(self):
        """Toggle developer tools."""
        if self.devtools is None:
            self.devtools = DevToolsPanel(self)
            self.devtools.execute_js.connect(self._execute_javascript)
            self.devtools.resize(800, 400)

        if self.devtools.isVisible():
            self.devtools.hide()
        else:
            self.devtools.show()

    def _execute_javascript(self, code):
        """Execute JavaScript in current tab."""
        tab = self.tabs.get_current_tab()
        if tab:
            tab.execute_javascript(code, lambda result: self._on_js_result(result))

    def _on_js_result(self, result):
        """Handle JavaScript execution result."""
        if self.devtools:
            self.devtools.log_console(f"← {result}", "log")

    def _on_console_message(self, level, message, line, source):
        """Handle console message from web page."""
        if self.devtools and self.devtools.isVisible():
            self.devtools.handle_console_message(level, message, line, source)

    def _show_downloads(self):
        """Show downloads."""
        downloads = self.network_manager.get_active_downloads()
        if downloads:
            msg = "Active Downloads:\n\n"
            for filename, info in downloads.items():
                msg += f"• {filename}\n  From: {info['url']}\n\n"
            QMessageBox.information(self, "Downloads", msg)
        else:
            QMessageBox.information(self, "Downloads", "No active downloads.")

    def _on_download_started(self, filename, url):
        """Handle download started."""
        self.statusBar().showMessage(f"Downloading: {filename}", 3000)

    def _on_download_finished(self, filename, path):
        """Handle download finished."""
        self.statusBar().showMessage(f"Downloaded: {filename}", 3000)

    def _clear_cache(self):
        """Clear browser cache."""
        self.engine.clear_cache()
        QMessageBox.information(self, "Cache Cleared", "Browser cache has been cleared.")

    def _clear_cookies(self):
        """Clear cookies."""
        self.engine.clear_cookies()
        QMessageBox.information(self, "Cookies Cleared", "Cookies have been cleared.")

    def _find_in_page(self):
        """Find text in page."""
        text, ok = QInputDialog.getText(self, "Find", "Find text:")
        if ok and text:
            tab = self.tabs.get_current_tab()
            if tab:
                tab.find_text(text)

    def _show_about(self):
        """Show about dialog."""
        about_text = f"""
        <h2>{self.app_name}</h2>
        <p>Version 1.0.0</p>
        <p>A fully functional web browser built with Python and PyQt6.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>Full HTML5, CSS3, and JavaScript support</li>
            <li>Multi-tab browsing</li>
            <li>History and bookmarks</li>
            <li>Developer tools</li>
            <li>Incognito mode</li>
            <li>Network management</li>
            <li>Security features</li>
        </ul>
        """
        QMessageBox.about(self, "About", about_text)

    def _apply_stylesheet(self):
        """Apply premium Chrome-exact application stylesheet with polish."""
        self.setStyleSheet("""
            QMainWindow {
                background: white;
            }

            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f2f2f2, stop:0.5 #ececec, stop:1 #e5e5e5);
                border-bottom: 1px solid #bbbbbe;
                color: #202124;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 2px;
            }

            QMenuBar::item {
                padding: 7px 16px;
                border-radius: 5px;
                margin: 3px 2px;
            }

            QMenuBar::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(95,99,104,0.08), stop:1 rgba(95,99,104,0.12));
            }

            QMenuBar::item:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(95,99,104,0.15), stop:1 rgba(95,99,104,0.22));
            }

            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f2f2f2, stop:0.5 #ececec, stop:1 #e5e5e5);
                border-top: 1px solid #bbbbbe;
                color: #5f6368;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 4px 8px;
            }

            QDialog {
                background: white;
            }

            QListWidget {
                border: 1px solid #dadce0;
                border-radius: 8px;
                background: white;
                outline: none;
            }

            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e8eaed;
            }

            QListWidget::item:hover {
                background: #f8f9fa;
            }

            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8f0fe, stop:1 #d2e3fc);
                color: #1a73e8;
            }

            QDialogButtonBox QPushButton {
                padding: 8px 24px;
                border-radius: 6px;
                border: 1px solid #dadce0;
                background: white;
                color: #1a73e8;
                font-weight: 500;
                font-size: 14px;
                min-width: 80px;
            }

            QDialogButtonBox QPushButton:hover {
                background: #f8f9fa;
                border-color: #1a73e8;
            }

            QDialogButtonBox QPushButton:pressed {
                background: #e8f0fe;
            }
        """)

    def closeEvent(self, event):
        """Handle window close."""
        # Clean up developer tools
        if self.devtools:
            self.devtools.close()

        event.accept()


class HistoryDialog(QDialog):
    """Dialog for browsing history."""

    def __init__(self, history_manager, parent=None):
        """Initialize history dialog."""
        super().__init__(parent)

        self.history_manager = history_manager
        self.setWindowTitle("History")
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        # History list
        self.history_list = QListWidget()
        history = self.history_manager.get_history()

        for entry in history:
            item_text = f"{entry['title']}\n{entry['url']}"
            self.history_list.addItem(item_text)

        layout.addWidget(self.history_list)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Open |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_url(self):
        """Get selected URL."""
        item = self.history_list.currentItem()
        if item:
            text = item.text()
            # Extract URL (second line)
            lines = text.split('\n')
            if len(lines) >= 2:
                return lines[1]
        return None


class BookmarksDialog(QDialog):
    """Dialog for browsing bookmarks."""

    def __init__(self, bookmarks_manager, parent=None):
        """Initialize bookmarks dialog."""
        super().__init__(parent)

        self.bookmarks_manager = bookmarks_manager
        self.setWindowTitle("Bookmarks")
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        # Bookmarks list
        self.bookmarks_list = QListWidget()
        bookmarks = self.bookmarks_manager.get_bookmarks()

        for bookmark in bookmarks:
            item_text = f"{bookmark['title']}\n{bookmark['url']}"
            self.bookmarks_list.addItem(item_text)

        layout.addWidget(self.bookmarks_list)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Open |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_url(self):
        """Get selected URL."""
        item = self.bookmarks_list.currentItem()
        if item:
            text = item.text()
            # Extract URL (second line)
            lines = text.split('\n')
            if len(lines) >= 2:
                return lines[1]
        return None
