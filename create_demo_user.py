import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import PregnantWomanProfile

# Create demo user
username = 'demo_mom'
password = 'password123'
email = 'demo@example.com'

try:
    user = User.objects.get(username=username)
    print(f"User {username} already exists.")
    # Update password just in case
    user.set_password(password)
    user.save()
except User.DoesNotExist:
    user = User.objects.create_user(username=username, email=email, password=password)
    print(f"Created user {username}.")

# Create profile
if not hasattr(user, 'pregnantwomanprofile'):
    PregnantWomanProfile.objects.create(
        user=user,
        name="Sita Sharma",
        age=24,
        due_date=timezone.now().date() + timedelta(days=60), # 3rd Trimester
        phone_number="9800000000"
    )
    print("Created pregnant profile.")
else:
    print("Profile already exists.")

print(f"\nLOGIN DETAILS:\nUsername: {username}\nPassword: {password}")
