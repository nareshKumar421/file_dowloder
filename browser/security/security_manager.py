"""
Security Manager

Handles browser security features including HTTPS enforcement,
Content Security Policy, and security indicators.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class SecurityManager(QObject):
    """
    Manages browser security features.

    Signals:
        security_alert: Emitted when security issue is detected
        certificate_error: Emitted on SSL certificate error
    """

    security_alert = pyqtSignal(str, str)  # title, message
    certificate_error = pyqtSignal(str)  # error description

    def __init__(self, parent=None):
        """Initialize security manager."""
        super().__init__(parent)

        # Security settings
        self.enforce_https = False
        self.block_mixed_content = True
        self.enable_csp = True
        self.block_popups = True

        # Blocked domains
        self.blocked_domains = set()

        # Security exceptions
        self.https_exceptions = set()

    def set_enforce_https(self, enforce):
        """
        Enable/disable HTTPS enforcement.

        Args:
            enforce: True to enforce HTTPS
        """
        self.enforce_https = enforce

    def is_https_enforced(self):
        """
        Check if HTTPS is enforced.

        Returns:
            True if HTTPS is enforced
        """
        return self.enforce_https

    def set_block_mixed_content(self, block):
        """
        Enable/disable mixed content blocking.

        Args:
            block: True to block mixed content
        """
        self.block_mixed_content = block

    def should_block_mixed_content(self):
        """
        Check if mixed content should be blocked.

        Returns:
            True if mixed content should be blocked
        """
        return self.block_mixed_content

    def validate_url(self, url):
        """
        Validate URL for security.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if domain is blocked
        if self._is_domain_blocked(url):
            return False, "This domain has been blocked for security reasons"

        # Check HTTPS enforcement
        if self.enforce_https:
            if url.startswith('http://') and not self._is_https_exception(url):
                return False, "This site uses an insecure connection (HTTP). HTTPS is required."

        return True, ""

    def check_url_security(self, url):
        """
        Check URL security level.

        Args:
            url: URL to check

        Returns:
            Security level: 'secure', 'warning', 'insecure'
        """
        if url.startswith('https://'):
            return 'secure'
        elif url.startswith('http://'):
            return 'insecure'
        elif url.startswith(('file://', 'about:', 'chrome://')):
            return 'local'
        else:
            return 'warning'

    def block_domain(self, domain):
        """
        Block a domain.

        Args:
            domain: Domain to block
        """
        self.blocked_domains.add(domain)

    def unblock_domain(self, domain):
        """
        Unblock a domain.

        Args:
            domain: Domain to unblock
        """
        self.blocked_domains.discard(domain)

    def is_domain_blocked(self, domain):
        """
        Check if domain is blocked.

        Args:
            domain: Domain to check

        Returns:
            True if blocked
        """
        return domain in self.blocked_domains

    def _is_domain_blocked(self, url):
        """
        Check if URL's domain is blocked.

        Args:
            url: URL to check

        Returns:
            True if blocked
        """
        from urllib.parse import urlparse

        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            return domain in self.blocked_domains
        except:
            return False

    def add_https_exception(self, domain):
        """
        Add HTTPS enforcement exception.

        Args:
            domain: Domain to exempt from HTTPS requirement
        """
        self.https_exceptions.add(domain)

    def remove_https_exception(self, domain):
        """
        Remove HTTPS enforcement exception.

        Args:
            domain: Domain to remove from exceptions
        """
        self.https_exceptions.discard(domain)

    def _is_https_exception(self, url):
        """
        Check if URL is an HTTPS exception.

        Args:
            url: URL to check

        Returns:
            True if URL is exempt from HTTPS enforcement
        """
        from urllib.parse import urlparse

        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            return domain in self.https_exceptions
        except:
            return False

    def get_blocked_domains(self):
        """
        Get list of blocked domains.

        Returns:
            Set of blocked domains
        """
        return self.blocked_domains.copy()

    def clear_blocked_domains(self):
        """Clear all blocked domains."""
        self.blocked_domains.clear()

    def get_security_info(self, url):
        """
        Get security information for URL.

        Args:
            url: URL to check

        Returns:
            Dictionary with security information
        """
        level = self.check_url_security(url)

        info = {
            'url': url,
            'security_level': level,
            'is_https': url.startswith('https://'),
            'is_secure': level == 'secure',
            'warnings': []
        }

        # Add warnings
        if level == 'insecure':
            info['warnings'].append('Connection is not encrypted')

        if self._is_domain_blocked(url):
            info['warnings'].append('Domain is blocked')

        return info
