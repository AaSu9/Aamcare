import os
import django
from twilio.rest import Client

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.models import PregnantWomanProfile, NewMotherProfile

# Twilio credentials from your account
TWILIO_ACCOUNT_SID = 'ACcd8a206b626859f47e411bf8c8f67674'
TWILIO_AUTH_TOKEN = 'cbd0e2bad3a95a6ea02ee06a433f06b2'
TWILIO_WHATSAPP_NUMBER = '+12186169659'  # Your current US number

def send_whatsapp_message(to_number, message_body):
    """Send a WhatsApp message using Twilio"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format the phone number (ensure it has +country_code)
        if not to_number.startswith('+'):
            # Assuming Nepal numbers, add +977 country code
            if to_number.startswith('98') or to_number.startswith('97'):
                formatted_number = f'+977{to_number}'
            else:
                formatted_number = f'+{to_number}'
        else:
            formatted_number = to_number
            
        message = client.messages.create(
            body=message_body,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{formatted_number}'
        )
        
        print(f"✅ Message sent to {formatted_number}")
        print(f"   SID: {message.sid}")
        print(f"   Status: {message.status}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send message to {to_number}: {str(e)}")
        return False

def get_all_user_phone_numbers():
    """Get all phone numbers from registered users"""
    phone_numbers = []
    
    # Get pregnant women phone numbers
    for user in PregnantWomanProfile.objects.all():
        if user.phone_number:
            phone_numbers.append(user.phone_number)
    
    # Get new mothers phone numbers
    for user in NewMotherProfile.objects.all():
        if user.phone_number:
            phone_numbers.append(user.phone_number)
            
    return phone_numbers

def send_message_to_all_users():
    """Send a message to all registered users"""
    print("📢 Sending Message to All Registered Users")
    print("=" * 45)
    
    # Get all user phone numbers
    phone_numbers = get_all_user_phone_numbers()
    
    if not phone_numbers:
        print("❌ No phone numbers found for registered users")
        return
    
    print(f"📱 Found {len(phone_numbers)} registered users")
    for i, number in enumerate(phone_numbers, 1):
        print(f"   {i}. {number}")
    
    # Message to send
    message_body = (
        "🏥 Hello from Aamcare Health!\n\n"
        "This is a test message to all registered users. "
        "In the future, you'll receive daily health tips at 7 AM.\n\n"
        "Stay healthy! 💪"
    )
    
    print(f"\n💬 Message Content:")
    print("-" * 20)
    print(message_body)
    print("-" * 20)
    
    # Send message to each user
    success_count = 0
    fail_count = 0
    
    print(f"\n🚀 Sending Messages...")
    print("-" * 20)
    
    for number in phone_numbers:
        if send_whatsapp_message(number, message_body):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n📊 Sending Summary:")
    print("-" * 20)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📈 Total: {len(phone_numbers)}")
    
    # Important note
    print(f"\n⚠️  Important Note:")
    print(f"   If messages failed, it's likely because recipients haven't opted in to your WhatsApp sandbox.")
    print(f"   They need to send 'join aamcare' to +14155238886 to receive messages.")

if __name__ == "__main__":
    send_message_to_all_users()