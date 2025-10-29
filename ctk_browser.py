"""
CustomTkinter Browser - Modern, Beautiful Web Browser
Built with CustomTkinter and pywebview
"""

import customtkinter as ctk
import webview
import threading
import json
import os
from datetime import datetime
from typing import List, Dict
import webbrowser
from pathlib import Path

# Configure CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"


class BrowserTab:
    """Represents a single browser tab with webview"""

    def __init__(self, url: str = "https://www.google.com"):
        self.url = url
        self.title = "New Tab"
        self.window = None
        self.webview_ready = False

    def create_webview(self, parent_window):
        """Create the webview window"""
        self.window = webview.create_window(
            self.title,
            self.url,
            width=1200,
            height=800,
            resizable=True,
            fullscreen=False,
            hidden=False
        )
        return self.window

    def navigate(self, url: str):
        """Navigate to a URL"""
        if not url.startswith(('http://', 'https://')):
            if '.' in url:
                url = 'https://' + url
            else:
                # Search query
                url = f'https://www.google.com/search?q={url}'
        self.url = url
        if self.window:
            self.window.load_url(url)

    def reload(self):
        """Reload current page"""
        if self.window:
            self.window.load_url(self.url)

    def go_back(self):
        """Go back in history"""
        if self.window:
            self.window.evaluate_js('window.history.back()')

    def go_forward(self):
        """Go forward in history"""
        if self.window:
            self.window.evaluate_js('window.history.forward()')


class BookmarkManager:
    """Manages browser bookmarks"""

    def __init__(self):
        self.bookmarks_file = Path.home() / '.ctk_browser' / 'bookmarks.json'
        self.bookmarks_file.parent.mkdir(exist_ok=True)
        self.bookmarks: List[Dict] = self.load_bookmarks()

    def load_bookmarks(self) -> List[Dict]:
        """Load bookmarks from file"""
        if self.bookmarks_file.exists():
            try:
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_bookmarks(self):
        """Save bookmarks to file"""
        with open(self.bookmarks_file, 'w') as f:
            json.dump(self.bookmarks, f, indent=2)

    def add_bookmark(self, title: str, url: str):
        """Add a bookmark"""
        bookmark = {
            'title': title,
            'url': url,
            'added': datetime.now().isoformat()
        }
        self.bookmarks.append(bookmark)
        self.save_bookmarks()

    def remove_bookmark(self, url: str):
        """Remove a bookmark"""
        self.bookmarks = [b for b in self.bookmarks if b['url'] != url]
        self.save_bookmarks()

    def is_bookmarked(self, url: str) -> bool:
        """Check if URL is bookmarked"""
        return any(b['url'] == url for b in self.bookmarks)


