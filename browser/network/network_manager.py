"""
Network Manager

Handles network requests, cookies, cache, and download management.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QNetworkCookie
from datetime import datetime
import json
import os


class NetworkManager(QObject):
    """
    Manages network operations including cookies, cache, and downloads.

    Signals:
        download_started: Download started (filename, url)
        download_progress: Download progress (filename, bytes_received, bytes_total)
        download_finished: Download finished (filename, path)
        request_intercepted: Request intercepted (url, request_type)
    """

    download_started = pyqtSignal(str, str)
    download_progress = pyqtSignal(str, int, int)
    download_finished = pyqtSignal(str, str)
    request_intercepted = pyqtSignal(str, str)

    def __init__(self, profile, storage_path, parent=None):
        """
        Initialize network manager.

        Args:
            profile: QWebEngineProfile instance
            storage_path: Path for storing network data
            parent: Parent QObject
        """
        super().__init__(parent)

        self.profile = profile
        self.storage_path = storage_path

        # Create network storage directories
        self.cookies_path = os.path.join(storage_path, "cookies")
        self.cache_path = os.path.join(storage_path, "cache")
        self.downloads_path = os.path.join(storage_path, "downloads")

        os.makedirs(self.cookies_path, exist_ok=True)
        os.makedirs(self.cache_path, exist_ok=True)
        os.makedirs(self.downloads_path, exist_ok=True)

        # Cookie store
        self.cookie_store = profile.cookieStore()

        # Active downloads
        self.active_downloads = {}

        # Request statistics
        self.request_stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'cached_requests': 0,
        }

        # Connect download handler
        self.profile.downloadRequested.connect(self._on_download_requested)

    def _on_download_requested(self, download):
        """
        Handle download request.

        Args:
            download: QWebEngineDownloadRequest
        """
        # Get download info
        url = download.url().toString()
        filename = download.downloadFileName()

        # Set download path
        download_path = os.path.join(self.downloads_path, filename)
        download.setDownloadDirectory(self.downloads_path)
        download.setDownloadFileName(filename)

        # Connect download signals
        download.receivedBytesChanged.connect(
            lambda: self._on_download_progress(download)
        )
        download.isFinishedChanged.connect(
            lambda: self._on_download_finished(download)
        )

        # Accept download
        download.accept()

        # Track download
        self.active_downloads[filename] = {
            'download': download,
            'url': url,
            'path': download_path,
            'started': datetime.now(),
        }

        self.download_started.emit(filename, url)

    def _on_download_progress(self, download):
        """
        Handle download progress.

        Args:
            download: QWebEngineDownloadRequest
        """
        filename = download.downloadFileName()
        received = download.receivedBytes()
        total = download.totalBytes()

        self.download_progress.emit(filename, received, total)

    def _on_download_finished(self, download):
        """
        Handle download completion.

        Args:
            download: QWebEngineDownloadRequest
        """
        if not download.isFinished():
            return

        filename = download.downloadFileName()

        if filename in self.active_downloads:
            info = self.active_downloads[filename]
            self.download_finished.emit(filename, info['path'])
            del self.active_downloads[filename]

    def get_all_cookies(self):
        """
        Get all cookies.

        Returns:
            List of cookie dictionaries
        """
        cookies = []
        # Note: QWebEngine doesn't provide direct access to all cookies
        # This would need to be implemented using the cookie store's signals
        return cookies

    def clear_cookies(self, domain=None):
        """
        Clear cookies.

        Args:
            domain: Specific domain to clear (None for all)
        """
        if domain:
            # Clear cookies for specific domain
            self.cookie_store.deleteCookie(QNetworkCookie(), domain)
        else:
            # Clear all cookies
            self.cookie_store.deleteAllCookies()

    def clear_cache(self):
        """Clear the HTTP cache."""
        self.profile.clearHttpCache()

    def get_downloads_path(self):
        """
        Get the downloads directory path.

        Returns:
            Downloads directory path
        """
        return self.downloads_path

    def set_downloads_path(self, path):
        """
        Set the downloads directory path.

        Args:
            path: New downloads directory path
        """
        self.downloads_path = path
        os.makedirs(path, exist_ok=True)

    def get_active_downloads(self):
        """
        Get active downloads.

        Returns:
            Dictionary of active downloads
        """
        return self.active_downloads.copy()

    def cancel_download(self, filename):
        """
        Cancel a download.

        Args:
            filename: Download filename
        """
        if filename in self.active_downloads:
            download = self.active_downloads[filename]['download']
            download.cancel()
            del self.active_downloads[filename]

    def get_request_stats(self):
        """
        Get request statistics.

        Returns:
            Dictionary of request statistics
        """
        return self.request_stats.copy()

    def save_cookies(self):
        """Save cookies to disk (for persistence)."""
        # This is a placeholder - actual implementation would use
        # QWebEngineCookieStore's cookieAdded signal to track cookies
        pass

    def load_cookies(self):
        """Load cookies from disk."""
        # This is a placeholder - actual implementation would restore
        # cookies using QWebEngineCookieStore's setCookie method
        pass

    def block_url(self, url_pattern):
        """
        Block URLs matching pattern.

        Args:
            url_pattern: URL pattern to block
        """
        # This would be implemented using QWebEngineUrlRequestInterceptor
        pass

    def get_cache_size(self):
        """
        Get cache size in bytes.

        Returns:
            Cache size in bytes
        """
        total_size = 0
        if os.path.exists(self.cache_path):
            for dirpath, dirnames, filenames in os.walk(self.cache_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
        return total_size

    def format_size(self, size_bytes):
        """
        Format bytes to human-readable size.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
