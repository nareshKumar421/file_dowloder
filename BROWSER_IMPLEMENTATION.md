# PyBrowser Implementation Details

## Overview

This document provides technical details about the PyBrowser implementation.

## Architecture Summary

PyBrowser is built using a modular architecture with the following components:

### 1. Core Engine (`browser/core/`)

**BrowserEngine** (`engine.py`)
- Manages QtWebEngine profiles (default and incognito)
- Configures global web engine settings
- Handles user agent and storage paths
- Provides cache and cookie management

**BrowserTab** (`tab.py`)
- Individual tab implementation with QtWebEngineView
- Handles page loading, navigation, and events
- Provides JavaScript execution interface
- Manages zoom, find, and other tab-specific features

**HistoryManager** (`history.py`)
- Persistent browsing history storage
- Visit count tracking
- Search and filtering capabilities
- Configurable retention policies

**BookmarksManager** (`bookmarks.py`)
- Bookmark storage with folder organization
- Import/export functionality
- Search and management features

### 2. UI Components (`browser/ui/`)

**BrowserMainWindow** (`main_window.py`)
- Main application window
- Integrates all components
- Manages tabs, navigation, and menu
- Handles global shortcuts and actions

**NavigationBar** (`navigation_bar.py`)
- Address bar with security indicator
- Navigation buttons (back, forward, reload, home)
- Progress bar for page loading
- Menu for additional options

**BrowserTabWidget** (`tabs_widget.py`)
- Tab management with drag-and-drop reordering
- Tab close buttons
- New tab button
- Tab title and icon updates

### 3. Network Layer (`browser/network/`)

**NetworkManager** (`network_manager.py`)
- Download management and tracking
- Cookie access and management
- Cache size monitoring
- Request statistics

### 4. Storage Layer (`browser/storage/`)

**StorageManager** (`storage_manager.py`)
- LocalStorage implementation (persistent)
- SessionStorage implementation (session-only)
- Storage quota management
- Import/export capabilities

### 5. Security Layer (`browser/security/`)

**SecurityManager** (`security_manager.py`)
- HTTPS enforcement
- Mixed content blocking
- Domain blocking/whitelisting
- Security indicators and warnings

### 6. Developer Tools (`browser/devtools/`)

**DevToolsPanel** (`devtools_panel.py`)
- Console for JavaScript execution
- DOM inspector
- Network request monitor
- Storage viewer

## Key Technologies

### QtWebEngine
- Based on Chromium rendering engine
- Provides full HTML5, CSS3, JavaScript support
- Handles security, sandboxing, and process isolation
- Includes built-in PDF viewer, media codecs, etc.

### PyQt6
- Python bindings for Qt 6
- Provides GUI framework
- Event loop and signal/slot mechanism
- Cross-platform support

## Data Storage

Browser data is stored in `~/.pybrowser/`:
```
~/.pybrowser/
├── storage/          # Persistent storage (LocalStorage)
├── cache/            # HTTP cache
├── downloads/        # Downloaded files
├── history.json      # Browsing history
├── bookmarks.json    # Bookmarks
└── cookies/          # Cookies (managed by QtWebEngine)
```

## Signal/Slot Architecture

PyBrowser uses Qt's signal/slot mechanism for event handling:

**Tab Signals:**
- `url_changed` - URL navigation
- `title_changed` - Page title updates
- `loading_started/finished` - Page load state
- `icon_changed` - Favicon updates

**Window Signals:**
- `navigate_*` - Navigation actions
- `url_submitted` - Address bar submission
- `bookmark_added` - Bookmark requests
- `download_*` - Download events

## JavaScript Bridge

JavaScript execution is handled through QtWebEngine's JavaScript bridge:

```python
tab.execute_javascript("document.title", callback)
```

Console messages from web pages are captured:
```python
page.javaScriptConsoleMessage = handler
```

## Security Implementation

### HTTPS Enforcement
- Optional enforcement of HTTPS connections
- Exception list for trusted HTTP sites
- Visual indicators for connection security

### Content Security
- Same-origin policy (enforced by Chromium)
- Mixed content blocking (configurable)
- XSS protection (built into Chromium)

### Privacy
- Incognito mode with separate profile
- No persistent storage in incognito
- Cookie isolation

## Performance Considerations

### Memory Management
- Each tab runs in separate process (Chromium architecture)
- Lazy tab loading
- Cache size limits
- History size limits (10,000 entries)

### Rendering Optimization
- Hardware acceleration enabled
- Accelerated 2D canvas
- WebGL support
- GPU compositing

## Extension Points

The architecture allows for easy extensions:

### Custom Protocol Handlers
```python
# Register custom protocol
scheme_handler = CustomSchemeHandler()
profile.installUrlSchemeHandler(b"custom", scheme_handler)
```

### Request Interceptors
```python
# Intercept network requests
interceptor = CustomRequestInterceptor()
profile.setUrlRequestInterceptor(interceptor)
```

### JavaScript Injection
```python
# Inject JavaScript into all pages
script = QWebEngineScript()
script.setSourceCode(js_code)
profile.scripts().insert(script)
```

## Testing

The browser includes comprehensive test pages:

**test_browser.html**
- Tests all browser features
- DOM manipulation
- Event handling
- Storage APIs
- Canvas
- Fetch API
- Timers and async operations

**welcome.html**
- Welcome page with feature overview
- Quick access to test page
- Keyboard shortcuts reference

## Limitations and Future Improvements

### Current Limitations
1. No extension API (Chrome/Firefox style)
2. Limited DevTools (not as comprehensive as Chrome)
3. No sync functionality
4. Basic download manager

### Potential Improvements
1. Add extension/plugin system
2. Implement bookmarks sync
3. Enhanced developer tools
4. Better download manager with pause/resume
5. Reader mode
6. Password manager
7. Form auto-fill
8. Ad blocker
9. Mobile device emulation
10. Screenshot tools

## Dependencies

Core dependencies:
- **PyQt6** (6.6.0+) - GUI framework
- **PyQt6-WebEngine** (6.6.0+) - Web rendering engine
- **requests** - HTTP library (for additional features)
- **beautifulsoup4** - HTML parsing (for additional features)
- **lxml** - XML/HTML processing
- **cssutils** - CSS parsing
- **cryptography** - Secure storage

## Code Style

The codebase follows:
- PEP 8 style guidelines
- Type hints where appropriate
- Comprehensive docstrings
- Signal/slot naming convention
- Clear separation of concerns

## Contributing

To contribute:
1. Follow the existing architecture
2. Add docstrings to all public methods
3. Use signals for event communication
4. Keep UI and logic separated
5. Add tests for new features
6. Update documentation

## License

MIT License - See LICENSE file for details.

---

**For more information, see BROWSER_README.md**
