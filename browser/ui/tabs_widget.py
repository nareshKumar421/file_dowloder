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
        """Apply Chrome-like stylesheet."""
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: white;
                top: -1px;
            }

            QTabWidget::tab-bar {
                alignment: left;
            }

            QTabBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8eaed, stop:1 #dadce0);
                border-bottom: 1px solid #c0c0c0;
            }

            QTabBar::tab {
                background: #dadce0;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 16px 10px 16px;
                margin-right: 1px;
                margin-top: 4px;
                min-width: 120px;
                max-width: 240px;
                color: #5f6368;
            }

            QTabBar::tab:selected {
                background: white;
                color: #202124;
                font-weight: 500;
            }

            QTabBar::tab:hover:!selected {
                background: #e8eaed;
            }

            QTabBar::close-button {
                image: none;
                subcontrol-position: right;
                margin-right: 4px;
                border-radius: 10px;
                width: 20px;
                height: 20px;
            }

            QTabBar::close-button:hover {
                background: rgba(95,99,104,0.2);
            }

            QPushButton {
                border: none;
                border-radius: 18px;
                background: transparent;
                font-size: 20px;
                font-weight: bold;
                color: #5f6368;
                min-width: 36px;
                min-height: 36px;
            }

            QPushButton:hover {
                background: rgba(95,99,104,0.1);
            }

            QPushButton:pressed {
                background: rgba(95,99,104,0.2);
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
