#!/usr/bin/env python3
"""
WhatsApp Business API Implementation Script for Aamcare

This script demonstrates how to implement WhatsApp Business API using your Twilio credentials.
It includes examples for sending messages, handling templates, and managing user registrations.

Credentials:
- Account SID: ACcd8a206b626859f47e411bf8c8f67674
- Auth Token: cbd0e2bad3a95a6ea02ee06a433f06b2
"""

import os
from twilio.rest import Client
from typing import Dict, Optional

class AamcareWhatsAppManager:
    def __init__(self):
        """Initialize WhatsApp manager with your Twilio credentials"""
        self.account_sid = 'ACcd8a206b626859f47e411bf8c8f67674'
        self.auth_token = 'cbd0e2bad3a95a6ea02ee06a433f06b2'
        self.whatsapp_number = '+12186169659'  # Your current US number
        
        try:
            self.client = Client(self.account_sid, self.auth_token)
            print("✅ WhatsApp Manager initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize WhatsApp Manager: {e}")
            self.client = None
    
    def check_account_status(self) -> Dict:
        """Check Twilio account status"""
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            return {
                "status": account.status,
                "type": account.type,
                "friendly_name": account.friendly_name
            }
        except Exception as e:
            return {"error": str(e)}
    
    def list_phone_numbers(self) -> Dict:
        """List all phone numbers in the account"""
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            numbers = self.client.incoming_phone_numbers.list()
            return {
                "count": len(numbers),
                "numbers": [
                    {
                        "friendly_name": num.friendly_name,
                        "phone_number": num.phone_number,
                        "capabilities": num.capabilities
                    }
                    for num in numbers
                ]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def send_test_message(self, to_number: str, message: str) -> Dict:
        """
        Send a test message (will only work if recipient has opted in)
        For production, use approved templates
        """
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            # This will work only if the number has opted in to your sandbox
            # For production, you'll need approved templates
            msg = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{to_number}'
            )
            return {
                "success": True,
                "message_sid": msg.sid,
                "status": msg.status
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def prepare_for_business_api(self) -> Dict:
        """
        Check what's needed to move to WhatsApp Business API
        """
        status = self.check_account_status()
        numbers = self.list_phone_numbers()
        
        recommendations = []
        
        # Check account type
        if status.get("type") == "Trial":
            recommendations.append("⚠️  Upgrade from Trial to Paid account for WhatsApp Business API access")
        
        # Check if using sandbox number
        if "+14155238886" in str(numbers):
            recommendations.append("⚠️  Currently using sandbox number - migrate to dedicated business number")
        else:
            recommendations.append("✅  Using dedicated phone number")
        
        # Check for Nepal number
        nepal_numbers = [num for num in numbers.get("numbers", []) 
                        if "+977" in num.get("phone_number", "")]
        if not nepal_numbers:
            recommendations.append("💡  Consider getting a Nepal phone number (+977) for better local recognition")
        
        return {
            "account_status": status,
            "phone_numbers": numbers,
            "recommendations": recommendations
        }

def main():
    """Main function to demonstrate WhatsApp API implementation"""
    print("🚀 Aamcare WhatsApp Business API Implementation")
    print("=" * 50)
    
    # Initialize the manager
    whatsapp_manager = AamcareWhatsAppManager()
    
    # Check account status
    print("\n🔍 Account Status:")
    status = whatsapp_manager.check_account_status()
    if "error" in status:
        print(f"❌ {status['error']}")
        return
    
    print(f"  Status: {status['status']}")
    print(f"  Type: {status['type']}")
    print(f"  Name: {status['friendly_name']}")
    
    # List phone numbers
    print("\n📞 Phone Numbers:")
    numbers = whatsapp_manager.list_phone_numbers()
    if "error" in numbers:
        print(f"❌ {numbers['error']}")
        return
    
    print(f"  Total: {numbers['count']}")
    for num in numbers['numbers']:
        print(f"  - {num['friendly_name']}: {num['phone_number']}")
        caps = num['capabilities']
        print(f"    Capabilities: SMS={caps.get('sms')}, MMS={caps.get('mms')}, Voice={caps.get('voice')}")
    
    # Prepare for Business API
    print("\n📋 Migration Preparation:")
    prep = whatsapp_manager.prepare_for_business_api()
    for rec in prep['recommendations']:
        print(f"  {rec}")
    
    # Example usage instructions
    print("\n📖 Next Steps:")
    print("1. Upgrade your Twilio account from Trial to Paid")
    print("2. Apply for WhatsApp Business API access in Twilio Console")
    print("3. Complete Facebook Business verification")
    print("4. Get a Nepal phone number for better local recognition")
    print("5. Create and submit message templates for approval")
    
    print("\n📝 For Testing (Limited):")
    print("# Send a test message (recipient must opt-in first)")
    print("# whatsapp_manager.send_test_message('+977XXXXXXXXX', 'Hello from Aamcare!')")
    
    print("\n💡 Production Implementation:")
    print("# Use approved templates with content variables")
    print("# Implement proper error handling and logging")
    print("# Set up webhooks for delivery confirmations")

if __name__ == "__main__":
    main()