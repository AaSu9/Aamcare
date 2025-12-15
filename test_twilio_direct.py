#!/usr/bin/env python
"""
Direct HTTP test for Twilio credentials
"""
import requests
import base64
from aamcare.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

def test_twilio_credentials():
    print("Testing Twilio credentials with direct HTTP request...")
    print(f"Account SID: {TWILIO_ACCOUNT_SID[:10]}...{TWILIO_ACCOUNT_SID[-5:]}")
    
    # Create basic auth header
    credentials = base64.b64encode(f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}".encode()).decode()
    
    # Test endpoint
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}.json"
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json",
        "User-Agent": "Aamcare Direct Test"
    }
    
    print(f"Testing URL: {url}")
    print("Sending request...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Credentials are valid!")
            print(f"Account Status: {data.get('status', 'Unknown')}")
            print(f"Account Type: {data.get('type', 'Unknown')}")
            return True
        else:
            print(f"❌ Credentials invalid or account issue")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_twilio_credentials()