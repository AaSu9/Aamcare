#!/usr/bin/env python3
"""
Scheduler script for Aamcare daily notifications.
This script sets up a Windows Task Scheduler task to run daily notifications at 7 AM Nepali time.
"""

import os
import sys
import subprocess
import winreg
from datetime import datetime, timedelta

def check_python_installed():
    """Check if Python is installed and accessible"""
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_windows_scheduler_task():
    """Create a Windows Task Scheduler task to run daily notifications at 7 AM Nepal time"""
    
    # Calculate 7 AM Nepal time (UTC+5:45)
    # Nepal time is UTC+5:45, so we need to convert to local system time
    nepal_offset = timedelta(hours=5, minutes=45)
    
    # For demonstration, we'll create a task that runs daily at 7 AM
    # In a real scenario, you'd adjust this based on your system's time zone
    
    task_name = "Aamcare_Daily_Notifications"
    
    # Path to the project directory
    project_path = os.path.abspath(".")
    bat_file = os.path.join(project_path, "run_notifications.bat")
    
    # Create the task using schtasks command
    task_command = [
        'schtasks', '/create', 
        '/tn', task_name,
        '/tr', f'"{bat_file}"',
        '/sc', 'daily',
        '/st', '07:00',  # 7 AM
        '/f'  # Force creation (overwrite if exists)
    ]
    
    try:
        result = subprocess.run(task_command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Windows Task Scheduler task created successfully!")
            print(f"Task Name: {task_name}")
            print(f"Execution Time: Daily at 7:00 AM")
            print(f"Command: {bat_file}")
            return True
        else:
            print(f"❌ Failed to create scheduler task: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error creating scheduler task: {str(e)}")
        return False

def setup_nepal_time_zone():
    """Provide instructions for setting up Nepal time zone"""
    print("\n🕐 Nepal Time Zone Information:")
    print("Nepal Time (NPT) is UTC+5:45")
    print("To ensure accurate timing, make sure your system clock is set correctly.")
    print("\nIf you need to adjust for Nepal time specifically:")
    print("1. Windows automatically handles time zones")
    print("2. The scheduler will run at 7 AM according to your system's local time")
    print("3. If your system is in a different time zone, adjust the scheduled time accordingly")

def main():
    print("📅 Aamcare Daily Notification Scheduler Setup")
    print("=" * 50)
    
    # Check if we're in the correct directory
    if not os.path.exists("manage.py"):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Check Python installation
    if not check_python_installed():
        print("❌ Error: Python not found. Please ensure Python is installed and in your PATH.")
        return False
    
    print("✅ Prerequisites check passed")
    
    # Setup Nepal time information
    setup_nepal_time_zone()
    
    # Create Windows scheduler task
    print("\n🔧 Creating Windows Task Scheduler Task...")
    success = create_windows_scheduler_task()
    
    if success:
        print("\n🎉 Setup Complete!")
        print("The daily notification system will now run automatically at 7 AM.")
        print("\nTo manually test the notifications, run:")
        print("  python manage.py send_daily_notifications")
        print("\nTo check the scheduled task, open Task Scheduler and look for 'Aamcare_Daily_Notifications'")
    else:
        print("\n⚠️  Setup failed. You can still run notifications manually:")
        print("  python manage.py send_daily_notifications")
    
    return success

if __name__ == "__main__":
    main()