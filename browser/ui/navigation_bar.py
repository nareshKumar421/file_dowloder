"""
Browser Navigation Bar

Contains address bar, navigation buttons, and browser controls.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton,
    QToolBar, QLabel, QProgressBar, QMenu, QToolButton
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QKeySequence


class NavigationBar(QToolBar):
    """
    Browser navigation bar with URL entry and navigation controls.

    Signals:
        navigate_home: Navigate to home page
        navigate_back: Navigate back
        navigate_forward: Navigate forward
        reload: Reload current page
        stop: Stop loading page
        url_submitted: URL submitted (str)
        bookmark_added: Add current page to bookmarks
        settings_clicked: Open settings
        new_tab: Open new tab
        new_incognito_tab: Open new incognito tab
    """

    navigate_home = pyqtSignal()
    navigate_back = pyqtSignal()
    navigate_forward = pyqtSignal()
    reload = pyqtSignal()
    stop = pyqtSignal()
    url_submitted = pyqtSignal(str)
    bookmark_added = pyqtSignal()
    settings_clicked = pyqtSignal()
    new_tab = pyqtSignal()
    new_incognito_tab = pyqtSignal()
    toggle_devtools = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the navigation bar."""
        super().__init__(parent)

        self.setMovable(False)
        self.setIconSize(QSize(20, 20))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        # Loading state
        self._is_loading = False

        # Create UI elements
        self._create_buttons()
        self._create_address_bar()
        self._create_extra_buttons()

        # Apply stylesheet
        self._apply_stylesheet()

    def _create_buttons(self):
        """Create navigation buttons."""
        # Back button
        self.back_btn = QAction("←", self)
        self.back_btn.setShortcut(QKeySequence("Alt+Left"))
        self.back_btn.setToolTip("Back (Alt+Left)")
        self.back_btn.triggered.connect(self.navigate_back.emit)
        self.addAction(self.back_btn)

        # Forward button
        self.forward_btn = QAction("→", self)
        self.forward_btn.setShortcut(QKeySequence("Alt+Right"))
        self.forward_btn.setToolTip("Forward (Alt+Right)")
        self.forward_btn.triggered.connect(self.navigate_forward.emit)
        self.addAction(self.forward_btn)

        # Reload/Stop button
        self.reload_btn = QAction("⟳", self)
        self.reload_btn.setShortcut(QKeySequence("Ctrl+R"))
        self.reload_btn.setToolTip("Reload (Ctrl+R)")
        self.reload_btn.triggered.connect(self._on_reload_stop_clicked)
        self.addAction(self.reload_btn)

        # Home button
        self.home_btn = QAction("⌂", self)
        self.home_btn.setShortcut(QKeySequence("Alt+Home"))
        self.home_btn.setToolTip("Home (Alt+Home)")
        self.home_btn.triggered.connect(self.navigate_home.emit)
        self.addAction(self.home_btn)

        # Separator
        self.addSeparator()

    def _create_address_bar(self):
        """Create the address bar."""
        # Container widget for address bar
        address_container = QWidget()
        address_layout = QHBoxLayout(address_container)
        address_layout.setContentsMargins(5, 0, 5, 0)

        # Security indicator
        self.security_label = QLabel("🔒")
        self.security_label.setToolTip("Connection is secure (HTTPS)")
        self.security_label.setFixedWidth(25)
        address_layout.addWidget(self.security_label)

        # URL input
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search...")
        self.url_bar.returnPressed.connect(self._on_url_submitted)
        self.url_bar.setMinimumWidth(400)
        address_layout.addWidget(self.url_bar)

        # Loading progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(3)
        self.progress_bar.hide()

        # Add to toolbar
        self.addWidget(address_container)

    def _create_extra_buttons(self):
        """Create extra control buttons."""
        # Separator
        self.addSeparator()

        # Bookmark button
        self.bookmark_btn = QAction("⭐", self)
        self.bookmark_btn.setShortcut(QKeySequence("Ctrl+D"))
        self.bookmark_btn.setToolTip("Bookmark this page (Ctrl+D)")
        self.bookmark_btn.triggered.connect(self.bookmark_added.emit)
        self.addAction(self.bookmark_btn)

        # Developer tools button
        self.devtools_btn = QAction("⚙", self)
        self.devtools_btn.setShortcut(QKeySequence("F12"))
        self.devtools_btn.setToolTip("Developer Tools (F12)")
        self.devtools_btn.triggered.connect(self.toggle_devtools.emit)
        self.addAction(self.devtools_btn)

        # Menu button
        self.menu_btn = QToolButton()
        self.menu_btn.setText("☰")
        self.menu_btn.setToolTip("Menu")
        self.menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        # Create menu
        menu = QMenu(self.menu_btn)

        # New tab
        new_tab_action = QAction("New Tab", menu)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(self.new_tab.emit)
        menu.addAction(new_tab_action)

        # New incognito tab
        new_incognito_action = QAction("New Incognito Tab", menu)
        new_incognito_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_incognito_action.triggered.connect(self.new_incognito_tab.emit)
        menu.addAction(new_incognito_action)

        menu.addSeparator()

        # Settings
        settings_action = QAction("Settings", menu)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self.settings_clicked.emit)
        menu.addAction(settings_action)

        self.menu_btn.setMenu(menu)
        self.addWidget(self.menu_btn)

    def _on_reload_stop_clicked(self):
        """Handle reload/stop button click."""
        if self._is_loading:
            self.stop.emit()
        else:
            self.reload.emit()

    def _on_url_submitted(self):
        """Handle URL submission."""
        url = self.url_bar.text().strip()
        if url:
            # Check if it's a search query or URL
            if ' ' in url or '.' not in url:
                # Treat as search query
                search_url = f"https://www.google.com/search?q={url}"
                self.url_submitted.emit(search_url)
            else:
                self.url_submitted.emit(url)

    def set_url(self, url):
        """
        Set the URL in the address bar.

        Args:
            url: URL string or QUrl
        """
        if hasattr(url, 'toString'):
            url = url.toString()

        self.url_bar.setText(url)

        # Update security indicator
        if url.startswith('https://'):
            self.security_label.setText("🔒")
            self.security_label.setToolTip("Connection is secure (HTTPS)")
        elif url.startswith('http://'):
            self.security_label.setText("⚠")
            self.security_label.setToolTip("Connection is not secure (HTTP)")
        else:
            self.security_label.setText("ℹ")
            self.security_label.setToolTip("Local or special page")

    def set_loading_state(self, is_loading):
        """
        Set the loading state.

        Args:
            is_loading: True if page is loading
        """
        self._is_loading = is_loading

        if is_loading:
            self.reload_btn.setText("✕")
            self.reload_btn.setToolTip("Stop loading")
            self.progress_bar.show()
        else:
            self.reload_btn.setText("⟳")
            self.reload_btn.setToolTip("Reload (Ctrl+R)")
            self.progress_bar.hide()

    def set_progress(self, progress):
        """
        Set loading progress.

        Args:
            progress: Progress value (0-100)
        """
        self.progress_bar.setValue(progress)

    def set_back_enabled(self, enabled):
        """Enable/disable back button."""
        self.back_btn.setEnabled(enabled)

    def set_forward_enabled(self, enabled):
        """Enable/disable forward button."""
        self.forward_btn.setEnabled(enabled)

    def focus_address_bar(self):
        """Focus the address bar and select all text."""
        self.url_bar.setFocus()
        self.url_bar.selectAll()

    def _apply_stylesheet(self):
        """Apply custom stylesheet."""
        self.setStyleSheet("""
            QToolBar {
                background: #f0f0f0;
                border: none;
                border-bottom: 1px solid #d0d0d0;
                spacing: 3px;
                padding: 5px;
            }

            QLineEdit {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 6px 10px;
                background: white;
                selection-background-color: #4a90e2;
            }

            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }

            QPushButton, QToolButton {
                border: none;
                border-radius: 4px;
                padding: 6px 10px;
                background: transparent;
                font-size: 16px;
            }

            QPushButton:hover, QToolButton:hover {
                background: #e0e0e0;
            }

            QPushButton:pressed, QToolButton:pressed {
                background: #d0d0d0;
            }

            QPushButton:disabled {
                color: #a0a0a0;
            }

            QProgressBar {
                border: none;
                background: #f0f0f0;
            }

            QProgressBar::chunk {
                background: #4a90e2;
            }
        """)
