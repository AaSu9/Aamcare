import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

User = get_user_model()
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

try:
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"Updated password for existing superuser '{username}'.")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"Created new superuser '{username}'.")
    
    print(f"Username: {username}")
    print(f"Password: {password}")

except Exception as e:
    print(f"Error: {e}")
