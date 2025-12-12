import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.models import PregnantWomanProfile

target_phone = "9741690374"

# Get first profile or create one
profile = PregnantWomanProfile.objects.first()
if profile:
    print(f"Updating profile {profile.name} phone from {profile.phone_number} to {target_phone}")
    profile.phone_number = target_phone
    profile.save()
    print("Update successful.")
else:
    print("No pregnant profile found to update.")
