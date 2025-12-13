from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from core.models import PregnantWomanProfile, NewMotherProfile, VaccinationRecord, VaccinationNotificationLog
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send daily WhatsApp notifications for nutrition and vaccine delays'

    def handle(self, *args, **options):
        # Check for Twilio
        client = None
        from_number = None
        
        try:
            from twilio.rest import Client
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)

            if all([account_sid, auth_token, whatsapp_number]):
                client = Client(account_sid, auth_token)
                from_number = whatsapp_number
            else:
                 self.stdout.write(self.style.WARNING("Twilio WhatsApp settings not found. Running in DEMO/MOCK mode."))
                 client = "MOCK_CLIENT"
                 from_number = "MOCK_NUMBER"
        except ImportError:
            self.stdout.write(self.style.WARNING("Twilio library not installed. Running in DEMO/MOCK mode."))
            client = "MOCK_CLIENT"
            from_number = "MOCK_NUMBER"

        today = timezone.now().date()
        self.stdout.write(f"Starting daily notification check for {today}...")

        # Nutrition Plans (Hardcoded from setup_nutrition_plans.py for reliability)
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

        # 1. Process Pregnant Women
        self.stdout.write("Processing Pregnant Women...")
        pregnant_profiles = PregnantWomanProfile.objects.all()
        self.stdout.write(f"Found {pregnant_profiles.count()} pregnant profiles.")
        
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
            
            # Combine
            full_message = "\n\n".join(messages_to_send)
            
            # Send
            success = self.send_whatsapp(client, from_number, profile.phone_number, full_message)
            
            if success and overdue_vaccines.exists():
                # Log Vaccines
                for vaccine in overdue_vaccines:
                    VaccinationNotificationLog.objects.create(
                        user=profile.user,
                        pregnant_woman=profile,
                        vaccination_record=vaccine,
                        notification_type='whatsapp',
                        status='success',
                        message=full_message
                    )

        # 2. Process New Mothers
        self.stdout.write("Processing New Mothers...")
        mother_profiles = NewMotherProfile.objects.all()
        self.stdout.write(f"Found {mother_profiles.count()} mother profiles.")

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

            full_message = "\n\n".join(messages_to_send)
            
            # Send
            success = self.send_whatsapp(client, from_number, profile.phone_number, full_message)

            if success and overdue_vaccines.exists():
                # Log
                for vaccine in overdue_vaccines:
                    VaccinationNotificationLog.objects.create(
                        user=profile.user,
                        mother=profile,
                        vaccination_record=vaccine,
                        notification_type='whatsapp',
                        status='success',
                        message=full_message
                    )

    def send_whatsapp(self, client, from_, to, body):
        # MOCK MODE
        if client == "MOCK_CLIENT":
             self.stdout.write(self.style.SUCCESS(f"[MOCK] Would send WhatsApp to {to}:\n---\n{body}\n---"))
             return True

        try:
            # Format numbers for Twilio WhatsApp
            # Ensure 'whatsapp:' prefix
            formatted_to = to.strip()
            # Basic sanitization
            formatted_to = formatted_to.replace('-', '').replace(' ', '')
            
            if not formatted_to.startswith('+'):
                 # Default to Nepal +977 if no country code provided
                 formatted_to = f"+977{formatted_to}"
            
            # Ensure WhatsApp prefix for recipient
            if not formatted_to.startswith('whatsapp:'):
                formatted_to = f"whatsapp:{formatted_to}"
                
            # Ensure WhatsApp prefix for sender
            formatted_from = from_
            if not formatted_from.startswith('whatsapp:'):
                formatted_from = f"whatsapp:{formatted_from}"

            # Send as WhatsApp message
            message = client.messages.create(
                from_=formatted_from,
                body=body,
                to=formatted_to
            )
            self.stdout.write(self.style.SUCCESS(f"Sent message to {to}: {message.sid}"))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send to {to}: {str(e)}"))
            return False