class HistoryManager:
    """Manages browser history"""

    def __init__(self):
        self.history_file = Path.home() / '.ctk_browser' / 'history.json'
        self.history_file.parent.mkdir(exist_ok=True)
        self.history: List[Dict] = self.load_history()

    def load_history(self) -> List[Dict]:
        """Load history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        """Save history to file"""
        # Keep only last 1000 entries
        self.history = self.history[-1000:]
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_entry(self, title: str, url: str):
        """Add a history entry"""
        entry = {
            'title': title,
            'url': url,
            'visited': datetime.now().isoformat()
        }
        self.history.append(entry)
        self.save_history()

    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.save_history()


class CTKBrowser(ctk.CTk):
    """Main browser window with CustomTkinter"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("CTK Browser - Modern Web Browser")
        self.geometry("1400x900")
        self.minsize(1000, 600)

        # Managers
        self.bookmark_manager = BookmarkManager()
        self.history_manager = HistoryManager()

        # Current tab
        self.current_tab: BrowserTab = None
        self.tabs: List[BrowserTab] = []

        # Setup UI
        self.setup_ui()

        # Create first tab
        self.create_new_tab()

    def setup_ui(self):
        """Setup the user interface"""

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top bar frame
        self.top_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.top_bar.grid_columnconfigure(1, weight=1)

        # Navigation buttons frame
        nav_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        nav_frame.grid(row=0, column=0, padx=10, pady=10)

        # Back button
        self.back_btn = ctk.CTkButton(
            nav_frame,
            text="←",
            width=40,
            height=40,
            font=("Arial", 20, "bold"),
            command=self.go_back,
            corner_radius=10
        )
        self.back_btn.pack(side="left", padx=2)

        # Forward button
        self.forward_btn = ctk.CTkButton(
            nav_frame,
            text="→",
            width=40,
            height=40,
            font=("Arial", 20, "bold"),
            command=self.go_forward,
            corner_radius=10
        )
        self.forward_btn.pack(side="left", padx=2)

        # Reload button
        self.reload_btn = ctk.CTkButton(
            nav_frame,
            text="⟳",
            width=40,
            height=40,
            font=("Arial", 20, "bold"),
            command=self.reload_page,
            corner_radius=10
        )
        self.reload_btn.pack(side="left", padx=2)

        # Home button
        self.home_btn = ctk.CTkButton(
            nav_frame,
            text="🏠",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.go_home,
            corner_radius=10
        )
        self.home_btn.pack(side="left", padx=2)

        # Address bar frame
        address_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        address_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        address_frame.grid_columnconfigure(0, weight=1)

        # Address bar
        self.address_bar = ctk.CTkEntry(
            address_frame,
            placeholder_text="Enter URL or search...",
            height=40,
            font=("Arial", 14),
            corner_radius=20
        )
        self.address_bar.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.address_bar.bind("<Return>", lambda e: self.navigate_to_url())

        # Go button
        self.go_btn = ctk.CTkButton(
            address_frame,
            text="Go",
            width=60,
            height=40,
            command=self.navigate_to_url,
            corner_radius=20,
            font=("Arial", 14, "bold")
        )
        self.go_btn.grid(row=0, column=1)

        # Right buttons frame
        right_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        right_frame.grid(row=0, column=2, padx=10, pady=10)

        # Bookmark button
        self.bookmark_btn = ctk.CTkButton(
            right_frame,
            text="⭐",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.toggle_bookmark,
            corner_radius=10
        )
        self.bookmark_btn.pack(side="left", padx=2)

        # Bookmarks list button
        self.bookmarks_list_btn = ctk.CTkButton(
            right_frame,
            text="📚",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.show_bookmarks,
            corner_radius=10
        )
        self.bookmarks_list_btn.pack(side="left", padx=2)

        # History button
        self.history_btn = ctk.CTkButton(
            right_frame,
            text="🕐",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.show_history,
            corner_radius=10
        )
        self.history_btn.pack(side="left", padx=2)

        # Settings button
        self.settings_btn = ctk.CTkButton(
            right_frame,
            text="⚙",
            width=40,
            height=40,
            font=("Arial", 16),
            command=self.show_settings,
            corner_radius=10
        )
        self.settings_btn.pack(side="left", padx=2)

        # New tab button
        self.new_tab_btn = ctk.CTkButton(
            right_frame,
            text="+",
            width=40,
            height=40,
            font=("Arial", 20, "bold"),
            command=self.create_new_tab,
            corner_radius=10,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.new_tab_btn.pack(side="left", padx=2)

        # Content area (for webview info)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Info label
        self.info_label = ctk.CTkLabel(
            self.content_frame,
            text="🌐 Browser Window Will Open in Separate Window\n\nUse the navigation bar above to control the browser",
            font=("Arial", 16),
            text_color="#7f8c8d"
        )
        self.info_label.grid(row=0, column=0, pady=200)

        # Status bar
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=0, pady=0)

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=("Arial", 12),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=5)

    def create_new_tab(self):
        """Create a new browser tab"""
        tab = BrowserTab()
        self.tabs.append(tab)
        self.current_tab = tab

        # Start webview in separate thread
        def start_webview():
            window = tab.create_webview(self)
            webview.start(debug=False)

        thread = threading.Thread(target=start_webview, daemon=True)
        thread.start()

        self.update_ui()
        self.status_label.configure(text=f"New tab opened - Total tabs: {len(self.tabs)}")

    def navigate_to_url(self):
        """Navigate to URL from address bar"""
        url = self.address_bar.get().strip()
        if url and self.current_tab:
            self.current_tab.navigate(url)
            self.history_manager.add_entry(url, url)
            self.update_ui()
            self.status_label.configure(text=f"Navigating to: {url}")

    def go_back(self):
        """Go back in history"""
        if self.current_tab:
            self.current_tab.go_back()
            self.status_label.configure(text="Going back...")

    def go_forward(self):
        """Go forward in history"""
        if self.current_tab:
            self.current_tab.go_forward()
            self.status_label.configure(text="Going forward...")

    def reload_page(self):
        """Reload current page"""
        if self.current_tab:
            self.current_tab.reload()
            self.status_label.configure(text="Reloading page...")

    def go_home(self):
        """Go to home page"""
        if self.current_tab:
            self.current_tab.navigate("https://www.google.com")
            self.address_bar.delete(0, "end")
            self.address_bar.insert(0, "https://www.google.com")
            self.status_label.configure(text="Going home...")

    def toggle_bookmark(self):
        """Toggle bookmark for current page"""
        if not self.current_tab:
            return

        url = self.current_tab.url
        if self.bookmark_manager.is_bookmarked(url):
            self.bookmark_manager.remove_bookmark(url)
            self.status_label.configure(text="Bookmark removed")
        else:
            # Show dialog to add bookmark
            self.show_add_bookmark_dialog(url)

    def show_add_bookmark_dialog(self, url: str):
        """Show dialog to add bookmark"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Bookmark")
        dialog.geometry("500x200")
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"500x200+{x}+{y}")

        # Title label
        title_label = ctk.CTkLabel(
            dialog,
            text="Bookmark Title:",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(20, 5))

        # Title entry
        title_entry = ctk.CTkEntry(
            dialog,
            width=400,
            height=40,
            font=("Arial", 14)
        )
        title_entry.pack(pady=5)
        title_entry.insert(0, url)
        title_entry.select_range(0, "end")
        title_entry.focus()

        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        def add():
            title = title_entry.get().strip()
            if title:
                self.bookmark_manager.add_bookmark(title, url)
                self.status_label.configure(text="Bookmark added!")
                dialog.destroy()

        # Add button
        add_btn = ctk.CTkButton(
            btn_frame,
            text="Add Bookmark",
            width=150,
            height=40,
            command=add,
            font=("Arial", 14, "bold")
        )
        add_btn.pack(side="left", padx=5)

        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            height=40,
            command=dialog.destroy,
            font=("Arial", 14),
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=5)

        title_entry.bind("<Return>", lambda e: add())
        dialog.bind("<Escape>", lambda e: dialog.destroy())

    def show_bookmarks(self):
        """Show bookmarks list"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Bookmarks")
        dialog.geometry("700x500")
        dialog.transient(self)

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"700x500+{x}+{y}")

        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="📚 Your Bookmarks",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=20)

        # Scrollable frame for bookmarks
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=650, height=350)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Display bookmarks
        if not self.bookmark_manager.bookmarks:
            no_bookmarks = ctk.CTkLabel(
                scroll_frame,
                text="No bookmarks yet. Add some!",
                font=("Arial", 14),
                text_color="gray"
            )
            no_bookmarks.pack(pady=50)
        else:
            for bookmark in reversed(self.bookmark_manager.bookmarks):
                bookmark_frame = ctk.CTkFrame(scroll_frame)
                bookmark_frame.pack(pady=5, padx=5, fill="x")

                # Bookmark info
                info_frame = ctk.CTkFrame(bookmark_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

                title_label = ctk.CTkLabel(
                    info_frame,
                    text=bookmark['title'],
                    font=("Arial", 14, "bold"),
                    anchor="w"
                )
                title_label.pack(anchor="w")

                url_label = ctk.CTkLabel(
                    info_frame,
                    text=bookmark['url'],
                    font=("Arial", 11),
                    text_color="gray",
                    anchor="w"
                )
                url_label.pack(anchor="w")

                # Buttons
                btn_frame = ctk.CTkFrame(bookmark_frame, fg_color="transparent")
                btn_frame.pack(side="right", padx=10)

                open_btn = ctk.CTkButton(
                    btn_frame,
                    text="Open",
                    width=80,
                    height=30,
                    command=lambda url=bookmark['url']: self.open_url(url, dialog)
                )
                open_btn.pack(side="left", padx=2)

                delete_btn = ctk.CTkButton(
                    btn_frame,
                    text="Delete",
                    width=80,
                    height=30,
                    fg_color="red",
                    hover_color="darkred",
                    command=lambda url=bookmark['url']: self.delete_bookmark(url, dialog)
                )
                delete_btn.pack(side="left", padx=2)

        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            width=150,
            height=40,
            command=dialog.destroy,
            font=("Arial", 14)
        )
        close_btn.pack(pady=10)

    def show_history(self):
        """Show history"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("History")
        dialog.geometry("700x500")
        dialog.transient(self)

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"700x500+{x}+{y}")

        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="🕐 Browsing History",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=20)

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=650, height=350)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Display history
        if not self.history_manager.history:
            no_history = ctk.CTkLabel(
                scroll_frame,
                text="No history yet. Start browsing!",
                font=("Arial", 14),
                text_color="gray"
            )
            no_history.pack(pady=50)
        else:
            for entry in reversed(self.history_manager.history[-100:]):  # Last 100 entries
                history_frame = ctk.CTkFrame(scroll_frame)
                history_frame.pack(pady=5, padx=5, fill="x")

                # History info
                info_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

                title_label = ctk.CTkLabel(
                    info_frame,
                    text=entry['title'],
                    font=("Arial", 13, "bold"),
                    anchor="w"
                )
                title_label.pack(anchor="w")

                url_label = ctk.CTkLabel(
                    info_frame,
                    text=entry['url'],
                    font=("Arial", 10),
                    text_color="gray",
                    anchor="w"
                )
                url_label.pack(anchor="w")

                # Open button
                open_btn = ctk.CTkButton(
                    history_frame,
                    text="Open",
                    width=80,
                    height=30,
                    command=lambda url=entry['url']: self.open_url(url, dialog)
                )
                open_btn.pack(side="right", padx=10)

        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)

        # Clear history button
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear History",
            width=150,
            height=40,
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.clear_history(dialog),
            font=("Arial", 14)
        )
        clear_btn.pack(side="left", padx=5)

        # Close button
        close_btn = ctk.CTkButton(
            btn_frame,
            text="Close",
            width=150,
            height=40,
            command=dialog.destroy,
            font=("Arial", 14)
        )
        close_btn.pack(side="left", padx=5)

    def show_settings(self):
        """Show settings dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Settings")
        dialog.geometry("500x400")
        dialog.transient(self)

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")

        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="⚙ Settings",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=30)

        # Appearance mode
        appearance_frame = ctk.CTkFrame(dialog)
        appearance_frame.pack(pady=15, padx=40, fill="x")

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="Appearance Mode:",
            font=("Arial", 16, "bold")
        )
        appearance_label.pack(pady=10)

        appearance_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode,
            width=200,
            height=40,
            font=("Arial", 14)
        )
        appearance_menu.set("Dark")
        appearance_menu.pack(pady=10)

        # Color theme
        theme_frame = ctk.CTkFrame(dialog)
        theme_frame.pack(pady=15, padx=40, fill="x")

        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Color Theme:",
            font=("Arial", 16, "bold")
        )
        theme_label.pack(pady=10)

        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Blue", "Green", "Dark-Blue"],
            command=self.change_color_theme,
            width=200,
            height=40,
            font=("Arial", 14)
        )
        theme_menu.set("Blue")
        theme_menu.pack(pady=10)

        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            width=150,
            height=40,
            command=dialog.destroy,
            font=("Arial", 14, "bold")
        )
        close_btn.pack(pady=30)

    def change_appearance_mode(self, mode: str):
        """Change appearance mode"""
        ctk.set_appearance_mode(mode.lower())
        self.status_label.configure(text=f"Appearance changed to {mode}")

    def change_color_theme(self, theme: str):
        """Change color theme"""
        self.status_label.configure(text=f"Theme changed to {theme}. Restart to see changes.")

    def open_url(self, url: str, dialog=None):
        """Open URL in current tab"""
        if self.current_tab:
            self.current_tab.navigate(url)
            self.address_bar.delete(0, "end")
            self.address_bar.insert(0, url)
            self.history_manager.add_entry(url, url)
            self.status_label.configure(text=f"Opening: {url}")
            if dialog:
                dialog.destroy()

    def delete_bookmark(self, url: str, dialog):
        """Delete a bookmark"""
        self.bookmark_manager.remove_bookmark(url)
        self.status_label.configure(text="Bookmark deleted")
        dialog.destroy()
        self.show_bookmarks()  # Refresh list

    def clear_history(self, dialog):
        """Clear browsing history"""
        self.history_manager.clear_history()
        self.status_label.configure(text="History cleared")
        dialog.destroy()
        self.show_history()  # Refresh list

    def update_ui(self):
        """Update UI elements"""
        if self.current_tab:
            self.address_bar.delete(0, "end")
            self.address_bar.insert(0, self.current_tab.url)


def main():
    """Main entry point"""
    app = CTKBrowser()
    app.mainloop()


if __name__ == "__main__":
    main()
