# 🌐 CTK Browser - Modern, Beautiful Web Browser

A stunning, easy-to-use web browser built with **CustomTkinter** and **pywebview**. Features a modern UI with dark/light themes, bookmarks, history, and intuitive navigation.

![CustomTkinter Browser](https://img.shields.io/badge/CustomTkinter-5.2%2B-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🎨 Beautiful Modern UI
- **CustomTkinter Design** - Modern, sleek interface
- **Dark/Light Themes** - Switch between appearance modes
- **Smooth Animations** - Polished user experience
- **Responsive Layout** - Works on any screen size
- **Rounded Corners** - Contemporary design elements

### 🌐 Core Browser Features
- **Web Navigation** - Back, forward, reload, home buttons
- **Smart Address Bar** - Enter URLs or search directly
- **Multiple Tabs** - Open and manage multiple tabs
- **Bookmarks** - Save and organize your favorite sites
- **History** - Track all visited pages
- **Native Web Engine** - Uses your OS's native webview
  - Edge WebView2 on Windows
  - WebKit on macOS
  - WebKitGTK on Linux

### ⚙️ Advanced Features
- **Theme Customization** - Blue, Green, Dark-Blue themes
- **Appearance Modes** - Dark, Light, or System
- **Easy Navigation** - Intuitive controls
- **Persistent Data** - Bookmarks and history saved locally
- **Search Integration** - Auto-search with Google

---

## 🚀 Quick Start

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd file_dowloder
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-ctk-browser.txt
   ```

3. **Run the browser**:
   ```bash
   python ctk_browser.py
   ```

### First Launch

When you launch CTK Browser:
1. The main control window opens with navigation controls
2. A separate webview window opens for displaying web content
3. Use the control window to navigate, manage bookmarks, and settings

---

## 📖 User Guide

### Navigation

#### Address Bar
- **Type a URL**: Enter `google.com` or `https://example.com`
- **Search**: Type any text to search on Google
- **Press Enter** or click **Go** to navigate

#### Navigation Buttons
- **← Back**: Go to previous page
- **→ Forward**: Go to next page
- **⟳ Reload**: Refresh current page
- **🏠 Home**: Go to Google homepage

### Bookmarks

#### Adding Bookmarks
1. Navigate to a page you like
2. Click the **⭐** star button
3. Enter a title for the bookmark
4. Click **Add Bookmark**

#### Viewing Bookmarks
1. Click the **📚** bookmarks button
2. Browse your saved bookmarks
3. Click **Open** to visit a bookmarked page
4. Click **Delete** to remove a bookmark

### History

#### Viewing History
1. Click the **🕐** history button
2. Browse your recent browsing history
3. Click **Open** to revisit a page
4. Click **Clear History** to delete all history

### Tabs

#### Managing Tabs
- Click the **+** button to open a new tab
- Each tab has its own browser window
- Navigate independently in each tab

### Settings

#### Changing Appearance
1. Click the **⚙** settings button
2. Select your preferred:
   - **Appearance Mode**: Dark, Light, or System
   - **Color Theme**: Blue, Green, or Dark-Blue
3. Changes apply immediately (theme changes need restart)

---

## 🎨 Appearance Customization

### Dark Mode (Default)
- Modern dark theme
- Easy on the eyes
- Perfect for night browsing

### Light Mode
- Clean, bright interface
- Great for daytime use
- Professional look

### Themes
- **Blue**: Classic blue accent (default)
- **Green**: Fresh green accent
- **Dark-Blue**: Deep blue accent

---

## 🔧 Technical Details

### Architecture

```
CTKBrowser (Main Window)
├── Top Bar (Navigation & Controls)
│   ├── Navigation Buttons (Back, Forward, Reload, Home)
│   ├── Address Bar (URL entry with search)
│   └── Action Buttons (Bookmark, History, Settings, New Tab)
├── Content Area (Web display info)
├── Status Bar (Status messages)
└── Managers
    ├── BookmarkManager (JSON storage)
    └── HistoryManager (JSON storage)

BrowserTab
└── Webview Window (Separate native browser window)
```

### Data Storage

All data is stored in `~/.ctk_browser/`:
- `bookmarks.json` - Your saved bookmarks
- `history.json` - Browsing history (last 1000 entries)

### Web Rendering

CTK Browser uses **pywebview**, which provides:
- **Windows**: Edge WebView2 (Chromium-based)
- **macOS**: WebKit
- **Linux**: WebKitGTK

This gives you:
✅ Native performance
✅ Full HTML5/CSS3/JavaScript support
✅ Automatic security updates from your OS
✅ Small application size

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` in address bar | Navigate to URL/Search |
| `Escape` in dialogs | Close dialog |
| `Return` in bookmark dialog | Add bookmark |

---

## 🎯 Use Cases

### Perfect For:
- **Web Development Testing** - Test your websites
- **Lightweight Browsing** - Fast, minimal browser
- **Custom Browser Projects** - Extend and customize
- **Learning** - Study browser architecture
- **Privacy** - Local bookmarks and history

### Educational Purpose:
- Learn CustomTkinter GUI development
- Understand browser architecture
- Practice Python application development
- Study UI/UX design principles

---

## 🔒 Privacy & Security

### Data Privacy
- ✅ All data stored locally
- ✅ No telemetry or tracking
- ✅ No cloud sync
- ✅ You own your data

### Security
- ✅ HTTPS support through native webview
- ✅ Security updates from your OS
- ✅ Same security as native browser
- ✅ Sandboxed web content

---

## 🛠️ Development

### Project Structure

```
ctk_browser.py                 # Main application
requirements-ctk-browser.txt   # Python dependencies
CTK_BROWSER_README.md         # This file

~/.ctk_browser/               # User data directory
├── bookmarks.json            # Bookmarks storage
└── history.json              # History storage
```

### Requirements
- Python 3.8+
- customtkinter 5.2+
- pywebview 4.4+
- Operating System:
  - Windows 10+ (with Edge WebView2)
  - macOS 10.14+
  - Linux (with WebKitGTK)

### Extending the Browser

The code is designed to be easy to extend:

#### Add New Features
```python
# Add a new button to the navigation bar
self.my_button = ctk.CTkButton(
    right_frame,
    text="🎨",
    width=40,
    height=40,
    command=self.my_feature
)
self.my_button.pack(side="left", padx=2)
```

#### Customize Appearance
```python
# Change the default theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
```

#### Add Storage
```python
# Create a new manager
class DownloadManager:
    def __init__(self):
        self.downloads_file = Path.home() / '.ctk_browser' / 'downloads.json'
        # ... implementation
```

---

## 🎨 Design Philosophy

### Modern & Beautiful
- Clean, uncluttered interface
- Smooth rounded corners
- Consistent spacing
- Professional color schemes

### Easy to Use
- Intuitive controls
- Clear visual feedback
- Helpful status messages
- Simple dialogs

### Responsive
- Adapts to window size
- Smooth animations
- Fast performance
- Native feel

### Customizable
- Multiple themes
- Dark/Light modes
- Easy to extend
- Clean code structure

---

## 📊 Features Comparison

| Feature | CTK Browser | Chrome | Firefox |
|---------|-------------|--------|---------|
| Modern UI | ✅ | ✅ | ✅ |
| Dark/Light Theme | ✅ | ✅ | ✅ |
| Bookmarks | ✅ | ✅ | ✅ |
| History | ✅ | ✅ | ✅ |
| Multiple Tabs | ✅ | ✅ | ✅ |
| Extensions | ❌ | ✅ | ✅ |
| Sync | ❌ | ✅ | ✅ |
| Size | 🟢 Small | 🟡 Large | 🟡 Large |
| Customizable | ✅ Full | ⚠️ Limited | ⚠️ Limited |
| Open Source | ✅ | ⚠️ Partial | ✅ |

---

## 🚀 Performance

### Fast Startup
- Launches in seconds
- Minimal memory usage
- Native rendering engine

### Lightweight
- Small codebase (~600 lines)
- Few dependencies
- No bloat

### Efficient
- Native webview performance
- Low CPU usage
- Responsive UI

---

## 🤝 Contributing

Want to improve CTK Browser? Here's how:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Ideas for Contributions
- Add download manager
- Implement tab management UI
- Add developer tools
- Create browser extensions support
- Add password manager
- Implement find in page
- Add printing support
- Create mobile-responsive design

---

## 🐛 Troubleshooting

### Browser Window Not Opening
**Problem**: Webview window doesn't appear
**Solution**:
- On Windows: Install Edge WebView2 Runtime
- On Linux: Install `python3-gi python3-gi-cairo gir1.2-webkit2-4.0`
- On macOS: Should work out of the box

### Dependencies Issues
**Problem**: Import errors
**Solution**:
```bash
pip install --upgrade -r requirements-ctk-browser.txt
```

### Theme Not Changing
**Problem**: Theme changes don't apply
**Solution**: Restart the application after changing color theme

### Bookmarks Not Saving
**Problem**: Bookmarks disappear
**Solution**: Check write permissions for `~/.ctk_browser/` directory

---

## 📝 FAQ

**Q: Can I use this as my daily browser?**
A: CTK Browser is great for lightweight browsing and testing, but lacks some features of full browsers (extensions, sync, etc.)

**Q: Is it safe to use?**
A: Yes! It uses your operating system's native webview with the same security as your system browser.

**Q: Can I customize the appearance?**
A: Absolutely! The code is designed to be easily customizable. Change themes, colors, and layouts as you like.

**Q: Does it support extensions?**
A: Not currently, but this could be added as a future feature.

**Q: Why separate windows for tabs?**
A: This design choice makes the code simpler while maintaining full browser functionality. Future versions could embed webviews.

**Q: Can I build this into a standalone app?**
A: Yes! Use PyInstaller or similar tools to create executables.

---

## 🎉 Screenshots

### Main Window (Dark Mode)
- Beautiful dark theme with rounded buttons
- Clean navigation bar
- Status bar with helpful messages

### Bookmarks Dialog
- Modern scrollable list
- Easy add/delete actions
- Clean, organized display

### History Dialog
- Chronological browsing history
- Quick navigation to past pages
- Clear history option

### Settings Panel
- Theme customization
- Appearance mode switcher
- Simple, intuitive controls

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **CustomTkinter** - Amazing modern UI framework
- **pywebview** - Excellent web rendering library
- **Python Community** - For awesome tools and libraries

---

## 📞 Support

Having issues or questions?
1. Check the **Troubleshooting** section above
2. Review the code comments in `ctk_browser.py`
3. Open an issue on GitHub

---

## 🔮 Future Plans

- [ ] Embedded tab management (tabs in same window)
- [ ] Download manager with progress
- [ ] Find in page functionality
- [ ] Print support
- [ ] Reader mode
- [ ] Screenshot tool
- [ ] Password manager
- [ ] Developer tools integration
- [ ] Browser extensions support
- [ ] Sync across devices

---

## 🌟 Star This Project

If you find CTK Browser useful, please consider giving it a star! ⭐

---

**Made with ❤️ using CustomTkinter**

*Happy Browsing! 🌐✨*
