"""
Browser History Manager

Tracks and manages browsing history.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
import json
import os


class HistoryManager(QObject):
    """
    Manages browser history.

    Signals:
        history_updated: Emitted when history is updated
    """

    history_updated = pyqtSignal()

    def __init__(self, storage_path, parent=None):
        """
        Initialize history manager.

        Args:
            storage_path: Path for storing history data
            parent: Parent QObject
        """
        super().__init__(parent)

        self.storage_path = storage_path
        self.history_file = os.path.join(storage_path, "history.json")

        # Load history
        self.history = self._load_history()

    def _load_history(self):
        """
        Load history from disk.

        Returns:
            List of history entries
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self):
        """Save history to disk."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_entry(self, url, title):
        """
        Add a history entry.

        Args:
            url: Page URL
            title: Page title
        """
        entry = {
            'url': url,
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'visit_count': 1
        }

        # Check if URL already exists
        for i, item in enumerate(self.history):
            if item['url'] == url:
                # Update existing entry
                self.history[i]['timestamp'] = entry['timestamp']
                self.history[i]['visit_count'] += 1
                self.history[i]['title'] = title
                self._save_history()
                self.history_updated.emit()
                return

        # Add new entry
        self.history.insert(0, entry)

        # Limit history size
        max_entries = 10000
        if len(self.history) > max_entries:
            self.history = self.history[:max_entries]

        self._save_history()
        self.history_updated.emit()

    def get_history(self, limit=100):
        """
        Get recent history.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of history entries
        """
        return self.history[:limit]

    def search_history(self, query, limit=50):
        """
        Search history.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching history entries
        """
        query = query.lower()
        results = []

        for entry in self.history:
            if query in entry['url'].lower() or query in entry['title'].lower():
                results.append(entry)
                if len(results) >= limit:
                    break

        return results

    def get_most_visited(self, limit=10):
        """
        Get most visited pages.

        Args:
            limit: Maximum number of entries

        Returns:
            List of most visited pages
        """
        sorted_history = sorted(
            self.history,
            key=lambda x: x.get('visit_count', 1),
            reverse=True
        )
        return sorted_history[:limit]

    def remove_entry(self, url):
        """
        Remove a history entry.

        Args:
            url: URL to remove
        """
        self.history = [item for item in self.history if item['url'] != url]
        self._save_history()
        self.history_updated.emit()

    def clear_history(self, days=None):
        """
        Clear history.

        Args:
            days: Clear history older than X days (None for all)
        """
        if days is None:
            # Clear all history
            self.history = []
        else:
            # Clear history older than X days
            cutoff = datetime.now()
            from datetime import timedelta
            cutoff -= timedelta(days=days)

            self.history = [
                item for item in self.history
                if datetime.fromisoformat(item['timestamp']) > cutoff
            ]

        self._save_history()
        self.history_updated.emit()

    def get_history_count(self):
        """
        Get total history count.

        Returns:
            Number of history entries
        """
        return len(self.history)
