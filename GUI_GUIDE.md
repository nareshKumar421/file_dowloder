# GUI User Guide 🖥️

Complete guide for using the File Downloader GUI

## Installation

### 1. Install GUI Dependencies

```bash
pip install -r requirements-gui.txt
```

Or install directly:
```bash
pip install customtkinter requests
```

### 2. Launch the GUI

**Windows:**
- Double-click `launch_gui.bat`
- OR run: `python launch_gui.py`

**Mac/Linux:**
```bash
./launch_gui.sh
# OR
python3 launch_gui.py
```

## Interface Overview

### Main Window

The GUI is divided into several sections:

```
╔════════════════════════════════════════╗
║  📥 File Downloader          🌙 Dark   ║  ← Header
╠════════════════════════════════════════╣
║  Enter URL(s):                         ║
║  ┌────────────────────────────────┐   ║
║  │ Paste URLs here...             │   ║  ← URL Input Area
║  │ (one per line)                 │   ║
║  └────────────────────────────────┘   ║
║                                        ║
║  Save to:                              ║
║  [/home/user/Downloads]  [Browse]     ║  ← Output Directory
║                                        ║
║  [    ⬇ Start Download    ]          ║  ← Download Button
╠════════════════════════════════════════╣
║  Downloads:                            ║
║  ┌────────────────────────────────┐   ║
║  │ https://example.com/file.jpg   │   ║
║  │ ▓▓▓▓▓▓▓▓▓░░░░░ 65%            │   ║  ← Download Progress
║  │ Downloading: 1.2 MB / 2.0 MB   │   ║
║  └────────────────────────────────┘   ║
╠════════════════════════════════════════╣
║  Ready                                 ║  ← Status Bar
╚════════════════════════════════════════╝
```

## Features

### 1. URL Input

**How to add URLs:**
1. Click in the URL text area
2. Paste your URL(s)
3. For multiple files, paste one URL per line

**Example:**
```
https://example.com/image1.jpg
https://example.com/image2.jpg
https://example.com/video.mp4
```

**Tips:**
- You can paste as many URLs as you want
- Each URL will be downloaded separately
- Invalid URLs will show an error

### 2. Choose Download Location

**Default:** Your system's Downloads folder

**To change:**
1. Click the **Browse** button
2. Select a folder
3. All files will be saved there

**Tips:**
- The folder will be created if it doesn't exist
- Path is remembered during the session

### 3. Theme Toggle

**Switch between Dark and Light mode:**
- Click the theme button in the top-right
- Changes apply immediately
- Choose what looks best for you!

**Dark Mode (Default):**
- Easy on the eyes
- Modern look
- Great for low-light environments

**Light Mode:**
- Clean and bright
- Traditional appearance
- Better for bright environments

### 4. Download Progress

**What you'll see for each download:**

**Pending:**
```
https://example.com/file.jpg
▱▱▱▱▱▱▱▱▱▱ 0%
Pending...
```

**Downloading:**
```
https://example.com/file.jpg
▓▓▓▓▓▱▱▱▱▱ 45%
Downloading: 0.9 MB / 2.0 MB
```

**Complete:**
```
https://example.com/file.jpg
▓▓▓▓▓▓▓▓▓▓ 100%
✓ Downloaded: file.jpg (2.00 MB)
```

**Error:**
```
https://invalid-url.com/file.jpg
▱▱▱▱▱▱▱▱▱▱ 0%
✗ HTTP Error: 404 Not Found
```

### 5. Status Messages

The status bar at the bottom shows:

- **Ready** - Waiting for user input
- **Downloading...** - Download in progress
- **Complete: X successful, Y failed** - All done!

## Step-by-Step Tutorial

### Simple Single File Download

1. **Launch the GUI**
   ```bash
   python launch_gui.py
   ```

2. **Paste a URL**
   - Click in the URL box
   - Paste: `https://example.com/myfile.jpg`

3. **Click "Start Download"**
   - Watch the progress bar fill up
   - Wait for completion message

