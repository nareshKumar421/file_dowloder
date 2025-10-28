# PyBrowser - A Fully Functional Python Web Browser

<div align="center">

**A complete, feature-rich web browser built entirely in Python using PyQt6 and QtWebEngine**

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

---

## Overview

PyBrowser is a fully functional web browser that demonstrates how modern browsers work. It includes all the core features you'd expect from a production browser, built using Python and the Chromium-based QtWebEngine.

### Key Features

- **Full Web Support**: HTML5, CSS3, JavaScript (ES6+), WebGL, Canvas
- **Modern UI**: Clean interface with tabs, navigation, and address bar
- **Developer Tools**: Console, DOM inspector, network monitor, storage viewer
- **Privacy**: Incognito mode with no persistent storage
- **Bookmarks & History**: Full bookmark management and browsing history
- **Security**: HTTPS enforcement, mixed content blocking, security indicators
- **Storage APIs**: LocalStorage, SessionStorage, and Cookie management
- **Downloads**: Integrated download manager
- **Customization**: Zoom, fullscreen, find in page, and more

---

## Architecture

PyBrowser follows a modular architecture with clean separation of concerns:

```
PyBrowser
├── Core Engine
│   ├── BrowserEngine (QtWebEngine wrapper)
│   ├── BrowserTab (individual tab management)
│   ├── HistoryManager (browsing history)
│   └── BookmarksManager (bookmarks)
├── UI Components
│   ├── MainWindow (main browser window)
│   ├── NavigationBar (address bar, buttons)
│   └── TabsWidget (tab management)
├── Network Layer
│   └── NetworkManager (requests, cookies, downloads)
├── Storage Layer
│   └── StorageManager (LocalStorage, SessionStorage)
├── Security Layer
│   └── SecurityManager (HTTPS, CSP, security policies)
└── Developer Tools
    └── DevToolsPanel (console, inspector, network)
```

---

## Installation

### Prerequisites

- **Python 3.7 or higher**
- **PyQt6 6.6.0+** (includes QtWebEngine)

### Install Dependencies

```bash
# Install from requirements file
pip install -r requirements-browser.txt

# Or install manually
pip install PyQt6 PyQt6-WebEngine requests beautifulsoup4 lxml cssutils cryptography
```

### Verify Installation

```bash
python -c "from PyQt6.QtWebEngineWidgets import QWebEngineView; print('✓ PyQt6-WebEngine installed')"
```

---

## Usage

### Launch the Browser

```bash
# Basic launch
python pybrowser.py

# Open with specific URL
python pybrowser.py https://www.example.com

# Make executable and run (Linux/Mac)
chmod +x pybrowser.py
./pybrowser.py
```

### Keyboard Shortcuts

#### Navigation
- **Ctrl+T** - New tab
- **Ctrl+W** - Close tab
- **Ctrl+N** - New window
- **Ctrl+Shift+N** - New incognito tab
- **Alt+Left** - Back
- **Alt+Right** - Forward
- **Ctrl+R** / **F5** - Reload
- **Alt+Home** - Home page

#### View
- **Ctrl++** - Zoom in
- **Ctrl+-** - Zoom out
- **Ctrl+0** - Reset zoom
- **F11** - Fullscreen
- **Ctrl+F** - Find in page

#### Tools
- **Ctrl+H** - History
- **Ctrl+D** - Bookmark page
- **Ctrl+Shift+B** - Show bookmarks
- **Ctrl+J** - Downloads
- **F12** - Developer tools

#### Application
- **Ctrl+Q** - Quit browser

---

## Features in Detail

### 1. Browser Engine & Rendering

- **QtWebEngine** (Chromium-based) provides production-quality rendering
- Full HTML5 support with semantic elements
- Complete CSS3 support including flexbox, grid, animations
- JavaScript ES6+ with full DOM API
- WebGL for 3D graphics
- Canvas API for 2D graphics
- SVG support
- Video and audio playback

### 2. DOM Management

The browser provides full DOM API access:

```javascript
// All standard DOM methods work
document.getElementById('myElement')
document.querySelector('.className')
document.querySelectorAll('div.item')
element.appendChild(child)
element.removeChild(child)
element.classList.add('active')
element.style.color = 'red'
```

### 3. Event System

Complete event handling with capturing and bubbling:

```javascript
element.addEventListener('click', handler)
element.removeEventListener('click', handler)

// All event types supported:
// Mouse: click, dblclick, mousedown, mouseup, mousemove, mouseover, mouseout
// Keyboard: keydown, keyup, keypress
// Form: submit, change, input, focus, blur
// Window: load, resize, scroll, beforeunload
```

### 4. Network Layer

- HTTP/HTTPS requests with proper headers
- Cookie management (view, edit, delete)
- Cache system with size management
- Download manager with progress tracking
- Request/response monitoring
- Support for all HTTP methods (GET, POST, PUT, DELETE)

### 5. Browser UI

**Navigation Bar:**
- Address bar with URL input
- Back/Forward buttons with history
- Reload/Stop button
- Home button
- Security indicator (🔒 for HTTPS)

