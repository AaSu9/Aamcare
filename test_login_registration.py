#!/usr/bin/env python
"""
Test script for login and registration functionality
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import PregnantWomanProfile, NewMotherProfile

def test_user_setup():
    """Test that users and profiles are properly set up"""
    print("=" * 50)
    print("USER AND PROFILE SETUP TEST")
    print("=" * 50)
    
    # Check all users
    print("1. Existing Users:")
    users = User.objects.all()
    for user in users:
        print(f"   - {user.username} (superuser: {user.is_superuser})")
        
        # Check if user has a pregnant profile
        try:
            profile = PregnantWomanProfile.objects.get(user=user)
            print(f"     → Pregnant profile: {profile.name} ({profile.phone_number})")
        except PregnantWomanProfile.DoesNotExist:
            pass
            
        # Check if user has a mother profile
        try:
            profile = NewMotherProfile.objects.get(user=user)
            print(f"     → Mother profile: {profile.name} ({profile.phone_number})")
        except NewMotherProfile.DoesNotExist:
            pass
    
    print(f"\n2. Profile Counts:")
    print(f"   Pregnant women profiles: {PregnantWomanProfile.objects.count()}")
    print(f"   New mother profiles: {NewMotherProfile.objects.count()}")
    
    print("\n3. Login Test URLs:")
    print("   Admin login: http://127.0.0.1:8000/admin/")
    print("   User login: http://127.0.0.1:8000/login/")
    print("   Register as pregnant: http://127.0.0.1:8000/register/pregnant/")
    print("   Register as mother: http://127.0.0.1:8000/register/mother/")
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    test_user_setup()