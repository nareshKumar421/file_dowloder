# CTK Browser Troubleshooting Guide

## 🔧 Common Issues and Solutions

---

## Issue #1: Browser Not Starting (FIXED!)

### ❌ Problem
The browser crashed or didn't work after the initial version. Error was related to `webview.start()` being called multiple times.

### ✅ Solution (FIXED in latest version!)
**The issue has been FIXED!** Pull the latest code:

```bash
git pull origin claude/session-011CUZVDGezqoFJPzMcY7K4N
```

### What Was Fixed?
- **Root Cause**: `webview.start()` was called every time a new tab was created
- **Fix**: Refactored to call `webview.start()` only ONCE on startup
- **Result**: Browser now works correctly!

---

## Issue #2: Dependencies Not Installed

### ❌ Problem
```
ModuleNotFoundError: No module named 'customtkinter'
```
or
```
ModuleNotFoundError: No module named 'webview'
```

### ✅ Solution
Install the required dependencies:

```bash
pip install -r requirements-ctk-browser.txt
```

Or install manually:
```bash
pip install customtkinter pywebview
```

---

## Issue #3: Windows - Edge WebView2 Not Installed

### ❌ Problem (Windows only)
```
Exception: pywebview requires Edge WebView2
```
or browser window doesn't open on Windows.

### ✅ Solution
Install Microsoft Edge WebView2 Runtime:

