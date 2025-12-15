#!/usr/bin/env python3
"""
WhatsApp User Opt-in Manager for Aamcare

This script helps manage the WhatsApp opt-in process for users,
providing instructions and tracking opt-in status.
"""

import os
import django
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.models import PregnantWomanProfile, NewMotherProfile

class WhatsAppOptInManager:
    def __init__(self):
        self.sandbox_number = "+14155238886"
        self.join_keyword = "join aamcare"
    
    def get_all_users(self):
        """Get all users with phone numbers"""
        users = []
        
        # Get pregnant women
        for profile in PregnantWomanProfile.objects.all():
            if profile.phone_number:
                users.append({
                    'id': profile.id,
                    'type': 'pregnant',
                    'name': profile.name,
                    'phone': profile.phone_number,
                    'profile': profile
                })
        
        # Get new mothers
        for profile in NewMotherProfile.objects.all():
            if profile.phone_number:
                users.append({
                    'id': profile.id,
                    'type': 'mother',
                    'name': profile.name,
                    'phone': profile.phone_number,
                    'profile': profile
                })
        
        return users
    
    def print_opt_in_instructions(self):
        """Print detailed opt-in instructions"""
        print("=" * 60)
        print("📱 AAMCARE WHATSAPP OPT-IN INSTRUCTIONS")
        print("=" * 60)
        print()
        print("To receive daily health tips and vaccine reminders via WhatsApp:")
        print()
        print("STEP-BY-STEP GUIDE:")
        print("──────────────────")
        print("1. Open WhatsApp on your mobile phone")
        print("2. Tap the 'Chat' icon (pencil and paper) to start a new chat")
        print(f"3. Type '{self.sandbox_number}' in the search/contact field")
        print("4. Tap on the number when it appears in search results")
        print("5. (Optional) Save the contact as 'Aamcare Health'")
        print(f"6. Send this exact message: '{self.join_keyword}'")
        print()
        print("✅ WHAT HAPPENS NEXT:")
        print("────────────────────")
        print("• You'll receive a confirmation message from WhatsApp")
        print("• You'll then receive a welcome message from Aamcare")
        print("• Starting tomorrow, you'll get daily health tips at 7 AM")
        print()
        print("⚠️  IMPORTANT NOTES:")
        print("────────────────────")
        print("• This is a ONE-TIME process")
        print("• You only need to do this once")
        print("• After opt-in, messages come automatically at 7 AM daily")
        print("• Reply 'stop' anytime to unsubscribe")
        print("• Standard messaging rates may apply")
        print()
    
    def list_users_needing_opt_in(self):
        """List all users who need to opt-in"""
        users = self.get_all_users()
        
        if not users:
            print("No users with phone numbers found.")
            return
        
        print("USERS WHO NEED TO OPT-IN:")
        print("─────────────────────────")
        for i, user in enumerate(users, 1):
            print(f"{i:2d}. {user['name']:<20} ({user['phone']}) [{user['type'].upper()}]")
        print()
        print(f"Total users needing opt-in: {len(users)}")
        print()
    
    def generate_individual_messages(self):
        """Generate personalized opt-in messages for each user"""
        users = self.get_all_users()
        
        if not users:
            print("No users found.")
            return
        
        print("PERSONALIZED OPT-IN MESSAGES:")
        print("─────────────────────────────")
        
        for user in users:
            message = f"""नमस्ते {user['name']}!

Aamcare स्वास्थ्य सेवाबाट दैनिक स्वास्थ्य टिप्स र खोप रिमाइन्डर प्राप्त गर्न:

1. WhatsApp मा '{self.sandbox_number}' सेभ गर्नुहोस्
2. '{self.join_keyword}' सन्देश पठाउनुहोस्

एक पटक मात्र गर्नुपर्नेछ। पछि सबै बिहान 7 बजे स्वचालित सन्देश प्राप्त हुनेछ।

धन्यवाद!"""

            print(f"To {user['name']} ({user['phone']}):")
            print("-" * 40)
            print(message)
            print()
    
    def generate_qr_code_instructions(self):
        """Generate QR code-based opt-in instructions"""
        print("QR CODE OPT-IN METHOD:")
        print("──────────────────────")
        print("For easier opt-in, you can also:")
        print()
        print("1. Ask users to scan this QR code with their phone camera:")
        print("   [QR CODE PLACEHOLDER - Would contain WhatsApp URL]")
        print()
        print("2. Or click this link on their mobile device:")
        print(f"   https://wa.me/{self.sandbox_number.replace('+', '')}?text={self.join_keyword.replace(' ', '%20')}")
        print()
        print("This will pre-fill the message and open directly in WhatsApp.")

def main():
    manager = WhatsAppOptInManager()
    
    print("Aamcare WhatsApp Opt-in Manager")
    print("=" * 40)
    print()
    
    # Show opt-in instructions
    manager.print_opt_in_instructions()
    
    # List users
    manager.list_users_needing_opt_in()
    
    # Show personalized messages
    print("\n" + "=" * 60)
    manager.generate_individual_messages()
    
    # Show QR code option
    print("=" * 60)
    manager.generate_qr_code_instructions()

if __name__ == "__main__":
    main()