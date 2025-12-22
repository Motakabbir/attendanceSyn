#!/usr/bin/env python3
"""
Attendance Sync Installer
Sets up the environment variables for MySQL and Supabase connections.
"""

import os
import sys
from pathlib import Path

def get_input(prompt, default=None):
    if default:
        response = input(f"{prompt} (default: {default}): ").strip()
        return response if response else default
    else:
        return input(f"{prompt}: ").strip()

def main():
    print("Attendance Sync Service Installer")
    print("=" * 40)

    # Get current values if .env exists
    env_file = Path('.env')
    current_values = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    current_values[key] = value

    # Prompt for MySQL settings
    print("\nMySQL Configuration:")
    mysql_host = get_input("MySQL Host", current_values.get('MYSQL_HOST', 'localhost'))
    mysql_port = get_input("MySQL Port", current_values.get('MYSQL_PORT', '3306'))
    mysql_user = get_input("MySQL User", current_values.get('MYSQL_USER', 'root'))
    mysql_password = get_input("MySQL Password", current_values.get('MYSQL_PASSWORD', ''))
    mysql_database = get_input("MySQL Database", current_values.get('MYSQL_DATABASE', 'att'))

    # Prompt for Supabase settings
    print("\nSupabase Configuration:")
    supabase_url = get_input("Supabase URL", current_values.get('SUPABASE_URL', ''))
    supabase_key = get_input("Supabase Key", current_values.get('SUPABASE_KEY', ''))

    # Sync interval
    sync_interval = get_input("Sync Interval Seconds", current_values.get('SYNC_INTERVAL_SECONDS', '5'))

    # Write to .env
    env_content = f"""MYSQL_HOST={mysql_host}
MYSQL_PORT={mysql_port}
MYSQL_USER={mysql_user}
MYSQL_PASSWORD={mysql_password}
MYSQL_DATABASE={mysql_database}

SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}

SYNC_INTERVAL_SECONDS={sync_interval}
"""

    with open('.env', 'w') as f:
        f.write(env_content)

    print("\nConfiguration saved to .env")
    print("Run 'python main.py' to start the service.")

if __name__ == "__main__":
    main()