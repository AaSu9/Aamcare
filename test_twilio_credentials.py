import os
import django
from twilio.rest import Client

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from django.conf import settings

def test_twilio_connection():
    """Test Twilio connection with current credentials"""
    print("Testing Twilio Connection...")
    
    # Get credentials from Django settings
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)
    
    print(f"Account SID: {account_sid}")
    print(f"Auth Token: {auth_token[:5]}...{auth_token[-5:] if auth_token else 'None'}")
    print(f"WhatsApp Number: {whatsapp_number}")
    
    if not all([account_sid, auth_token, whatsapp_number]):
        print("❌ Missing Twilio credentials in settings")
        return False
    
    try:
        # Try to create client
        client = Client(account_sid, auth_token)
        print("✅ Twilio client created successfully")
        
        # Try to fetch account details
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Account status: {account.status}")
        print(f"✅ Account type: {account.type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Twilio connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_twilio_connection()