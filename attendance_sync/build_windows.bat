@echo off
REM Windows Build Script for Attendance Sync Installer
REM Run this on Windows to create the executable

echo Building Attendance Sync Installer for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.10+ is required.
    echo Download from: https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Build the executable
echo Building executable...
python build_exe.py

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Executable created in dist\ folder
    echo Copy AttendanceSyncInstaller.exe to target Windows machines.
    echo.
) else (
    echo Build failed!
)

pause