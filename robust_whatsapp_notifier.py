#!/usr/bin/env python3
"""
Fixed WhatsApp Notification System for Aamcare

This script provides a more robust implementation of the WhatsApp notification system
with better error handling and clearer messaging about the sandbox limitations.
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

class RobustWhatsAppNotifier:
    def __init__(self):
        """Initialize WhatsApp notifier with proper error handling"""
        self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        self.whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)
        self.client = None
        
        # Log configuration
        logger.info("Initializing WhatsApp Notifier")
        logger.info(f"Account SID configured: {bool(self.account_sid)}")
        logger.info(f"Auth Token configured: {bool(self.auth_token)}")
        logger.info(f"WhatsApp Number: {self.whatsapp_number}")
        
        # Validate basic configuration
        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            raise ValueError("Missing Twilio credentials in Django settings. Please check aamcare/settings.py")
        
        # Initialize client with error handling
        try:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("✅ Twilio client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Twilio client: {e}")
            raise
    
    def test_authentication(self):
        """Test if credentials work for basic API access"""
        if not self.client:
            return False, "Client not initialized"
        
        try:
            # Simple test - try to fetch account info
            account = self.client.api.accounts(self.account_sid).fetch()
            logger.info(f"✅ Authentication test successful - Account status: {account.status}")
            return True, f"Account status: {account.status}"
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Authentication test failed: {error_msg}")
            
            # Provide specific guidance based on error
            if "20003" in error_msg or "Authenticate" in error_msg:
                return False, "Authentication failed - Check your TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in settings.py"
            elif "401" in error_msg:
                return False, "Unauthorized - Credentials may be incorrect or expired"
            else:
                return False, f"Authentication error: {error_msg}"
    
    def format_phone_number(self, phone_number):
        """Format phone number for international use"""
        if not phone_number:
            return None
            
        # Clean the number
        cleaned = str(phone_number).strip().replace('-', '').replace(' ', '')
        
        # Add country code if missing
        if not cleaned.startswith('+'):
            # Default to Nepal +977 for local numbers
            if cleaned.startswith('98') or cleaned.startswith('97'):
                cleaned = f"+977{cleaned}"
            else:
                # For other numbers, we need proper country code
                logger.warning(f"Phone number {phone_number} may need proper country code")
                cleaned = f"+{cleaned}"
        
        return cleaned
    
    def send_whatsapp_message(self, to_number, message_body):
        """Send WhatsApp message with comprehensive error handling"""
        if not self.client:
            return {
                'success': False,
                'error': 'Twilio client not initialized'
            }
        
        try:
            # Format the phone number
            formatted_to = self.format_phone_number(to_number)
            if not formatted_to:
                return {
                    'success': False,
                    'error': 'Invalid phone number'
                }
            
            # Ensure WhatsApp prefixes
            whatsapp_to = f"whatsapp:{formatted_to}" if not formatted_to.startswith('whatsapp:') else formatted_to
            whatsapp_from = self.whatsapp_number if self.whatsapp_number.startswith('whatsapp:') else f"whatsapp:{self.whatsapp_number}"
            
            logger.info(f"Attempting to send message from {whatsapp_from} to {whatsapp_to}")
            
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
            error_msg = str(e)
            logger.error(f"❌ Failed to send message to {to_number}: {error_msg}")
            
            # Provide specific error guidance
            if "21211" in error_msg:
                return {
                    'success': False,
                    'error': 'Invalid phone number format. Please check the number.'
                }
            elif "21610" in error_msg:
                return {
                    'success': False,
                    'error': 'Recipient not opted in. User must send "join aamcare" to +14155238886 first.'
                }
            elif "20003" in error_msg or "Authenticate" in error_msg:
                return {
                    'success': False,
                    'error': 'Authentication failed. Please check your Twilio credentials.'
                }
            elif "63016" in error_msg:
                return {
                    'success': False,
                    'error': 'WhatsApp sandbox restriction. User must opt-in first.'
                }
            else:
                return {
                    'success': False,
                    'error': f'Message sending failed: {error_msg}'
                }
    
    def send_daily_notifications(self):
        """Send daily notifications with proper error handling"""
        logger.info("Starting daily notification process...")
        
        # Test authentication first
        auth_success, auth_message = self.test_authentication()
        if not auth_success:
            logger.error(f"Cannot proceed due to authentication issues: {auth_message}")
            return False
        
        today = timezone.now().date()
        logger.info(f"Processing notifications for {today}")
        
        # Clear nutrition messages
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
        
        pregnant_success_count = 0
        pregnant_failure_count = 0
        
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
                pregnant_success_count += 1
                
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
                pregnant_failure_count += 1
                
                # Log failure
                if overdue_vaccines.exists():
                    for vaccine in overdue_vaccines:
                        VaccinationNotificationLog.objects.create(
                            user=profile.user,
                            pregnant_woman=profile,
                            vaccination_record=vaccine,
                            notification_type='whatsapp',
                            status='failure',
                            message=result['error']
                        )
        
        # Process New Mothers
        logger.info("Processing New Mothers...")
        mother_profiles = NewMotherProfile.objects.all()
        logger.info(f"Found {mother_profiles.count()} mother profiles")
        
        mother_success_count = 0
        mother_failure_count = 0
        
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
                mother_success_count += 1
                
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
                mother_failure_count += 1
                
                # Log failure
                if overdue_vaccines.exists():
                    for vaccine in overdue_vaccines:
                        VaccinationNotificationLog.objects.create(
                            user=profile.user,
                            mother=profile,
                            vaccination_record=vaccine,
                            notification_type='whatsapp',
                            status='failure',
                            message=result['error']
                        )
        
        # Summary
        total_success = pregnant_success_count + mother_success_count
        total_failure = pregnant_failure_count + mother_failure_count
        
        logger.info("=" * 50)
        logger.info("DAILY NOTIFICATION SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Pregnant Women - Success: {pregnant_success_count}, Failures: {pregnant_failure_count}")
        logger.info(f"New Mothers - Success: {mother_success_count}, Failures: {mother_failure_count}")
        logger.info(f"TOTAL - Success: {total_success}, Failures: {total_failure}")
        
        if total_failure > 0:
            logger.warning("Some messages failed to send. Check error logs above.")
            logger.warning("Common reasons:")
            logger.warning("1. Users haven't opted in to WhatsApp sandbox")
            logger.warning("2. Invalid phone numbers")
            logger.warning("3. Twilio credential issues")
        
        logger.info("Daily notification process completed")
        return total_success > 0

def main():
    """Main function to run the notification system"""
    try:
        notifier = RobustWhatsAppNotifier()
        success = notifier.send_daily_notifications()
        
        if success:
            print("\n✅ Notification process completed with some successes")
        else:
            print("\n❌ Notification process completed with no successes")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please check your Twilio credentials in aamcare/settings.py")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        logger.exception("Unexpected error in main function")

if __name__ == "__main__":
    main()