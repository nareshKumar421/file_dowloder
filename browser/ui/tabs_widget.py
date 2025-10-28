"""
Browser Tabs Widget

Manages multiple browser tabs with tab bar and tab switching.
"""

from PyQt6.QtWidgets import QTabWidget, QTabBar, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon
from browser.core.tab import BrowserTab


class BrowserTabWidget(QTabWidget):
    """
    Tab widget for managing multiple browser tabs.

    Signals:
        tab_changed: Emitted when active tab changes
        tab_close_requested: Emitted when tab close is requested
        new_tab_requested: Emitted when new tab is requested
    """

    tab_changed = pyqtSignal(int)
    tab_close_requested = pyqtSignal(int)
    new_tab_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the tabs widget."""
        super().__init__(parent)

        # Configure tab widget
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setElideMode(Qt.TextElideMode.ElideRight)

        # Tab bar configuration
        self.tabBar().setExpanding(False)
        self.tabBar().setSelectionBehaviorOnRemove(
            QTabBar.SelectionBehavior.SelectPreviousTab
        )

        # Connect signals
        self.currentChanged.connect(self.tab_changed.emit)
        self.tabCloseRequested.connect(self._on_tab_close_requested)

        # Add new tab button
        self._add_new_tab_button()

        # Apply stylesheet
        self._apply_stylesheet()

    def _add_new_tab_button(self):
        """Add a button to create new tabs."""
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setFixedSize(30, 30)
        self.new_tab_btn.setToolTip("New Tab (Ctrl+T)")
        self.new_tab_btn.clicked.connect(self.new_tab_requested.emit)

        # Add button to corner
        self.setCornerWidget(self.new_tab_btn, Qt.Corner.TopRightCorner)

    def _on_tab_close_requested(self, index):
        """
        Handle tab close request.

        Args:
            index: Index of tab to close
        """
        # Don't close if it's the last tab
        if self.count() <= 1:
            # Create new tab before closing
            self.new_tab_requested.emit()

        self.tab_close_requested.emit(index)

    def add_tab(self, tab, title="New Tab", icon=None):
        """
        Add a new tab.

        Args:
            tab: BrowserTab widget
            title: Tab title
            icon: Tab icon

        Returns:
            Index of the new tab
        """
        if icon:
            index = super().addTab(tab, icon, title)
        else:
            index = super().addTab(tab, title)

        # Connect tab signals
        tab.title_changed.connect(lambda title: self._on_tab_title_changed(tab, title))
        tab.icon_changed.connect(lambda: self._on_tab_icon_changed(tab))

        return index

    def _on_tab_title_changed(self, tab, title):
        """
        Handle tab title change.

        Args:
            tab: The tab widget
            title: New title
        """
        index = self.indexOf(tab)
        if index >= 0:
            # Limit title length
            if len(title) > 30:
                title = title[:27] + "..."
            self.setTabText(index, title if title else "New Tab")

    def _on_tab_icon_changed(self, tab):
        """
        Handle tab icon change.

        Args:
            tab: The tab widget
        """
        index = self.indexOf(tab)
        if index >= 0:
            icon = tab.icon()
            if not icon.isNull():
                self.setTabIcon(index, icon)

    def get_current_tab(self):
        """
        Get the current active tab.

        Returns:
            BrowserTab instance or None
        """
        return self.currentWidget()

    def get_tab(self, index):
        """
        Get tab at index.

        Args:
            index: Tab index

        Returns:
            BrowserTab instance or None
        """
        return self.widget(index)

    def remove_tab(self, index):
        """
        Remove tab at index.

        Args:
            index: Tab index
        """
        tab = self.widget(index)
        self.removeTab(index)

        # Clean up the tab
        if tab:
            tab.deleteLater()

    def close_current_tab(self):
        """Close the current active tab."""
        current_index = self.currentIndex()
        if current_index >= 0:
            self._on_tab_close_requested(current_index)

    def close_other_tabs(self):
        """Close all tabs except the current one."""
        current_index = self.currentIndex()
        if current_index < 0:
            return

        # Remove tabs after current
        while self.count() > current_index + 1:
            self.remove_tab(current_index + 1)

        # Remove tabs before current
        while current_index > 0:
            self.remove_tab(0)
            current_index -= 1

    def close_all_tabs(self):
        """Close all tabs."""
        while self.count() > 0:
            self.remove_tab(0)

    def next_tab(self):
        """Switch to next tab."""
        current = self.currentIndex()
        if current < self.count() - 1:
            self.setCurrentIndex(current + 1)
        else:
            self.setCurrentIndex(0)

    def previous_tab(self):
        """Switch to previous tab."""
        current = self.currentIndex()
        if current > 0:
            self.setCurrentIndex(current - 1)
        else:
            self.setCurrentIndex(self.count() - 1)

    def _apply_stylesheet(self):
        """Apply custom stylesheet."""
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: white;
            }

            QTabWidget::tab-bar {
                alignment: left;
            }

            QTabBar::tab {
                background: #e0e0e0;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
                min-width: 100px;
                max-width: 200px;
            }

            QTabBar::tab:selected {
                background: white;
            }

            QTabBar::tab:hover:!selected {
                background: #f0f0f0;
            }

            QTabBar::close-button {
                image: url(none);
                subcontrol-position: right;
                margin-right: 4px;
            }

            QTabBar::close-button:hover {
                background: #d0d0d0;
                border-radius: 2px;
            }

            QPushButton {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                background: white;
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #f0f0f0;
            }

            QPushButton:pressed {
                background: #e0e0e0;
            }
        """)


class TabButton(QPushButton):
    """Custom close button for tabs."""

    def __init__(self, parent=None):
        """Initialize the tab button."""
        super().__init__("×", parent)
        self.setFixedSize(16, 16)
        self.setFlat(True)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 8px;
                background: transparent;
                color: #666;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #d0d0d0;
                color: #000;
            }
        """)
