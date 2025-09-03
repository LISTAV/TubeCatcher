import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import webbrowser
import threading
import os
import sys
from yt_dlp import YoutubeDL

class TubeCatcher:
    """A simple GUI for yt-dlp to download videos and audio."""

    def __init__(self, root):
        self.root = root
        self.root.title("TubeCatcher v1.0")
        
        # --- State Variables ---
        self.stop_event = threading.Event()
        self.formats_map = {}  # Maps display string to format_id
        
        # --- UI Setup ---
        self.setup_ui()
        self.check_dependencies()

    def setup_ui(self):
        """Initializes and lays out the graphical user interface."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # --- URL Input ---
        ttk.Label(main_frame, text="Video URL:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.url_entry = ttk.Entry(main_frame)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5, pady=2)
        self.fetch_btn = ttk.Button(main_frame, text="Fetch Formats", command=self.fetch_formats)
        self.fetch_btn.grid(row=0, column=3, padx=5, pady=2)

        # --- Format Selection ---
        ttk.Label(main_frame, text="Format:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.format_var = tk.StringVar()
        self.format_combobox = ttk.Combobox(main_frame, textvariable=self.format_var, state="readonly")
        self.format_combobox.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=2)
        self.audio_only_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Audio Only", variable=self.audio_only_var, command=self.filter_formats).grid(row=1, column=3, padx=5, pady=2)

        # --- Output Path ---
        ttk.Label(main_frame, text="Output Folder:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.output_var = tk.StringVar(value=os.getcwd())
        ttk.Entry(main_frame, textvariable=self.output_var, state="readonly").grid(row=2, column=1, columnspan=2, sticky='ew', padx=5, pady=2)
        ttk.Button(main_frame, text="Browse...", command=self.browse_output).grid(row=2, column=3, padx=5, pady=2)

        # --- Options ---
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=3, column=1, columnspan=2, sticky='w', pady=5)
        self.subs_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Subtitles", variable=self.subs_var).pack(side='left', padx=10)
        self.thumbnail_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Thumbnail", variable=self.thumbnail_var).pack(side='left', padx=10)

        # --- Progress & Console ---
        self.progress = ttk.Progressbar(main_frame, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=4, sticky="ew", pady=5, padx=5)
        self.console = tk.Text(main_frame, height=8, state="disabled", wrap="word")
        self.console.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        main_frame.rowconfigure(5, weight=1) # Allow console to expand
        main_frame.columnconfigure(1, weight=1) # Allow entry/combobox to expand

        # --- Controls ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=4, pady=5)
        self.download_btn = ttk.Button(button_frame, text="Start Download", command=self.start_download)
        self.download_btn.pack(side='left', padx=5)
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_download, state="disabled")
        self.stop_btn.pack(side='left', padx=5)
        
        # --- Support Link ---
        ttk.Button(main_frame, text="🌐 Support the Developer", command=lambda: webbrowser.open("https://buymeacoffee.com/xuvidhah")).grid(row=7, column=0, columnspan=4, pady=10)

    def log(self, message):
        """Logs a message to the console widget, ensuring it's thread-safe."""
        def _update():
            self.console.config(state="normal")
            self.console.insert("end", message + "\n")
            self.console.see("end")
            self.console.config(state="disabled")
        self.root.after(0, _update)

    def toggle_controls(self, is_downloading):
        """Enable/disable controls based on download state."""
        self.download_btn.config(state="disabled" if is_downloading else "normal")
        self.stop_btn.config(state="normal" if is_downloading else "disabled")
        self.fetch_btn.config(state="disabled" if is_downloading else "normal")

    def fetch_formats(self):
        """Fetches video formats in a separate thread to avoid freezing the GUI."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        self.toggle_controls(is_downloading=True)
        self.log(f"Fetching formats for: {url}")
        
        def _fetch_thread():
            try:
                with YoutubeDL({'quiet': True, 'no_warnings': True, 'noplaylist': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                
                self.formats_map.clear()
                # Add a "best" option by default for non-audio-only downloads
                self.formats_map['Best Quality (Video+Audio)'] = {'id': 'bestvideo+bestaudio/best', 'audio_only': False}

                for f in info.get('formats', []):
                    is_audio = f.get('vcodec') == 'none'
                    res = f.get('resolution', 'audio')
                    ext = f.get('ext')
                    note = f.get('format_note', '')
                    display_str = f"{res} ({ext}) - {note}"
                    self.formats_map[display_str] = {'id': f['format_id'], 'audio_only': is_audio}

                self.root.after(0, self.filter_formats)
                self.root.after(0, lambda: self.log("Formats fetched successfully."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch formats:\n{e}"))
            finally:
                self.root.after(0, lambda: self.toggle_controls(is_downloading=False))
        
        threading.Thread(target=_fetch_thread, daemon=True).start()

    def filter_formats(self):
        """Filters the formats in the combobox based on the 'Audio Only' checkbox."""
        is_audio = self.audio_only_var.get()
        filtered_formats = [
            display for display, data in self.formats_map.items() if data['audio_only'] == is_audio
        ]
        self.format_combobox['values'] = filtered_formats
        if filtered_formats:
            self.format_combobox.current(0)

    def browse_output(self):
        """Opens a dialog to choose an output directory."""
        if folder := filedialog.askdirectory():
            self.output_var.set(folder)
            
    def start_download(self):
        """Starts the video download in a separate thread."""
        url = self.url_entry.get().strip()
        selected_format = self.format_var.get()

        if not url or not selected_format:
            messagebox.showerror("Error", "URL and Format must be selected.")
            return

        self.stop_event.clear()
        self.toggle_controls(is_downloading=True)
        self.progress['value'] = 0
        self.console.config(state="normal"); self.console.delete("1.0", "end"); self.console.config(state="disabled")
        self.log("Starting download...")

        def _download_thread():
            format_id = self.formats_map[selected_format]['id']
            # If a video-only format is chosen, automatically select the best audio to merge
            if not self.formats_map[selected_format]['audio_only'] and '+bestaudio' not in format_id:
                format_id = f"{format_id}+bestaudio"

            ydl_opts = {
                'format': format_id,
                'outtmpl': os.path.join(self.output_var.get(), '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
                'writesubtitles': self.subs_var.get(),
                'writethumbnail': self.thumbnail_var.get(),
                'merge_output_format': 'mp4',
            }
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                if not self.stop_event.is_set():
                    self.log("\nDownload completed successfully!")
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Download finished!"))
            except Exception as e:
                if not self.stop_event.is_set():
                    self.log(f"\nError: {e}")
            finally:
                self.root.after(0, lambda: self.toggle_controls(is_downloading=False))
        
        threading.Thread(target=_download_thread, daemon=True).start()

    def stop_download(self):
        """Signals the download thread to stop."""
        self.stop_event.set()
        self.log("\nStopping download...")

    def progress_hook(self, d):
        """yt-dlp hook to update progress bar and log status."""
        if self.stop_event.is_set():
            raise Exception("Download stopped by user.")

        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                percent = (d['downloaded_bytes'] / total) * 100
                self.progress['value'] = percent
                speed = d.get('_speed_str', 'N/A').strip()
                eta = d.get('_eta_str', 'N/A').strip()
                # Use '\r' to overwrite the same line in the log for cleaner output
                self.log(f"\rDownloading: {percent:.1f}% | Speed: {speed} | ETA: {eta}")

        elif d['status'] == 'finished':
            self.progress['value'] = 100
            self.log("\nProcessing and merging files...")

    def check_dependencies(self):
        """Checks for the presence of FFmpeg."""
        try:
            subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showwarning(
                "FFmpeg Missing",
                "FFmpeg is not found in your system's PATH.\n"
                "It is required for merging video and audio files.\n"
                "Please download it from ffmpeg.org and add it to your PATH."
            )

def main():
    root = tk.Tk()
    app = TubeCatcher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
