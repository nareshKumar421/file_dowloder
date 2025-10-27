# File Downloader 📥

A professional and beautiful file downloader with both **GUI** and **CLI** interfaces! Download files (images, videos, documents, etc.) from URLs with style.

## Two Interfaces Available

### 🖥️ **GUI Version** (NEW!)
Beautiful, minimal, and professional graphical interface built with **CustomTkinter**
- Modern dark/light theme
- Drag and paste URLs
- Real-time progress bars
- Batch downloads with visual feedback
- Perfect for users who prefer graphical interfaces

### 💻 **CLI Version**
Powerful command-line interface built with **Typer** and **Rich**
- Terminal-based with beautiful colors
- Perfect for automation and scripts
- Ideal for power users and developers

## Which Version Should You Use?

| Feature | GUI Version 🖥️ | CLI Version 💻 |
|---------|----------------|----------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Beginner friendly | ⭐⭐⭐ Requires terminal knowledge |
| **Visual Appeal** | ⭐⭐⭐⭐⭐ Modern interface | ⭐⭐⭐⭐ Colored terminal output |
| **Automation** | ⭐⭐ Manual operation | ⭐⭐⭐⭐⭐ Perfect for scripts |
| **Batch Downloads** | ⭐⭐⭐⭐⭐ Visual feedback | ⭐⭐⭐⭐ Table summary |
| **Best For** | Regular users | Developers & power users |

**💡 Tip:** You can install both! Use GUI for daily tasks and CLI for automation.

## Features ✨

- 📥 Download any file type (images, videos, PDFs, documents, archives, etc.)
- 🎨 Beautiful progress bars with transfer speed and ETA
- 📊 Rich colored output for better readability
- 🔄 Support for multiple URLs in a single command
- 📁 Custom output directory
- ✏️ Custom filename for downloads
- 🔍 Automatic filename detection from URL or server headers
- 📈 File size display in human-readable format
- 🛡️ File overwrite protection with confirmation
- ⚡ Force mode for automation
- 🤫 Quiet mode for minimal output
- 📋 Summary table for multiple downloads
- 🎯 Professional error handling with colored messages
- 📚 Built-in help and documentation
- ℹ️ Version and info commands

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nareshKumar421/file_dowloder.git
cd file_dowloder
```

### 2. Install Dependencies

**For CLI version only:**
```bash
pip install -r requirements.txt
```

**For GUI version (includes CLI):**
```bash
pip install -r requirements-gui.txt
```

Or install manually:
```bash
# CLI only
pip install requests typer rich

# GUI version (add this)
pip install customtkinter
```

### 3. Make it Executable (Optional, for Unix/Linux/Mac)

```bash
chmod +x downloader.py launch_gui.sh
```

## Usage

### 🖥️ GUI Version

Launch the beautiful graphical interface:

**On Windows:**
```bash
# Double-click launch_gui.bat
# OR run in terminal:
python launch_gui.py
```

**On Mac/Linux:**
```bash
./launch_gui.sh
# OR
python3 launch_gui.py
```

**GUI Features:**
- **Paste multiple URLs** (one per line) in the text area
- **Choose download directory** with the Browse button
- **Toggle dark/light theme** with the theme button
- **Watch real-time progress** for each download
- **See beautiful summary** when downloads complete

---

### 💻 CLI Version

### Basic Commands

The tool uses a command-based structure. The main command is `download`.

#### Show Help

```bash
python downloader.py --help
python downloader.py download --help
```

#### Download a Single File

```bash
python downloader.py download https://example.com/image.jpg
```

#### Download with Custom Filename

```bash
python downloader.py download https://example.com/video.mp4 -o my_video.mp4
```

#### Download to Custom Directory

```bash
python downloader.py download https://example.com/file.pdf -d ~/Documents
```

#### Download Multiple Files

```bash
python downloader.py download https://example.com/image1.jpg https://example.com/image2.jpg
```

#### Force Overwrite (No Confirmation)

```bash
python downloader.py download https://example.com/file.pdf -f
```

#### Quiet Mode (Minimal Output)

```bash
python downloader.py download https://example.com/file.pdf -q
```

### Additional Commands

#### Show Version

```bash
python downloader.py version
```

#### Show Tool Information

```bash
python downloader.py info
```

## Command-Line Options

### Download Command

```
Usage: downloader.py download [OPTIONS] URLS...

📥 Download files from URLs (images, videos, documents, etc.)

Arguments:
  URLS...  URL(s) to download [required]

Options:
  -o, --output TEXT      Output filename (only works with single URL)
  -d, --directory TEXT   Output directory for downloaded files [default: downloads]
  -f, --force           Force overwrite existing files without confirmation
  -q, --quiet           Minimal output mode
  --help                Show this message and exit
```

## Examples

### Example 1: Download an Image

```bash
python downloader.py download https://example.com/photo.jpg
```

**Output:**
```
╭──────────────── 📥 File Downloader ────────────────╮
│ Output Directory: /path/to/downloads               │
│ Files to Download: 1                               │
╰────────────────────────────────────────────────────╯

