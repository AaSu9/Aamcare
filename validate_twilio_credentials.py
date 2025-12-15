#!/usr/bin/env python
"""
Script to validate Twilio credentials
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from aamcare.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def validate_credentials():
    print("Validating Twilio credentials...")
    print(f"Account SID: {TWILIO_ACCOUNT_SID[:10]}...{TWILIO_ACCOUNT_SID[-5:]}")
    print(f"Auth Token length: {len(TWILIO_AUTH_TOKEN)} characters")
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # Try to fetch the account details
        account = client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
        print(f"✅ SUCCESS: Account status is '{account.status}'")
        print(f"✅ Account type: {account.type}")
        return True
    except TwilioRestException as e:
        print(f"❌ FAILED: Twilio API error - {e}")
        print(f"Error code: {e.code}")
        print(f"More info: {e.uri}")
        return False
    except Exception as e:
        print(f"❌ FAILED: General error - {e}")
        return False

if __name__ == "__main__":
    validate_credentials()