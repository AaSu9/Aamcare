from django.core.management.base import BaseCommand
from core.models import PregnantWomanProfile, NewMotherProfile, VaccinationRecord
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Setup vaccination records for existing users'

    def handle(self, *args, **options):
        self.stdout.write('Setting up vaccination records for existing users...')
        
        # Setup vaccination records for pregnant women
        pregnant_profiles = PregnantWomanProfile.objects.all()
        for profile in pregnant_profiles:
            # Check if vaccination records already exist
            if not VaccinationRecord.objects.filter(pregnant_profile=profile).exists():
                self.create_pregnancy_vaccination_schedule(profile)
                self.stdout.write(f'Created vaccination schedule for pregnant woman: {profile.name}')
        
        # Setup vaccination records for new mothers
        mother_profiles = NewMotherProfile.objects.all()
        for profile in mother_profiles:
            # Check if vaccination records already exist
            if not VaccinationRecord.objects.filter(mother_profile=profile).exists():
                self.create_baby_vaccination_schedule(profile)
                self.stdout.write(f'Created vaccination schedule for new mother: {profile.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created vaccination records for all users!')
        )

    def create_pregnancy_vaccination_schedule(self, profile):
        """Create vaccination schedule for pregnant women"""
        today = date.today()
        
        # Tdap vaccine (27-36 weeks)
        tdap_due = profile.due_date - timedelta(weeks=10)  # Approximate 30 weeks
        VaccinationRecord.objects.create(
            pregnant_profile=profile,
            vaccine_name='tdap',
            due_date=tdap_due,
            status='pending'
        )
        
        # Influenza vaccine (seasonal)
        VaccinationRecord.objects.create(
            pregnant_profile=profile,
            vaccine_name='influenza',
            due_date=today + timedelta(days=30),
            status='pending'
        )
        
        # COVID-19 vaccine (if recommended)
        VaccinationRecord.objects.create(
            pregnant_profile=profile,
            vaccine_name='covid19',
            due_date=today + timedelta(days=14),
            status='pending'
        )

    def create_baby_vaccination_schedule(self, profile):
        """Create vaccination schedule for baby"""
        birth_date = profile.child_birth_date
        
        # Birth vaccines
        VaccinationRecord.objects.create(
            mother_profile=profile,
            vaccine_name='hepb_birth',
            due_date=birth_date,
            status='pending'
        )
        
        # 2 months vaccines
        two_months = birth_date + timedelta(days=60)
        vaccines_2m = ['dtap_2m', 'hib_2m', 'pcv13_2m', 'ipv_2m', 'rotavirus_2m']
        for vaccine in vaccines_2m:
            VaccinationRecord.objects.create(
                mother_profile=profile,
                vaccine_name=vaccine,
                due_date=two_months,
                status='pending'
            )
        
        # 4 months vaccines
        four_months = birth_date + timedelta(days=120)
        vaccines_4m = ['dtap_4m', 'hib_4m', 'pcv13_4m', 'ipv_4m', 'rotavirus_4m']
        for vaccine in vaccines_4m:
            VaccinationRecord.objects.create(
                mother_profile=profile,
                vaccine_name=vaccine,
                due_date=four_months,
                status='pending'
            )
        
        # 6 months vaccines
        six_months = birth_date + timedelta(days=180)
        vaccines_6m = ['dtap_6m', 'hib_6m', 'pcv13_6m', 'ipv_6m', 'rotavirus_6m', 'hepb_6m']
        for vaccine in vaccines_6m:
            VaccinationRecord.objects.create(
                mother_profile=profile,
                vaccine_name=vaccine,
                due_date=six_months,
                status='pending'
            )
        
        # 12 months vaccines
        twelve_months = birth_date + timedelta(days=365)
        vaccines_12m = ['mmr_12m', 'varicella_12m', 'hepa_12m']
        for vaccine in vaccines_12m:
            VaccinationRecord.objects.create(
                mother_profile=profile,
                vaccine_name=vaccine,
                due_date=twelve_months,
                status='pending'
            ) 