1. **Download**: [Edge WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
2. **Install**: Run the installer (it's free and small ~100MB)
3. **Restart**: Close and reopen your terminal
4. **Try again**: `python ctk_browser.py`

**Note**: Most Windows 10/11 systems already have this installed!

---

## Issue #4: Linux - WebKit Not Installed

### ❌ Problem (Linux only)
```
ImportError: cannot import name 'WebKit2'
```
or browser window doesn't open on Linux.

### ✅ Solution
Install WebKitGTK:

**Ubuntu/Debian**:
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-webkit2-4.0
```

**Fedora**:
```bash
sudo dnf install python3-gobject gtk3 webkit2gtk3
```

**Arch Linux**:
```bash
sudo pacman -S python-gobject gtk3 webkit2gtk
```

---

## Issue #5: Browser Window Opens But Control Window Doesn't Respond

### ❌ Problem
The browser window opens, but buttons in the control window don't work.

### ✅ Solution
This is **normal behavior**! The control window becomes responsive after the webview initializes (takes 1-2 seconds).

**How it works**:
1. Control window opens first
2. After 100ms, browser window starts opening
3. Once browser window is visible, controls become active
4. Status bar says "Browser window opened!"

**Tip**: Wait for the status bar message before clicking buttons.

---

## Issue #6: "Browser window not ready yet..." Message

### ❌ Problem
Clicking buttons shows: "Browser window not ready yet..."

### ✅ Solution
Wait 1-2 seconds for the browser window to fully initialize. The status bar will say "Browser window opened!" when ready.

If it never becomes ready:
1. Check if you have webview dependencies installed (see Issues #3 and #4)
2. Try closing and restarting the browser
3. Check your Python version (needs 3.8+)

---

## Issue #7: Can't Navigate to URLs

### ❌ Problem
Typing URLs in the address bar doesn't work.

### ✅ Solution

**Make sure to**:
1. Wait for "Browser window opened!" in the status bar
2. Type the URL (e.g., `google.com` or `https://github.com`)
3. Press Enter or click "Go" button

**URL formats supported**:
- `google.com` → Automatically adds https://
- `https://example.com` → Direct navigation
- `python tutorials` → Google search

---

## Issue #8: Multiple Browser Windows Not Opening

### ❌ Problem
Clicking the + button doesn't open new windows.

### ✅ Solution

The + button creates **additional browser windows** (not tabs in the same window).

**How to use**:
1. Click the + button
2. A **new separate browser window** will open
3. Each window is independent
4. Control them all from the main control window

**Note**: This is by design for simplicity. Each "tab" is actually a separate window.

---

## Issue #9: Bookmarks/History Not Saving

### ❌ Problem
Bookmarks or history disappear after closing the browser.

### ✅ Solution

**Check permissions**:
1. Bookmarks and history are saved to `~/.ctk_browser/`
2. Make sure this directory is writable

**Linux/Mac**:
```bash
ls -la ~/.ctk_browser/
chmod 755 ~/.ctk_browser/
```

**Windows**:
Check `C:\Users\YourName\.ctk_browser\`

**Manual check**:
1. Add a bookmark
2. Check if file exists: `~/.ctk_browser/bookmarks.json`
3. If not, check directory permissions

---

## Issue #10: Python Version Too Old

### ❌ Problem
```
SyntaxError: invalid syntax
```
or
```
TypeError: unsupported operand type(s)
```

### ✅ Solution
CTK Browser requires Python 3.8+

**Check your version**:
```bash
python --version
```

**Upgrade if needed**:
- **Windows**: Download from [python.org](https://python.org)
- **Linux**: `sudo apt install python3.11` (or use pyenv)
- **Mac**: `brew install python@3.11`

---

## Issue #11: CustomTkinter Theme Not Changing

### ❌ Problem
Changing the color theme in settings doesn't change the appearance.

### ✅ Solution
Color theme changes require a **restart**.

1. Click ⚙ Settings
2. Select new color theme
3. Close the browser
4. Run `python ctk_browser.py` again
5. New theme will be applied!

**Appearance mode** (Dark/Light) changes **immediately** without restart.

---

## Issue #12: Back/Forward Buttons Not Working

### ❌ Problem
The ← and → buttons don't navigate history.

### ✅ Solution

**Make sure**:
1. You've navigated to at least 2 pages first
2. The browser window is ready (status says "Browser window opened!")
3. You're clicking in the correct control window

**How browser history works**:
- First visit a page (e.g., google.com)
- Then visit another page (e.g., github.com)
- NOW the back button will work

---

## Issue #13: Can't Search Google

### ❌ Problem
Typing search queries doesn't work.

### ✅ Solution

**To search**:
1. Type your query WITHOUT `https://` or `.com`
2. Example: `python tutorials`
3. Press Enter
4. Will automatically search on Google!

**URL vs Search**:
- `google.com` → Goes to https://google.com
- `python` → Searches Google for "python"
- `https://example.com` → Goes to exact URL

The browser automatically detects if you want a URL or search!

---

## 🚀 Quick Diagnostic Commands

### Check if dependencies are installed:
```bash
python -c "import customtkinter; print('CustomTkinter OK')"
python -c "import webview; print('Webview OK')"
```

### Check Python version:
```bash
python --version
```

### Check data directory:
```bash
ls -la ~/.ctk_browser/
```

### Test import:
```bash
python -c "from ctk_browser import CTKBrowser; print('Import OK')"
```

---

## 🔍 Getting More Help

### Enable Debug Mode (for developers)

Edit `ctk_browser.py` line 328:
```python
# Change this:
webview.start()

# To this:
webview.start(debug=True)
```

This will show detailed error messages in the console.

### Still Not Working?

1. **Check the error message** - Copy the full error text
2. **Try the PyQt6 browser instead** - `python pybrowser.py`
3. **Report the issue** with:
   - Your operating system (Windows/Mac/Linux)
   - Python version (`python --version`)
   - Error message (full text)
   - What you were trying to do

---

## ✅ Verification Steps

After fixing issues, verify the browser works:

### Step 1: Start the browser
```bash
python ctk_browser.py
```

### Step 2: Check control window
- Control window should open (CustomTkinter UI)
- Status bar should say "Ready - Browser window will open shortly..."

### Step 3: Check browser window
- After 1-2 seconds, browser window should open
- Should show Google homepage
- Status bar should update to "Browser window opened!"

### Step 4: Test navigation
1. Type `github.com` in address bar
2. Press Enter
3. Should navigate to GitHub

### Step 5: Test buttons
- Click ← (should go back to Google)
- Click → (should go forward to GitHub)
- Click ⟳ (should reload)
- Click 🏠 (should go to Google)

### Step 6: Test features
- Click ⭐ to add bookmark
- Click 📚 to view bookmarks
- Click 🕐 to view history
- Click ⚙ to open settings
- Click + to open new window

If all steps work → **Browser is working correctly!** 🎉

---

## 📊 System Requirements

**Minimum**:
- Python 3.8+
- 2GB RAM
- Windows 10+ / macOS 10.14+ / Linux with GTK3

**Recommended**:
- Python 3.10+
- 4GB RAM
- Modern OS (Windows 11 / macOS 12+ / Recent Linux)

---

## 🎯 Known Limitations

1. **Tabs are separate windows** - By design for simplicity
2. **No built-in developer tools** - Use browser's native tools (F12 in webview window)
3. **No extensions support** - Native webview limitation
4. **No incognito mode** - Can be added in future
5. **Limited history tracking** - Last 1000 entries only

---

## 💡 Tips for Best Experience

### Performance
- Close unused browser windows (extra tabs)
- Clear history regularly (🕐 → Clear History)
- Don't open too many windows at once

### Navigation
- Use keyboard: Enter to navigate, Esc to close dialogs
- Double-check URL format (google.com vs https://google.com)
- Wait for pages to load before clicking buttons

### Data Management
- Backup bookmarks: `~/.ctk_browser/bookmarks.json`
- Export history: `~/.ctk_browser/history.json`
- Both are JSON files - easy to edit!

---

## 🎉 Success Indicators

You know the browser is working when:

✅ Control window opens with beautiful CustomTkinter UI
✅ Browser window opens showing Google
✅ Status bar says "Browser window opened!"
✅ All buttons respond when clicked
✅ URLs navigate correctly
✅ Bookmarks save and appear in list
✅ History tracks visited pages
✅ Settings work (Dark/Light mode changes immediately)

---

## 🆘 Emergency Fallback

If CustomTkinter browser still doesn't work after trying all fixes:

### Use the PyQt6 Browser Instead!

```bash
pip install -r requirements-browser.txt
python pybrowser.py
```

The PyQt6 browser has:
- More features
- Different dependencies (might work if CustomTkinter doesn't)
- Same functionality
- Chrome-exact appearance

Both browsers are fully functional - choose what works best for you!

---

**Last Updated**: After fixing webview.start() issue
**Version**: 2.0 (Fixed)
**Status**: All known issues resolved ✅