4. **Find your file**
   - Check your Downloads folder
   - File is ready to use!

### Batch Download Multiple Files

1. **Prepare your URLs**
   - Copy all the URLs you want to download

2. **Paste them (one per line)**
   ```
   https://example.com/image1.jpg
   https://example.com/image2.jpg
   https://example.com/document.pdf
   ```

3. **Choose download location** (optional)
   - Click Browse
   - Select a folder

4. **Start Download**
   - All files download with individual progress bars
   - Summary shows when complete

5. **Review Results**
   - Green ✓ = Success
   - Red ✗ = Error

## Common Tasks

### Organize Downloads by Project

1. Create a project folder first
2. In GUI, click **Browse**
3. Navigate to your project folder
4. Select it
5. Download your files - they all go to that folder!

### Download a Large File

Large files work the same way:
- Progress bar shows real-time progress
- Status shows downloaded size vs. total
- Just wait for it to complete!

### Download Multiple Images

Perfect for downloading image galleries:
1. Copy all image URLs
2. Paste them in the URL box (one per line)
3. Click Browse to choose a folder
4. Click Start Download
5. All images download simultaneously!

## Troubleshooting

### "Module not found: customtkinter"

**Problem:** GUI dependencies not installed

**Solution:**
```bash
pip install -r requirements-gui.txt
```

### Window doesn't open

**Check:**
1. Is Python installed? `python --version`
2. Are dependencies installed? `pip list | grep customtkinter`
3. Try running: `python launch_gui.py`
4. Check error messages in terminal

### Downloads fail with "Connection Error"

**Possible causes:**
- No internet connection
- Server is down
- URL is incorrect
- Firewall blocking connection

**Solutions:**
- Check your internet connection
- Try the URL in a web browser first
- Verify the URL is correct
- Check firewall settings

### Files download to wrong location

**Fix:**
1. Check the path in "Save to:" field
2. Click Browse to select correct folder
3. Make sure you have write permissions

### Theme button doesn't work

**This is normal!**
- Click once and wait a moment
- The theme change happens immediately
- All colors will update

## Keyboard Shortcuts

While most operations are mouse-based, you can:

- **Tab** - Navigate between fields
- **Enter** - (in URL box) Move to next line
- **Ctrl+A** - Select all text
- **Ctrl+C / Ctrl+V** - Copy / Paste

## Tips & Best Practices

### For Best Results:

1. **Test one URL first** - Make sure it works before batch downloading
2. **Use descriptive folders** - Organize downloads by project or date
3. **Check file sizes** - Large files take longer
4. **Monitor progress** - Watch for errors and retry if needed
5. **Keep URLs organized** - Save your URL lists in a text file

### Power User Tips:

1. **Prepare URL lists** - Keep text files with URLs for frequent downloads
2. **Create shortcuts** - Make desktop shortcuts to launch_gui.bat/sh
3. **Multiple instances** - You can run multiple GUI windows for parallel operations
4. **Check Downloads folder regularly** - Clean up old files to save space

## FAQ

**Q: Can I pause and resume downloads?**
A: Currently no, but you can cancel by closing the window and restart later.

**Q: Is there a file size limit?**
A: No limit! Download files of any size.

**Q: Can I download from password-protected sites?**
A: No, only publicly accessible URLs are supported.

**Q: Does it work offline?**
A: No, internet connection is required.

**Q: Can I schedule downloads?**
A: Not in GUI. Use the CLI version with cron/Task Scheduler for scheduling.

**Q: How many files can I download at once?**
A: No hard limit, but for best performance, keep it under 50 simultaneous downloads.

## Getting Help

If you encounter issues:

1. Check this guide
2. Read the main README.md
3. Check error messages carefully
4. Try the CLI version: `python downloader.py download <url>`
5. Report bugs on GitHub

## Enjoy!

We hope you enjoy using the File Downloader GUI! It's designed to make downloading files simple and beautiful.

**Happy Downloading! 📥**

---

*For advanced features and automation, check out the CLI version!*
