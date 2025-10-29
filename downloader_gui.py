#!/usr/bin/env python3
"""
File Downloader - Modern GUI Application
A beautiful, Chrome-inspired GUI for downloading files from URLs
Built with CustomTkinter for a modern, professional look
"""

import os
import sys
import threading
import time
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlparse, unquote
from datetime import datetime
import re

try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
    import requests
except ImportError as e:
    print(f"Error: Required module not installed: {e}")
    print("Please install dependencies: pip install -r requirements-gui.txt")
    sys.exit(1)


# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Default to dark mode
ctk.set_default_color_theme("blue")


class DownloadTask:
    """Represents a single download task with all its properties"""

    def __init__(self, url: str, output_dir: str, filename: Optional[str] = None):
        self.url = url
        self.output_dir = output_dir
        self.filename = filename
        self.status = "pending"  # pending, downloading, completed, failed, cancelled
        self.progress = 0.0
        self.file_size = 0
        self.downloaded = 0
        self.error_message = ""
        self.start_time = None
        self.end_time = None
        self.speed = 0.0
        self.cancelled = False

        # UI elements (set later)
        self.frame = None
        self.url_label = None
        self.progress_bar = None
        self.status_label = None
        self.cancel_button = None


class ModernFileDownloaderGUI:
    """Modern, Chrome-inspired GUI Application"""

    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("File Downloader")
        self.window.geometry("1000x750")
        self.window.minsize(900, 650)

        # Variables
        self.download_tasks: List[DownloadTask] = []
        self.is_downloading = False
        self.output_directory = str(Path.home() / "Downloads")
        self.current_theme = "dark"
        self.download_count = 0
        self.successful_downloads = 0
        self.failed_downloads = 0

        # Setup UI
        self.setup_ui()

        # Center window on screen
        self.center_window()

        # Set icon if available
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass

    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Setup the modern Chrome-like user interface"""

        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(3, weight=1)

        # ==================== HEADER / TITLE BAR ====================
        header_frame = ctk.CTkFrame(
            self.window,
            corner_radius=0,
            fg_color=("gray95", "gray10"),
            height=70
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)

        # Logo/Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text="📥",
            font=ctk.CTkFont(size=32)
        )
        icon_label.grid(row=0, column=0, padx=(30, 15), pady=15)

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="File Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=1, sticky="w", pady=15)

        # Header buttons frame
        header_buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_buttons_frame.grid(row=0, column=2, padx=20, pady=15)

        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            header_buttons_frame,
            text="☀️ Light",
            width=90,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self.toggle_theme,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        self.theme_button.pack(side="left", padx=5)

        # About button
        about_button = ctk.CTkButton(
            header_buttons_frame,
            text="ℹ️ About",
            width=90,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self.show_about,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        about_button.pack(side="left", padx=5)

        # ==================== URL INPUT SECTION ====================
        input_container = ctk.CTkFrame(self.window, fg_color="transparent")
        input_container.grid(row=1, column=0, sticky="ew", padx=25, pady=(20, 10))
        input_container.grid_columnconfigure(0, weight=1)

        # URL Input Card
        url_card = ctk.CTkFrame(input_container, corner_radius=12)
        url_card.grid(row=0, column=0, sticky="ew")
        url_card.grid_columnconfigure(0, weight=1)

        # URL Label with helper text
        url_header_frame = ctk.CTkFrame(url_card, fg_color="transparent")
        url_header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 5))
        url_header_frame.grid_columnconfigure(1, weight=1)

        url_label = ctk.CTkLabel(
            url_header_frame,
            text="Enter URLs",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        url_label.grid(row=0, column=0, sticky="w")

        helper_label = ctk.CTkLabel(
            url_header_frame,
            text="One URL per line • Supports HTTP/HTTPS",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="e"
        )
        helper_label.grid(row=0, column=1, sticky="e")

        # URL Entry with custom styling
        self.url_entry = ctk.CTkTextbox(
            url_card,
            height=120,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        self.url_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.url_entry.insert("1.0", "https://example.com/file.jpg\nhttps://example.com/image.png")
        self.url_entry.bind("<FocusIn>", self.on_url_focus)
        self.url_entry.bind("<FocusOut>", self.on_url_unfocus)

        # URL Action Buttons
        url_actions_frame = ctk.CTkFrame(url_card, fg_color="transparent")
        url_actions_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))

        clear_button = ctk.CTkButton(
            url_actions_frame,
            text="🗑️ Clear",
            width=100,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self.clear_urls,
            fg_color="transparent",
            border_width=1.5,
            border_color=("gray60", "gray40"),
            text_color=("gray20", "gray80")
        )
        clear_button.pack(side="left", padx=(0, 5))

        validate_button = ctk.CTkButton(
            url_actions_frame,
            text="✓ Validate URLs",
            width=120,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self.validate_urls,
            fg_color="transparent",
            border_width=1.5,
            border_color=("gray60", "gray40"),
            text_color=("gray20", "gray80")
        )
        validate_button.pack(side="left")

        # ==================== OUTPUT DIRECTORY SECTION ====================
        dir_container = ctk.CTkFrame(self.window, fg_color="transparent")
        dir_container.grid(row=2, column=0, sticky="ew", padx=25, pady=(10, 15))
        dir_container.grid_columnconfigure(0, weight=1)

        dir_card = ctk.CTkFrame(dir_container, corner_radius=12)
        dir_card.grid(row=0, column=0, sticky="ew")
        dir_card.grid_columnconfigure(1, weight=1)

        dir_icon = ctk.CTkLabel(
            dir_card,
            text="📁",
            font=ctk.CTkFont(size=20)
        )
        dir_icon.grid(row=0, column=0, padx=(20, 10), pady=15)

        dir_label = ctk.CTkLabel(
            dir_card,
            text="Save to:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        dir_label.grid(row=0, column=1, sticky="w", pady=15)

        self.dir_entry = ctk.CTkEntry(
            dir_card,
            placeholder_text="Output directory",
            font=ctk.CTkFont(size=13),
            height=38,
            corner_radius=8,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        self.dir_entry.grid(row=0, column=2, sticky="ew", padx=15, pady=15)
        self.dir_entry.insert(0, self.output_directory)

        browse_button = ctk.CTkButton(
            dir_card,
            text="Browse",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.browse_directory,
            corner_radius=8
        )
        browse_button.grid(row=0, column=3, padx=(0, 15), pady=15)

        open_folder_button = ctk.CTkButton(
            dir_card,
            text="📂 Open",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.open_download_folder,
            corner_radius=8,
            fg_color="transparent",
            border_width=1.5,
            text_color=("gray20", "gray80")
        )
        open_folder_button.grid(row=0, column=4, padx=(0, 20), pady=15)

        # ==================== DOWNLOAD BUTTON ====================
        self.download_button = ctk.CTkButton(
            self.window,
            text="⬇ Start Download",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            corner_radius=10,
            command=self.start_download,
            fg_color=("#1f6aa5", "#144870"),
            hover_color=("#1557a0", "#0d3a5a")
        )
        self.download_button.grid(row=3, column=0, sticky="ew", padx=25, pady=(0, 15))

        # ==================== DOWNLOADS LIST HEADER ====================
        list_header_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        list_header_frame.grid(row=4, column=0, sticky="ew", padx=25, pady=(10, 5))
        list_header_frame.grid_columnconfigure(1, weight=1)

        list_label = ctk.CTkLabel(
            list_header_frame,
            text="Downloads",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        list_label.pack(side="left")

        # Control buttons
        controls_frame = ctk.CTkFrame(list_header_frame, fg_color="transparent")
        controls_frame.pack(side="right")

        self.stop_all_button = ctk.CTkButton(
            controls_frame,
            text="⏸ Stop All",
            width=90,
            height=28,
            font=ctk.CTkFont(size=11),
            command=self.stop_all_downloads,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray80"),
            state="disabled"
        )
        self.stop_all_button.pack(side="left", padx=5)

        self.clear_list_button = ctk.CTkButton(
            controls_frame,
            text="🗑 Clear List",
            width=90,
            height=28,
            font=ctk.CTkFont(size=11),
            command=self.clear_completed,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray80")
        )
        self.clear_list_button.pack(side="left")

        # ==================== DOWNLOADS LIST ====================
        # Scrollable frame for download items
        self.downloads_frame = ctk.CTkScrollableFrame(
            self.window,
            corner_radius=12,
            fg_color=("gray95", "gray10")
        )
        self.downloads_frame.grid(row=5, column=0, sticky="nsew", padx=25, pady=(5, 15))
        self.downloads_frame.grid_columnconfigure(0, weight=1)

        # Empty state
        self.empty_state_frame = ctk.CTkFrame(
            self.downloads_frame,
            fg_color="transparent"
        )
        self.empty_state_frame.grid(row=0, column=0, pady=80)

        empty_icon = ctk.CTkLabel(
            self.empty_state_frame,
            text="📥",
            font=ctk.CTkFont(size=48)
        )
        empty_icon.pack(pady=(0, 10))

        self.empty_label = ctk.CTkLabel(
            self.empty_state_frame,
            text="No downloads yet",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        self.empty_label.pack()

        empty_hint = ctk.CTkLabel(
            self.empty_state_frame,
            text="Add URLs above and click 'Start Download' to begin",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        empty_hint.pack()

        # ==================== STATUS BAR ====================
        status_frame = ctk.CTkFrame(
            self.window,
            corner_radius=0,
            height=45,
            fg_color=("gray92", "gray15")
        )
        status_frame.grid(row=6, column=0, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_propagate(False)

        # Status icon
        self.status_icon = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=16),
            text_color=("green", "lightgreen")
        )
        self.status_icon.grid(row=0, column=0, padx=(20, 5), pady=12)

        # Status text
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=1, sticky="w", pady=12)

        # Stats
        self.stats_label = ctk.CTkLabel(
            status_frame,
            text="Total: 0 • Success: 0 • Failed: 0",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.stats_label.grid(row=0, column=2, padx=20, pady=12)

    def on_url_focus(self, event):
        """Handle URL entry focus"""
        current_text = self.url_entry.get("1.0", "end-1c")
        if "https://example.com" in current_text:
            self.url_entry.delete("1.0", "end")

    def on_url_unfocus(self, event):
        """Handle URL entry unfocus"""
        pass

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙 Dark")
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀️ Light")
            self.current_theme = "dark"

    def show_about(self):
        """Show about dialog"""
        about_text = (
            "File Downloader v2.1.0\n\n"
            "A beautiful, modern file downloader\n"
            "with Chrome-inspired design.\n\n"
            "Built with CustomTkinter and Python\n\n"
            "Features:\n"
            "• Multi-URL batch downloads\n"
            "• Real-time progress tracking\n"
            "• Dark/Light themes\n"
            "• Modern, intuitive interface\n\n"
            "© 2024 File Downloader"
        )
        messagebox.showinfo("About File Downloader", about_text)

    def clear_urls(self):
        """Clear all URLs from the text box"""
        self.url_entry.delete("1.0", "end")
        self.update_status("URLs cleared", "gray")

    def validate_urls(self):
        """Validate entered URLs"""
        urls_text = self.url_entry.get("1.0", "end-1c").strip()
        if not urls_text:
            messagebox.showwarning("No URLs", "Please enter at least one URL.")
            return

        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

        valid_urls = []
        invalid_urls = []

        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        for url in urls:
            if url_pattern.match(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)

        if invalid_urls:
            message = f"Found {len(invalid_urls)} invalid URL(s):\n\n"
            message += "\n".join(invalid_urls[:5])
            if len(invalid_urls) > 5:
                message += f"\n... and {len(invalid_urls) - 5} more"
            messagebox.showwarning("Invalid URLs", message)

        if valid_urls:
            message = f"✓ All {len(valid_urls)} URL(s) are valid!"
            messagebox.showinfo("Validation Complete", message)

        self.update_status(f"Validated: {len(valid_urls)} valid, {len(invalid_urls)} invalid", "blue")

    def browse_directory(self):
        """Open directory browser"""
        directory = filedialog.askdirectory(
            initialdir=self.output_directory,
            title="Select Download Directory"
        )
        if directory:
            self.output_directory = directory
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, directory)
            self.update_status(f"Output directory: {directory}", "blue")

    def open_download_folder(self):
        """Open the downloads folder"""
        output_dir = self.dir_entry.get().strip() or self.output_directory
        if os.path.exists(output_dir):
            import platform
            if platform.system() == "Windows":
                os.startfile(output_dir)
            elif platform.system() == "Darwin":  # macOS
                os.system(f'open "{output_dir}"')
            else:  # Linux
                os.system(f'xdg-open "{output_dir}"')
        else:
            messagebox.showwarning("Folder Not Found", f"The folder does not exist:\n{output_dir}")

    def get_filename_from_url(self, url: str) -> str:
        """Extract filename from URL"""
        parsed_url = urlparse(url)
        filename = unquote(os.path.basename(parsed_url.path))
        if not filename or filename == "/" or filename == "":
            # Generate filename from timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"download_{timestamp}"
        return filename

    def update_status(self, message: str, color: str = "gray"):
        """Update status bar"""
        self.status_label.configure(text=message)
        color_map = {
            "green": ("green", "lightgreen"),
            "red": ("red", "lightcoral"),
            "blue": ("blue", "lightblue"),
            "orange": ("orange", "lightyellow"),
            "gray": ("gray50", "gray60")
        }
        self.status_icon.configure(text_color=color_map.get(color, color_map["gray"]))

    def update_stats(self):
        """Update statistics in status bar"""
        stats_text = f"Total: {self.download_count} • Success: {self.successful_downloads} • Failed: {self.failed_downloads}"
        self.stats_label.configure(text=stats_text)

    def start_download(self):
        """Start downloading files"""
        # Get URLs from text box
        urls_text = self.url_entry.get("1.0", "end-1c").strip()

        if not urls_text:
            messagebox.showwarning("No URLs", "Please enter at least one URL to download.")
            return

        # Parse URLs
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

        if not urls:
            messagebox.showwarning("No URLs", "Please enter at least one valid URL.")
            return

        # Get output directory
        output_dir = self.dir_entry.get().strip()
        if not output_dir:
            output_dir = self.output_directory

        # Create output directory if it doesn't exist
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Directory Error", f"Cannot create directory:\n{str(e)}")
            return

        # Remove empty state
        if hasattr(self, 'empty_state_frame'):
            self.empty_state_frame.destroy()

        # Create download tasks
        for url in urls:
            task = DownloadTask(url, output_dir)
            self.download_tasks.append(task)
            self.add_download_item(task)
            self.download_count += 1

        # Update UI
        self.download_button.configure(
            state="disabled",
            text="⏳ Downloading...",
            fg_color="gray"
        )
        self.stop_all_button.configure(state="normal")
        self.is_downloading = True

        # Update status
        self.update_status(f"Downloading {len(urls)} file(s)...", "blue")
        self.update_stats()

        # Start downloads in separate thread
        threading.Thread(target=self.download_files, daemon=True).start()

    def add_download_item(self, task: DownloadTask):
        """Add a download item to the list with modern styling"""
        # Create card for this download
        item_card = ctk.CTkFrame(
            self.downloads_frame,
            corner_radius=10,
            fg_color=("white", "gray20")
        )
        item_card.grid(sticky="ew", padx=8, pady=6)
        item_card.grid_columnconfigure(1, weight=1)
        task.frame = item_card

        # File icon
        file_icon = ctk.CTkLabel(
            item_card,
            text="📄",
            font=ctk.CTkFont(size=20)
        )
        file_icon.grid(row=0, column=0, rowspan=3, padx=(15, 10), pady=15)

        # URL label (truncated)
        url_display = task.url if len(task.url) <= 70 else task.url[:67] + "..."
        url_label = ctk.CTkLabel(
            item_card,
            text=url_display,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        url_label.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(15, 2))
        task.url_label = url_label

        # Progress container
        progress_container = ctk.CTkFrame(item_card, fg_color="transparent")
        progress_container.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=5)
        progress_container.grid_columnconfigure(0, weight=1)

        # Progress bar with custom styling
        progress_bar = ctk.CTkProgressBar(
            progress_container,
            mode="determinate",
            height=8,
            corner_radius=4
        )
        progress_bar.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        progress_bar.set(0)
        task.progress_bar = progress_bar

        # Progress percentage
        progress_label = ctk.CTkLabel(
            progress_container,
            text="0%",
            font=ctk.CTkFont(size=11),
            width=40
        )
        progress_label.grid(row=0, column=1)
        task.progress_label = progress_label

        # Status label
        status_label = ctk.CTkLabel(
            item_card,
            text="⏳ Waiting...",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        status_label.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=(2, 15))
        task.status_label = status_label

        # Cancel button
        cancel_button = ctk.CTkButton(
            item_card,
            text="✕",
            width=30,
            height=30,
            corner_radius=6,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray80", "gray25"),
            text_color=("gray40", "gray60"),
            command=lambda: self.cancel_download(task)
        )
        cancel_button.grid(row=0, column=2, rowspan=3, padx=(5, 15), pady=15)
        task.cancel_button = cancel_button

    def cancel_download(self, task: DownloadTask):
        """Cancel a specific download"""
        task.cancelled = True
        task.status = "cancelled"
        self.window.after(0, task.status_label.configure, {"text": "✕ Cancelled", "text_color": "orange"})
        self.window.after(0, task.cancel_button.configure, {"state": "disabled"})
        self.failed_downloads += 1
        self.update_stats()

    def stop_all_downloads(self):
        """Stop all active downloads"""
        for task in self.download_tasks:
            if task.status == "downloading" or task.status == "pending":
                task.cancelled = True
                task.status = "cancelled"
        self.update_status("Stopping all downloads...", "orange")

    def clear_completed(self):
        """Clear completed/failed downloads from the list"""
        tasks_to_remove = [task for task in self.download_tasks if task.status in ["completed", "failed", "cancelled"]]

        if not tasks_to_remove:
            messagebox.showinfo("Nothing to Clear", "No completed or failed downloads to clear.")
            return

        for task in tasks_to_remove:
            if hasattr(task, 'frame') and task.frame:
                task.frame.destroy()
            self.download_tasks.remove(task)

        # Show empty state if no tasks left
        if not self.download_tasks:
            self.show_empty_state()

        self.update_status(f"Cleared {len(tasks_to_remove)} item(s)", "gray")

    def show_empty_state(self):
        """Show empty state when no downloads"""
        self.empty_state_frame = ctk.CTkFrame(
            self.downloads_frame,
            fg_color="transparent"
        )
        self.empty_state_frame.grid(row=0, column=0, pady=80)

        empty_icon = ctk.CTkLabel(
            self.empty_state_frame,
            text="📥",
            font=ctk.CTkFont(size=48)
        )
        empty_icon.pack(pady=(0, 10))

        self.empty_label = ctk.CTkLabel(
            self.empty_state_frame,
            text="No downloads",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        self.empty_label.pack()

    def download_files(self):
        """Download all files in tasks"""
        for task in self.download_tasks:
            if task.cancelled:
                continue

            if self.download_file(task):
                self.successful_downloads += 1
            else:
                if not task.cancelled:
                    self.failed_downloads += 1

        # Update UI when done
        self.window.after(0, self.download_complete)

    def download_file(self, task: DownloadTask) -> bool:
        """Download a single file with detailed progress"""
        if task.cancelled:
            return False

        try:
            task.start_time = time.time()
            task.status = "downloading"

            # Update status
            self.window.after(0, task.status_label.configure, {
                "text": "🔍 Connecting...",
                "text_color": ("blue", "lightblue")
            })

            # Get file info
            head_response = requests.head(task.url, allow_redirects=True, timeout=10)
            head_response.raise_for_status()

            file_size = int(head_response.headers.get('content-length', 0))
            task.file_size = file_size

            # Get filename
            filename = task.filename or self.get_filename_from_url(task.url)
            output_path = Path(task.output_dir) / filename

            # Check if cancelled
            if task.cancelled:
                return False

            # Update status
            self.window.after(0, task.url_label.configure, {"text": filename})
            self.window.after(0, task.status_label.configure, {
                "text": "⬇ Downloading...",
                "text_color": ("blue", "lightblue")
            })

            # Download file
            response = requests.get(task.url, stream=True, timeout=30)
            response.raise_for_status()

            downloaded = 0
            last_update_time = time.time()

            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if task.cancelled:
                        file.close()
                        output_path.unlink(missing_ok=True)
                        return False

                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        task.downloaded = downloaded

                        # Update progress (throttle updates)
                        current_time = time.time()
                        if current_time - last_update_time >= 0.1 or downloaded >= file_size:  # Update every 100ms
                            last_update_time = current_time

                            if file_size > 0:
                                progress = downloaded / file_size
                                task.progress = progress

                                # Calculate speed
                                elapsed = current_time - task.start_time
                                speed = downloaded / elapsed if elapsed > 0 else 0

                                # Format status text
                                downloaded_mb = downloaded / (1024 * 1024)
                                total_mb = file_size / (1024 * 1024)
                                speed_mb = speed / (1024 * 1024)
                                percent = int(progress * 100)

                                status_text = f"⬇ {downloaded_mb:.1f} MB / {total_mb:.1f} MB • {speed_mb:.1f} MB/s"

                                # Update UI
                                self.window.after(0, task.progress_bar.set, progress)
                                self.window.after(0, task.progress_label.configure, {"text": f"{percent}%"})
                                self.window.after(0, task.status_label.configure, {"text": status_text})

            # Success
            task.end_time = time.time()
            task.status = "completed"
            elapsed_total = task.end_time - task.start_time
            file_size_mb = output_path.stat().st_size / (1024 * 1024)

            success_text = f"✓ Complete • {file_size_mb:.2f} MB • {elapsed_total:.1f}s"

            self.window.after(0, task.status_label.configure, {
                "text": success_text,
                "text_color": ("green", "lightgreen")
            })
            self.window.after(0, task.progress_bar.set, 1.0)
            self.window.after(0, task.progress_label.configure, {"text": "100%"})
            self.window.after(0, task.cancel_button.configure, {"state": "disabled", "text": "✓"})

            return True

        except requests.exceptions.HTTPError as e:
            error_text = f"✗ HTTP Error: {e.response.status_code if hasattr(e, 'response') else 'Unknown'}"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": ("red", "lightcoral")})
            task.status = "failed"
            return False
        except requests.exceptions.ConnectionError:
            error_text = "✗ Connection failed"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": ("red", "lightcoral")})
            task.status = "failed"
            return False
        except requests.exceptions.Timeout:
            error_text = "✗ Timeout"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": ("red", "lightcoral")})
            task.status = "failed"
            return False
        except Exception as e:
            error_text = f"✗ Error: {str(e)[:50]}"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": ("red", "lightcoral")})
            task.status = "failed"
            return False

    def download_complete(self):
        """Called when all downloads are complete"""
        self.is_downloading = False
        self.download_button.configure(
            state="normal",
            text="⬇ Start Download",
            fg_color=("#1f6aa5", "#144870")
        )
        self.stop_all_button.configure(state="disabled")

        # Update status
        if self.failed_downloads == 0:
            status_text = f"✓ All {self.successful_downloads} file(s) downloaded successfully!"
            self.update_status(status_text, "green")
            messagebox.showinfo("Download Complete", status_text)
        else:
            status_text = f"Download complete: {self.successful_downloads} succeeded, {self.failed_downloads} failed"
            self.update_status(status_text, "orange")
            messagebox.showwarning("Download Complete", status_text)

        self.update_stats()

    def run(self):
        """Run the application"""
        self.window.mainloop()


def main():
    """Main entry point for GUI application"""
    try:
        app = ModernFileDownloaderGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
