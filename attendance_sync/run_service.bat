@echo off
REM One-Click Attendance Sync Installer and Launcher
REM This script sets up everything and runs the service

echo Attendance Sync Service Setup and Launcher
echo ===========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if not installed
if not exist venv\Lib\site-packages\mysql (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Run installer if .env doesn't exist or is incomplete
if not exist .env (
    echo Running configuration setup...
    python install.py
    if %errorlevel% neq 0 (
        echo ERROR: Configuration setup failed.
        pause
        exit /b 1
    )
) else (
    REM Check if .env has required values
    findstr /C:"MYSQL_HOST=" .env >nul
    if %errorlevel% neq 0 (
        echo Running configuration setup...
        python install.py
    )
)

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Attendance Sync.lnk'))
$Shortcut.TargetPath = '%~f0'
$Shortcut.WorkingDirectory = '%~dp0'
$Shortcut.Description = 'Start Attendance Sync Service'
$Shortcut.Save()
"

echo Starting Attendance Sync Service in background...
start /B python main.py

echo.
echo Service started successfully!
echo A shortcut 'Attendance Sync' has been created on your desktop.
echo Use it to start the service in the future.
echo.
echo Press any key to exit...
pause >nul