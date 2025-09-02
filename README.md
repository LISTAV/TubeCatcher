TubeCatcher - A Simple YouTube Downloader GUI

TubeCatcher is a user-friendly, cross-platform desktop application for downloading videos and audio from YouTube and other video sites. It uses the powerful yt-dlp backend, providing a graphical interface to manage your downloads.
Features

    Download Videos & Audio: Easily download videos in your desired quality or extract just the audio.

    Format Selection: Fetch all available formats for a given URL and choose the one you want.

    Progress Bar: Monitor the download progress in real-time.

    Output Folder: Select a custom location to save your downloaded files.

    Additional Options: Download subtitles and video thumbnails.

    Dependency Management: The Run.bat script automatically checks for and installs required dependencies like Python and FFmpeg on Windows, making it easy to get started.

How to Use

    Run the application:

        On Windows, simply double-click the Run.bat file. This script will automatically handle the initial setup for you.

        On other systems, you will need to manually install Python, FFmpeg, and yt-dlp first. Then, you can run the app directly using Python: python ytdlp6.py.

    Enter a URL: Paste the URL of the YouTube video you want to download into the "Video URL" text box.

    Fetch Formats: Click the "Fetch Formats" button. This will populate a dropdown menu with all the available download options.

    Select a Format: Choose your desired format from the dropdown. You can also check the "Audio Only" box to filter for audio-only formats.

    Set Output Folder: Click "Browse" to select where you want to save the downloaded file. By default, it will save to the same folder where the app is located.

    Start Download: Click the "Start Download" button to begin the process. You can monitor the progress in the console log and the progress bar.

    Stop Download: You can click the "Stop" button at any time to cancel an ongoing download.

Dependencies

This application relies on the following open-source tools:

    Python: A versatile programming language. The Windows batch script will automatically download and install Python 3.11.3 for you if it's not detected.

    yt-dlp: A powerful command-line program to download videos from YouTube and a variety of other video sites. It is installed automatically by the Python pip package manager if it's not found.

    FFmpeg: A powerful and essential tool for processing multimedia files, required for merging video and audio streams into a single file. The Windows batch script will automatically install FFmpeg for you if it's not detected.

Credits

This tool would not be possible without the incredible work of the following open-source projects. A huge thank you to:

    yt-dlp: For providing the core functionality that powers this application. Their work is invaluable to the community.

    FFmpeg: For their robust and reliable multimedia framework.

    The Python community: For the language and its amazing ecosystem, including libraries like tkinter for the GUI.
