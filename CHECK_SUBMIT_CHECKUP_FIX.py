#!/usr/bin/env python
"""
Script to verify the submit_checkup URL fix
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from django.urls import reverse

def check_submit_checkup_urls():
    """Check that the submit_checkup URLs work correctly"""
    print("=" * 50)
    print("CHECKING SUBMIT CHECKUP URL FIX")
    print("=" * 50)
    
    try:
        # Test reversing the URLs with profile types
        pregnant_url = reverse('submit_checkup', args=['pregnant'])
        mother_url = reverse('submit_checkup', args=['mother'])
        
        print("✅ URL reversal successful!")
        print(f"   Pregnant checkup URL: {pregnant_url}")
        print(f"   Mother checkup URL: {mother_url}")
        
        # Verify the URLs match the expected pattern
        expected_pregnant = '/submit-checkup/pregnant/'
        expected_mother = '/submit-checkup/mother/'
        
        if pregnant_url == expected_pregnant:
            print("✅ Pregnant URL pattern correct")
        else:
            print(f"❌ Pregnant URL mismatch. Expected: {expected_pregnant}, Got: {pregnant_url}")
            
        if mother_url == expected_mother:
            print("✅ Mother URL pattern correct")
        else:
            print(f"❌ Mother URL mismatch. Expected: {expected_mother}, Got: {mother_url}")
            
    except Exception as e:
        print(f"❌ Error reversing URLs: {e}")
    
    print("\n" + "=" * 50)
    print("URL FIX VERIFICATION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    check_submit_checkup_urls()