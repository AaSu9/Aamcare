from core.models import PregnantWomanProfile, VaccinationRecord, VaccinationNotificationLog
from datetime import date

profiles = PregnantWomanProfile.objects.filter(name__icontains='rita')
print(f'Found {profiles.count()} profiles with name containing "rita":')
for profile in profiles:
    print(f'Profile: {profile} | Phone: {profile.phone_number}')
    overdue = VaccinationRecord.objects.filter(pregnant_profile=profile, status='pending', due_date__lt=date.today())
    print('  Overdue Vaccination Records:')
    for rec in overdue:
        print(f'    - {rec} (Due: {rec.due_date}, Status: {rec.status})')
    logs = VaccinationNotificationLog.objects.filter(pregnant_woman=profile)
    print('  Notification Logs:')
    for log in logs:
        print(f'    - {log.sent_at}: {log.notification_type} ({log.status}) - {log.message[:100]}')
    print('-' * 40)
if not profiles:
    print('No profiles found with name containing "rita".') 