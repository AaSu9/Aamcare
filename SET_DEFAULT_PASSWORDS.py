#!/usr/bin/env python
"""
Script to set default passwords for existing users
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from django.contrib.auth.models import User

def set_default_passwords():
    """Set default passwords for existing users"""
    print("=" * 50)
    print("SETTING DEFAULT PASSWORDS")
    print("=" * 50)
    
    # Users and their default passwords
    user_passwords = {
        'rita': 'password123',
        'sita': 'password123',
        'demo_mom': 'password123'
    }
    
    for username, password in user_passwords.items():
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"✓ Set password for user '{username}'")
        except User.DoesNotExist:
            print(f"✗ User '{username}' not found")
    
    print("\n" + "=" * 50)
    print("DEFAULT PASSWORDS SET")
    print("=" * 50)
    print("Users can now log in with:")
    for username, password in user_passwords.items():
        print(f"  {username}: {password}")

if __name__ == "__main__":
    set_default_passwords()