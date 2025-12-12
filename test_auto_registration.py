#!/usr/bin/env python
"""
Test script for automated Twilio phone number registration
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.notifications import register_phone_with_twilio, send_whatsapp_welcome_message

def test_phone_registration():
    """Test the automated phone registration function"""
    print("Testing automated Twilio phone number registration...")
    
    # Test cases
    test_numbers = [
        "+9779807969278",  # Valid Nepal number with country code
        "9807969278",      # Nepal number without country code
        "09807969278",     # Nepal number with leading zero
        "+14155238886",    # US number (Twilio sandbox)
        "invalid-number",   # Invalid format
    ]
    
    for number in test_numbers:
        print(f"\nTesting number: {number}")
        result = register_phone_with_twilio(number)
        print(f"Result: {result}")
        
        if result['success']:
            print("✓ Registration successful")
            # Send welcome message
            welcome_result = send_whatsapp_welcome_message(result['formatted_number'])
            print(f"Welcome message result: {welcome_result}")
        else:
            print("✗ Registration failed")

if __name__ == "__main__":
    test_phone_registration()