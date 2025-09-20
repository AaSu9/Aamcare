from django.core.management.base import BaseCommand
from core.models import InfoContent

class Command(BaseCommand):
    help = 'Setup sample data for AamCare application'

    def handle(self, *args, **options):
        self.stdout.write('Setting up sample data...')
        
        # Sample diet content
        diet_content = [
            {
                'title': 'First Trimester Nutrition',
                'body': '''During the first trimester, focus on:
• Folic acid-rich foods (leafy greens, beans, fortified cereals)
• Iron-rich foods (lean meat, spinach, lentils)
• Small, frequent meals to manage nausea
• Stay hydrated with water and herbal teas
• Avoid raw fish, unpasteurized dairy, and excessive caffeine'''
            },
            {
                'title': 'Second Trimester Diet Plan',
                'body': '''Second trimester nutrition guidelines:
• Increase protein intake (lean meats, fish, eggs, legumes)
• Calcium-rich foods (dairy, fortified plant milk, leafy greens)
• Omega-3 fatty acids (salmon, walnuts, chia seeds)
• Complex carbohydrates (whole grains, fruits, vegetables)
• Continue taking prenatal vitamins as prescribed'''
            },
            {
                'title': 'Third Trimester Nutrition',
                'body': '''Third trimester dietary recommendations:
• High-fiber foods to prevent constipation
• Iron-rich foods to prevent anemia
• Protein for baby's growth
• Healthy fats for brain development
• Small, frequent meals as stomach space is limited'''
            },
            {
                'title': 'Postpartum Recovery Diet',
                'body': '''Postpartum nutrition for recovery:
• High-protein foods for healing
• Iron-rich foods to replenish blood loss
• Calcium for bone health
• Omega-3s for mood and brain health
• Plenty of fluids, especially if breastfeeding'''
            }
        ]

        # Sample vaccine content
        vaccine_content = [
            {
                'title': 'Pregnancy Vaccination Schedule',
                'body': '''Essential vaccinations during pregnancy:
• Tdap (Tetanus, Diphtheria, Pertussis) - 27-36 weeks
• Influenza vaccine (seasonal)
• COVID-19 vaccine (if recommended by healthcare provider)
• Avoid live vaccines during pregnancy
• Discuss all vaccinations with your healthcare provider'''
            },
            {
                'title': 'Newborn Vaccination Schedule',
                'body': '''Baby's first year vaccinations:
• Birth: Hepatitis B
• 2 months: DTaP, Hib, PCV13, IPV, Rotavirus
• 4 months: DTaP, Hib, PCV13, IPV, Rotavirus
• 6 months: DTaP, Hib, PCV13, IPV, Rotavirus, Hepatitis B
• 12 months: MMR, Varicella, Hepatitis A'''
            }
        ]

        # Sample exercise content
        exercise_content = [
            {
                'title': 'First Trimester Exercises',
                'body': '''Safe exercises for first trimester:
• Walking (30 minutes daily)
• Prenatal yoga (gentle poses)
• Swimming (low-impact cardio)
• Pelvic floor exercises (Kegels)
• Avoid high-impact activities and contact sports
• Listen to your body and rest when needed'''
            },
            {
                'title': 'Second Trimester Workouts',
                'body': '''Second trimester exercise guidelines:
• Continue walking and swimming
• Prenatal Pilates for core strength
• Light strength training with modifications
• Pelvic tilts and gentle stretches
• Avoid exercises lying on your back
• Stay hydrated and take breaks'''
            },
            {
                'title': 'Third Trimester Movement',
                'body': '''Third trimester exercise tips:
• Gentle walking and swimming
• Prenatal yoga for flexibility
• Pelvic floor exercises
• Breathing exercises for labor preparation
• Avoid strenuous activities
• Focus on comfort and relaxation'''
            },
            {
                'title': 'Postpartum Exercise Plan',
                'body': '''Safe postpartum exercises:
• Start with gentle walking
• Pelvic floor rehabilitation
• Core strengthening (after clearance)
• Gentle stretching
• Wait 6 weeks before intense exercise
• Listen to your body and go slowly'''
            }
        ]

        # Sample breastfeeding content
        breastfeeding_content = [
            {
                'title': 'Breastfeeding Basics',
                'body': '''Getting started with breastfeeding:
• Start within the first hour after birth
• Hold baby skin-to-skin
• Ensure proper latch (mouth wide open)
• Feed on demand (8-12 times daily)
• Watch for hunger cues
• Seek help from lactation consultant if needed'''
            },
            {
                'title': 'Breastfeeding Nutrition',
                'body': '''Nutrition for breastfeeding mothers:
• Extra 500 calories daily
• High-protein foods
• Plenty of fluids (water, milk, juice)
• Iron-rich foods
• Calcium for bone health
• Omega-3s for baby's brain development'''
            }
        ]

        # Sample mental health content
        mental_content = [
            {
                'title': 'Pregnancy Mental Health',
                'body': '''Mental health during pregnancy:
• Mood changes are normal
• Practice stress management techniques
• Maintain social connections
• Get adequate sleep
• Exercise regularly (with doctor's approval)
• Seek professional help if needed'''
            },
            {
                'title': 'Postpartum Mental Health',
                'body': '''Postpartum emotional well-being:
• Baby blues are common (2-3 weeks)
• Postpartum depression is treatable
• Get support from family and friends
• Sleep when baby sleeps
• Practice self-care
• Don't hesitate to seek professional help'''
            }
        ]

        # Create content for each category
        categories = {
            'diet': diet_content,
            'vaccine': vaccine_content,
            'exercise': exercise_content,
            'breastfeeding': breastfeeding_content,
            'mental': mental_content
        }

        for category, content_list in categories.items():
            for content_data in content_list:
                InfoContent.objects.get_or_create(
                    title=content_data['title'],
                    defaults={
                        'category': category,
                        'body': content_data['body']
                    }
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        ) 