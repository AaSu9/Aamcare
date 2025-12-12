from twilio.rest import Client

# Your Twilio credentials
account_sid = 'ACcd8a206b626859f47e411bf8c8f67674'
auth_token = 'cbd0e2bad3a95a6ea02ee06a433f06b2'

try:
    client = Client(account_sid, auth_token)
    print("✅ Twilio credentials are valid")
    
    # Check if we can access the account
    account = client.api.accounts(account_sid).fetch()
    print(f"✅ Account status: {account.status}")
    
    # Try to list available phone numbers
    incoming_phone_numbers = client.incoming_phone_numbers.list(limit=10)
    print(f"📞 Phone numbers available: {len(incoming_phone_numbers)}")
    
    if incoming_phone_numbers:
        for number in incoming_phone_numbers:
            print(f"  - {number.friendly_name} ({number.phone_number})")
    
    # Check for WhatsApp-enabled numbers
    try:
        # This will show if you have WhatsApp-enabled numbers
        phone_numbers = client.api.account.incoming_phone_numbers.list()
        whatsapp_numbers = [num for num in phone_numbers if hasattr(num, 'capabilities') and num.capabilities.get('sms')]
        print(f"📱 SMS-capable numbers: {len(whatsapp_numbers)}")
    except Exception as e:
        print(f"ℹ️  Note on WhatsApp check: {str(e)}")
        
    print("\n📝 Next steps:")
    print("1. If you don't see a WhatsApp-enabled number above, you'll need to:")
    print("   - Get a dedicated phone number from Twilio")
    print("   - Enable it for WhatsApp Business API")
    print("   - Complete Facebook Business verification")
    print("\n2. If you do see numbers, check the Twilio Console for WhatsApp setup")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\n🔧 Troubleshooting:")
    print("- Verify your credentials are correct")
    print("- Ensure you have internet connectivity")
    print("- Check if Twilio package is installed: pip install twilio")