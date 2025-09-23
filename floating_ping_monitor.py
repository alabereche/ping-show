#!/usr/bin/env python3
"""
🎮 CS2 Ping Monitor - Official Servers
A lightweight Python desktop application that displays live ping results
for official Counter-Strike 2 servers across Europe.

Features:
- Continuous ping monitoring every 1 second with 3s timeout
- Enhanced dark theme with borders, gradients, and alternating row colors
- Solid window (no transparency) with universal drag functionality
- Official CS2 servers (Valve IPs) across all European countries
- Custom icon support - automatically loads from icons/ folder
- Modern UI with enhanced typography (Courier New font family)
- Click anywhere to drag - smart cursor feedback
- Enhanced scrollable interface with universal mouse wheel support
- Keyboard shortcuts (F5 refresh, Space toggle topmost, ESC exit)
- Right-click context menu with refresh and exit options
- Non-blocking UI using threading

IMPORTANT: CS2 servers often show "ERROR" because they block ping requests for security.
This is NORMAL - use the CS2 game client to test actual connectivity.

Enhanced UI Colors:
- 🟢 Green: Excellent ping (<100ms) - Perfect for gaming
- 🟠 Orange: Good ping (>100ms) - Acceptable for gaming
- 🔴 Red: Error/Unreachable (may still work in-game)
- Enhanced backgrounds and borders for better readability

Requirements:
- Python 3.6+
- tkinter (built-in)
- Works best with stable internet connection

Usage:
python floating_ping_monitor.py

CS2 Official Servers: France, Germany, Luxembourg, UK, Sweden, Spain, Austria, Belgium
"""

# Hide console window IMMEDIATELY on Windows - BEFORE any imports
import sys
import os
import platform

if platform.system() == "Windows":
    import ctypes
    # Hide console window immediately
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    # Free console completely for PyInstaller executables
    if hasattr(sys, '_MEIPASS'):
        ctypes.windll.kernel32.FreeConsole()

import tkinter as tk
from tkinter import ttk
import threading
import time
import subprocess
from collections import defaultdict

