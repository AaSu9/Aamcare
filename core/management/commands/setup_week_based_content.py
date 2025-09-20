from django.core.management.base import BaseCommand
from core.models import InfoContent

class Command(BaseCommand):
    help = 'Setup week-based diet and exercise content for personalized pregnancy guidance'

    def handle(self, *args, **options):
        self.stdout.write('Setting up week-based content...')
        
        # Week-based diet content
        diet_content = [
            {
                'title': 'Early Pregnancy Nutrition (Weeks 1-12)',
                'body': '''First trimester nutrition focus:
• Folic acid (400-800 mcg daily) - leafy greens, fortified cereals, beans
• Iron-rich foods - lean meat, spinach, lentils, fortified grains
• Small, frequent meals to manage morning sickness
• Stay hydrated with water, ginger tea, and clear broths
• Avoid raw fish, unpasteurized dairy, excessive caffeine
• Take prenatal vitamins as prescribed by your doctor''',
                'week_start': 1,
                'week_end': 12
            },
            {
                'title': 'Second Trimester Nutrition (Weeks 13-26)',
                'body': '''Second trimester dietary needs:
• Increase protein intake (75-100g daily) - lean meats, fish, eggs, legumes
• Calcium-rich foods (1000mg daily) - dairy, fortified plant milk, leafy greens
• Omega-3 fatty acids - salmon, walnuts, chia seeds, flaxseeds
• Complex carbohydrates - whole grains, fruits, vegetables
• Iron for increased blood volume - red meat, spinach, fortified cereals
• Continue prenatal vitamins and stay well-hydrated''',
                'week_start': 13,
                'week_end': 26
            },
            {
                'title': 'Third Trimester Nutrition (Weeks 27-40)',
                'body': '''Third trimester nutrition priorities:
• High-fiber foods to prevent constipation - whole grains, fruits, vegetables
• Iron-rich foods to prevent anemia - red meat, spinach, fortified cereals
• Protein for baby's growth (80-100g daily) - lean meats, fish, eggs, legumes
• Healthy fats for brain development - avocados, nuts, olive oil
• Small, frequent meals as stomach space is limited
• Calcium for baby's bone development - dairy, fortified foods
• Stay hydrated and avoid large meals before bedtime''',
                'week_start': 27,
                'week_end': 40
            },
            {
                'title': 'Postpartum Recovery Nutrition',
                'body': '''Postpartum nutrition for healing and breastfeeding:
• High-protein foods for tissue repair - lean meats, fish, eggs, legumes
• Iron-rich foods to replenish blood loss - red meat, spinach, fortified cereals
• Calcium for bone health - dairy, fortified plant milk, leafy greens
• Omega-3s for mood and brain health - salmon, walnuts, chia seeds
• Plenty of fluids, especially if breastfeeding (3-4 liters daily)
• Fiber to prevent constipation - whole grains, fruits, vegetables
• Small, frequent meals to maintain energy levels''',
                'week_start': None,
                'week_end': None
            }
        ]

        # Week-based exercise content
        exercise_content = [
            {
                'title': 'First Trimester Safe Exercises (Weeks 1-12)',
                'body': '''Safe exercises for early pregnancy:
• Walking (30 minutes daily) - low impact, improves circulation
• Prenatal yoga (gentle poses) - improves flexibility and relaxation
• Swimming (low-impact cardio) - supports joints and reduces swelling
• Pelvic floor exercises (Kegels) - strengthens muscles for labor
• Light stretching - improves flexibility and reduces muscle tension
• Avoid high-impact activities, contact sports, and exercises lying on back
• Listen to your body and rest when needed
• Stay hydrated and avoid overheating''',
                'week_start': 1,
                'week_end': 12
            },
            {
                'title': 'Second Trimester Workouts (Weeks 13-26)',
                'body': '''Second trimester exercise guidelines:
• Continue walking and swimming (30-45 minutes daily)
• Prenatal Pilates for core strength and stability
• Light strength training with modifications - focus on form
• Pelvic tilts and gentle stretches for back support
• Prenatal yoga for flexibility and breathing techniques
• Avoid exercises lying flat on your back
• Stay hydrated and take frequent breaks
• Monitor your heart rate and energy levels''',
                'week_start': 13,
                'week_end': 26
            },
            {
                'title': 'Third Trimester Movement (Weeks 27-40)',
                'body': '''Third trimester exercise tips:
• Gentle walking and swimming (20-30 minutes daily)
• Prenatal yoga for flexibility and labor preparation
• Pelvic floor exercises for labor and recovery
• Breathing exercises for labor preparation
• Gentle stretching for comfort and flexibility
• Avoid strenuous activities and exercises on your back
• Focus on comfort and relaxation
• Listen to your body and reduce intensity as needed
• Stay hydrated and take frequent rest breaks''',
                'week_start': 27,
                'week_end': 40
            },
            {
                'title': 'Postpartum Exercise Recovery',
                'body': '''Safe postpartum exercise progression:
• Start with gentle walking (10-15 minutes daily)
• Pelvic floor rehabilitation exercises
• Gentle stretching and mobility work
• Core strengthening (after 6-week clearance)
• Low-impact cardio (walking, swimming)
• Wait 6 weeks before intense exercise
• Listen to your body and go slowly
• Focus on healing and gradual progression
• Consult your doctor before starting any exercise program''',
                'week_start': None,
                'week_end': None
            }
        ]

        # Create week-based content
        for content_data in diet_content:
            InfoContent.objects.get_or_create(
                title=content_data['title'],
                defaults={
                    'category': 'diet',
                    'body': content_data['body'],
                    'week_start': content_data['week_start'],
                    'week_end': content_data['week_end']
                }
            )

        for content_data in exercise_content:
            InfoContent.objects.get_or_create(
                title=content_data['title'],
                defaults={
                    'category': 'exercise',
                    'body': content_data['body'],
                    'week_start': content_data['week_start'],
                    'week_end': content_data['week_end']
                }
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created week-based content!')
        ) 