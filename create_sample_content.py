import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

from core.models import InfoContent

# Create sample trimester-specific diet content
diet_content = [
    # First Trimester Diet
    {
        'category': 'diet',
        'title': 'First Trimester Nutrition Essentials',
        'body': 'Focus on folic acid-rich foods like leafy greens, legumes, and fortified cereals. Eat small, frequent meals to manage nausea. Stay hydrated and include iron-rich foods.',
        'trimester': '1',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    {
        'category': 'diet',
        'title': 'Foods to Avoid in Early Pregnancy',
        'body': 'Avoid raw or undercooked eggs, meat, and fish. Stay away from unpasteurized dairy. Limit caffeine to 200mg per day. Avoid alcohol completely.',
        'trimester': '1',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    # Second Trimester Diet
    {
        'category': 'diet',
        'title': 'Second Trimester Protein Boost',
        'body': 'Increase protein intake for baby\'s rapid growth. Include lean meats, fish, eggs, beans, and dairy. Aim for 70-100g of protein daily.',
        'trimester': '2',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    {
        'category': 'diet',
        'title': 'Calcium-Rich Foods for Strong Bones',
        'body': 'Your baby\'s bones are developing. Eat dairy products, leafy greens, and calcium-fortified foods. Include vitamin D for calcium absorption.',
        'trimester': '2',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    # Third Trimester Diet
    {
        'category': 'diet',
        'title': 'Third Trimester Energy Foods',
        'body': 'Eat smaller, frequent meals as space is limited. Focus on complex carbohydrates for sustained energy. Include omega-3 rich foods for brain development.',
        'trimester': '3',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    {
        'category': 'diet',
        'title': 'Preparing for Breastfeeding',
        'body': 'Build up nutrient stores for breastfeeding. Include iron, zinc, and B-vitamins. Stay well-hydrated with 8-10 glasses of water daily.',
        'trimester': '3',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    # Postpartum Diet - Early Stage
    {
        'category': 'diet',
        'title': 'Early Postpartum Nutrition',
        'body': 'Focus on recovery foods rich in protein and iron. Eat plenty of fruits, vegetables, and whole grains. Stay hydrated for milk production.',
        'trimester': 'all',
        'postpartum_stage': 'early',
        'target_audience': 'mother',
    },
    # Postpartum Diet - Mid Stage
    {
        'category': 'diet',
        'title': 'Mid Recovery Nutrition Plan',
        'body': 'Continue nutritious diet supporting breastfeeding. Include galactagogues like oats and fenugreek if needed. Balance calories for gradual weight management.',
        'trimester': 'all',
        'postpartum_stage': 'mid',
        'target_audience': 'mother',
    },
]

# Create sample trimester-specific exercise content
exercise_content = [
    # First Trimester Exercise
    {
        'category': 'exercise',
        'title': 'Safe First Trimester Exercises',
        'body': 'Gentle walking for 20-30 minutes daily. Light stretching and yoga. Swimming is excellent. Avoid high-impact and contact sports.',
        'trimester': '1',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    {
        'category': 'exercise',
        'title': 'Managing Fatigue with Movement',
        'body': 'Light exercise can help combat first trimester fatigue. Try prenatal yoga or gentle stretches. Rest when needed but stay active.',
        'trimester': '1',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    # Second Trimester Exercise
    {
        'category': 'exercise',
        'title': 'Second Trimester Workouts',
        'body': 'Continue walking and swimming. Add prenatal yoga and Pilates. Strength training with light weights. Focus on posture and balance.',
        'trimester': '2',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    {
        'category': 'exercise',
        'title': 'Pelvic Floor Exercises (Kegels)',
        'body': 'Strengthen pelvic floor muscles with Kegel exercises. Do 10-15 repetitions, 3 times daily. These help prepare for labor and recovery.',
        'trimester': '2',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    # Third Trimester Exercise
    {
        'category': 'exercise',
        'title': 'Third Trimester Movement',
        'body': 'Gentle walking and stretching. Prenatal yoga for flexibility. Swimming for relief from swelling. Avoid lying flat on back.',
        'trimester': '3',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    {
        'category': 'exercise',
        'title': 'Labor Preparation Exercises',
        'body': 'Practice breathing techniques. Squats and pelvic tilts for labor prep. Stretches for hip flexibility. Deep relaxation exercises.',
        'trimester': '3',
        'postpartum_stage': 'all',
        'target_audience': 'pregnant',
    },
    # Postpartum Exercise - Early Stage
    {
        'category': 'exercise',
        'title': 'Early Postpartum Recovery',
        'body': 'Start with gentle walking. Kegel exercises to rebuild pelvic floor. Deep breathing exercises. Avoid strenuous activity for 6 weeks.',
        'trimester': 'all',
        'postpartum_stage': 'early',
        'target_audience': 'mother',
    },
    # Postpartum Exercise - Mid Stage
    {
        'category': 'exercise',
        'title': 'Mid Recovery Workouts',
        'body': 'Gradually increase activity with doctor approval. Light cardio and strength training. Postnatal yoga classes. Core rebuilding exercises.',
        'trimester': 'all',
        'postpartum_stage': 'mid',
        'target_audience': 'mother',
    },
    # Postpartum Exercise - Established
    {
        'category': 'exercise',
        'title': 'Full Postpartum Fitness',
        'body': 'Resume regular exercise routine. Include cardio, strength, and flexibility. Join mom-and-baby fitness classes. Listen to your body.',
        'trimester': 'all',
        'postpartum_stage': 'established',
        'target_audience': 'mother',
    },
]

# Create content in database
created_count = 0
for content_data in diet_content + exercise_content:
    obj, created = InfoContent.objects.get_or_create(
        title=content_data['title'],
        defaults=content_data
    )
    if created:
        created_count += 1
        print(f"Created: {content_data['title']}")
    else:
        # Update existing content with new fields
        for key, value in content_data.items():
            setattr(obj, key, value)
        obj.save()
        print(f"Updated: {content_data['title']}")

print(f"\nTotal new content created: {created_count}")
print("Sample trimester-specific content has been added to the database!")
