# Attendance Sync Service

A Python service that syncs attendance records from MySQL to Supabase in real-time.

## Installation

### Prerequisites
- Python 3.10+
- MySQL database with `attlog` table
- Supabase project

### Setup
1. Clone or download the project files.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the installer:
   ```
   python install.py
   ```
   This will prompt for MySQL and Supabase credentials and create/update the `.env` file.

### MySQL Schema Changes
Run this on your MySQL database:
```sql
ALTER TABLE attlog
ADD COLUMN synced_at DATETIME NULL,
ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
```

### Supabase Setup
1. Create `employees` table:
   ```sql
   CREATE TABLE employees (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       attendance_device_id VARCHAR(50)
   );
   ```
2. Create `attendance_records` table:
   ```sql
   CREATE TABLE attendance_records (
       employee_id UUID REFERENCES employees(id),
       date DATE,
       office_in_time TIME,
       office_out_time TIME,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW(),
       UNIQUE (employee_id, date)
   );
   ```

## Running the Service

### Windows (One-Click Setup)
1. Double-click `run_service.bat`.
2. The script will:
   - Create virtual environment if needed.
   - Install dependencies.
   - Run configuration setup (prompts for credentials).
   - Start the service in background.
   - Create a desktop shortcut for future use.

### Linux/Mac
```bash
python install.py  # Configure credentials
python main.py     # Run service
```

## Building Executable (Windows)
To create a standalone installer exe:
1. Install PyInstaller: `pip install pyinstaller`
2. Run: `python build_exe.py`
3. The exe `AttendanceSyncInstaller.exe` will be in `dist/` folder.
4. Distribute this single file - it includes everything needed.

## Using the Executable
- Double-click `AttendanceSyncInstaller.exe` on any Windows machine with Python installed.
- It will prompt for configuration if needed, then start the service in background.
- No additional files required!

## Updating Configuration
Run `python install.py` again to update credentials.

## Stopping the Service
- Linux/Mac: `Ctrl+C` or `pkill -f "python main.py"`
- Windows: Use Task Manager to kill the process.