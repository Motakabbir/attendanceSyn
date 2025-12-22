#!/usr/bin/env python3
"""
Main entry point for the Attendance Sync executable.
Handles installation and service startup.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_installer():
    """Run the installer if .env doesn't exist or is incomplete."""
    env_file = Path('.env')
    if not env_file.exists():
        print("Configuration not found. Running setup...")
        result = subprocess.run([sys.executable, 'install.py'], capture_output=False)
        if result.returncode != 0:
            print("Installation failed.")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        # Check if required values are present
        with open(env_file, 'r') as f:
            content = f.read()
        required = ['MYSQL_HOST=', 'SUPABASE_URL=', 'SUPABASE_KEY=']
        if not all(req in content for req in required):
            print("Configuration incomplete. Running setup...")
            result = subprocess.run([sys.executable, 'install.py'], capture_output=False)
            if result.returncode != 0:
                print("Installation failed.")
                input("Press Enter to exit...")
                sys.exit(1)

def start_service():
    """Start the sync service in background."""
    print("Starting Attendance Sync Service...")
    try:
        # On Windows, use pythonw to run without console
        if os.name == 'nt':
            subprocess.Popen([sys.executable, 'main.py'], creationflags=subprocess.DETACHED_PROCESS)
        else:
            subprocess.Popen([sys.executable, 'main.py'])
        print("Service started successfully!")
        print("The service is running in the background.")
        print("You can close this window.")
    except Exception as e:
        print(f"Failed to start service: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def main():
    print("Attendance Sync Service")
    print("=" * 25)

    # Run installer if needed
    run_installer()

    # Start the service
    start_service()

    # Keep window open briefly
    time.sleep(2)

if __name__ == "__main__":
    main()