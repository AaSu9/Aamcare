#!/usr/bin/env python3
"""
WhatsApp Opt-in Helper for Aamcare

This script helps users opt-in to WhatsApp notifications by providing
clear instructions and verifying the opt-in process.
"""

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.models import PregnantWomanProfile, NewMotherProfile
from django.core.management.base import BaseCommand

class WhatsAppOptInHelper:
    def __init__(self):
        self.whatsapp_sandbox_number = "+14155238886"
        self.whatsapp_keyword = "join aamcare"
    
    def get_all_users_with_phones(self):
        """Get all users with phone numbers"""
        users = []
        
        # Get pregnant women
        for profile in PregnantWomanProfile.objects.all():
            if profile.phone_number:
                users.append({
                    'type': 'pregnant',
                    'name': profile.name,
                    'phone': profile.phone_number,
                    'profile': profile
                })
        
        # Get new mothers
        for profile in NewMotherProfile.objects.all():
            if profile.phone_number:
                users.append({
                    'type': 'mother',
                    'name': profile.name,
                    'phone': profile.phone_number,
                    'profile': profile
                })
        
        return users
    
    def generate_opt_in_instructions(self):
        """Generate clear opt-in instructions for users"""
        instructions = f"""
📱 WhatsApp Opt-in Instructions for Aamcare Notifications
=====================================================

To receive health notifications via WhatsApp, please follow these steps:

1. Open WhatsApp on your phone
2. Tap the chat icon (new message)
3. Type "{self.whatsapp_sandbox_number}" in the search box
4. Select the number when it appears
5. Save this number as "Aamcare Health" (optional but recommended)
6. Send this exact message: "{self.whatsapp_keyword}"

✅ After sending the message, you'll receive a confirmation
✅ You'll then start receiving daily health tips and vaccine reminders

Important Notes:
- This is a one-time process
- You only need to do this once
- After opt-in, you'll receive automated messages at 7 AM daily
- Reply "stop" at any time to unsubscribe

Users who need to opt-in:
"""
        
        users = self.get_all_users_with_phones()
        for i, user in enumerate(users, 1):
            instructions += f"{i}. {user['name']} ({user['phone']})\n"
        
        instructions += f"""
Need Help?
Contact: [Your support contact information]

Technical Note:
This is a temporary requirement while we migrate to WhatsApp Business API,
which will eliminate the need for manual opt-in.
"""
        
        return instructions
    
    def print_opt_in_status(self):
        """Print current opt-in status for all users"""
        print("Current WhatsApp Opt-in Status:")
        print("=" * 40)
        
        users = self.get_all_users_with_phones()
        if not users:
            print("No users with phone numbers found.")
            return
        
        for user in users:
            status = "❓ Unknown"  # We don't have a field to track this yet
            print(f"{user['name']} ({user['phone']}): {status}")
    
    def send_opt_in_reminder(self):
        """In a real implementation, this would send SMS/email reminders"""
        print("Opt-in Reminder Messages (Sample):")
        print("=" * 40)
        
        users = self.get_all_users_with_phones()
        for user in users:
            message = f"""Hi {user['name']}!

To receive daily health tips and vaccine reminders from Aamcare, please opt-in to WhatsApp notifications:

1. Save {self.whatsapp_sandbox_number} as "Aamcare Health"
2. Send "{self.whatsapp_keyword}" to that number

This is a one-time process. After opt-in, you'll receive automated messages at 7 AM daily.

Thank you for using Aamcare!"""
            
            print(f"To {user['name']} ({user['phone']}):")
            print(message)
            print("-" * 30)

def main():
    helper = WhatsAppOptInHelper()
    
    print("Aamcare WhatsApp Opt-in Helper")
    print("=" * 40)
    
    # Show instructions
    print(helper.generate_opt_in_instructions())
    
    print("\n" + "=" * 40)
    
    # Show current status
    helper.print_opt_in_status()
    
    print("\n" + "=" * 40)
    
    # Show reminder messages
    helper.send_opt_in_reminder()

if __name__ == "__main__":
    main()