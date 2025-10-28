"""
Browser Bookmarks Manager

Manages bookmarks and favorites.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
import json
import os


class BookmarksManager(QObject):
    """
    Manages browser bookmarks.

    Signals:
        bookmarks_updated: Emitted when bookmarks are updated
    """

    bookmarks_updated = pyqtSignal()

    def __init__(self, storage_path, parent=None):
        """
        Initialize bookmarks manager.

        Args:
            storage_path: Path for storing bookmarks data
            parent: Parent QObject
        """
        super().__init__(parent)

        self.storage_path = storage_path
        self.bookmarks_file = os.path.join(storage_path, "bookmarks.json")

        # Load bookmarks
        self.bookmarks = self._load_bookmarks()

    def _load_bookmarks(self):
        """
        Load bookmarks from disk.

        Returns:
            List of bookmarks
        """
        if os.path.exists(self.bookmarks_file):
            try:
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_bookmarks(self):
        """Save bookmarks to disk."""
        try:
            with open(self.bookmarks_file, 'w') as f:
                json.dump(self.bookmarks, f, indent=2)
        except Exception as e:
            print(f"Error saving bookmarks: {e}")

    def add_bookmark(self, url, title, folder=""):
        """
        Add a bookmark.

        Args:
            url: Page URL
            title: Page title
            folder: Bookmark folder/category

        Returns:
            True if bookmark was added, False if already exists
        """
        # Check if bookmark already exists
        for bookmark in self.bookmarks:
            if bookmark['url'] == url:
                return False

        bookmark = {
            'url': url,
            'title': title,
            'folder': folder,
            'added': datetime.now().isoformat()
        }

        self.bookmarks.append(bookmark)
        self._save_bookmarks()
        self.bookmarks_updated.emit()
        return True

    def remove_bookmark(self, url):
        """
        Remove a bookmark.

        Args:
            url: URL to remove

        Returns:
            True if bookmark was removed
        """
        original_count = len(self.bookmarks)
        self.bookmarks = [b for b in self.bookmarks if b['url'] != url]

        if len(self.bookmarks) < original_count:
            self._save_bookmarks()
            self.bookmarks_updated.emit()
            return True

        return False

    def is_bookmarked(self, url):
        """
        Check if URL is bookmarked.

        Args:
            url: URL to check

        Returns:
            True if bookmarked
        """
        return any(b['url'] == url for b in self.bookmarks)

    def get_bookmarks(self, folder=None):
        """
        Get bookmarks.

        Args:
            folder: Filter by folder (None for all)

        Returns:
            List of bookmarks
        """
        if folder is None:
            return self.bookmarks.copy()

        return [b for b in self.bookmarks if b['folder'] == folder]

    def get_folders(self):
        """
        Get all bookmark folders.

        Returns:
            List of unique folder names
        """
        folders = set()
        for bookmark in self.bookmarks:
            if bookmark.get('folder'):
                folders.add(bookmark['folder'])
        return sorted(list(folders))

    def search_bookmarks(self, query):
        """
        Search bookmarks.

        Args:
            query: Search query

        Returns:
            List of matching bookmarks
        """
        query = query.lower()
        results = []

        for bookmark in self.bookmarks:
            if (query in bookmark['url'].lower() or
                query in bookmark['title'].lower() or
                query in bookmark.get('folder', '').lower()):
                results.append(bookmark)

        return results

    def update_bookmark(self, url, title=None, folder=None):
        """
        Update a bookmark.

        Args:
            url: URL of bookmark to update
            title: New title (None to keep current)
            folder: New folder (None to keep current)

        Returns:
            True if bookmark was updated
        """
        for bookmark in self.bookmarks:
            if bookmark['url'] == url:
                if title is not None:
                    bookmark['title'] = title
                if folder is not None:
                    bookmark['folder'] = folder

                self._save_bookmarks()
                self.bookmarks_updated.emit()
                return True

        return False

    def clear_bookmarks(self, folder=None):
        """
        Clear bookmarks.

        Args:
            folder: Clear specific folder (None for all)
        """
        if folder is None:
            self.bookmarks = []
        else:
            self.bookmarks = [b for b in self.bookmarks if b['folder'] != folder]

        self._save_bookmarks()
        self.bookmarks_updated.emit()

    def export_bookmarks(self, filepath):
        """
        Export bookmarks to a file.

        Args:
            filepath: Output file path
        """
        data = {
            'exported': datetime.now().isoformat(),
            'bookmarks': self.bookmarks
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def import_bookmarks(self, filepath):
        """
        Import bookmarks from a file.

        Args:
            filepath: Import file path
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        imported_bookmarks = data.get('bookmarks', [])

        # Add imported bookmarks (skip duplicates)
        added_count = 0
        for bookmark in imported_bookmarks:
            if not self.is_bookmarked(bookmark['url']):
                self.bookmarks.append(bookmark)
                added_count += 1

        if added_count > 0:
            self._save_bookmarks()
            self.bookmarks_updated.emit()

        return added_count

    def get_bookmark_count(self):
        """
        Get total bookmark count.

        Returns:
            Number of bookmarks
        """
        return len(self.bookmarks)
