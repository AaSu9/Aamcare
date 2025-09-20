from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import VaccinationRecord, PregnantWomanProfile, NewMotherProfile, VaccinationNotificationLog
from core.notifications import send_sms, send_email
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send SMS and email notifications for upcoming and overdue vaccinations.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        reminder_day = today + timedelta(days=3)

        # Reminders: due in 3 days
        reminders = VaccinationRecord.objects.filter(
            due_date=reminder_day,
            status='pending'
        )
        # Overdue: due in the past, not completed
        overdue = VaccinationRecord.objects.filter(
            due_date__lt=today,
            status='pending'
        )

        for record in reminders:
            profile = record.pregnant_profile or record.mother_profile
            if not profile:
                continue
            user = profile.user
            phone = getattr(profile, 'phone_number', None)
            email = getattr(user, 'email', None)
            vaccine = record.get_vaccine_name_display()
            due = record.due_date.strftime('%Y-%m-%d')
            message = f'Reminder: {vaccine} vaccination is scheduled for {due}. Please visit your health center.'
            subject = 'Vaccination Reminder'
            if phone:
                try:
                    send_sms(phone, message)
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='sms',
                        status='success',
                        message=message,
                    )
                    self.stdout.write(f'SMS sent to {phone} for {vaccine}')
                except Exception as e:
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='sms',
                        status='failure',
                        message=str(e),
                    )
                    self.stderr.write(f'Failed to send SMS to {phone}: {e}')
            if email:
                try:
                    send_email(email, subject, message)
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='email',
                        status='success',
                        message=message,
                    )
                    self.stdout.write(f'Email sent to {email} for {vaccine}')
                except Exception as e:
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='email',
                        status='failure',
                        message=str(e),
                    )
                    self.stderr.write(f'Failed to send email to {email}: {e}')

        for record in overdue:
            profile = record.pregnant_profile or record.mother_profile
            if not profile:
                continue
            user = profile.user
            phone = getattr(profile, 'phone_number', None)
            email = getattr(user, 'email', None)
            vaccine = record.get_vaccine_name_display()
            due = record.due_date.strftime('%Y-%m-%d')
            message = f'Overdue: {vaccine} vaccination was scheduled for {due} and has not been completed. Please visit your health center as soon as possible.'
            subject = 'Vaccination Overdue Alert'
            if phone:
                try:
                    send_sms(phone, message)
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='sms',
                        status='success',
                        message=message,
                    )
                    self.stdout.write(f'Overdue SMS sent to {phone} for {vaccine}')
                except Exception as e:
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='sms',
                        status='failure',
                        message=str(e),
                    )
                    self.stderr.write(f'Failed to send overdue SMS to {phone}: {e}')
            if email:
                try:
                    send_email(email, subject, message)
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='email',
                        status='success',
                        message=message,
                    )
                    self.stdout.write(f'Overdue email sent to {email} for {vaccine}')
                except Exception as e:
                    VaccinationNotificationLog.objects.create(
                        pregnant_woman=record.pregnant_profile if hasattr(record, 'pregnant_profile') else None,
                        mother=record.mother_profile if hasattr(record, 'mother_profile') else None,
                        vaccination_record=record,
                        notification_type='email',
                        status='failure',
                        message=str(e),
                    )
                    self.stderr.write(f'Failed to send overdue email to {email}: {e}')

        self.stdout.write(self.style.SUCCESS('Vaccination notifications sent.')) 