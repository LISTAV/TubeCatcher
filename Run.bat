@echo off
setlocal

:: ============================================================================
:: TubeCatcher Dependency Installer
:: This script checks for and installs Python, FFmpeg, and yt-dlp.
:: It must be run as an Administrator.
:: ============================================================================
title TubeCatcher Setup

:: 1️⃣ Administrator Check
echo Checking for Administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] This script requires Administrator privileges.
    echo Please right-click the file and select "Run as administrator".
    pause
    exit /b
)
echo Privileges OK.


:: 2️⃣ Internet Connection Check
echo.
echo Checking internet connection...
ping -n 1 8.8.8.8 >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No internet connection detected. Please connect and try again.
    pause
    exit /b
)
echo Connection OK.


:: 3️⃣ Python Check & Installation
:CheckPython
echo.
echo Checking for Python...
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Python is already installed.
    goto CheckFFmpeg
)

echo Python not found. Starting installation...
echo Downloading Python installer...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = 'TLS12'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe' -OutFile 'python_installer.exe'}"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to download Python.
    pause
    exit /b
)

echo Installing Python silently...
start /wait "" "python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
del "python_installer.exe"

echo.
echo Python has been installed successfully.
echo You may need to run this script again for the changes to take effect.
pause
exit /b


:: 4️⃣ FFmpeg Check & Installation
:CheckFFmpeg
echo.
echo Checking for FFmpeg...
where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    echo FFmpeg is already installed.
    goto CheckYTDLP
)

echo FFmpeg not found. Starting installation...
set "FFMPEG_DIR=%~dp0ffmpeg"
if not exist "%FFMPEG_DIR%" mkdir "%FFMPEG_DIR%"

echo Downloading FFmpeg...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = 'TLS12'; Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile '%FFMPEG_DIR%\ffmpeg.zip'}"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to download FFmpeg.
    pause
    exit /b
)

echo Extracting FFmpeg...
powershell -Command "Expand-Archive -Path '%FFMPEG_DIR%\ffmpeg.zip' -DestinationPath '%FFMPEG_DIR%' -Force"
del "%FFMPEG_DIR%\ffmpeg.zip"

:: Find the versioned subfolder and add its 'bin' directory to the session PATH
for /d %%i in ("%FFMPEG_DIR%\ffmpeg-*") do (
    set "FFMPEG_BIN_PATH=%%i\bin"
)

echo Setting FFmpeg path for this session...
set "PATH=%FFMPEG_BIN_PATH%;%PATH%"

echo FFmpeg is ready.


:: 5️⃣ yt-dlp Check & Update
:CheckYTDLP
echo.
echo Checking for and updating yt-dlp...
python -m pip install --upgrade --no-warn-script-location yt-dlp
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install/update yt-dlp.
    pause
    exit /b
)
echo yt-dlp is installed and up-to-date.


:: 6️⃣ Run the GUI Application
:RunGUI
echo.
echo All dependencies are ready. Starting the application...
cd /d "%~dp0"
start "" /b pythonw ytdlp6.py

timeout /t 2 >nul
exit
