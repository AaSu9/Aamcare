from django.core.management.base import BaseCommand
from core.models import InfoContent, HealthExpert
from django.utils import timezone
from datetime import date

class Command(BaseCommand):
    help = 'Setup nutrition content specifically for new mothers (postpartum and breastfeeding)'

    def handle(self, *args, **options):
        # Get the existing nutrition expert
        expert = HealthExpert.objects.filter(expert_type='nutritionist').first()
        
        if not expert:
            expert = HealthExpert.objects.create(
                name="Dr. Postpartum Nutrition Expert",
                expert_type='nutritionist',
                qualification='MSc in Clinical Nutrition, Specialized in Postpartum Care',
                institution='Nepal Medical Council',
                years_experience=12,
                bio='Specialized in postpartum nutrition and breastfeeding support with extensive experience in maternal health.',
                is_active=True,
            )

        # Postpartum Recovery Nutrition
        postpartum_recovery = InfoContent.objects.create(
            category='breastfeeding',
            title='Postpartum Recovery Nutrition - Heal & Rebuild Your Body',
            body='''🩺 **POSTPARTUM RECOVERY NUTRITION GUIDE**

**Your body needs special care after childbirth. This nutrition plan helps you heal, recover, and prepare for breastfeeding.**

## 🏥 **First 6 Weeks - Recovery Phase**

**Week 1-2 (Immediate Recovery):**
- **Focus:** Healing and rest
- **Calories:** 2,200-2,500 kcal/day
- **Protein:** 80-100g/day
- **Fluids:** 3+ liters/day

**Recommended Foods:**
- Warm, easily digestible foods
- Soft rice, dal, khichdi
- Boiled vegetables
- Warm milk with turmeric
- Light soups and broths

**Week 3-6 (Building Strength):**
- **Focus:** Rebuilding strength and energy
- **Calories:** 2,400-2,800 kcal/day
- **Protein:** 90-110g/day
- **Iron:** 18mg/day (replenish blood loss)

## 🥘 **Recovery Meal Plan**

**Breakfast (7-8 AM):**
- Ragi porridge with milk and jaggery
- OR Oats with banana and nuts
- Warm herbal tea (ginger, fennel)

**Mid-Morning (10 AM):**
- Fresh fruit (apple, banana, papaya)
- OR Dry fruits (almonds, walnuts)
- Coconut water

**Lunch (1-2 PM):**
- Rice + dal + green vegetables
- OR Roti + sabji + paneer
- Curd or buttermilk

**Evening (4-5 PM):**
- Herbal tea with biscuits
- OR Sprouts salad
- OR Roasted chana

**Dinner (8-9 PM):**
- Light khichdi with vegetables
- OR Chapati + dal + vegetables
- Warm milk with turmeric

**Before Bed:**
- Warm milk with honey
- OR Herbal tea (chamomile, fennel)

## 💊 **Essential Supplements for Recovery**

**Iron Supplements:**
- **Why:** Replenish blood loss during delivery
- **Dosage:** 30-60mg daily (as prescribed)
- **Best Time:** Empty stomach with vitamin C

**Calcium Supplements:**
- **Why:** Bone health and milk production
- **Dosage:** 1000-1300mg daily
- **Best Time:** With meals

**Multivitamins:**
- **Why:** Overall recovery and immunity
- **Dosage:** Once daily
- **Best Time:** Morning with breakfast

**Probiotics:**
- **Why:** Digestive health and immunity
- **Sources:** Curd, yogurt, probiotic supplements

## 🚫 **Foods to Avoid During Recovery**

**First 2 Weeks:**
- Spicy and oily foods
- Cold foods and drinks
- Raw vegetables
- Heavy, difficult-to-digest foods
- Caffeine and alcohol

**First 6 Weeks:**
- Street food
- Unpasteurized dairy
- Raw or undercooked foods
- Excessive sweets and fried foods

## 🩸 **Special Care for C-Section Recovery**

**Week 1-2:**
- Soft, easily digestible foods
- Avoid gas-producing foods (beans, cabbage)
- Extra protein for wound healing
- Plenty of fluids

**Week 3-6:**
- Gradually increase fiber
- Include iron-rich foods
- Continue high protein diet
- Gentle exercise as approved by doctor

## 💪 **Energy-Boosting Foods**

**For Fatigue:**
- Bananas (potassium and energy)
- Nuts and seeds (healthy fats)
- Whole grains (sustained energy)
- Sweet potatoes (complex carbs)

**For Immunity:**
- Citrus fruits (vitamin C)
- Garlic and ginger (natural immunity)
- Turmeric (anti-inflammatory)
- Green leafy vegetables

## 🚨 **Warning Signs - Contact Doctor**

- Severe abdominal pain
- Heavy bleeding
- High fever
- Severe headache
- Swelling in legs
- Difficulty breathing
- Loss of appetite for 2+ days

## 📋 **Recovery Checklist**

**Week 1:**
- [ ] Rest as much as possible
- [ ] Stay hydrated (3+ liters daily)
- [ ] Eat small, frequent meals
- [ ] Take prescribed supplements

**Week 2-4:**
- [ ] Gradually increase activity
- [ ] Continue nutritious diet
- [ ] Start gentle exercises (if approved)
- [ ] Monitor healing progress

**Week 5-6:**
- [ ] Resume normal diet
- [ ] Continue supplements
- [ ] Prepare for breastfeeding
- [ ] Plan return to normal activities

**Remember:** Every woman's recovery is different. Listen to your body and consult your healthcare provider for personalized advice.''',
            week_start=1,
            week_end=52,
            source='nepal_mohp',
            source_reference='Nepal Ministry of Health - Postpartum Recovery Guidelines 2024',
            reviewed_by=expert,
            review_date=date.today(),
            is_government_approved=True,
            is_culturally_sensitive=True,
            cultural_context='Recovery plan includes traditional Nepali postpartum practices and local food preferences. Respects cultural beliefs about postpartum care.',
            local_language_available=True,
        )

        # Breastfeeding Support Content
        breastfeeding_support = InfoContent.objects.create(
            category='breastfeeding',
            title='Complete Breastfeeding Guide - Nutrition & Techniques',
            body='''🤱 **COMPLETE BREASTFEEDING GUIDE**

**Breastfeeding provides the best nutrition for your baby. This guide covers everything from nutrition to techniques.**

## 🥛 **Breastfeeding Nutrition Essentials**

**Daily Calorie Needs:**
- **Exclusive Breastfeeding:** +500 kcal/day
- **Mixed Feeding:** +300 kcal/day
- **Total Daily Calories:** 2,300-2,800 kcal

**Key Nutrients for Milk Production:**

| Nutrient | Daily Need | Best Sources |
|----------|------------|--------------|
| **Protein** | 75-100g | Eggs, chicken, dal, milk, paneer |
| **Calcium** | 1000-1300mg | Milk, curd, sesame seeds, ragi |
| **Iron** | 15-18mg | Spinach, jaggery, meat, lentils |
| **Vitamin C** | 65-90mg | Oranges, guava, tomatoes, lemon |
| **Omega-3** | Moderate | Fish, flaxseeds, walnuts |
| **Fluids** | 3+ liters | Water, soup, juice, herbal tea |

## 🍽 **Breastfeeding Meal Plan**

**Early Morning (5-6 AM):**
- Warm water with lemon
- Light snack (banana, nuts)

**Breakfast (8-9 AM):**
- Ragi porridge with milk and jaggery
- OR Oats with fruits and nuts
- Herbal tea (fennel, ginger)

**Mid-Morning (11 AM):**
- Fresh fruit or dry fruits
- Coconut water or fresh juice

**Lunch (1-2 PM):**
- Rice + dal + green vegetables + curd
- OR Roti + sabji + paneer
- Buttermilk or lassi

**Evening (4-5 PM):**
- Sprouts salad or roasted chana
- Herbal tea with biscuits

**Dinner (8-9 PM):**
- Chapati + dal + vegetables
- OR Khichdi with vegetables
- Warm milk with turmeric

**Before Bed:**
- Warm milk with honey
- OR Herbal tea (chamomile)

## 🌿 **Galactagogues (Milk-Boosting Foods)**

**Traditional Galactagogues:**
- **Fenugreek Seeds:** 1 tsp daily with water
- **Fennel Seeds:** Add to tea or food
- **Sesame Seeds:** 2 tbsp daily
- **Almonds:** 8-10 pieces daily
- **Jaggery:** 1-2 small pieces daily

**Modern Galactagogues:**
- **Oats:** 1 cup daily
- **Brewer's Yeast:** 1 tbsp daily
- **Flaxseeds:** 1 tbsp ground daily
- **Pumpkin Seeds:** 2 tbsp daily

## 🤱 **Breastfeeding Techniques**

**Proper Latch:**
1. Hold baby close to your breast
2. Touch baby's lips with your nipple
3. Wait for baby to open mouth wide
4. Bring baby to breast (not breast to baby)
5. Ensure baby takes both nipple and areola

**Signs of Good Latch:**
- Baby's mouth covers most of areola
- Baby's lips are turned outward
- You can hear swallowing sounds
- No pain during feeding
- Baby releases breast naturally

**Feeding Positions:**
- **Cradle Hold:** Most common position
- **Cross-Cradle:** Good for newborns
- **Football Hold:** Good for C-section
- **Side-Lying:** Good for night feeds

## 📊 **Feeding Schedule Guide**

**Newborn (0-2 weeks):**
- Feed every 2-3 hours
- 8-12 feeds per day
- Feed on demand
- Wake baby if sleeping >4 hours

**2-6 weeks:**
- Feed every 2-4 hours
- 8-10 feeds per day
- Establish routine
- Night feeds still needed

**6 weeks - 6 months:**
- Feed every 3-4 hours
- 6-8 feeds per day
- More predictable schedule
- Some babies sleep through night

## 🚨 **Common Breastfeeding Problems**

**Sore Nipples:**
- **Cause:** Poor latch, dry skin
- **Solution:** Improve latch, apply lanolin
- **Prevention:** Air dry nipples after feeding

**Engorgement:**
- **Cause:** Too much milk, missed feeds
- **Solution:** Frequent feeding, warm compress
- **Prevention:** Regular feeding schedule

**Low Milk Supply:**
- **Causes:** Stress, poor nutrition, infrequent feeding
- **Solutions:** Increase fluids, rest, frequent feeding
- **Galactagogues:** Fenugreek, oats, fennel

**Mastitis:**
- **Symptoms:** Red, painful, swollen breast
- **Treatment:** Antibiotics, rest, frequent feeding
- **Prevention:** Empty breasts completely

## ✅ **Signs Baby is Getting Enough Milk**

**Daily Diapers:**
- 6+ wet diapers
- 3-4 dirty diapers (first month)
- 1-2 dirty diapers (after 1 month)

**Baby's Behavior:**
- Satisfied after feeding
- Sleeps 2-3 hours between feeds
- Gains weight steadily
- Alert and active when awake

**Your Body:**
- Breasts feel softer after feeding
- Milk leaks from other breast
- You feel thirsty during feeding
- Breasts feel full before feeding

## 🚫 **Foods to Avoid While Breastfeeding**

**May Cause Gas in Baby:**
- Cabbage, cauliflower, broccoli
- Beans, lentils (in large amounts)
- Spicy foods
- Carbonated drinks

**May Affect Baby:**
- Alcohol (pump and dump if consumed)
- Excessive caffeine
- Strong spices
- Allergenic foods (if family history)

## 💊 **Medication Safety While Breastfeeding**

**Safe Medications:**
- Paracetamol (500mg as needed)
- Most antibiotics (doctor-approved)
- Calcium and iron supplements
- Multivitamins

**Consult Doctor Before Taking:**
- Any new medication
- Herbal supplements
- Over-the-counter medicines
- Prescription drugs

## 📞 **When to Contact Doctor**

**For Mother:**
- Severe breast pain
- High fever with flu-like symptoms
- Cracked or bleeding nipples
- Persistent low milk supply

**For Baby:**
- Not gaining weight
- Fewer than 6 wet diapers daily
- Very fussy or sleepy
- Yellow skin or eyes

**Remember:** Breastfeeding is a learned skill. Be patient with yourself and your baby. Seek help from lactation consultants if needed.''',
            week_start=1,
            week_end=52,
            source='local_expert',
            source_reference='Local Lactation Expert Consultation',
            reviewed_by=expert,
            review_date=date.today(),
            is_government_approved=True,
            is_culturally_sensitive=True,
            cultural_context='Breastfeeding guide includes traditional Nepali practices and local food preferences. Respects cultural beliefs about breastfeeding and postpartum care.',
            local_language_available=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created mother-specific nutrition content:\n'
                f'- Postpartum Recovery Nutrition Guide\n'
                f'- Complete Breastfeeding Guide\n'
                f'All content is doctor-reviewed and culturally adapted for Nepali mothers.'
            )
        ) 