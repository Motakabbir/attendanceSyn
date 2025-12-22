#!/usr/bin/env python3
"""
Build script to create executable
Requires pyinstaller: pip install pyinstaller
"""

import os
import subprocess
import sys

def build_exe():
    print("Building Attendance Sync executable...")

    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Determine path separator for --add-data
    sep = ';' if os.name == 'nt' else ':'

    # PyInstaller command
    pyinstaller_path = os.path.join(os.path.dirname(sys.executable), 'pyinstaller')
    cmd = [
        pyinstaller_path,
        '--onefile',  # Single executable
        '--console',  # Show console for installer prompts
        '--name', 'AttendanceSyncInstaller',
        f'--add-data=requirements.txt{sep}.',
        f'--add-data=install.py{sep}.',
        f'--add-data=main.py{sep}.',
        f'--add-data=config.py{sep}.',
        f'--add-data=logger.py{sep}.',
        f'--add-data=mysql_reader.py{sep}.',
        f'--add-data=supabase_writer.py{sep}.',
        f'--add-data=.env{sep}.env',  # Include .env if exists
        'installer_main.py'  # New entry point
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Build successful! Executable created in dist/ folder")
        if os.name == 'nt':
            print("Run 'AttendanceSyncInstaller.exe' to install and start the service.")
        else:
            print("Note: Built on Linux. For Windows exe, run this script on Windows.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()