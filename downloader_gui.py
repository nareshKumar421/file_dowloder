#!/usr/bin/env python3
"""
File Downloader GUI Application
A beautiful, minimal, and professional GUI for downloading files from URLs
Built with CustomTkinter for a modern look and feel
"""

import os
import sys
import threading
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, unquote
import requests

try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
except ImportError:
    print("Error: CustomTkinter is not installed.")
    print("Please install it using: pip install customtkinter")
    sys.exit(1)


# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class DownloadTask:
    """Represents a single download task"""

    def __init__(self, url: str, output_dir: str, filename: Optional[str] = None):
        self.url = url
        self.output_dir = output_dir
        self.filename = filename
        self.status = "pending"  # pending, downloading, completed, failed
        self.progress = 0.0
        self.file_size = 0
        self.downloaded = 0
        self.error_message = ""


class FileDownloaderGUI:
    """Main GUI Application"""

    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("File Downloader")
        self.window.geometry("900x700")
        self.window.minsize(800, 600)

        # Variables
        self.download_tasks = []
        self.is_downloading = False
        self.output_directory = str(Path.home() / "Downloads")

        # Setup UI
        self.setup_ui()

        # Center window on screen
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Setup the user interface"""

        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

        # ==================== HEADER ====================
        header_frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="📥 File Downloader",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(side="left")

        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            header_frame,
            text="🌙 Dark",
            width=100,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=10)

        # ==================== URL INPUT SECTION ====================
        input_frame = ctk.CTkFrame(self.window)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        # URL Entry
        url_label = ctk.CTkLabel(input_frame, text="Enter URL(s):", font=ctk.CTkFont(size=14))
        url_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        self.url_entry = ctk.CTkTextbox(input_frame, height=100, font=ctk.CTkFont(size=12))
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        self.url_entry.insert("1.0", "Paste URLs here (one per line)...")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)

        # Output Directory
        dir_label = ctk.CTkLabel(input_frame, text="Save to:", font=ctk.CTkFont(size=14))
        dir_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))

        dir_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        dir_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        dir_frame.grid_columnconfigure(0, weight=1)

        self.dir_entry = ctk.CTkEntry(
            dir_frame,
            placeholder_text="Output directory",
            font=ctk.CTkFont(size=12)
        )
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.dir_entry.insert(0, self.output_directory)

        browse_button = ctk.CTkButton(
            dir_frame,
            text="Browse",
            width=100,
            command=self.browse_directory
        )
        browse_button.grid(row=0, column=1)

        # Download Button
        self.download_button = ctk.CTkButton(
            input_frame,
            text="⬇ Start Download",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.start_download
        )
        self.download_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 20))

        # ==================== DOWNLOADS LIST ====================
        list_label = ctk.CTkLabel(self.window, text="Downloads:", font=ctk.CTkFont(size=14))
        list_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))

        # Scrollable frame for download items
        self.downloads_frame = ctk.CTkScrollableFrame(
            self.window,
            label_text="",
            corner_radius=10
        )
        self.downloads_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 10))
        self.downloads_frame.grid_columnconfigure(0, weight=1)

        # Initial message
        self.empty_label = ctk.CTkLabel(
            self.downloads_frame,
            text="No downloads yet. Add URLs above to get started!",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.empty_label.grid(row=0, column=0, pady=50)

        # ==================== STATUS BAR ====================
        status_frame = ctk.CTkFrame(self.window, corner_radius=0, height=40)
        status_frame.grid(row=4, column=0, sticky="ew", padx=0, pady=0)
        status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=20)

    def clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        current_text = self.url_entry.get("1.0", "end-1c")
        if current_text == "Paste URLs here (one per line)...":
            self.url_entry.delete("1.0", "end")

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="☀️ Light")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="🌙 Dark")

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

    def get_filename_from_url(self, url: str) -> str:
        """Extract filename from URL"""
        parsed_url = urlparse(url)
        filename = unquote(os.path.basename(parsed_url.path))
        if not filename or filename == "/" or filename == "":
            filename = "downloaded_file"
        return filename

    def start_download(self):
        """Start downloading files"""
        # Get URLs from text box
        urls_text = self.url_entry.get("1.0", "end-1c").strip()

        if not urls_text or urls_text == "Paste URLs here (one per line)...":
            messagebox.showwarning("No URLs", "Please enter at least one URL to download.")
            return

        # Parse URLs (one per line)
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

        if not urls:
            messagebox.showwarning("No URLs", "Please enter at least one valid URL.")
            return

        # Get output directory
        output_dir = self.dir_entry.get().strip()
        if not output_dir:
            output_dir = self.output_directory

        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Clear previous downloads display
        if hasattr(self, 'empty_label'):
            self.empty_label.destroy()

        # Create download tasks
        self.download_tasks = []
        for url in urls:
            task = DownloadTask(url, output_dir)
            self.download_tasks.append(task)
            self.add_download_item(task)

        # Disable download button
        self.download_button.configure(state="disabled", text="Downloading...")
        self.is_downloading = True

        # Start downloads in separate thread
        threading.Thread(target=self.download_files, daemon=True).start()

    def add_download_item(self, task: DownloadTask):
        """Add a download item to the list"""
        # Create frame for this download
        item_frame = ctk.CTkFrame(self.downloads_frame, corner_radius=8)
        item_frame.grid(sticky="ew", padx=10, pady=5)
        item_frame.grid_columnconfigure(0, weight=1)

        # Store reference
        task.frame = item_frame

        # URL label (truncated)
        url_display = task.url if len(task.url) <= 60 else task.url[:57] + "..."
        url_label = ctk.CTkLabel(
            item_frame,
            text=url_display,
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        url_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))
        task.url_label = url_label

        # Progress bar
        progress_bar = ctk.CTkProgressBar(item_frame, mode="determinate")
        progress_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))
        progress_bar.set(0)
        task.progress_bar = progress_bar

        # Status label
        status_label = ctk.CTkLabel(
            item_frame,
            text="Pending...",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        status_label.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 10))
        task.status_label = status_label

    def download_files(self):
        """Download all files in tasks"""
        successful = 0
        failed = 0

        for task in self.download_tasks:
            if self.download_file(task):
                successful += 1
            else:
                failed += 1

        # Update UI when done
        self.window.after(0, self.download_complete, successful, failed)

    def download_file(self, task: DownloadTask) -> bool:
        """Download a single file"""
        try:
            # Update status
            self.window.after(0, task.status_label.configure, {"text": "Fetching...", "text_color": "blue"})

            # Get file info
            head_response = requests.head(task.url, allow_redirects=True, timeout=10)
            head_response.raise_for_status()

            file_size = int(head_response.headers.get('content-length', 0))
            task.file_size = file_size

            # Get filename
            filename = task.filename or self.get_filename_from_url(task.url)
            output_path = Path(task.output_dir) / filename

            # Update status
            self.window.after(0, task.status_label.configure, {"text": f"Downloading {filename}...", "text_color": "blue"})

            # Download file
            response = requests.get(task.url, stream=True, timeout=30)
            response.raise_for_status()

            downloaded = 0
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)

                        # Update progress
                        if file_size > 0:
                            progress = downloaded / file_size
                            self.window.after(0, task.progress_bar.set, progress)

                            # Update status with size
                            size_mb = downloaded / (1024 * 1024)
                            total_mb = file_size / (1024 * 1024)
                            status_text = f"Downloading: {size_mb:.1f} MB / {total_mb:.1f} MB"
                            self.window.after(0, task.status_label.configure, {"text": status_text})

            # Success
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            success_text = f"✓ Downloaded: {filename} ({file_size_mb:.2f} MB)"
            self.window.after(0, task.status_label.configure, {"text": success_text, "text_color": "green"})
            self.window.after(0, task.progress_bar.set, 1.0)

            return True

        except requests.exceptions.HTTPError as e:
            error_text = f"✗ HTTP Error: {str(e)}"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": "red"})
            return False
        except requests.exceptions.ConnectionError:
            error_text = "✗ Connection Error: Unable to connect"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": "red"})
            return False
        except requests.exceptions.Timeout:
            error_text = "✗ Timeout: Request timed out"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": "red"})
            return False
        except Exception as e:
            error_text = f"✗ Error: {str(e)}"
            self.window.after(0, task.status_label.configure, {"text": error_text, "text_color": "red"})
            return False

    def download_complete(self, successful: int, failed: int):
        """Called when all downloads are complete"""
        self.is_downloading = False
        self.download_button.configure(state="normal", text="⬇ Start Download")

        # Update status
        status_text = f"Complete: {successful} successful, {failed} failed"
        self.status_label.configure(text=status_text)

        # Show message
        if failed == 0:
            messagebox.showinfo("Download Complete", f"All {successful} file(s) downloaded successfully!")
        else:
            messagebox.showwarning(
                "Download Complete",
                f"Downloaded {successful} file(s) successfully.\n{failed} file(s) failed."
            )

    def run(self):
        """Run the application"""
        self.window.mainloop()


def main():
    """Main entry point for GUI application"""
    app = FileDownloaderGUI()
    app.run()


if __name__ == "__main__":
    main()
