# TubeCatcher

![TubeCatcher Logo](/favicon.ico)

TubeCatcher is a user-friendly graphical user interface (GUI) for downloading videos and audio from YouTube and other supported platforms using the powerful `yt-dlp` library. Built with Python and Tkinter, TubeCatcher allows users to fetch available formats, select video or audio quality, and download content with options for subtitles and thumbnails. It simplifies the process of downloading media for users who prefer a GUI over command-line tools.

## Support the Project
If you find TubeCatcher useful, please consider supporting the developer by buying a coffee! Your support helps keep this project alive and funds future improvements.

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-orange?logo=buymeacoffee)](https://buymeacoffee.com/xuvidhah)

## Features
- **Fetch Available Formats**: Retrieve and display all available video and audio formats for a given URL.
- **Video and Audio Downloads**: Download videos with audio or audio-only files, with automatic merging of video and audio streams when needed.
- **Format Selection**: Choose from a list of formats, including a "Best Video + Audio" option for optimal quality.
- **Subtitles and Thumbnails**: Option to include subtitles and embed thumbnails in downloaded files.
- **Progress Tracking**: Real-time progress bar and console output to monitor download status.
- **Custom Output Folder**: Select a custom directory for saving downloaded files.
- **Cross-Platform**: Works on Windows, macOS, and Linux (with proper dependencies installed).
- **Windows Convenience**: Includes a `Run.bat` script for Windows users to automatically install dependencies and launch the application.

## Requirements
- **Python 3.6+**: Ensure Python is installed on your system.
- **yt-dlp**: The core library for downloading media.
- **FFmpeg**: Required for merging video and audio streams and embedding subtitles/thumbnails.
- **Tkinter**: Usually included with Python, used for the GUI.

## Installation
### Windows (Using Run.bat)
For Windows users, the provided `Run.bat` script automates the installation of dependencies (Python, FFmpeg, and yt-dlp) and launches the application. Follow these steps:

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/yourusername/tubecatcher.git
   cd tubecatcher
   ```
   Alternatively, download and extract the ZIP file from GitHub.

2. **Run the Batch File**:
   - Double-click `Run.bat` in the `tubecatcher` folder.
   - The script will:
     - Check for an internet connection.
     - Install Python 3.11.3 if not found.
     - Install FFmpeg if not found and add it to the system PATH.
     - Install or update `yt-dlp` using pip.
     - Launch the TubeCatcher GUI.
   - **Note**: You may need to run `Run.bat` as an administrator to install dependencies successfully. Right-click the file and select "Run as administrator."

3. **Verify Installation**:
   - If prompted, allow the script to download and install dependencies.
   - The GUI should launch automatically after setup.
  
## Why Not an Executable (.exe)?

TubeCatcher is distributed as a Python script (ytdlp5.py) with a Run.bat script for Windows, rather than a standalone executable (.exe). This design choice was made for the following reasons:
- Ease of Updating Dependencies: TubeCatcher relies on yt-dlp and FFmpeg, which are frequently updated to support new websites, fix bugs, and adapt to changes in platform APIs (e.g., YouTube). Bundling these dependencies into an .exe file using tools like PyInstaller would make it difficult for users to update yt-dlp and FFmpeg independently. By keeping the application as a Python script, users can easily update yt-dlp with pip install --upgrade yt-dlp or reinstall FFmpeg to ensure compatibility with the latest platforms.
- Flexibility and Transparency: A Python script allows users to inspect and modify the code if needed, fostering transparency and customization. An .exe file would obscure the code and make it harder for users to troubleshoot or extend functionality. 
- Smaller Distribution Size: An .exe file bundling Python, yt-dlp, FFmpeg, and Tkinter can be significantly larger (hundreds of MBs) compared to the lightweight Python script and Run.bat. Users with Python and FFmpeg installed can run TubeCatcher with minimal additional setup.
- Cross-Platform Compatibility: Distributing as a Python script ensures compatibility across Windows, macOS, and Linux without requiring separate executables for each platform. The Run.bat script simplifies setup for Windows users while maintaining flexibility for others.
- For convenience, the Run.bat script automates dependency installation and launching on Windows, providing a near-executable experience without the drawbacks of a static .exe file. Users can still update yt-dlp and FFmpeg as needed to maintain functionality.

### Manual Installation (Windows, macOS, Linux)
If you prefer manual setup or are using macOS/Linux, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/tubecatcher.git
   cd tubecatcher
   ```

2. **Install Python Dependencies**:
   Install `yt-dlp` using pip:
   ```bash
   pip install yt-dlp
   ```

3. **Install FFmpeg**:
   - **Windows**: Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or use a package manager like Chocolatey (`choco install ffmpeg`). Add `ffmpeg.exe` to your system PATH.
   - **macOS**: Install via Homebrew (`brew install ffmpeg`).
   - **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg` on Ubuntu/Debian).

4. **Run the Application**:
   ```bash
   python ytdlp5.py
   ```

   If you encounter a "yt-dlp not found" error, the application will prompt you to install it automatically. Ensure FFmpeg is installed and accessible in your PATH, or the application will display an error message.

## How to Use
### Using Run.bat (Windows)
1. **Double-Click Run.bat**:
   - Run `Run.bat` from the `tubecatcher` folder (use "Run as administrator" if prompted for permissions).
   - The script will check and install dependencies, then launch the TubeCatcher GUI.

2. **Follow GUI Instructions**:
   - Once the GUI opens, follow the steps below under "Using the GUI."

### Using the GUI
1. **Launch TubeCatcher**:
   - On Windows, use `Run.bat` or run `python ytdlp5.py`.
   - On macOS/Linux, run `python ytdlp5.py` from the terminal.

2. **Enter a URL**:
   Paste the URL of the video or audio you want to download (e.g., a YouTube video link) into the "Video URL" field.

3. **Fetch Formats**:
   Click the "Fetch Formats" button to retrieve available formats. The formats will appear in the dropdown menu, including options like "Best Video + Audio" for combined video and audio downloads.

4. **Select Format**:
   - Choose a format from the dropdown menu.
   - Check the "Audio Only" box to filter and download audio-only formats (e.g., MP3, M4A).
   - If a video-only format is selected, TubeCatcher will automatically pair it with the best audio stream to ensure the output includes both video and audio.

5. **Choose Output Folder**:
   Click the "Browse" button to select a directory for saving downloaded files. The default is the current directory.

6. **Configure Options**:
   - Check "Subtitles" to download and embed subtitles (if available).
   - Check "Thumbnail" to download and embed the video thumbnail in the output file.

7. **Start Download**:
   Click "Start Download" to begin downloading. The progress bar and console will show real-time download status.

8. **Stop Download**:
   Click the "Stop" button to cancel an ongoing download.

9. **View Output**:
   Once the download completes, a success message will appear, and the file will be saved in the specified output folder.

## Troubleshooting
- **No Audio in Videos**: Ensure FFmpeg is installed and added to your system PATH. TubeCatcher requires FFmpeg to merge video and audio streams. On Windows, `Run.bat` should handle FFmpeg installation, but verify it’s in your PATH if issues persist.
- **Formats Not Loading**: Check your internet connection and ensure the URL is valid. Some platforms may require additional configuration in `yt-dlp`.
- **Errors During Download**: Review the console output in the GUI for detailed error messages. Common issues include missing dependencies or invalid format selections.
- **Run.bat Issues (Windows)**:
  - If `Run.bat` fails, ensure you have an active internet connection.
  - Run the script as an administrator to allow dependency installation.
  - Check that sufficient disk space is available for downloading and extracting FFmpeg.

## Credits
- **yt-dlp Community**: TubeCatcher is built on top of the amazing [yt-dlp](https://github.com/yt-dlp/yt-dlp) library, a fork of youtube-dl. A huge thank you to the yt-dlp developers and contributors for their work in creating a robust and versatile tool for downloading online media.
- **FFmpeg**: Thanks to the FFmpeg team for providing the essential tools for media processing.
- **Tkinter**: The Python standard library's Tkinter module powers the GUI.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please submit issues or pull requests on the [GitHub repository](https://github.com/yourusername/tubecatcher). Ensure any changes are tested and maintain compatibility with `yt-dlp`.

## Support
If you find TubeCatcher useful, consider supporting the developer by visiting [Buy Me a Coffee](https://buymeacoffee.com/xuvidhah). Your support helps keep this project alive!
