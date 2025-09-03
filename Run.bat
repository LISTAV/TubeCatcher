@echo off
setlocal


:: 1️⃣ Check Internet Connection
echo Checking internet connection...
ping -n 1 8.8.8.8 >nul 2>&1
if %errorlevel% neq 0 (
    echo No internet connection detected. Please connect to the internet and try again.
    pause
    exit /b 1
) else (
    echo Internet connection is available.
    ping 127.0.0.1 -n 1 -w 10 > nul
)

echo Checking dependencies...

:: 1️⃣ Install Python if missing
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Installing...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = 'TLS12'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe' -OutFile 'python_installer.exe'; Start-Process -FilePath 'python_installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait}"
    echo Python installed.
) else (
    echo Python is already installed.
    ping 127.0.0.1 -n 1 -w 10 > nul
)

:: 2️⃣ Install FFmpeg if missing
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo FFmpeg not found. Installing...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = 'TLS12'; Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'}"
    powershell -Command "Expand-Archive -Path ffmpeg.zip -DestinationPath ffmpeg-folder -Force"
    setx PATH "%CD%\ffmpeg-folder\bin;%PATH%"
    echo FFmpeg installed.
) else (
    echo FFmpeg is already installed.
    
)

:: 3️⃣ Install yt-dlp
where yt-dlp >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing yt-dlp...
    python -m pip install --upgrade yt-dlp
) else (
    echo yt-dlp is already installed.
    ping 127.0.0.1 -n 1 -w 20 > nul
)

:: 3️⃣ Update yt-dlp
echo Updating yt-dlp to the latest version...
python -m pip install --upgrade yt-dlp
echo yt-dlp is now up-to-date.
ping 127.0.0.1 -n 1 -w 20 > nul

:: 4️⃣ Run YTDL GUI and Force Normal Window Size
echo Starting YTDL GUI...
cd /d "%~dp0"  :: Ensure we are in the script's directory
start /b pythonw ytdlp6.py  :: Start the GUI without a console
powershell -Command "Start-Sleep -Milliseconds 70" >nul 2>&1
exit