**Tabs:**
- Multiple tab support
- Drag to reorder
- Close individual tabs
- Tab icons (favicons)
- New tab button

**Developer Tools:**
- **Console**: JavaScript execution and logging
- **Inspector**: DOM tree viewer
- **Network**: Request monitoring
- **Storage**: View LocalStorage, SessionStorage, Cookies

### 6. JavaScript Integration

Execute JavaScript in page context:

```python
# From Python code
tab.execute_javascript('document.title', callback)

# Or use developer console
# Type JavaScript directly in the console tab
```

Access browser APIs from JavaScript:
```javascript
// Console
console.log('Hello, World!')
console.error('Error message')

// Timers
setTimeout(() => console.log('Delayed'), 1000)
setInterval(() => console.log('Repeated'), 1000)

// Window
window.location.href
window.history.back()
window.localStorage.setItem('key', 'value')
```

### 7. Storage APIs

**LocalStorage** (persistent):
```javascript
localStorage.setItem('username', 'john')
localStorage.getItem('username')
localStorage.removeItem('username')
localStorage.clear()
```

**SessionStorage** (session-only):
```javascript
sessionStorage.setItem('sessionId', '12345')
sessionStorage.getItem('sessionId')
sessionStorage.clear()
```

**Cookies**:
Managed automatically by the browser engine with full RFC compliance.

### 8. Security Features

- **HTTPS Enforcement**: Optional enforcement of HTTPS connections
- **Mixed Content Blocking**: Blocks insecure content on secure pages
- **Same-Origin Policy**: Enforced by the rendering engine
- **XSS Protection**: Built into Chromium
- **CSP Support**: Content Security Policy headers respected
- **Domain Blocking**: Block specific domains
- **Security Indicators**: Visual indicators for connection security

### 9. History & Bookmarks

**History:**
- Automatic tracking of visited pages
- Search history
- View most visited sites
- Clear history (all or by time period)
- Visit count tracking

**Bookmarks:**
- Bookmark any page
- Organize with folders
- Search bookmarks
- Import/export bookmarks
- Quick access from bookmarks menu

### 10. Incognito Mode

- No persistent history
- No persistent cookies
- Separate profile from normal browsing
- All data deleted when tab closes
- Visual indicator in tab title

---

## Developer Tools

### Console Tab

Execute JavaScript and view console output:

```javascript
// Type in console input:
document.querySelector('h1').textContent = 'Modified!'

// View console messages from the page:
console.log('Debug message')
console.warn('Warning message')
console.error('Error message')
```

### Inspector Tab

- View DOM tree structure
- Inspect element attributes
- Navigate parent/child relationships

### Network Tab

- Monitor all network requests
- View request method, URL, status
- See response size and type
- Track timing information

### Storage Tab

- View LocalStorage keys and values
- View SessionStorage data
- Inspect cookies
- Monitor storage usage

---

## Customization & Extension

### Setting Home Page

```python
# In pybrowser.py or after creating window
window.home_url = "https://your-homepage.com"
```

### Custom User Agent

```python
window.engine.set_http_user_agent("Custom User Agent String")
```

### Enable HTTPS Enforcement

```python
window.security_manager.set_enforce_https(True)
```

### Block Domains

```python
window.security_manager.block_domain("example.com")
```

### Custom Download Directory

```python
window.network_manager.set_downloads_path("/path/to/downloads")
```

---

## Code Examples

### Example 1: Open Browser with Multiple Tabs

```python
from PyQt6.QtWidgets import QApplication
from browser import BrowserMainWindow

app = QApplication([])
window = BrowserMainWindow("MyBrowser")

# Add multiple tabs
window.add_new_tab("https://www.python.org")
window.add_new_tab("https://www.github.com")
window.add_new_tab("https://www.stackoverflow.com")

window.show()
app.exec()
```

### Example 2: Execute JavaScript

```python
# Get current tab
tab = window.tabs.get_current_tab()

# Execute JavaScript
tab.execute_javascript("""
    // Modify page
    document.body.style.background = 'lightblue';

    // Return value
    document.title;
""", lambda result: print(f"Page title: {result}"))
```

### Example 3: Monitor Downloads

```python
def on_download_started(filename, url):
    print(f"Downloading {filename} from {url}")

def on_download_finished(filename, path):
    print(f"Downloaded to {path}")

window.network_manager.download_started.connect(on_download_started)
window.network_manager.download_finished.connect(on_download_finished)
```

### Example 4: Access Browser Data

```python
# Get browsing history
history = window.history_manager.get_history(limit=50)
for entry in history:
    print(f"{entry['title']} - {entry['url']}")

# Get bookmarks
bookmarks = window.bookmarks_manager.get_bookmarks()
for bookmark in bookmarks:
    print(f"{bookmark['title']} - {bookmark['url']}")

# Get storage usage
usage = window.storage_manager.get_storage_usage()
print(f"Storage used: {window.storage_manager.format_size(usage)}")
```

---

## Testing

### Test with Local HTML Files

