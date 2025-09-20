from django.core.management.base import BaseCommand
from core.models import PregnancyTip

class Command(BaseCommand):
    help = 'Setup comprehensive trimester-specific Do\'s and Don\'ts for pregnancy'

    def handle(self, *args, **options):
        self.stdout.write('Setting up trimester-specific pregnancy tips...')
        
        # First Trimester Tips (Weeks 1-13)
        first_trimester_tips = [
            # DO's for First Trimester
            {
                'tip_type': 'do',
                'text_en': 'Take folic acid supplements (400-800 mcg daily)',
                'text_ne': 'फोलिक एसिड सप्लिमेंट लिनुहोस् (दैनिक 400-800 mcg)',
                'trimester': 1,
                'icon': 'fa-pills',
                'source': 'WHO',
                'info': 'Essential for neural tube development and preventing birth defects'
            },
            {
                'tip_type': 'do',
                'text_en': 'Eat small, frequent meals to manage morning sickness',
                'text_ne': 'सुबहको बिरामी व्यवस्थापन गर्न साना, बारम्बार भोजन खानुहोस्',
                'trimester': 1,
                'icon': 'fa-utensils',
                'source': 'MoHP',
                'info': 'Helps reduce nausea and maintain nutrition'
            },
            {
                'tip_type': 'do',
                'text_en': 'Stay hydrated with water, ginger tea, and clear broths',
                'text_ne': 'पानी, अदुवा चिया र सफा सूपले हाइड्रेटेड रहनुहोस्',
                'trimester': 1,
                'icon': 'fa-tint',
                'source': 'Local Expert',
                'info': 'Prevents dehydration and helps with morning sickness'
            },
            {
                'tip_type': 'do',
                'text_en': 'Get plenty of rest and sleep (8-10 hours daily)',
                'text_ne': 'धेरै आराम र निद्रा लिनुहोस् (दैनिक 8-10 घण्टा)',
                'trimester': 1,
                'icon': 'fa-bed',
                'source': 'WHO',
                'info': 'Your body needs extra energy for baby development'
            },
            {
                'tip_type': 'do',
                'text_en': 'Start prenatal vitamins as prescribed by your doctor',
                'text_ne': 'आफ्नो डाक्टरको सल्लाह अनुसार प्रसवपूर्व भिटामिन सुरु गर्नुहोस्',
                'trimester': 1,
                'icon': 'fa-heart',
                'source': 'MoHP',
                'info': 'Ensures proper nutrition for you and your baby'
            },
            {
                'tip_type': 'do',
                'text_en': 'Schedule your first prenatal appointment',
                'text_ne': 'आफ्नो पहिलो प्रसवपूर्व अपाइन्टमेन्ट तोक्नुहोस्',
                'trimester': 1,
                'icon': 'fa-calendar-check',
                'source': 'Local Expert',
                'info': 'Early prenatal care is crucial for healthy pregnancy'
            },
            {
                'tip_type': 'do',
                'text_en': 'Practice gentle exercises like walking and prenatal yoga',
                'text_ne': 'हिड्ने र प्रसवपूर्व योग जस्ता सान्त्वना व्यायाम गर्नुहोस्',
                'trimester': 1,
                'icon': 'fa-walking',
                'source': 'WHO',
                'info': 'Improves circulation and reduces stress'
            },
            
            # DON'Ts for First Trimester
            {
                'tip_type': 'dont',
                'text_en': 'Avoid raw fish, unpasteurized dairy, and undercooked meat',
                'text_ne': 'कच्चा माछा, बिना पास्चराइज गरिएको दूध र कच्चा मासु नखानुहोस्',
                'trimester': 1,
                'icon': 'fa-fish',
                'source': 'WHO',
                'info': 'Risk of foodborne illnesses that can harm the baby'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Limit caffeine intake (max 200mg daily)',
                'text_ne': 'क्याफिन सेवन सीमित गर्नुहोस् (दैनिक अधिकतम 200mg)',
                'trimester': 1,
                'icon': 'fa-coffee',
                'source': 'MoHP',
                'info': 'High caffeine can affect baby development'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid alcohol and smoking completely',
                'text_ne': 'पूर्ण रूपमा रक्सी र धुम्रपान नगर्नुहोस्',
                'trimester': 1,
                'icon': 'fa-ban',
                'source': 'WHO',
                'info': 'Can cause serious birth defects and complications'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t take hot baths or use hot tubs',
                'text_ne': 'तातो पानीको स्नान वा हट टब प्रयोग नगर्नुहोस्',
                'trimester': 1,
                'icon': 'fa-hot-tub',
                'source': 'Local Expert',
                'info': 'High temperatures can harm the developing baby'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid strenuous exercise and heavy lifting',
                'text_ne': 'कठिन व्यायाम र भारी वस्तु उचाल्न नगर्नुहोस्',
                'trimester': 1,
                'icon': 'fa-dumbbell',
                'source': 'WHO',
                'info': 'Can cause stress and potential complications'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t skip meals even if you feel nauseous',
                'text_ne': 'बिरामी लागे पनि भोजन छोड्न नगर्नुहोस्',
                'trimester': 1,
                'icon': 'fa-times-circle',
                'source': 'MoHP',
                'info': 'Your baby needs regular nutrition for development'
            },
        ]

        # Second Trimester Tips (Weeks 14-26)
        second_trimester_tips = [
            # DO's for Second Trimester
            {
                'tip_type': 'do',
                'text_en': 'Increase protein intake (75-100g daily)',
                'text_ne': 'प्रोटिन सेवन बढाउनुहोस् (दैनिक 75-100g)',
                'trimester': 2,
                'icon': 'fa-drumstick-bite',
                'source': 'WHO',
                'info': 'Essential for baby growth and development'
            },
            {
                'tip_type': 'do',
                'text_en': 'Eat calcium-rich foods (1000mg daily)',
                'text_ne': 'क्याल्सियम युक्त खाना खानुहोस् (दैनिक 1000mg)',
                'trimester': 2,
                'icon': 'fa-cheese',
                'source': 'MoHP',
                'info': 'Builds strong bones for you and your baby'
            },
            {
                'tip_type': 'do',
                'text_en': 'Continue regular prenatal checkups',
                'text_ne': 'नियमित प्रसवपूर्व जाँच जारी राख्नुहोस्',
                'trimester': 2,
                'icon': 'fa-stethoscope',
                'source': 'Local Expert',
                'info': 'Monitor your health and baby development'
            },
            {
                'tip_type': 'do',
                'text_en': 'Start pelvic floor exercises (Kegels)',
                'text_ne': 'श्रोणि तल्लो व्यायाम सुरु गर्नुहोस् (केगेल्स)',
                'trimester': 2,
                'icon': 'fa-dumbbell',
                'source': 'WHO',
                'info': 'Strengthens muscles for labor and recovery'
            },
            {
                'tip_type': 'do',
                'text_en': 'Wear comfortable, supportive maternity clothes',
                'text_ne': 'आरामदायक, सहयोगी मातृत्व कपडा लगाउनुहोस्',
                'trimester': 2,
                'icon': 'fa-tshirt',
                'source': 'Local Expert',
                'info': 'Supports your growing belly and reduces discomfort'
            },
            {
                'tip_type': 'do',
                'text_en': 'Practice good posture and body mechanics',
                'text_ne': 'राम्रो मुद्रा र शरीर यान्त्रिकी अभ्यास गर्नुहोस्',
                'trimester': 2,
                'icon': 'fa-user',
                'source': 'MoHP',
                'info': 'Reduces back pain and improves comfort'
            },
            {
                'tip_type': 'do',
                'text_en': 'Start planning for childbirth and baby care',
                'text_ne': 'प्रसव र बच्चा हेरचाहको योजना सुरु गर्नुहोस्',
                'trimester': 2,
                'icon': 'fa-baby',
                'source': 'Local Expert',
                'info': 'Prepare mentally and practically for the arrival'
            },
            
            # DON'Ts for Second Trimester
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t lie flat on your back for long periods',
                'text_ne': 'लामो समयसम्म आफ्नो पछाडि सपाट नसुत्नुहोस्',
                'trimester': 2,
                'icon': 'fa-bed',
                'source': 'WHO',
                'info': 'Can reduce blood flow to the baby'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid high-impact exercises and contact sports',
                'text_ne': 'उच्च प्रभाव व्यायाम र सम्पर्क खेलहरू नगर्नुहोस्',
                'trimester': 2,
                'icon': 'fa-running',
                'source': 'MoHP',
                'info': 'Risk of injury to you and your baby'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t skip meals or diet excessively',
                'text_ne': 'भोजन छोड्न वा अत्यधिक आहार नगर्नुहोस्',
                'trimester': 2,
                'icon': 'fa-times',
                'source': 'Local Expert',
                'info': 'Your baby needs consistent nutrition'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid standing for long periods',
                'text_ne': 'लामो समयसम्म उभिन नगर्नुहोस्',
                'trimester': 2,
                'icon': 'fa-user',
                'source': 'WHO',
                'info': 'Can cause swelling and discomfort'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t wear tight clothing around your waist',
                'text_ne': 'आफ्नो कम्मरमा तंग कपडा नलगाउनुहोस्',
                'trimester': 2,
                'icon': 'fa-tshirt',
                'source': 'MoHP',
                'info': 'Can restrict blood flow and cause discomfort'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid exposure to harmful chemicals and fumes',
                'text_ne': 'हानिकारक रसायन र धुवाँको संपर्क नगर्नुहोस्',
                'trimester': 2,
                'icon': 'fa-flask',
                'source': 'Local Expert',
                'info': 'Can affect baby development'
            },
        ]

        # Third Trimester Tips (Weeks 27-40)
        third_trimester_tips = [
            # DO's for Third Trimester
            {
                'tip_type': 'do',
                'text_en': 'Practice breathing exercises for labor',
                'text_ne': 'प्रसवको लागि सास फेर्ने व्यायाम अभ्यास गर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-lungs',
                'source': 'WHO',
                'info': 'Helps with pain management during labor'
            },
            {
                'tip_type': 'do',
                'text_en': 'Pack your hospital bag and prepare for delivery',
                'text_ne': 'आफ्नो अस्पताल बैग प्याक गर्नुहोस् र प्रसवको लागि तयार हुनुहोस्',
                'trimester': 3,
                'icon': 'fa-suitcase',
                'source': 'MoHP',
                'info': 'Be ready for when labor starts'
            },
            {
                'tip_type': 'do',
                'text_en': 'Continue gentle exercises like walking and swimming',
                'text_ne': 'हिड्ने र पौडी जस्ता सान्त्वना व्यायाम जारी राख्नुहोस्',
                'trimester': 3,
                'icon': 'fa-swimming-pool',
                'source': 'Local Expert',
                'info': 'Maintains fitness and reduces swelling'
            },
            {
                'tip_type': 'do',
                'text_en': 'Sleep on your left side for better blood flow',
                'text_ne': 'राम्रो रक्त प्रवाहको लागि आफ्नो बायाँतिर सुत्नुहोस्',
                'trimester': 3,
                'icon': 'fa-bed',
                'source': 'WHO',
                'info': 'Improves circulation to the baby'
            },
            {
                'tip_type': 'do',
                'text_en': 'Learn about labor signs and when to go to hospital',
                'text_ne': 'प्रसवको संकेत र कहिले अस्पताल जाने बारे सिक्नुहोस्',
                'trimester': 3,
                'icon': 'fa-hospital',
                'source': 'MoHP',
                'info': 'Know when it\'s time to seek medical help'
            },
            {
                'tip_type': 'do',
                'text_en': 'Eat small, frequent meals to avoid heartburn',
                'text_ne': 'एसिडिटी बाट बच्न साना, बारम्बार भोजन खानुहोस्',
                'trimester': 3,
                'icon': 'fa-utensils',
                'source': 'Local Expert',
                'info': 'Reduces digestive discomfort'
            },
            {
                'tip_type': 'do',
                'text_en': 'Stay hydrated and monitor swelling',
                'text_ne': 'हाइड्रेटेड रहनुहोस् र सुन्निने कुरा निरीक्षण गर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-tint',
                'source': 'WHO',
                'info': 'Prevents complications and monitors health'
            },
            
            # DON'Ts for Third Trimester
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t travel long distances without medical approval',
                'text_ne': 'चिकित्सकीय अनुमति बिना लामो दूरी यात्रा नगर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-plane',
                'source': 'MoHP',
                'info': 'Risk of preterm labor away from medical care'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid strenuous activities and heavy lifting',
                'text_ne': 'कठिन गतिविधिहरू र भारी वस्तु उचाल्न नगर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-dumbbell',
                'source': 'WHO',
                'info': 'Can trigger preterm labor'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t ignore signs of preterm labor',
                'text_ne': 'अकाल प्रसवको संकेतहरूलाई बेवास्ता नगर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-exclamation-triangle',
                'source': 'Local Expert',
                'info': 'Seek immediate medical attention if concerned'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid lying flat on your back',
                'text_ne': 'आफ्नो पछाडि सपाट नसुत्नुहोस्',
                'trimester': 3,
                'icon': 'fa-bed',
                'source': 'WHO',
                'info': 'Can cause dizziness and reduce blood flow'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Don\'t skip prenatal appointments',
                'text_ne': 'प्रसवपूर्व अपाइन्टमेन्टहरू छोड्न नगर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-calendar-times',
                'source': 'MoHP',
                'info': 'Regular monitoring is crucial in final trimester'
            },
            {
                'tip_type': 'dont',
                'text_en': 'Avoid hot baths and saunas',
                'text_ne': 'तातो पानीको स्नान र साउना नगर्नुहोस्',
                'trimester': 3,
                'icon': 'fa-hot-tub',
                'source': 'Local Expert',
                'info': 'Can cause overheating and complications'
            },
        ]

        # Combine all trimester tips
        all_tips = first_trimester_tips + second_trimester_tips + third_trimester_tips

        # Create tips in database
        created_count = 0
        for tip_data in all_tips:
            tip, created = PregnancyTip.objects.get_or_create(
                text_en=tip_data['text_en'],
                trimester=tip_data['trimester'],
                tip_type=tip_data['tip_type'],
                defaults={
                    'text_ne': tip_data['text_ne'],
                    'icon': tip_data['icon'],
                    'source': tip_data['source'],
                    'info': tip_data['info'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created tip: {tip.text_en[:50]}...")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} trimester-specific pregnancy tips!')
        )
        
        # Display summary
        for trimester in [1, 2, 3]:
            do_count = PregnancyTip.objects.filter(trimester=trimester, tip_type='do', is_active=True).count()
            dont_count = PregnancyTip.objects.filter(trimester=trimester, tip_type='dont', is_active=True).count()
            self.stdout.write(f'Trimester {trimester}: {do_count} Do\'s, {dont_count} Don\'ts') 