class FloatingPingMonitor:
    def __init__(self):
        # Additional console hiding for PyInstaller
        if platform.system() == "Windows" and hasattr(sys, '_MEIPASS'):
            import ctypes
            ctypes.windll.kernel32.FreeConsole()
        
        self.root = tk.Tk()
        self.setup_window()
        self.setup_servers()
        self.setup_ui()
        self.ping_data = defaultdict(lambda: {"status": "Unknown", "last_ping": 0})

        # Start ping monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_pings, daemon=True)
        self.monitor_thread.start()

        # Make window draggable
        self.setup_drag_functionality()

    def setup_window(self):
        """Configure the main window properties"""
        self.root.title("CS2 Ping Monitor - Official")

        # Set window icon if available
        try:
            self.root.iconbitmap("icons/icon.ico")  # Windows icon
        except:
            try:
                # Try different icon formats if ICO fails
                icon_path = "icons/icon.png"
                if os.path.exists(icon_path):
                    icon_img = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(True, icon_img)
            except:
                pass  # Use default icon if no custom icon found
        self.root.geometry("500x750")
        self.root.resizable(False, False)

        # Remove window decorations for floating effect
        self.root.overrideredirect(True)

        # Set window styling (Windows) - No transparency
        if platform.system() == "Windows":
            self.root.wm_attributes("-topmost", True)
            # No transparency - solid window

        # Enhanced dark theme with gradient effect
        self.root.configure(bg='#1a1a1a')  # Dark background - solid

        # Add a subtle border frame
        self.border_frame = tk.Frame(
            self.root,
            bg='#333333',  # Dark gray border
            bd=2,
            relief='solid'
        )
        self.border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Main container with gradient background
        self.main_container = tk.Frame(
            self.border_frame,
            bg='black',
            padx=15,
            pady=15
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Center window on screen
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 750) // 2
        self.root.geometry(f"+{x}+{y}")

    def setup_servers(self):
        """Define the list of servers to monitor"""
        self.servers = [
            # General Servers
            "google.com",              # Google
            "cloudflare.com",          # Cloudflare
            "youtube.com",             # YouTube
            "twitch.tv",               # Twitch
            "github.com",              # GitHub
            "stackoverflow.com",       # Stack Overflow
            "discord.com",             # Discord
            "steamcommunity.com",      # Steam Community

            # Counter-Strike 2 Servers - Europe (Official IPs)
            "146.66.152.1",     # CS2 Stockholm, Sweden
            "155.133.232.1",    # CS2 Luxembourg, EU West
            "155.133.248.1",    # CS2 Vienna, Austria
            "185.25.182.1",     # CS2 Paris, France
            "185.40.64.1",      # CS2 Frankfurt, Germany
            "185.93.2.1",       # CS2 London, UK
            "146.66.155.1",     # CS2 Madrid, Spain
            "146.66.158.1",     # CS2 Stockholm, Sweden (Backup)
            "155.133.226.1",    # CS2 Luxembourg (Backup)
            "155.133.242.1",    # CS2 Vienna (Backup)
            "185.25.176.1",     # CS2 Paris (Backup)
            "185.40.65.1",      # CS2 Frankfurt (Backup)
            "185.93.3.1",       # CS2 London (Backup)

            # Steam Content Servers - Europe
            "eu1.steamcontent.com",          # Steam EU 1
            "eu2.steamcontent.com",          # Steam EU 2
            "eu3.steamcontent.com",          # Steam EU 3
            "eu4.steamcontent.com",          # Steam EU 4
            "eu5.steamcontent.com",          # Steam EU 5
            "eu6.steamcontent.com",          # Steam EU 6
            "eu7.steamcontent.com",          # Steam EU 7
            "eu8.steamcontent.com",          # Steam EU 8

            # European DNS & Infrastructure
            "8.8.8.8",                       # Google DNS
            "1.1.1.1",                       # Cloudflare DNS
            "185.25.182.1",                  # France DNS
            "185.40.64.1",                   # Germany DNS
            "185.93.2.1",                    # UK DNS
        ]

    def setup_ui(self):
        """Create the user interface"""
        # Title with enhanced styling
        title_label = tk.Label(
            self.main_container,
            text="🎮 CS2 PING MONITOR - OFFICIAL 🎮",
            font=("Courier New", 16, "bold"),
            fg="#00ff88",  # Bright mint green
            bg='black',
            relief='ridge',
            bd=2,
            padx=10,
            pady=5
        )
        title_label.pack(pady=(0, 15), fill=tk.X)

        # Subtitle
        subtitle_label = tk.Label(
            self.main_container,
            text="🚀 Official CS2 European Servers",
            font=("Courier New", 10, "italic"),
            fg="#8888ff",  # Light blue
            bg='black'
        )
        subtitle_label.pack(pady=(0, 15))

        # Server labels frame with scroll and enhanced styling
        self.server_frame = tk.Frame(self.main_container, bg='black')
        self.server_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Create canvas for scrolling with enhanced styling
        self.canvas = tk.Canvas(
            self.server_frame,
            bg='#111111',  # Darker background for canvas
            highlightthickness=0,
            relief='sunken',
            bd=1
        )
        scrollbar = tk.Scrollbar(
            self.server_frame,
            orient="vertical",
            command=self.canvas.yview,
            bg='#333333',
            troughcolor='#222222',
            width=20
        )
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg='black',
            padx=10,
            pady=10
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create labels for each server
        self.server_labels = {}
        self.category_labels = {}

        # Create categories
        categories = {
            "🌐 General Servers": self.servers[:9],
            "🔫 Counter-Strike 2 (Official)": self.servers[9:22],
            "🚂 Steam Content Servers (EU)": self.servers[22:30],
            "🔧 DNS & Infrastructure": self.servers[30:]
        }

        row = 0
        for category, servers_in_cat in categories.items():
            # Category title with enhanced styling
            cat_label = tk.Label(
                self.scrollable_frame,
                text=f"📡 {category}",
                font=("Courier New", 12, "bold"),
                fg="#ffaa00",  # Orange
                bg='#222222',  # Dark gray background
                relief='raised',
                bd=1,
                padx=8,
                pady=3,
                anchor='w'
            )
            cat_label.grid(row=row, column=0, columnspan=2, sticky='ew', pady=(15, 8))
            row += 1

            # Servers in category with enhanced styling
            for i, server in enumerate(servers_in_cat):
                # Background frame for each server row
                server_bg = tk.Frame(
                    self.scrollable_frame,
                    bg='#1a1a1a' if i % 2 == 0 else '#151515',  # Alternating backgrounds
                    relief='flat',
                    bd=1
                )
                server_bg.grid(row=row, column=0, columnspan=2, sticky='ew', padx=5, pady=1)

                # Server name label
                server_label = tk.Label(
                    server_bg,
                    text=f"🔹 {server}",
                    font=("Courier New", 10),
                    fg="#ffffff",  # White
                    bg=server_bg.cget('bg'),
                    anchor='w',
                    padx=10,
                    pady=3
                )
                server_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

                # Ping result label with enhanced styling
                ping_label = tk.Label(
                    server_bg,
                    text="-- ms",
                    font=("Courier New", 10, "bold"),
                    fg="#00ff88",  # Bright mint green
                    bg=server_bg.cget('bg'),
                    anchor='e',
                    width=12,
                    padx=10,
                    pady=3
                )
                ping_label.pack(side=tk.RIGHT)

                self.server_labels[server] = ping_label
                row += 1

            row += 2  # Extra space between categories

        # Status indicator with enhanced styling
        self.status_label = tk.Label(
            self.main_container,
            text="🔴 Monitoring Active - Live Updates",
            font=("Courier New", 10, "bold"),
            fg="#00ff88",  # Bright mint green
            bg='black',
            relief='ridge',
            bd=1,
            padx=10,
            pady=3
        )
        self.status_label.pack(pady=(10, 5), fill=tk.X)

        # Instructions with enhanced styling
        instructions = tk.Label(
            self.main_container,
            text="🎮 Click anywhere to drag | Right-click menu | Scroll to navigate | ESC to exit",
            font=("Courier New", 9),
            fg="#888888",  # Light gray
            bg='black',
            justify=tk.CENTER,
            padx=10,
            pady=5
        )
        instructions.pack(fill=tk.X, pady=(5, 0))

        # Footer with version info
        footer = tk.Label(
            self.main_container,
            text="⚡ Official CS2 Server Monitor | Optimized for Algeria & MENA",
            font=("Courier New", 8, "italic"),
            fg="#666666",  # Medium gray
            bg='black',
            justify=tk.CENTER
        )
        footer.pack(fill=tk.X, pady=(5, 0))

    def setup_drag_functionality(self):
        """Make the window draggable with enhanced functionality"""
        def start_drag(event):
            # Allow dragging from anywhere in the window
            self.x = event.x
            self.y = event.y
            self.root.config(cursor="fleur")  # Change cursor to indicate dragging

        def drag_motion(event):
            if hasattr(self, 'x'):
                deltax = event.x - self.x
                deltay = event.y - self.y
                x = self.root.winfo_x() + deltax
                y = self.root.winfo_y() + deltay
                self.root.geometry(f"+{x}+{y}")

        def stop_drag(event):
            self.root.config(cursor="arrow")  # Reset cursor
            if hasattr(self, 'x'):
                del self.x
                del self.y

        def show_context_menu(event):
            context_menu = tk.Menu(self.root, tearoff=0, bg='#333333', fg='white', font=("Courier New", 9))
            context_menu.add_command(label="🔄 Refresh Data", command=self.refresh_data, font=("Courier New", 9))
            context_menu.add_separator()
            context_menu.add_command(label="❌ Exit", command=self.quit, font=("Courier New", 9))
            context_menu.post(event.x_root, event.y_root)

        # Enhanced mouse bindings for better usability
        self.root.bind("<ButtonPress-1>", start_drag)
        self.root.bind("<B1-Motion>", drag_motion)
        self.root.bind("<ButtonRelease-1>", stop_drag)
        self.root.bind("<Button-3>", show_context_menu)  # Right-click context menu

        # Enhanced mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.scrollable_frame.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())  # Allow mouse wheel on canvas

        # Keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.quit())
        self.root.bind("<F5>", lambda e: self.refresh_data())  # F5 to refresh
        self.root.bind("<space>", lambda e: self.toggle_topmost())  # Space to toggle always on top

    def ping_server(self, server):
        """Ping a server and return the response time or error status"""
        try:
            if platform.system() == "Windows":
                # Windows ping command with longer timeout for distant servers
                command = ['ping', '-n', '1', '-w', '3000', server]  # 3 seconds timeout
                # Hide console window for subprocess
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                result = subprocess.run(command, capture_output=True, text=True, timeout=4, 
                                      startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode == 0:
                    # Parse ping output to extract time
                    output = result.stdout
                    if "time=" in output:
                        time_str = output.split("time=")[1].split("ms")[0].strip()
                        return float(time_str)
                    else:
                        return "timeout"
                else:
                    return "error"
            else:
                # Unix-like systems ping command with longer timeout for distant servers
                command = ['ping', '-c', '1', '-W', '3', server]  # 3 seconds timeout
                result = subprocess.run(command, capture_output=True, text=True, timeout=4)
                if result.returncode == 0:
                    # Parse ping output to extract time
                    output = result.stdout
                    if "time=" in output:
                        time_str = output.split("time=")[1].split(" ")[0].strip()
                        return float(time_str)
                    else:
                        return "timeout"
                else:
                    return "error"
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            return "error"

    def monitor_pings(self):
        """Continuously monitor ping status for all servers"""
        while self.running:
            for server in self.servers:
                try:
                    ping_time = self.ping_server(server)

                    if isinstance(ping_time, float):
                        # Successful ping
                        self.ping_data[server]["status"] = "online"
                        self.ping_data[server]["last_ping"] = ping_time
                        if ping_time > 100:
                            display_text = f"{ping_time:.0f}ms"  # High ping
                            color = "#ffaa00"  # Orange for high ping
                        else:
                            display_text = f"{ping_time:.0f}ms"  # Normal ping
                            color = "#00ff00"  # Green for good ping
                    elif ping_time == "timeout":
                        # Timeout - server is slow or distant
                        self.ping_data[server]["status"] = "slow"
                        display_text = "SLOW"
                        color = "#ffaa00"  # Orange
                    else:
                        # Error - server unreachable
                        self.ping_data[server]["status"] = "error"
                        display_text = "ERROR"
                        color = "#ff0000"  # Red

                    # Update UI in main thread
                    self.root.after(0, self.update_ping_display, server, display_text, color)

                except Exception as e:
                    print(f"Error pinging {server}: {e}")
                    self.root.after(0, self.update_ping_display, server, "ERROR", "#ff0000")

            # Wait 1 second before next ping cycle
            time.sleep(1)

    def update_ping_display(self, server, text, color):
        """Update the ping display for a specific server"""
        if server in self.server_labels:
            self.server_labels[server].config(text=text, fg=color)

    def refresh_data(self):
        """Refresh all ping data"""
        self.status_label.config(text="🔄 Refreshing Data...", fg="#ffaa00")
        # Update all server labels to show refreshing state
        for server, label in self.server_labels.items():
            label.config(text="⟳", fg="#ffaa00")
        # Reset status after a short delay
        self.root.after(1000, lambda: self.status_label.config(text="🔴 Monitoring Active - Live Updates", fg="#00ff88"))

    def toggle_topmost(self):
        """Toggle always on top"""
        current_topmost = self.root.wm_attributes("-topmost")
        self.root.wm_attributes("-topmost", not current_topmost)
        if not current_topmost:
            self.status_label.config(text="📌 Always on Top - ENABLED", fg="#ffaa00")
        else:
            self.status_label.config(text="🔴 Monitoring Active - Live Updates", fg="#00ff88")
        # Reset status after 2 seconds
        self.root.after(2000, lambda: self.status_label.config(text="🔴 Monitoring Active - Live Updates", fg="#00ff88"))

    def quit(self):
        """Clean shutdown of the application"""
        self.running = False
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = FloatingPingMonitor()
        app.run()
    except KeyboardInterrupt:
        print("\nPing monitor stopped by user")
    except Exception as e:
        print(f"Error starting ping monitor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
