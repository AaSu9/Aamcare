import os
import django
from django.conf import settings

# Manual setup since we are running standalone
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
    django.setup()

from twilio.rest import Client

def send_test():
    sid = settings.TWILIO_ACCOUNT_SID
    token = settings.TWILIO_AUTH_TOKEN
    from_num = settings.TWILIO_FROM_NUMBER
    
    # Target number from user
    to_num = "9741690374"
    if not to_num.startswith('+'):
        to_num = f"+977{to_num}" # Assuming Nepal
    
    print(f"Debug Info:")
    print(f"SID: {sid[:5]}...")
    print(f"From: {from_num}")
    print(f"To: {to_num}")
    
    client = Client(sid, token)
    
    try:
        msg = client.messages.create(
            from_=from_num,
            body="🔴 AamCare System Test: If you see this, the connection is working!",
            to=f"whatsapp:{to_num}"
        )
        print(f"\nSUCCESS: Message accepted by Twilio.")
        print(f"SID: {msg.sid}")
        print(f"Status: {msg.status}")
        
        if msg.error_code:
            print(f"Error Code: {msg.error_code}")
            print(f"Error Msg: {msg.error_message}")
        else:
            print("\nIMPORTANT: If you did not receive this on your phone, you likely have not joined the Sandbox.")
            print(f"1. Save this number as a contact: {from_num.replace('whatsapp:', '')}")
            print("2. Open WhatsApp and send a message to it saying: join <your-sandbox-keyword>")
            print("(Check your Twilio Dashboard for the keyword)")
            
    except Exception as e:
        print(f"\nFAILED: {str(e)}")

if __name__ == "__main__":
    send_test()
