import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import webbrowser
import threading
import os
import re
import sys
import platform
from yt_dlp import YoutubeDL


def resource_path(relative_path):
    #""" Get absolute path to resource for both dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def conv_path_windows(v):
    if platform.system() == 'Windows':
        v1 = v.replace('\\','/')
        return v1

def get_current_directory():
    var = os.path.dirname(os.path.abspath(__file__))
    v2 = conv_path_windows(var)
    return v2

class YTDLPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TubeCatcher v1.0")
        self.running = False
        self.stop_event = threading.Event()
        self.ydl = None
        self.all_formats = []  # Store all available formats
        self.current_formats = []  # Current filtered formats
        try:
            icon_path = resource_path('favicon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon error: {e}")
        self.check_dependencies()
            
        # Initialize default output directory
        self.output_var = tk.StringVar()
        self.output_var.set(os.path.join(get_current_directory()))
        self.setup_ui()
        style = ttk.Style()
        style.configure("outputF.TLabel", foreground="red", font=("Arial", 12))

    def open_website(self):
        try:
            webbrowser.open("https://buymeacoffee.com/xuvidhah")
        except Exception as e:
            messagebox.showerror("Browser Error", f"Could not open browser: {str(e)}")
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # URL Input with Fetch button
        ttk.Label(main_frame, text="Video URL:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Add Fetch Formats button
        self.fetch_btn = ttk.Button(main_frame, text="Fetch Formats", command=self.fetch_formats)
        self.fetch_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Format Selection
        ttk.Label(main_frame, text="Format:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.format_var = tk.StringVar()
        self.format_combobox = ttk.Combobox(main_frame, textvariable=self.format_var, width=50, state="readonly")
        self.format_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w', columnspan=2)
        
        # Audio Only filter
        self.audio_only_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Audio Only", variable=self.audio_only_var,
                        command=self.filter_formats).grid(row=1, column=3, padx=5, pady=5)

        # Output Location
        ttk.Label(main_frame, text="Output Folder:", style="outputF.TLabel").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        #self.output_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable= self.output_var , width=40).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=3, column=2, padx=5, pady=5)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
        options_frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
        self.subs_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Subtitles", variable=self.subs_var).pack(side='left', padx=5)
        
        self.thumbnail_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Thumbnail", variable=self.thumbnail_var).pack(side='left', padx=5)
        
        #Progress Bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=4, padx=5, pady=10)
        
        #Console with progress bar
        self.console = tk.Text(main_frame, height=10, width=70, state="disabled")
        self.console.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=4, pady=10)
        
        self.download_btn = ttk.Button(button_frame, text="Start Download", command=self.start_download)
        self.download_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_download, state="disabled")
        self.stop_btn.pack(side='left', padx=5)
        
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.buy_btn = ttk.Button(main_frame, text="🌐 Help me BUY a Laptop", command=self.open_website, width=30)
        self.buy_btn.grid(row=8, column=0, columnspan=4, pady=10)
        
        

    def fetch_formats(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        self.fetch_btn.config(state="disabled")
        self.log_message("Fetching available formats...")
        
        # Run in a separate thread
        threading.Thread(target=self._fetch_formats_thread, args=(url,), daemon=True).start()
        
    def _fetch_formats_thread(self, url):
        try:
            with YoutubeDL({'quiet': True, 'no_warnings': True, 'noplaylist':True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Could not fetch video info"))
                    return
                    
                self.all_formats = []
                for f in info.get('formats', []):
                    if not f.get('format_id'):
                        continue
                        
                    # Get format details
                    vcodec = f.get('vcodec', 'none')
                    acodec = f.get('acodec', 'none')
                    resolution = f.get('resolution', 'unknown')
                    fps = f.get('fps', 0)
                    ext = f.get('ext', 'unknown')
                    
                    # Create display string
                    parts = []
                    if vcodec != 'none':
                        parts.append(f"{resolution}@{fps}fps" if resolution != 'unknown' else "video")
                    if acodec != 'none':
                        parts.append("audio")
                    
                    format_str = f"{f['format_id']} - {ext.upper()} ({' '.join(parts)})"
                    self.all_formats.append((f['format_id'], format_str, vcodec == 'none' and acodec != 'none'))
                
                # Update UI with formats
                self.root.after(0, self.filter_formats)
                self.root.after(0, lambda: self.log_message(f"Found {len(self.all_formats)} formats"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch formats: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.fetch_btn.config(state="normal"))
            
    def filter_formats(self):
        if self.audio_only_var.get():
            self.current_formats = [f for f in self.all_formats if f[2]]  # Audio only
        else:
            self.current_formats = self.all_formats
            
        # Update combobox
        format_strings = [f[1] for f in self.current_formats]
        self.format_combobox['values'] = format_strings
        
        # Select first item if available
        if format_strings:
            self.format_combobox.current(0)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_var.set(folder)
            

    def check_dependencies(self):
        # Check yt-dlp installation
        try:
            import yt_dlp
        except ImportError:
            if messagebox.askyesno("Dependency Missing", 
                                 "yt-dlp not found. Install now?"):
                self.install_via_pip("yt-dlp")
                
        # Check FFmpeg
        try:
            subprocess.run(["ffmpeg", "-version"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            messagebox.showwarning("FFmpeg Missing", 
                                  "FFmpeg is required for audio/video processing.\n"
                                  "Download from https://ffmpeg.org/ and add to PATH")

    def install_via_pip(self, package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            messagebox.showinfo("Success", f"{package} installed successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Failed to install {package}")

    def ydl_progress_hook(self, d):
        if self.stop_event.is_set():
            raise Exception("Download stopped by user")
            
        if d['status'] == 'downloading':
            msg = []
            if d.get('total_bytes'):
                msg.append(f"Total Size: {d['total_bytes']//(1024*1024)}MB")
            if d.get('downloaded_bytes'):
                msg.append(f"Downloaded: {d['downloaded_bytes']//(1024*1024)}MB")
            if d.get('speed'):
                msg.append(f"Speed: {d['speed']//(1024)}KB/s")
            if d.get('_percent_str'):
                raw_percent = d.get('_percent_str', '0.0%')
                # Remove ANSI escape codes (colors)
                clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', raw_percent).strip().replace('%', '')
                self.progress['value'] = float(clean_percent)
                msg.append(f"Progress: {clean_percent}%")
                
            self.log_message(" | ".join(msg))
            
        elif d['status'] == 'error':
            self.log_message(f"Error: {d['error']}")

    def log_message(self, message):
        self.root.after(0, self._update_console, message)

    def _update_console(self, message):
        self.console.config(state="normal")
        self.console.insert("end", message + "\n")
        self.console.see("end")
        self.console.config(state="disabled")

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return

        # Get selected format ID
        selected_format_str = self.format_var.get()
        if not selected_format_str:
            messagebox.showerror("Error", "Please select a format")
            return
            
        # Find format ID from display string
        format_id = None
        for fmt in self.current_formats:
            if fmt[1] == selected_format_str:
                format_id = fmt[0]
                break
                
        if not format_id:
            messagebox.showerror("Error", "Invalid format selected")
            return

        if self.running:
            return

        self.stop_event.clear()
        self.running = True
        self.download_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")

        options = {
            'outtmpl': os.path.join(self.output_var.get(), '%(title)s.%(ext)s'),
            'progress_hooks': [self.ydl_progress_hook],
            'noprogress': True,
            'socket_timeout': 30,
            'retries': 3,
            'format': format_id,
            'noplaylist': True
        }

        # Additional options
        if self.subs_var.get():
            options.update({
                'writesubtitles': True,
                'embedsubtitles': True
            })
            
        if self.thumbnail_var.get():
            options.update({
                'writethumbnail': True,
                'embedthumbnail': True
            })

        def download_thread():
            try:
                with YoutubeDL(options) as ydl:
                    self.ydl = ydl
                    ydl.download([url])
                if not self.stop_event.is_set():
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed!"))
                    self.log_message("\nDownload completed successfully!")
            except Exception as e:
                if not self.stop_event.is_set():
                    self.log_message(f"\nError: {str(e)}")
            finally:
                self.running = False
                self.root.after(0, self._update_buttons)

        threading.Thread(target=download_thread, daemon=True).start()

    def _update_buttons(self):
        self.download_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def stop_download(self):
        self.stop_event.set()
        if self.ydl:
            try:
                self.ydl._download_retcode = -1  # Force stop yt-dlp
            except AttributeError:
                pass
        self.log_message("\nStopping download...")
        self.running = False
        self._update_buttons()

def main():
    root = tk.Tk()
    app = YTDLPGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()