🔍 Fetching: https://example.com/photo.jpg
📥 Downloading to: downloads/photo.jpg
⠋ photo.jpg ━━━━━━━━━━━━━━━━ 100% 1.2 MB 2.5 MB/s 0:00:00
✓ Successfully downloaded: downloads/photo.jpg
File size: 1.23 MB
```

### Example 2: Download Multiple Files with Summary

```bash
python downloader.py download \
  https://example.com/image1.jpg \
  https://example.com/image2.png \
  https://example.com/video.mp4
```

**Output includes a beautiful summary table:**
```
───────────────────────── Summary ─────────────────────────
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Status ┃ URL                     ┃ Saved To             ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ ✓      │ https://example.com/... │ downloads/image1.jpg │
│ ✓      │ https://example.com/... │ downloads/image2.png │
│ ✓      │ https://example.com/... │ downloads/video.mp4  │
└────────┴─────────────────────────┴──────────────────────┘

✓ Successful: 3 | ✗ Failed: 0
```

### Example 3: Download with Custom Name and Directory

```bash
python downloader.py download https://example.com/report.pdf \
  -o monthly_report.pdf \
  -d ~/Documents/Reports
```

### Example 4: Force Overwrite for Automation

```bash
python downloader.py download https://example.com/data.json -f -q
```

## Supported File Types

This tool can download **any file type** accessible via HTTP/HTTPS:

- **Images**: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`, `.bmp`, `.ico`
- **Videos**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.webm`, `.flv`, `.wmv`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg`, `.aac`
- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.xlsx`, `.pptx`
- **Archives**: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`
- **Code**: `.py`, `.js`, `.html`, `.css`, `.json`, `.xml`
- And many more!

## Requirements

- **Python**: 3.7 or higher
- **Dependencies**:
  - `requests` - HTTP library for downloading
  - `typer` - Modern CLI framework
  - `rich` - Beautiful terminal formatting

## Features in Detail

### 🎨 Beautiful Progress Bars

- Real-time download progress with percentage
- Transfer speed display (MB/s)
- Estimated time remaining (ETA)
- Spinner animation
- Color-coded status indicators

### 🛡️ Error Handling

The tool gracefully handles various errors:

- **HTTP Errors**: 404, 403, 500, etc.
- **Connection Errors**: Network issues, DNS failures
- **Timeout Errors**: Slow or unresponsive servers
- **Keyboard Interrupt**: Clean cancellation with partial file cleanup

### 📊 Multiple Downloads

When downloading multiple files, you get:

- Individual progress bar for each file
- Summary table with results
- Success/failure statistics
- Proper exit codes for scripts

### 🤖 Automation Friendly

- Force mode (`-f`) bypasses confirmations
- Quiet mode (`-q`) for minimal output
- Proper exit codes (0 = success, 1 = failure)
- Perfect for scripts and automation

## Troubleshooting

### Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'typer'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Permission Denied

**Problem**: Cannot write to output directory

**Solution**: Make sure you have write permissions or use a different directory:
```bash
python downloader.py download URL -d ~/Downloads
```

### SSL Certificate Errors

**Problem**: SSL certificate verification failed

**Solution**: Update your certificates:
```bash
pip install --upgrade certifi
```

### 403 Forbidden or 404 Not Found

**Problem**: Server blocks the download or URL doesn't exist

**Solution**:
- Check if the URL is correct
- Some servers block automated downloads
- Try accessing the URL in a browser first

## Development

### Project Structure

```
file_dowloder/
├── downloader.py          # Main CLI application
├── downloader_gui.py      # GUI application (NEW!)
├── launch_gui.py          # GUI launcher script (NEW!)
├── launch_gui.sh          # Unix/Linux/Mac launcher (NEW!)
├── launch_gui.bat         # Windows launcher (NEW!)
├── requirements.txt       # CLI dependencies
├── requirements-gui.txt   # GUI dependencies (NEW!)
├── README.md             # This file
├── TESTING.md            # Testing guide
├── test_examples.sh      # Test script
└── .gitignore            # Git ignore rules
```

### Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - Feel free to use and modify as needed.

## Credits

Built with:
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework (NEW!)
- [Typer](https://typer.tiangolo.com/) - Modern CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [Requests](https://requests.readthedocs.io/) - HTTP library

## Changelog

### Version 2.1.0 (Current)
- 🖥️ **NEW: Beautiful GUI version with CustomTkinter**
- 🎨 Modern dark/light theme toggle
- 📥 Multi-URL batch downloads with visual feedback
- 📊 Real-time progress bars in GUI
- 🚀 Easy launcher scripts for all platforms
- 📱 Responsive and professional interface
- 🎯 Better user experience for non-technical users

### Version 2.0.0
- ✨ Migrated to Typer framework for professional CLI
- 🎨 Added Rich library for beautiful output
- 📊 Added summary tables for multiple downloads
- ⚡ Added force mode for automation
- 🤫 Added quiet mode for minimal output
- ℹ️ Added version and info commands
- 🎯 Improved error handling with colored messages
- 📈 Enhanced progress bars with speed and ETA

### Version 1.0.0
- 📥 Basic download functionality
- 📁 Custom output directory
- ✏️ Custom filename support
- 🔄 Multiple URL support
- 🛡️ Overwrite protection

---

**Made with ❤️ using Python, Typer, and Rich**