Create a test HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        button { padding: 10px 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>PyBrowser Test Page</h1>
    <button onclick="testFeatures()">Test Features</button>
    <div id="output"></div>

    <script>
        function testFeatures() {
            let output = document.getElementById('output');

            // Test DOM manipulation
            output.innerHTML = '<h2>Testing DOM...</h2>';

            // Test LocalStorage
            localStorage.setItem('test', 'success');
            output.innerHTML += '<p>LocalStorage: ' + localStorage.getItem('test') + '</p>';

            // Test Console
            console.log('Console test successful!');

            // Test Events
            output.innerHTML += '<p>All tests passed! ✓</p>';
        }
    </script>
</body>
</html>
```

Load it:
```bash
python pybrowser.py test.html
```

---

## Troubleshooting

### Issue: "No module named 'PyQt6'"

**Solution:**
```bash
pip install --upgrade PyQt6 PyQt6-WebEngine
```

### Issue: "QtWebEngine is not available"

**Solution:**
Make sure PyQt6-WebEngine is installed separately:
```bash
pip install PyQt6-WebEngine
```

### Issue: Blank page or rendering issues

**Solution:**
- Check your internet connection
- Try clearing cache: Menu → Tools → Clear Cache
- Check console for JavaScript errors (F12)

### Issue: Downloads not working

**Solution:**
- Check downloads directory permissions
- Set custom download path if needed
- Check browser console for errors

---

## Performance Considerations

- **Memory Usage**: Each tab runs in its own process (Chromium architecture)
- **Cache Size**: Default cache is 100MB, managed automatically
- **History Limit**: 10,000 entries maximum
- **Storage Quota**: 10MB per domain for LocalStorage

To reduce memory usage:
```python
# Limit tab count
# Close unused tabs regularly
# Clear cache periodically
window.engine.clear_cache()
```

---

## Security Best Practices

1. **Enable HTTPS Enforcement** for secure browsing
2. **Use Incognito Mode** for sensitive browsing
3. **Regularly clear cookies and cache**
4. **Keep PyQt6 updated** for security patches
5. **Block untrusted domains** using the security manager
6. **Review permissions** before allowing JavaScript

---

## Known Limitations

1. **Extensions**: Browser extensions (Chrome/Firefox style) are not supported
2. **PDF Viewer**: Uses system PDF viewer for PDF files
3. **Flash/Java**: No support for legacy plugins (by design)
4. **WebRTC**: Limited WebRTC support depending on Qt version
5. **DevTools Protocol**: Limited compared to Chrome DevTools

---

## Project Structure

```
file_dowloder/
├── browser/                    # Browser package
│   ├── __init__.py            # Package initialization
│   ├── core/                  # Core engine components
│   │   ├── engine.py          # Browser engine wrapper
│   │   ├── tab.py             # Tab implementation
│   │   ├── history.py         # History manager
│   │   └── bookmarks.py       # Bookmarks manager
│   ├── ui/                    # UI components
│   │   ├── main_window.py     # Main browser window
│   │   ├── navigation_bar.py  # Navigation bar
│   │   └── tabs_widget.py     # Tabs widget
│   ├── network/               # Network layer
│   │   └── network_manager.py # Network management
│   ├── storage/               # Storage layer
│   │   └── storage_manager.py # Storage APIs
│   ├── security/              # Security features
│   │   └── security_manager.py# Security management
│   └── devtools/              # Developer tools
│       └── devtools_panel.py  # DevTools panel
├── pybrowser.py               # Main launcher
├── requirements-browser.txt   # Browser dependencies
└── BROWSER_README.md          # This file
```

---

## Contributing

Contributions are welcome! Areas for improvement:

- Enhanced developer tools
- Additional security features
- Performance optimizations
- UI/UX improvements
- More keyboard shortcuts
- Extension API
- Mobile device emulation

---

## License

MIT License - Free to use, modify, and distribute.

---

## Credits

Built with:
- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Python bindings for Qt
- **[QtWebEngine](https://doc.qt.io/qt-6/qtwebengine-index.html)** - Chromium-based web engine
- **[Python](https://www.python.org/)** - Programming language

---

## Changelog

### Version 1.0.0
- Initial release
- Full browser functionality
- Multi-tab support
- Developer tools
- History and bookmarks
- Incognito mode
- Download manager
- Security features
- Storage APIs

---

## Frequently Asked Questions

**Q: Can I use this as my daily browser?**
A: While PyBrowser is fully functional, it's designed for educational purposes. For daily use, we recommend established browsers like Chrome, Firefox, or Edge.

**Q: How does it compare to Chrome/Firefox?**
A: PyBrowser uses the same rendering engine as Chrome (Chromium) for web pages, but has a simpler feature set. It's great for learning and custom applications.

**Q: Can I build a custom browser with this?**
A: Absolutely! PyBrowser is designed to be a foundation for custom browser projects.

**Q: Does it support extensions?**
A: Not currently, but the architecture allows for custom Python-based extensions.

**Q: Is it secure?**
A: PyBrowser uses Chromium's security features and follows web security best practices. However, always keep dependencies updated.

---

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation
- Review the code examples

---

**Made with ❤️ using Python and PyQt6**

Happy browsing! 🌐
