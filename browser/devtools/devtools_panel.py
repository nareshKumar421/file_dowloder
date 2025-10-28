"""
Developer Tools Panel

Provides browser developer tools including console, inspector, network monitor.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QTabWidget, QLabel, QSplitter, QTreeWidget,
    QTreeWidgetItem, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from datetime import datetime


class DevToolsPanel(QWidget):
    """
    Developer tools panel with console, inspector, and network monitor.

    Signals:
        closed: Emitted when dev tools are closed
        execute_js: Emitted when JavaScript should be executed
    """

    closed = pyqtSignal()
    execute_js = pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize developer tools panel."""
        super().__init__(parent)

        self.setWindowTitle("Developer Tools")

        # Create layout
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create tabs
        self._create_console_tab()
        self._create_inspector_tab()
        self._create_network_tab()
        self._create_storage_tab()

        # Apply stylesheet
        self._apply_stylesheet()

    def _create_console_tab(self):
        """Create console tab."""
        console_widget = QWidget()
        layout = QVBoxLayout(console_widget)

        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setFont(QFont("Courier", 10))
        layout.addWidget(self.console_output)

        # Console input
        input_layout = QHBoxLayout()

        self.console_input = QTextEdit()
        self.console_input.setMaximumHeight(60)
        self.console_input.setFont(QFont("Courier", 10))
        self.console_input.setPlaceholderText("Enter JavaScript code...")
        input_layout.addWidget(self.console_input)

        # Execute button
        execute_btn = QPushButton("Execute")
        execute_btn.clicked.connect(self._on_execute_js)
        input_layout.addWidget(execute_btn)

        layout.addLayout(input_layout)

        # Clear button
        clear_btn = QPushButton("Clear Console")
        clear_btn.clicked.connect(self.console_output.clear)
        layout.addWidget(clear_btn)

        self.tabs.addTab(console_widget, "Console")

    def _create_inspector_tab(self):
        """Create DOM inspector tab."""
        inspector_widget = QWidget()
        layout = QVBoxLayout(inspector_widget)

        # DOM tree
        self.dom_tree = QTreeWidget()
        self.dom_tree.setHeaderLabels(["Element", "Attributes"])
        layout.addWidget(self.dom_tree)

        # Refresh button
        refresh_btn = QPushButton("Refresh DOM Tree")
        refresh_btn.clicked.connect(self._refresh_dom_tree)
        layout.addWidget(refresh_btn)

        self.tabs.addTab(inspector_widget, "Inspector")

    def _create_network_tab(self):
        """Create network monitor tab."""
        network_widget = QWidget()
        layout = QVBoxLayout(network_widget)

        # Network requests table
        self.network_table = QTableWidget()
        self.network_table.setColumnCount(6)
        self.network_table.setHorizontalHeaderLabels([
            "Time", "Method", "URL", "Status", "Type", "Size"
        ])
        layout.addWidget(self.network_table)

        # Control buttons
        button_layout = QHBoxLayout()

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(lambda: self.network_table.setRowCount(0))
        button_layout.addWidget(clear_btn)

        preserve_log_btn = QPushButton("Preserve Log")
        preserve_log_btn.setCheckable(True)
        button_layout.addWidget(preserve_log_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.tabs.addTab(network_widget, "Network")

    def _create_storage_tab(self):
        """Create storage viewer tab."""
        storage_widget = QWidget()
        layout = QVBoxLayout(storage_widget)

        # Storage tree
        self.storage_tree = QTreeWidget()
        self.storage_tree.setHeaderLabels(["Key", "Value", "Size"])
        layout.addWidget(self.storage_tree)

        # Control buttons
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_storage_tree)
        button_layout.addWidget(refresh_btn)

        clear_btn = QPushButton("Clear All")
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.tabs.addTab(storage_widget, "Storage")

    def _on_execute_js(self):
        """Handle JavaScript execution."""
        code = self.console_input.toPlainText().strip()
        if code:
            # Log to console
            self.log_console(f"> {code}", "input")

            # Emit signal to execute
            self.execute_js.emit(code)

            # Clear input
            self.console_input.clear()

    def _refresh_dom_tree(self):
        """Refresh DOM tree (placeholder)."""
        self.dom_tree.clear()
        # This would need to be implemented with actual DOM inspection
        info_item = QTreeWidgetItem(["Refresh functionality requires integration with web page"])
        self.dom_tree.addTopLevelItem(info_item)

    def _refresh_storage_tree(self):
        """Refresh storage tree (placeholder)."""
        self.storage_tree.clear()
        # This would need to be implemented with actual storage inspection
        info_item = QTreeWidgetItem(["Storage inspection requires integration"])
        self.storage_tree.addTopLevelItem(info_item)

    def log_console(self, message, msg_type="log"):
        """
        Log message to console.

        Args:
            message: Message to log
            msg_type: Type of message (log, info, warn, error, input)
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Format message with color
        color_map = {
            "log": "#000000",
            "info": "#0000ff",
            "warn": "#ff8c00",
            "error": "#ff0000",
            "input": "#008000"
        }
        color = color_map.get(msg_type, "#000000")

        formatted = f'<span style="color: gray;">[{timestamp}]</span> '
        formatted += f'<span style="color: {color};">{message}</span><br>'

        self.console_output.insertHtml(formatted)

        # Scroll to bottom
        scrollbar = self.console_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def log_network_request(self, method, url, status, content_type, size):
        """
        Log network request.

        Args:
            method: HTTP method
            url: Request URL
            status: HTTP status code
            content_type: Content type
            size: Response size
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        row = self.network_table.rowCount()
        self.network_table.insertRow(row)

        self.network_table.setItem(row, 0, QTableWidgetItem(timestamp))
        self.network_table.setItem(row, 1, QTableWidgetItem(method))
        self.network_table.setItem(row, 2, QTableWidgetItem(url))
        self.network_table.setItem(row, 3, QTableWidgetItem(str(status)))
        self.network_table.setItem(row, 4, QTableWidgetItem(content_type))
        self.network_table.setItem(row, 5, QTableWidgetItem(size))

    def handle_console_message(self, level, message, line, source):
        """
        Handle console message from web page.

        Args:
            level: Message level
            message: Console message
            line: Line number
            source: Source file
        """
        msg_type_map = {
            0: "log",    # InfoMessageLevel
            1: "warn",   # WarningMessageLevel
            2: "error"   # ErrorMessageLevel
        }
        msg_type = msg_type_map.get(level, "log")

        formatted_msg = message
        if source and line:
            formatted_msg += f" ({source}:{line})"

        self.log_console(formatted_msg, msg_type)

    def _apply_stylesheet(self):
        """Apply custom stylesheet."""
        self.setStyleSheet("""
            QWidget {
                background: white;
            }

            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background: white;
            }

            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #c0c0c0;
                padding: 6px 12px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background: white;
                border-bottom: none;
            }

            QTextEdit {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 5px;
                background: #fafafa;
                font-family: 'Courier New', monospace;
            }

            QTreeWidget, QTableWidget {
                border: 1px solid #c0c0c0;
                background: white;
            }

            QPushButton {
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 6px 12px;
                background: #f0f0f0;
            }

            QPushButton:hover {
                background: #e0e0e0;
            }

            QPushButton:pressed {
                background: #d0d0d0;
            }
        """)
