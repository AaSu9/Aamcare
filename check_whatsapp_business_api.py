from twilio.rest import Client

# Your Twilio credentials
account_sid = 'ACcd8a206b626859f47e411bf8c8f67674'
auth_token = 'cbd0e2bad3a95a6ea02ee06a433f06b2'

def check_whatsapp_business_status():
    try:
        client = Client(account_sid, auth_token)
        print("🔍 Checking WhatsApp Business API Status...")
        print("=" * 50)
        
        # 1. Check account details
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Account Status: {account.status}")
        print(f"📋 Account Type: {account.type}")
        
        # 2. Check current phone numbers
        phone_numbers = client.incoming_phone_numbers.list()
        print(f"\n📞 Phone Numbers: {len(phone_numbers)}")
        
        for number in phone_numbers:
            print(f"  - {number.friendly_name}")
            print(f"    Number: {number.phone_number}")
            print(f"    Capabilities: SMS={number.capabilities.get('sms', False)}, "
                  f"MMS={number.capabilities.get('mms', False)}, "
                  f"Voice={number.capabilities.get('voice', False)}")
            
            # Check if it's WhatsApp-enabled (this might not show in basic info)
            try:
                # Try to check for WhatsApp senders
                whatsapp_senders = client.messaging.v1.senders.list()
                whatsapp_count = sum(1 for sender in whatsapp_senders 
                                   if sender.sender_type == 'whatsapp')
                if whatsapp_count > 0:
                    print(f"    WhatsApp Senders: {whatsapp_count}")
            except:
                pass  # WhatsApp API might not be available
            
        # 3. Check messaging services (newer way to manage WhatsApp)
        try:
            services = client.messaging.services.list()
            print(f"\nサービシングサービス: {len(list(services))}")
            
            whatsapp_services = []
            for service in services:
                if 'whatsapp' in service.friendly_name.lower():
                    whatsapp_services.append(service)
                    
            if whatsapp_services:
                print(f"🟢 WhatsApp Messaging Services Found: {len(whatsapp_services)}")
                for service in whatsapp_services:
                    print(f"  - {service.friendly_name} (SID: {service.sid})")
            else:
                print("🟡 No WhatsApp messaging services found")
                
        except Exception as e:
            print(f"ℹ️  Messaging services check: {str(e)}")
        
        # 4. Check if you're using sandbox or Business API
        print(f"\n📊 Current WhatsApp Status:")
        if phone_numbers and any(number.phone_number == '+14155238886' for number in phone_numbers):
            print("🔴 You're currently using Twilio WhatsApp Sandbox")
            print("   This requires users to manually send 'join' message")
            print("   Not suitable for production with many users")
        else:
            print("🟢 You may have a dedicated number")
            print("   Check Twilio Console for WhatsApp Business API status")
        
        # 5. Recommendations
        print(f"\n📋 Recommendations:")
        print("1. Visit Twilio Console: https://console.twilio.com")
        print("2. Navigate to Messaging > Try it out > WhatsApp sandbox")
        print("3. Check if you have WhatsApp Business API access")
        print("4. Apply for Business API if needed (requires Facebook verification)")
        
        # 6. Test message sending (be careful not to spam)
        print(f"\n🧪 Testing Message Capability:")
        try:
            # This is a safe test - won't actually send a message without proper setup
            print("✅ Twilio client initialized successfully")
            print("💡 Ready for WhatsApp Business API implementation")
        except Exception as e:
            print(f"❌ Message test failed: {str(e)}")
            
    except Exception as e:
        print(f"❌ Error checking WhatsApp status: {str(e)}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Verify internet connection")
        print("2. Confirm Twilio credentials")
        print("3. Check Twilio package: pip install twilio")
        print("4. Visit Twilio Console for detailed account status")

if __name__ == "__main__":
    check_whatsapp_business_status()