from django.core.management.base import BaseCommand
from core.models import PregnancyTip

class Command(BaseCommand):
    help = 'Setup sample pregnancy Do/Don\'t tips based on WHO and MoHP guidelines'

    def handle(self, *args, **options):
        self.stdout.write('Setting up pregnancy tips...')
        tips = [
            # First Trimester
            {'tip_type': 'do', 'text_en': 'Take folic acid supplements daily.', 'text_ne': 'दैनिक फोलिक एसिड लिनुहोस्।', 'trimester': 1, 'icon': 'fa-leaf', 'source': 'WHO', 'info': 'Prevents birth defects.'},
            {'tip_type': 'do', 'text_en': 'Eat small, frequent meals to manage nausea.', 'text_ne': 'बान्ता कम गर्न साना साना भोजन खानुहोस्।', 'trimester': 1, 'icon': 'fa-utensils', 'source': 'MoHP', 'info': 'Helps with morning sickness.'},
            {'tip_type': 'do', 'text_en': 'Attend your first antenatal checkup.', 'text_ne': 'पहिलो गर्भ जाँचमा जानुहोस्।', 'trimester': 1, 'icon': 'fa-hospital', 'source': 'MoHP', 'info': 'Early checkup is important.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t smoke or use tobacco.', 'text_ne': 'धूम्रपान नगर्नुहोस्।', 'trimester': 1, 'icon': 'fa-ban', 'source': 'WHO', 'info': 'Harms baby\'s development.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t drink alcohol.', 'text_ne': 'रक्सी नपिउनुहोस्।', 'trimester': 1, 'icon': 'fa-wine-bottle', 'source': 'WHO', 'info': 'Can cause birth defects.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t take medicines without doctor\'s advice.', 'text_ne': 'डाक्टरको सल्लाह बिना औषधि नखानुहोस्।', 'trimester': 1, 'icon': 'fa-pills', 'source': 'MoHP', 'info': 'Some medicines are unsafe.'},
            # Second Trimester
            {'tip_type': 'do', 'text_en': 'Increase iron-rich foods in your diet.', 'text_ne': 'आहारमा फलामयुक्त खानेकुरा बढाउनुहोस्।', 'trimester': 2, 'icon': 'fa-egg', 'source': 'WHO', 'info': 'Prevents anemia.'},
            {'tip_type': 'do', 'text_en': 'Continue regular antenatal checkups.', 'text_ne': 'नियमित गर्भ जाँचमा जानुहोस्।', 'trimester': 2, 'icon': 'fa-calendar-check', 'source': 'MoHP', 'info': 'Monitors baby\'s growth.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t lift heavy objects.', 'text_ne': 'गह्रौं सामान नउठाउनुहोस्।', 'trimester': 2, 'icon': 'fa-dumbbell', 'source': 'MoHP', 'info': 'Risk of injury or miscarriage.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t eat raw or undercooked meat.', 'text_ne': 'काँचो वा अधपकाएको मासु नखानुहोस्।', 'trimester': 2, 'icon': 'fa-drumstick-bite', 'source': 'WHO', 'info': 'Risk of infection.'},
            # Third Trimester
            {'tip_type': 'do', 'text_en': 'Prepare a birth plan and emergency contacts.', 'text_ne': 'जन्म योजना र आपतकालीन सम्पर्क तयार गर्नुहोस्।', 'trimester': 3, 'icon': 'fa-list-alt', 'source': 'MoHP', 'info': 'Be ready for delivery.'},
            {'tip_type': 'do', 'text_en': 'Practice gentle exercise like walking.', 'text_ne': 'हल्का व्यायाम (हिँड्न) गर्नुहोस्।', 'trimester': 3, 'icon': 'fa-walking', 'source': 'WHO', 'info': 'Helps with labor.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t ignore swelling, headache, or bleeding.', 'text_ne': 'सुजन, टाउको दुखाइ वा रक्तश्रावलाई बेवास्ता नगर्नुहोस्।', 'trimester': 3, 'icon': 'fa-exclamation-triangle', 'source': 'MoHP', 'info': 'These are danger signs.'},
            # All Trimesters
            {'tip_type': 'do', 'text_en': 'Drink plenty of clean water.', 'text_ne': 'धेरै सफा पानी पिउनुहोस्।', 'trimester': 0, 'icon': 'fa-tint', 'source': 'WHO', 'info': 'Prevents dehydration.'},
            {'tip_type': 'dont', 'text_en': 'Don\'t skip meals.', 'text_ne': 'खाना नछोड्नुहोस्।', 'trimester': 0, 'icon': 'fa-times-circle', 'source': 'MoHP', 'info': 'Regular meals are important.'},
        ]
        for tip in tips:
            PregnancyTip.objects.get_or_create(
                tip_type=tip['tip_type'],
                text_en=tip['text_en'],
                trimester=tip['trimester'],
                defaults=tip
            )
        self.stdout.write(self.style.SUCCESS('Pregnancy tips setup complete!')) 