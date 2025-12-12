from django.core.management.base import BaseCommand
from core.models import PregnantWomanProfile, NewMotherProfile
from core.notifications import register_phone_with_twilio, send_whatsapp_welcome_message
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Register all existing users with Twilio for automated messaging'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually registering numbers (for testing)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN: Testing registration without actual Twilio API calls')
            )
        
        # Register all pregnant women
        self.stdout.write('Registering pregnant women with Twilio...')
        pregnant_profiles = PregnantWomanProfile.objects.all()
        pregnant_count = pregnant_profiles.count()
        self.stdout.write(f'Found {pregnant_count} pregnant women profiles')
        
        for profile in pregnant_profiles:
            if profile.phone_number:
                self.stdout.write(f'Registering {profile.name} ({profile.phone_number})')
                if not dry_run:
                    result = register_phone_with_twilio(profile.phone_number)
                    if result['success']:
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Registered {result["formatted_number"]}')
                        )
                        # Send welcome message
                        welcome_result = send_whatsapp_welcome_message(result['formatted_number'])
                        if welcome_result['success']:
                            self.stdout.write(
                                self.style.SUCCESS(f'    ✓ Welcome message sent')
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR(f'    ✗ Failed to send welcome message: {welcome_result["message"]}')
                            )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Failed to register {profile.phone_number}: {result["message"]}')
                        )
                else:
                    self.stdout.write(f'  Would register {profile.phone_number}')
            else:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ Skipping {profile.name} (no phone number)')
                )
        
        # Register all new mothers
        self.stdout.write('\nRegistering new mothers with Twilio...')
        mother_profiles = NewMotherProfile.objects.all()
        mother_count = mother_profiles.count()
        self.stdout.write(f'Found {mother_count} new mother profiles')
        
        for profile in mother_profiles:
            if profile.phone_number:
                self.stdout.write(f'Registering {profile.name} ({profile.phone_number})')
                if not dry_run:
                    result = register_phone_with_twilio(profile.phone_number)
                    if result['success']:
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Registered {result["formatted_number"]}')
                        )
                        # Send welcome message
                        welcome_result = send_whatsapp_welcome_message(result['formatted_number'])
                        if welcome_result['success']:
                            self.stdout.write(
                                self.style.SUCCESS(f'    ✓ Welcome message sent')
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR(f'    ✗ Failed to send welcome message: {welcome_result["message"]}')
                            )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Failed to register {profile.phone_number}: {result["message"]}')
                        )
                else:
                    self.stdout.write(f'  Would register {profile.phone_number}')
            else:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ Skipping {profile.name} (no phone number)')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {pregnant_count + mother_count} user profiles'
            )
        )