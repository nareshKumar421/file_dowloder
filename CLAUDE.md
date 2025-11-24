# CLAUDE.md - AI Assistant Guide for File Downloader Project

This document provides comprehensive guidance for AI assistants (like Claude) working on this codebase. It explains the architecture, conventions, and best practices to follow when making modifications.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Codebase Structure](#codebase-structure)
3. [Architecture & Design](#architecture--design)
4. [Key Components](#key-components)
5. [Development Workflow](#development-workflow)
6. [Code Conventions](#code-conventions)
7. [Testing Guidelines](#testing-guidelines)
8. [Common Modification Patterns](#common-modification-patterns)
9. [Dependencies Management](#dependencies-management)
10. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## Project Overview

### Purpose
A professional file downloader with dual interfaces:
- **CLI Version**: Command-line interface using Typer and Rich for automation and power users
- **GUI Version**: Modern graphical interface using CustomTkinter for general users

### Version
- Current: v2.1.0
- CLI: v2.0.0 (in downloader.py)
- GUI: v2.1.0 (Chrome-inspired design)

### Core Functionality
- Download files from HTTP/HTTPS URLs
- Support for any file type (images, videos, documents, archives, etc.)
- Progress tracking with speed and ETA
- Batch/multi-file downloads
- Custom output directory and filenames
- Error handling for network issues
- Theme support (GUI: dark/light)

---

## Codebase Structure

```
file_dowloder/
├── downloader.py              # Main CLI application (Typer + Rich)
├── downloader_gui.py          # GUI application (CustomTkinter)
├── launch_gui.py              # GUI launcher script (cross-platform)
├── launch_gui.sh              # Unix/Linux/Mac launcher
├── launch_gui.bat             # Windows launcher
│
├── requirements.txt           # CLI dependencies (requests, typer, rich)
├── requirements-gui.txt       # GUI dependencies (includes CLI + customtkinter)
│
├── README.md                  # Main documentation
├── TESTING.md                 # CLI testing guide
├── GUI_GUIDE.md               # GUI user guide
├── GUI_TESTING.md             # GUI testing checklist
├── CLAUDE.md                  # This file - AI assistant guide
│
├── test_examples.sh           # Automated test script
├── .gitignore                 # Git ignore rules
└── downloads/                 # Default download directory (gitignored)
```

### File Purposes

| File | Purpose | Lines | Key Features |
|------|---------|-------|--------------|
| `downloader.py` | CLI application | 350 | Typer commands, Rich progress bars, FileDownloader class |
| `downloader_gui.py` | GUI application | 940 | CustomTkinter UI, DownloadTask class, threading |
| `launch_gui.py` | GUI launcher | ~50 | Platform-independent launcher |

---

## Architecture & Design

### CLI Architecture (`downloader.py`)

**Design Pattern**: Command-based CLI with single-responsibility classes

```python
# Structure:
app = typer.Typer()                # Main CLI app
console = Console()                # Rich console for output

class FileDownloader:               # Core download logic
    - __init__(output_dir)
    - get_filename_from_url()
    - get_filename_from_headers()
    - download()                    # Main download method

@app.command()                     # CLI commands
def download(urls, output, directory, force, quiet):
    # Handle multiple URLs
    # Display progress with Rich
    # Show summary table

@app.command()
def version():                     # Version info

@app.command()
def info():                        # Feature info
```

**Key Characteristics**:
- Synchronous downloads (one at a time)
- Rich progress bars with `Progress` context manager
- HTTP requests with streaming
- Proper error handling for network issues
- Exit codes for scripting (0=success, 1=failure)

### GUI Architecture (`downloader_gui.py`)

**Design Pattern**: Event-driven GUI with task-based threading

```python
class DownloadTask:                 # Data class for download state
    - url, output_dir, filename
    - status, progress, speed
    - UI elements (frame, progress_bar, labels)
    - cancelled flag

class ModernFileDownloaderGUI:      # Main application
    def __init__():                 # Setup window and UI
    def setup_ui():                 # Create all UI elements

    # UI Event Handlers
    def start_download():           # Button: Start downloads
    def browse_directory():         # Button: Browse folder
    def toggle_theme():             # Button: Dark/light theme
    def validate_urls():            # Button: Validate URLs
    def clear_urls():               # Button: Clear URL input

    # Download Logic
    def download_files():           # Thread: Download all tasks
    def download_file(task):        # Download single file
    def cancel_download(task):      # Cancel individual download
    def stop_all_downloads():       # Cancel all active downloads

    # UI Updates
    def add_download_item(task):    # Create download card UI
    def update_status(msg, color):  # Update status bar
    def update_stats():             # Update statistics
    def download_complete():        # Handle completion
```

**Key Characteristics**:
- Threading: Downloads run in background thread
- Task-based: Each download is a `DownloadTask` object
- Event-driven: UI updates via `window.after(0, ...)` for thread safety
- State management: Tasks track their own state
- Card-based UI: Each download has its own card with progress
- Theme support: Dark/light mode with CustomTkinter

### Common Patterns Used

1. **Progress Tracking** (both):
   - Chunked downloads (8192 bytes)
   - Progress calculation: `downloaded / file_size`
   - Speed: `downloaded / elapsed_time`

2. **Filename Detection** (both):
   - Priority: Custom name > Content-Disposition header > URL path
   - URL decoding with `unquote()`
   - Fallback: `downloaded_file` or `download_<timestamp>`

3. **Error Handling** (both):
   ```python
   try:
       # Download logic
   except requests.exceptions.HTTPError:
       # HTTP errors (404, 403, etc.)
   except requests.exceptions.ConnectionError:
       # Network errors
   except requests.exceptions.Timeout:
       # Timeout errors
   except KeyboardInterrupt:
       # User cancellation
   except Exception:
       # Catch-all
   ```

4. **Thread Safety** (GUI only):
   ```python
   # Update UI from background thread
   self.window.after(0, widget.configure, {"text": "value"})
   ```

---

## Key Components

### CLI: FileDownloader Class

**Location**: `downloader.py:41-181`

**Purpose**: Core download functionality with progress tracking

**Key Methods**:

```python
def download(url: str, output_filename: Optional[str] = None,
             force: bool = False, chunk_size: int = 8192) -> Optional[Path]:
    """
    Main download method
    Returns: Path to downloaded file or None if failed
    """
    # 1. Send HEAD request to get file info
    # 2. Determine filename (custom, header, or URL)
    # 3. Check if file exists (prompt if not force)
    # 4. Download with Rich progress bar
    # 5. Return path or None
```

**Usage Pattern**:
```python
downloader = FileDownloader(output_dir=Path("downloads"))
result = downloader.download(url, output_filename="custom.jpg", force=True)
if result:
    print(f"Success: {result}")
```

### GUI: DownloadTask Class

**Location**: `downloader_gui.py:33-56`

**Purpose**: Represent a single download with all its state and UI elements

**Attributes**:
```python
# Download data
url: str
output_dir: str
filename: Optional[str]

# State tracking
status: str  # pending, downloading, completed, failed, cancelled
progress: float
file_size: int
downloaded: int
speed: float
cancelled: bool

# UI elements (set by add_download_item)
frame: CTkFrame
url_label: CTkLabel
progress_bar: CTkProgressBar
status_label: CTkLabel
cancel_button: CTkButton
```

**Status Flow**:
```
pending → downloading → completed
                      ↘ failed
                      ↘ cancelled
```

### GUI: ModernFileDownloaderGUI Class

**Location**: `downloader_gui.py:58-926`

**Purpose**: Main application window with Chrome-inspired design

**UI Sections** (setup_ui):
1. **Header** (row 0): Title, icon, theme toggle, about button
2. **URL Input Card** (row 1): Textbox, clear/validate buttons
3. **Output Directory Card** (row 2): Path entry, browse/open buttons
4. **Download Button** (row 3): Large primary action button
5. **Downloads List** (rows 4-5): Header with controls, scrollable list
6. **Status Bar** (row 6): Status icon, message, statistics

**Threading Model**:
- Main thread: UI updates, event handling
- Background thread: Downloads (`download_files` → `download_file`)
- Communication: `window.after(0, ...)` for thread-safe UI updates

---

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/nareshKumar421/file_dowloder.git
cd file_dowloder

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install CLI dependencies only
pip install -r requirements.txt

# Install GUI dependencies (includes CLI)
pip install -r requirements-gui.txt

# Test CLI
python downloader.py --help

# Test GUI
python launch_gui.py
```

### Development Cycle

1. **Make changes** to `downloader.py` or `downloader_gui.py`
2. **Test locally**:
   - CLI: Run commands from TESTING.md
   - GUI: Follow GUI_TESTING.md checklist
3. **Verify dependencies** are correct in requirements files
4. **Update documentation** if adding features
5. **Test cross-platform** if possible

### Git Workflow

**Current Branch**: `claude/claude-md-mid5hhi603buzind-016TFJo7qCp8uBW3js54ERvL`

**Commit Guidelines**:
- Use descriptive commit messages
- Prefix: `Add`, `Update`, `Fix`, `Refactor`, `Upgrade`
- Examples:
  - "Add file validation feature to GUI"
  - "Fix progress bar update lag in CLI"
  - "Upgrade GUI design to Chrome-inspired theme"

**Branch Pattern**: Always work on branches starting with `claude/`

---

## Code Conventions

### Python Style

1. **Imports**: Standard library → Third-party → Local
   ```python
   import os
   import sys
   from pathlib import Path

   import requests
   import typer
   from rich.console import Console
   ```

2. **Type Hints**: Use consistently
   ```python
   def download(self, url: str, output_filename: Optional[str] = None) -> Optional[Path]:
   ```

3. **Docstrings**: Use for classes and public methods
   ```python
   def download(self, url: str) -> Optional[Path]:
       """
       Download a file from the given URL with progress bar

       Args:
           url: URL to download from

       Returns:
           Path to downloaded file or None if failed
       """
   ```

4. **Error Messages**: Use Rich/CustomTkinter formatting
   ```python
   # CLI
   console.print("[bold red]✗ Error:[/bold red] Message", style="red")

   # GUI
   messagebox.showerror("Error Title", "Error message")
   ```

### Naming Conventions

- **Classes**: `PascalCase` (FileDownloader, DownloadTask)
- **Functions/Methods**: `snake_case` (download_file, update_status)
- **Variables**: `snake_case` (output_dir, file_size)
- **Constants**: `UPPER_SNAKE_CASE` (__version__ = "2.0.0")
- **Private**: Prefix with `_` (not used much in this codebase)

### CLI-Specific Conventions

1. **Console Output**: Always use Rich
   ```python
   console.print("[cyan]Info message[/cyan]")
   console.print("[green]Success message[/green]")
   console.print("[red]Error message[/red]")
   ```

2. **Progress Bars**: Use Rich Progress
   ```python
   with Progress(
       SpinnerColumn(),
       TextColumn("[bold blue]{task.description}"),
       BarColumn(),
       DownloadColumn(),
       TransferSpeedColumn(),
       TimeRemainingColumn(),
   ) as progress:
       task = progress.add_task("filename", total=file_size)
       # Update with: progress.update(task, advance=len(chunk))
   ```

3. **Exit Codes**:
   ```python
   raise typer.Exit(0)  # Success
   raise typer.Exit(1)  # Failure
   ```

### GUI-Specific Conventions

1. **Widget Naming**: Use descriptive names with type
   ```python
   self.url_entry = ctk.CTkTextbox(...)
   self.download_button = ctk.CTkButton(...)
   self.status_label = ctk.CTkLabel(...)
   ```

2. **Colors**: Use theme-aware tuples
   ```python
   fg_color=("gray95", "gray10")  # (light mode, dark mode)
   text_color=("gray20", "gray80")
   ```

3. **Thread-Safe Updates**: Always use `window.after`
   ```python
   # WRONG:
   widget.configure(text="Updated")

   # CORRECT:
   self.window.after(0, widget.configure, {"text": "Updated"})
   ```

4. **Layout**: Use grid with proper weights
   ```python
   widget.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
   container.grid_columnconfigure(0, weight=1)  # Make expandable
   ```

### Common Patterns to Follow

1. **Filename Extraction**:
   ```python
   # Always follow this priority:
   if custom_filename:
       filename = custom_filename
   else:
       filename = self.get_filename_from_headers(response)
       if not filename:
           filename = self.get_filename_from_url(url)
   ```

2. **Download Loop**:
   ```python
   with open(output_path, 'wb') as file:
       for chunk in response.iter_content(chunk_size=8192):
           if chunk:  # Filter out keep-alive chunks
               file.write(chunk)
               downloaded += len(chunk)
               # Update progress
   ```

3. **Status Updates** (GUI):
   ```python
   # Use status label + status icon
   self.update_status("Message text", "color")  # green, red, blue, orange, gray
   ```

---

## Testing Guidelines

### CLI Testing

**Quick Test**:
```bash
# Basic functionality
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Multiple files
python downloader.py download URL1 URL2 URL3

# With options
python downloader.py download URL -o custom.txt -d ~/Downloads -f
```

**Test Checklist**:
- [ ] Single file download
- [ ] Multiple file download
- [ ] Custom filename (-o)
- [ ] Custom directory (-d)
- [ ] Force overwrite (-f)
- [ ] Quiet mode (-q)
- [ ] Error handling (404, network error)
- [ ] Progress bar display
- [ ] Summary table (multiple files)

See `TESTING.md` for complete test suite.

### GUI Testing

**Quick Test**:
```bash
python launch_gui.py
# 1. Paste a URL
# 2. Click Start Download
# 3. Verify progress updates
# 4. Check downloaded file
```

**Test Checklist**:
- [ ] URL input and validation
- [ ] Browse directory
- [ ] Theme toggle
- [ ] Single download
- [ ] Multiple downloads
- [ ] Progress tracking
- [ ] Cancel download
- [ ] Error handling
- [ ] Status updates
- [ ] Statistics counter

See `GUI_TESTING.md` for complete test suite.

### Automated Testing

Run the test script:
```bash
chmod +x test_examples.sh
./test_examples.sh
```

---

## Common Modification Patterns

### Adding a New CLI Command

```python
@app.command()
def new_command(
    arg1: str = typer.Argument(..., help="Description"),
    option1: bool = typer.Option(False, "--flag", "-f", help="Description")
):
    """Command description shown in --help"""
    # Implementation
    console.print("[cyan]Command output[/cyan]")
```

### Adding a GUI Feature

1. **Add UI element** in `setup_ui()`:
   ```python
   self.new_button = ctk.CTkButton(
       parent,
       text="New Feature",
       command=self.handle_new_feature
   )
   self.new_button.grid(row=X, column=Y, padx=10, pady=5)
   ```

2. **Add handler method**:
   ```python
   def handle_new_feature(self):
       """Handle new feature button click"""
       # Implementation
       self.update_status("Feature executed", "green")
   ```

3. **Add to task if download-related**:
   ```python
   # In DownloadTask class
   self.new_attribute = initial_value
   ```

### Modifying Download Logic

**CLI**: Modify `FileDownloader.download()` method at line 68-181

**GUI**: Modify `download_file(task)` method at line 780-899

**Common Changes**:
- Chunk size: Change `chunk_size=8192` parameter
- Headers: Add to `requests.head()` or `requests.get()` calls
- Timeout: Modify `timeout=10` or `timeout=30` parameters
- Retry logic: Add try/except with retry counter

### Adding Error Handling

```python
try:
    # Download code
except requests.exceptions.SpecificError as e:
    # CLI:
    console.print(f"[bold red]✗ Error:[/bold red] {e}")
    return None

    # GUI:
    error_text = f"✗ Error: {str(e)}"
    self.window.after(0, task.status_label.configure, {
        "text": error_text,
        "text_color": ("red", "lightcoral")
    })
    task.status = "failed"
    return False
```

### Updating Version

1. **Update version strings**:
   ```python
   # downloader.py
   __version__ = "2.1.0"

   # downloader_gui.py (in show_about)
   "File Downloader v2.1.0\n\n"
   ```

2. **Update README.md** changelog section

3. **Test both interfaces**

---

## Dependencies Management

### Current Dependencies

**CLI** (`requirements.txt`):
```
requests>=2.31.0    # HTTP library
typer>=0.9.0       # CLI framework
rich>=13.0.0       # Terminal formatting
```

**GUI** (`requirements-gui.txt`):
```
-r requirements.txt          # Include CLI deps
customtkinter>=5.2.0        # Modern GUI framework
```

### Adding Dependencies

1. **Install and test locally**:
   ```bash
   pip install new-package
   # Test functionality
   ```

2. **Add to appropriate requirements file**:
   - CLI feature → `requirements.txt`
   - GUI feature → `requirements-gui.txt`
   - Both → `requirements.txt`

3. **Use version pinning**:
   ```
   package>=1.0.0    # Minimum version (preferred)
   package==1.0.0    # Exact version (only if necessary)
   ```

4. **Update README if needed**

### Dependency Guidelines

- Keep dependencies minimal
- Use well-maintained packages
- Consider compatibility (Python 3.7+)
- Document why each dependency is needed

---

## AI Assistant Guidelines

### When Working on This Codebase

1. **Always Read First**:
   - Read the specific file before modifying
   - Check related documentation
   - Understand the context

2. **Maintain Consistency**:
   - Follow existing code style
   - Use the same patterns as existing code
   - Keep similar formatting

3. **Test Changes**:
   - Provide test commands
   - Consider edge cases
   - Test both success and failure paths

4. **Update Documentation**:
   - Update README.md if adding features
   - Update TESTING.md if adding test cases
   - Update this file (CLAUDE.md) if changing architecture

5. **Be Conservative**:
   - Don't over-engineer simple features
   - Don't add features that weren't requested
   - Don't refactor working code unless necessary

### Common Pitfalls to Avoid

1. **Threading Issues** (GUI):
   - ❌ Never update UI directly from background thread
   - ✅ Always use `window.after(0, ...)`

2. **Resource Leaks**:
   - ❌ Opening files without context managers
   - ✅ Use `with open(...) as file:`

3. **Error Handling**:
   - ❌ Bare `except:` clauses
   - ✅ Specific exception types

4. **Path Handling**:
   - ❌ String concatenation for paths
   - ✅ Use `Path()` from pathlib

5. **URL Handling**:
   - ❌ Forgetting to decode URLs
   - ✅ Use `unquote()` from urllib.parse

### Questions to Ask

Before modifying code, consider:

1. **What is the scope?**
   - CLI only, GUI only, or both?
   - Does it affect existing functionality?

2. **What are the dependencies?**
   - Do I need new packages?
   - Are there version conflicts?

3. **How to test?**
   - What test cases are needed?
   - Can users verify the change?

4. **Is it documented?**
   - Does README need updates?
   - Are code comments needed?

5. **Is it backwards compatible?**
   - Will existing commands still work?
   - Are there breaking changes?

### Helpful Commands for AI Assistants

```bash
# Check Python version
python --version

# List installed packages
pip list

# Test CLI help
python downloader.py --help

# Quick CLI test
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Launch GUI test
python launch_gui.py

# Check for syntax errors
python -m py_compile downloader.py
python -m py_compile downloader_gui.py

# Find todos
grep -r "TODO" *.py

# Count lines of code
wc -l *.py
```

---

## Quick Reference

### File Sizes
- `downloader.py`: ~350 lines
- `downloader_gui.py`: ~940 lines
- Total Python code: ~1,300 lines

### Key Line Numbers

**downloader.py**:
- FileDownloader class: 41-181
- download command: 184-292
- version command: 295-306
- info command: 309-340

**downloader_gui.py**:
- DownloadTask class: 33-56
- ModernFileDownloaderGUI class: 58-926
- setup_ui method: 97-431
- download_file method: 780-899

### External Resources

- **Typer docs**: https://typer.tiangolo.com/
- **Rich docs**: https://rich.readthedocs.io/
- **CustomTkinter docs**: https://customtkinter.tomschimansky.com/
- **Requests docs**: https://requests.readthedocs.io/

---

## Summary

This is a well-structured dual-interface file downloader:
- **CLI** for automation and power users
- **GUI** for general users with visual feedback
- Clean separation between interfaces
- Consistent error handling
- Good documentation

**Core Principle**: Keep it simple, maintainable, and user-friendly.

---

*Last Updated: 2025-11-24*
*For Repository: nareshKumar421/file_dowloder*
*AI Assistant: Claude (Anthropic)*
