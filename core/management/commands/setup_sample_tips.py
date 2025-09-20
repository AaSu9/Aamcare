from django.core.management.base import BaseCommand
from core.models import PregnancyTip

class Command(BaseCommand):
    help = 'Populate PregnancyTip with sample Do and Don\'t tips for each trimester.'

    def handle(self, *args, **options):
        tips = [
            # First Trimester Do's
            {"title": "Drink plenty of clean water.", "content": "धेरै सफा पानी पिउनुहोस्।", "week_start": 1, "is_active": True},
            {"title": "Take folic acid supplements daily.", "content": "दैनिक फोलिक एसिड लिनुहोस्।", "week_start": 1, "is_active": True},
            # First Trimester Don'ts
            {"title": "Don't skip meals.", "content": "खाना नछोड्नुहोस्।", "week_start": 1, "is_active": True},
            {"title": "Don't smoke or use tobacco.", "content": "धूम्रपान नगर्नुहोस्।", "week_start": 1, "is_active": True},
            # Second Trimester Do's
            {"title": "Eat iron-rich foods.", "content": "फलफूल, सागसब्जी, मासु आदि आइरनयुक्त खाना खानुहोस्।", "week_start": 14, "is_active": True},
            {"title": "Do regular gentle exercise.", "content": "नियमित हल्का व्यायाम गर्नुहोस्।", "week_start": 15, "is_active": True},
            # Second Trimester Don'ts
            {"title": "Don't lift heavy objects.", "content": "गह्रौं सामान नउठाउनुहोस्।", "week_start": 14, "is_active": True},
            {"title": "Don't consume unpasteurized dairy.", "content": "अशुद्ध दूधजन्य पदार्थ नखानुहोस्।", "week_start": 16, "is_active": True},
            # Third Trimester Do's
            {"title": "Attend all prenatal checkups.", "content": "सबै प्रसूति जाँचहरूमा जानुहोस्।", "week_start": 28, "is_active": True},
            {"title": "Practice relaxation techniques.", "content": "आरामदायक अभ्यासहरू गर्नुहोस्।", "week_start": 30, "is_active": True},
            # Third Trimester Don'ts
            {"title": "Don't ignore swelling or headaches.", "content": "सुन्निनु वा टाउको दुखाइलाई बेवास्ता नगर्नुहोस्।", "week_start": 28, "is_active": True},
            {"title": "Don't travel long distances without consulting your doctor.", "content": "डाक्टरको सल्लाह बिना लामो यात्रा नगर्नुहोस्।", "week_start": 32, "is_active": True},
        ]
        created = 0
        for tip in tips:
            if not PregnancyTip.objects.filter(title=tip["title"], week_start=tip["week_start"]).exists():
                PregnancyTip.objects.create(**tip)
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Added {created} sample pregnancy tips.")) 