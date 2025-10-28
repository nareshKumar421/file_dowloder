# PyBrowser Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements-browser.txt

# 2. Verify installation
python -c "from PyQt6.QtWebEngineWidgets import QWebEngineView; print('✓ Ready!')"
```

## Launch Browser

```bash
# Basic launch
python pybrowser.py

# Open specific URL
python pybrowser.py https://www.google.com

# Open test page
python pybrowser.py browser_examples/test_browser.html
```

## Essential Shortcuts

| Action | Shortcut |
|--------|----------|
| New tab | Ctrl+T |
| Close tab | Ctrl+W |
| Reload | Ctrl+R |
| Developer Tools | F12 |
| Find in page | Ctrl+F |
| Bookmark | Ctrl+D |
| History | Ctrl+H |
| Zoom in/out | Ctrl++/- |

## Test All Features

1. **Open the test page:**
   ```bash
   python pybrowser.py browser_examples/test_browser.html
   ```

2. **Click all test buttons** to verify:
   - DOM manipulation ✓
   - Event system ✓
   - LocalStorage ✓
   - SessionStorage ✓
   - Console (open F12) ✓
   - Canvas API ✓
   - Timers ✓
   - Forms ✓
   - Fetch API ✓

3. **Try developer tools (F12):**
   - Execute JavaScript in console
   - View console messages
   - Monitor network requests
   - Inspect storage

## Common Tasks

### Browse the Web
```bash
python pybrowser.py https://www.wikipedia.org
```

### Open Multiple Tabs
- Click the + button
- Or press Ctrl+T

### Bookmark a Page
- Press Ctrl+D
- Or click the ⭐ button

### View History
- Press Ctrl+H
- Or Menu → History → Show History

### Downloads
- Click any download link
- Files saved to `~/.pybrowser/downloads/`

### Incognito Mode
- Press Ctrl+Shift+N
- Or Menu → File → New Incognito Tab

## Customize

### Set Home Page
Edit `pybrowser.py`:
```python
window.home_url = "https://your-homepage.com"
```

### Change Download Location
```python
window.network_manager.set_downloads_path("/your/path")
```

### Enable HTTPS Enforcement
```python
window.security_manager.set_enforce_https(True)
```

## Troubleshooting

**Issue:** Blank page
- Check internet connection
- Clear cache: Menu → Tools → Clear Cache

**Issue:** Module not found
```bash
pip install --upgrade PyQt6 PyQt6-WebEngine
```

**Issue:** Can't see developer console
- Press F12
- Or Menu → Tools → Developer Tools

## Next Steps

- Read [BROWSER_README.md](BROWSER_README.md) for complete documentation
- Test with the included example page
- Build custom features on top of PyBrowser
- Explore the code in `browser/` directory

---

**That's it! You're ready to browse! 🌐**
