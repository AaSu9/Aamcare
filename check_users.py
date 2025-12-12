import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.models import PregnantWomanProfile, NewMotherProfile

def check_users():
    print("📋 Registered Users in Aamcare System")
    print("=" * 40)
    
    # Check pregnant women
    print(f"\n🤰 Pregnant Women: {PregnantWomanProfile.objects.count()}")
    for i, user in enumerate(PregnantWomanProfile.objects.all(), 1):
        print(f"  {i}. {user.name}")
        print(f"     Phone: {user.phone_number}")
        print(f"     Registration Date: {user.created_at if hasattr(user, 'created_at') else 'N/A'}")
        print()
    
    # Check new mothers
    print(f"👶 New Mothers: {NewMotherProfile.objects.count()}")
    for i, user in enumerate(NewMotherProfile.objects.all(), 1):
        print(f"  {i}. {user.name}")
        print(f"     Phone: {user.phone_number}")
        print(f"     Registration Date: {user.created_at if hasattr(user, 'created_at') else 'N/A'}")
        print()
    
    # Total users
    total = PregnantWomanProfile.objects.count() + NewMotherProfile.objects.count()
    print(f"📈 Total Registered Users: {total}")

if __name__ == "__main__":
    check_users()