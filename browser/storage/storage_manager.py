"""
Storage Manager

Manages browser storage including LocalStorage, SessionStorage, and Cookies.
Provides JavaScript APIs for web pages to access storage.
"""

from PyQt6.QtCore import QObject
import json
import os
from datetime import datetime


class StorageManager(QObject):
    """
    Manages browser storage APIs.

    Provides access to:
    - LocalStorage (persistent)
    - SessionStorage (session-only)
    - Cookie management
    - Storage quotas and usage
    """

    def __init__(self, storage_path, parent=None):
        """
        Initialize storage manager.

        Args:
            storage_path: Path for storing data
            parent: Parent QObject
        """
        super().__init__(parent)

        self.storage_path = storage_path
        self.local_storage_path = os.path.join(storage_path, "local_storage")
        self.session_storage_path = os.path.join(storage_path, "session_storage")

        # Create storage directories
        os.makedirs(self.local_storage_path, exist_ok=True)
        os.makedirs(self.session_storage_path, exist_ok=True)

        # In-memory session storage
        self.session_storage = {}

        # Storage quota (in bytes)
        self.quota = 10 * 1024 * 1024  # 10MB default

    def get_local_storage_file(self, origin):
        """
        Get the local storage file path for an origin.

        Args:
            origin: Origin (domain) string

        Returns:
            File path for the origin's local storage
        """
        # Sanitize origin for filename
        safe_origin = origin.replace('://', '_').replace('/', '_').replace(':', '_')
        return os.path.join(self.local_storage_path, f"{safe_origin}.json")

    def set_local_storage_item(self, origin, key, value):
        """
        Set a LocalStorage item.

        Args:
            origin: Origin (domain) string
            key: Storage key
            value: Value to store
        """
        storage_file = self.get_local_storage_file(origin)

        # Load existing storage
        storage = {}
        if os.path.exists(storage_file):
            try:
                with open(storage_file, 'r') as f:
                    storage = json.load(f)
            except:
                storage = {}

        # Set item
        storage[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }

        # Save storage
        with open(storage_file, 'w') as f:
            json.dump(storage, f, indent=2)

    def get_local_storage_item(self, origin, key):
        """
        Get a LocalStorage item.

        Args:
            origin: Origin (domain) string
            key: Storage key

        Returns:
            Stored value or None
        """
        storage_file = self.get_local_storage_file(origin)

        if not os.path.exists(storage_file):
            return None

        try:
            with open(storage_file, 'r') as f:
                storage = json.load(f)
                if key in storage:
                    return storage[key]['value']
        except:
            pass

        return None

    def remove_local_storage_item(self, origin, key):
        """
        Remove a LocalStorage item.

        Args:
            origin: Origin (domain) string
            key: Storage key
        """
        storage_file = self.get_local_storage_file(origin)

        if not os.path.exists(storage_file):
            return

        try:
            with open(storage_file, 'r') as f:
                storage = json.load(f)

            if key in storage:
                del storage[key]

                with open(storage_file, 'w') as f:
                    json.dump(storage, f, indent=2)
        except:
            pass

    def clear_local_storage(self, origin=None):
        """
        Clear LocalStorage.

        Args:
            origin: Specific origin to clear (None for all)
        """
        if origin:
            storage_file = self.get_local_storage_file(origin)
            if os.path.exists(storage_file):
                os.remove(storage_file)
        else:
            # Clear all local storage
            for filename in os.listdir(self.local_storage_path):
                filepath = os.path.join(self.local_storage_path, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)

    def set_session_storage_item(self, origin, key, value):
        """
        Set a SessionStorage item.

        Args:
            origin: Origin (domain) string
            key: Storage key
            value: Value to store
        """
        if origin not in self.session_storage:
            self.session_storage[origin] = {}

        self.session_storage[origin][key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }

    def get_session_storage_item(self, origin, key):
        """
        Get a SessionStorage item.

        Args:
            origin: Origin (domain) string
            key: Storage key

        Returns:
            Stored value or None
        """
        if origin in self.session_storage:
            if key in self.session_storage[origin]:
                return self.session_storage[origin][key]['value']
        return None

    def remove_session_storage_item(self, origin, key):
        """
        Remove a SessionStorage item.

        Args:
            origin: Origin (domain) string
            key: Storage key
        """
        if origin in self.session_storage:
            if key in self.session_storage[origin]:
                del self.session_storage[origin][key]

    def clear_session_storage(self, origin=None):
        """
        Clear SessionStorage.

        Args:
            origin: Specific origin to clear (None for all)
        """
        if origin:
            if origin in self.session_storage:
                del self.session_storage[origin]
        else:
            self.session_storage.clear()

    def get_storage_usage(self, origin=None):
        """
        Get storage usage.

        Args:
            origin: Specific origin (None for all)

        Returns:
            Storage usage in bytes
        """
        total_size = 0

        if origin:
            # Get size for specific origin
            storage_file = self.get_local_storage_file(origin)
            if os.path.exists(storage_file):
                total_size = os.path.getsize(storage_file)
        else:
            # Get total size
            for filename in os.listdir(self.local_storage_path):
                filepath = os.path.join(self.local_storage_path, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)

        return total_size

    def get_storage_quota(self):
        """
        Get storage quota.

        Returns:
            Storage quota in bytes
        """
        return self.quota

    def set_storage_quota(self, quota):
        """
        Set storage quota.

        Args:
            quota: Quota in bytes
        """
        self.quota = quota

    def format_size(self, size_bytes):
        """
        Format bytes to human-readable size.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def get_all_origins(self):
        """
        Get all origins with stored data.

        Returns:
            List of origin strings
        """
        origins = []

        # From local storage
        for filename in os.listdir(self.local_storage_path):
            if filename.endswith('.json'):
                origin = filename[:-5].replace('_', '://', 1).replace('_', '/')
                origins.append(origin)

        # From session storage
        origins.extend(self.session_storage.keys())

        return list(set(origins))

    def export_storage(self, origin, filepath):
        """
        Export storage data to a file.

        Args:
            origin: Origin to export
            filepath: Output file path
        """
        data = {
            'origin': origin,
            'exported': datetime.now().isoformat(),
            'local_storage': {},
            'session_storage': {}
        }

        # Export local storage
        storage_file = self.get_local_storage_file(origin)
        if os.path.exists(storage_file):
            with open(storage_file, 'r') as f:
                data['local_storage'] = json.load(f)

        # Export session storage
        if origin in self.session_storage:
            data['session_storage'] = self.session_storage[origin]

        # Save export
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def import_storage(self, filepath):
        """
        Import storage data from a file.

        Args:
            filepath: Import file path
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        origin = data.get('origin')
        if not origin:
            return

        # Import local storage
        if 'local_storage' in data:
            storage_file = self.get_local_storage_file(origin)
            with open(storage_file, 'w') as f:
                json.dump(data['local_storage'], f, indent=2)

        # Import session storage
        if 'session_storage' in data:
            self.session_storage[origin] = data['session_storage']
