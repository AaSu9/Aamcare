#!/usr/bin/env python3
"""
Fix for WhatsApp Notifications in Aamcare

This script addresses the authentication issues with Twilio WhatsApp notifications
and implements a more robust notification system.
"""

import os
import django
from twilio.rest import Client
from django.conf import settings
import logging

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from core.models import PregnantWomanProfile, NewMotherProfile, VaccinationRecord, VaccinationNotificationLog
from django.utils import timezone

class FixedWhatsAppNotifier:
    def __init__(self):
        """Initialize WhatsApp notifier with proper credentials"""
        self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        self.whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)
        
        # Validate credentials
        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            raise ValueError("Missing Twilio credentials in Django settings")
        
        # Initialize client
        try:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("✅ Twilio client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Twilio client: {e}")
            raise
    
    def validate_credentials(self):
        """Validate Twilio credentials by fetching account info"""
        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            logger.info(f"✅ Account validation successful - Status: {account.status}")
            return True
        except Exception as e:
            logger.error(f"❌ Account validation failed: {e}")
            return False
    
    def format_phone_number(self, phone_number):
        """Format phone number for international use"""
        # Clean the number
        cleaned = phone_number.strip().replace('-', '').replace(' ', '')
        
        # Add country code if missing
        if not cleaned.startswith('+'):
            # Default to Nepal +977 if no country code provided
            if cleaned.startswith('98') or cleaned.startswith('97'):
                cleaned = f"+977{cleaned}"
            else:
                cleaned = f"+{cleaned}"
        
        return cleaned
    
    def send_whatsapp_message(self, to_number, message_body):
        """Send WhatsApp message with proper formatting"""
        try:
            # Format the phone number
            formatted_to = self.format_phone_number(to_number)
            
            # Ensure WhatsApp prefixes
            whatsapp_to = f"whatsapp:{formatted_to}" if not formatted_to.startswith('whatsapp:') else formatted_to
            whatsapp_from = self.whatsapp_number if self.whatsapp_number.startswith('whatsapp:') else f"whatsapp:{self.whatsapp_number}"
            
            logger.info(f"Sending message from {whatsapp_from} to {whatsapp_to}")
            
            # Send the message
            message = self.client.messages.create(
                body=message_body,
                from_=whatsapp_from,
                to=whatsapp_to
            )
            
            logger.info(f"✅ Message sent successfully - SID: {message.sid}")
            return {
                'success': True,
                'sid': message.sid,
                'status': message.status
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to send message to {to_number}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_daily_notifications(self):
        """Send daily notifications to all users"""
        logger.info("Starting daily notification process...")
        
        # Validate credentials first
        if not self.validate_credentials():
            logger.error("Cannot proceed with notifications due to credential validation failure")
            return False
        
        today = timezone.now().date()
        logger.info(f"Processing notifications for {today}")
        
        # Nutrition messages
        PREGNANT_DIET = (
            "🤰 *Daily Nutrition Schedule*\n\n"
            "Morning: Warm water + banana + boiled egg\n"
            "Breakfast: Oats + milk + dry fruits\n"
            "Lunch: Rice + dal + spinach sabji + curd\n"
            "Snacks: Roasted chana, fruits, coconut water\n"
            "Dinner: Roti + mixed vegetables + paneer + turmeric milk"
        )
        
        MOTHER_DIET = (
            "🍼 *Daily Nutrition Schedule (Postpartum)*\n\n"
            "Breakfast: Ragi porridge + almonds + milk\n"
            "Lunch: Rice + dal + chicken curry + greens\n"
            "Snacks: Fruit salad + herbal tea\n"
            "Dinner: Chapati + sabji + paneer + turmeric milk"
        )
        
        # Process Pregnant Women
        logger.info("Processing Pregnant Women...")
        pregnant_profiles = PregnantWomanProfile.objects.all()
        logger.info(f"Found {pregnant_profiles.count()} pregnant profiles")
        
        for profile in pregnant_profiles:
            if not profile.phone_number:
                logger.warning(f"Skipping {profile.name} - No phone number")
                continue
            
            messages_to_send = []
            
            # Nutrition
            messages_to_send.append(PREGNANT_DIET)
            
            # Vaccine Delays
            overdue_vaccines = VaccinationRecord.objects.filter(
                pregnant_profile=profile,
                status__in=['pending', 'overdue'],
                due_date__lte=today
            )
            
            if overdue_vaccines.exists():
                vaccine_list = "\n".join([f"- {v.get_vaccine_name_display()} (Due: {v.due_date})" for v in overdue_vaccines])
                msg = f"⚠️ *Vaccine Alert*\nYou have overdue vaccines:\n{vaccine_list}\nPlease visit your health center."
                messages_to_send.append(msg)
            
            # Combine messages
            full_message = "\n\n".join(messages_to_send)
            
            # Send message
            result = self.send_whatsapp_message(profile.phone_number, full_message)
            
            if result['success']:
                logger.info(f"✅ Successfully sent message to {profile.name} ({profile.phone_number})")
                
                # Log vaccine notifications
                if overdue_vaccines.exists():
                    for vaccine in overdue_vaccines:
                        VaccinationNotificationLog.objects.create(
                            user=profile.user,
                            pregnant_woman=profile,
                            vaccination_record=vaccine,
                            notification_type='whatsapp',
                            status='success',
                            message=full_message
                        )
            else:
                logger.error(f"❌ Failed to send message to {profile.name} ({profile.phone_number}): {result['error']}")
        
        # Process New Mothers
        logger.info("Processing New Mothers...")
        mother_profiles = NewMotherProfile.objects.all()
        logger.info(f"Found {mother_profiles.count()} mother profiles")
        
        for profile in mother_profiles:
            if not profile.phone_number:
                logger.warning(f"Skipping {profile.name} - No phone number")
                continue
            
            messages_to_send = []
            
            # Nutrition
            messages_to_send.append(MOTHER_DIET)
            
            # Vaccine Delays
            overdue_vaccines = VaccinationRecord.objects.filter(
                mother_profile=profile,
                status__in=['pending', 'overdue'],
                due_date__lte=today
            )
            
            if overdue_vaccines.exists():
                vaccine_list = "\n".join([f"- {v.get_vaccine_name_display()} (Due: {v.due_date})" for v in overdue_vaccines])
                msg = f"⚠️ *Vaccine Alert*\nYou have overdue vaccines:\n{vaccine_list}\nPlease visit your health center."
                messages_to_send.append(msg)
            
            # Combine messages
            full_message = "\n\n".join(messages_to_send)
            
            # Send message
            result = self.send_whatsapp_message(profile.phone_number, full_message)
            
            if result['success']:
                logger.info(f"✅ Successfully sent message to {profile.name} ({profile.phone_number})")
                
                # Log vaccine notifications
                if overdue_vaccines.exists():
                    for vaccine in overdue_vaccines:
                        VaccinationNotificationLog.objects.create(
                            user=profile.user,
                            mother=profile,
                            vaccination_record=vaccine,
                            notification_type='whatsapp',
                            status='success',
                            message=full_message
                        )
            else:
                logger.error(f"❌ Failed to send message to {profile.name} ({profile.phone_number}): {result['error']}")
        
        logger.info("Daily notification process completed")
        return True

def main():
    """Main function to run the notification system"""
    try:
        notifier = FixedWhatsAppNotifier()
        notifier.send_daily_notifications()
    except Exception as e:
        logger.error(f"Failed to run notification system: {e}")

if __name__ == "__main__":
    main()