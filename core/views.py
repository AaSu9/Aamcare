from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.views import LoginView
from .forms import PregnantWomanRegistrationForm, NewMotherRegistrationForm, CheckupProgressForm, VaccinationRecordForm, UserTestimonialForm, GiveBirthForm, PregnantWomanProfileUpdateForm, NewMotherProfileUpdateForm
from .models import (
    PregnantWomanProfile, NewMotherProfile, CheckupProgress, InfoContent, 
    VaccinationRecord, HealthExpert, UserTestimonial, CommunityHealthWorker, PregnancyTip, HealthRecommendation
)
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
# Custom language session key
LANGUAGE_SESSION_KEY = 'django_language'

def home(request):
    # Get featured testimonials for the homepage
    featured_testimonials = UserTestimonial.objects.filter(is_approved=True, is_featured=True)[:4]
    
    # Get active health experts
    health_experts = HealthExpert.objects.filter(is_active=True)[:4]
    
    # Get government-approved content count
    gov_approved_count = InfoContent.objects.filter(is_government_approved=True).count()
    
    # Get current language from session
    language = request.session.get('django_language', 'en')
    
    context = {
        'featured_testimonials': featured_testimonials,
        'health_experts': health_experts,
        'gov_approved_count': gov_approved_count,
        'language': language,
    }
    return render(request, 'core/home.html', context)

def whatsapp_setup_guide(request):
    """Display the WhatsApp setup guide"""
    return render(request, 'core/whatsapp_setup_guide.html')

def generate_whatsapp_qr(request):
    """Generate a QR code for WhatsApp setup"""
    # WhatsApp join URL
    whatsapp_url = "https://wa.me/14155238886?text=join+machinery-egg"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(whatsapp_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Return as HTTP response
    return HttpResponse(buffer.getvalue(), content_type="image/png")

def register_pregnant_woman(request):
    if request.method == 'POST':
        form = PregnantWomanRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = PregnantWomanProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                due_date=form.cleaned_data['due_date'],
                medical_history=form.cleaned_data['medical_history'],
                phone_number=form.cleaned_data['phone_number']
            )
            
            # Create vaccination schedule for pregnant woman
            create_pregnancy_vaccination_schedule(profile)
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AamCare.')
            return redirect('pregnant_dashboard')
    else:
        form = PregnantWomanRegistrationForm()
    return render(request, 'core/register_pregnant.html', {'form': form})

def register_new_mother(request):
    if request.method == 'POST':
        form = NewMotherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = NewMotherProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                child_birth_date=form.cleaned_data['child_birth_date'],
                current_health_status=form.cleaned_data['current_health_status'],
                phone_number=form.cleaned_data['phone_number']
            )
            
            # Create vaccination schedule for baby
            create_baby_vaccination_schedule(profile)
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AamCare.')
            return redirect('mother_dashboard')
    else:
        form = NewMotherRegistrationForm()
    return render(request, 'core/register_mother.html', {'form': form})

def create_pregnancy_vaccination_schedule(profile):
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

def create_baby_vaccination_schedule(profile):
    """Create vaccination schedule for baby and mother based on actual birth date"""
    birth_date = profile.child_birth_date
    
    # MOTHER VACCINES (Postpartum)
    # Tdap for mother (if not received during pregnancy)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Tdap (Mother)',
        due_date=birth_date + timedelta(days=7),  # 1 week after birth
        status='pending'
    )
    
    # Influenza for mother (seasonal)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Influenza (Mother)',
        due_date=birth_date + timedelta(days=14),  # 2 weeks after birth
        status='pending'
    )
    
    # COVID-19 for mother (if needed)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='COVID-19 (Mother)',
        due_date=birth_date + timedelta(days=21),  # 3 weeks after birth
        status='pending'
    )
    
    # BABY VACCINES
    # Birth vaccines (BCG, Hepatitis B)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='BCG (Birth)',
        due_date=birth_date,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hepatitis B (Birth)',
        due_date=birth_date,
        status='pending'
    )
    
    # 6 weeks vaccines
    six_weeks = birth_date + timedelta(days=42)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='OPV-1 (Oral Polio)',
        due_date=six_weeks,
        status='pending'
    )
    
    # 10 weeks vaccines
    ten_weeks = birth_date + timedelta(days=70)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='OPV-2 (Oral Polio)',
        due_date=ten_weeks,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='DPT-1 (Diphtheria, Pertussis, Tetanus)',
        due_date=ten_weeks,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hepatitis B-1',
        due_date=ten_weeks,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hib-1 (Haemophilus influenzae type b)',
        due_date=ten_weeks,
        status='pending'
    )
    
    # 14 weeks vaccines
    fourteen_weeks = birth_date + timedelta(days=98)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='OPV-3 (Oral Polio)',
        due_date=fourteen_weeks,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='DPT-2 (Diphtheria, Pertussis, Tetanus)',
        due_date=fourteen_weeks,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hepatitis B-2',
        due_date=fourteen_weeks,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hib-2 (Haemophilus influenzae type b)',
        due_date=fourteen_weeks,
        status='pending'
    )
    
    # 9 months vaccines
    nine_months = birth_date + timedelta(days=270)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='OPV-4 (Oral Polio)',
        due_date=nine_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='DPT-3 (Diphtheria, Pertussis, Tetanus)',
        due_date=nine_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hepatitis B-3',
        due_date=nine_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hib-3 (Haemophilus influenzae type b)',
        due_date=nine_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Measles-1',
        due_date=nine_months,
        status='pending'
    )
    
    # 15 months vaccines
    fifteen_months = birth_date + timedelta(days=450)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='MMR-1 (Measles, Mumps, Rubella)',
        due_date=fifteen_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Varicella-1 (Chickenpox)',
        due_date=fifteen_months,
        status='pending'
    )
    
    # 18 months vaccines
    eighteen_months = birth_date + timedelta(days=540)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='DPT Booster-1',
        due_date=eighteen_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='OPV Booster-1',
        due_date=eighteen_months,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Hib Booster-1',
        due_date=eighteen_months,
        status='pending'
    )
    
    # 24 months vaccines
    twenty_four_months = birth_date + timedelta(days=720)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='Typhoid Conjugate Vaccine',
        due_date=twenty_four_months,
        status='pending'
    )
    
    # 5 years vaccines
    five_years = birth_date + timedelta(days=1825)
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='DPT Booster-2',
        due_date=five_years,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='OPV Booster-2',
        due_date=five_years,
        status='pending'
    )
    VaccinationRecord.objects.create(
        mother_profile=profile,
        vaccine_name='MMR-2 (Measles, Mumps, Rubella)',
        due_date=five_years,
        status='pending'
    )

@login_required
def pregnant_dashboard(request):
    try:
        profile = PregnantWomanProfile.objects.get(user=request.user)
        checkups = CheckupProgress.objects.filter(pregnant_profile=profile).order_by('-created_at')
        vaccinations = VaccinationRecord.objects.filter(pregnant_profile=profile).order_by('due_date')
        
        # Calculate pregnancy dates and current status
        pregnancy_dates = profile.get_pregnancy_dates()
        current_week = profile.get_current_pregnancy_week()
        current_month = profile.get_current_pregnancy_month()
        current_trimester = profile.get_trimester()
        baby_size_fruit, baby_size_emoji = profile.get_baby_size_description()
        
        # Get trimester-specific content using Q objects for OR conditions
        from django.db.models import Q
        
        # Filter diet content by trimester
        diet_content = InfoContent.objects.filter(
            category='diet'
        ).filter(
            Q(trimester=str(current_trimester)) | Q(trimester='all')
        ).filter(
            Q(target_audience='pregnant') | Q(target_audience='both')
        )
        
        # Filter exercise content by trimester
        exercise_content = InfoContent.objects.filter(
            category='exercise'
        ).filter(
            Q(trimester=str(current_trimester)) | Q(trimester='all')
        ).filter(
            Q(target_audience='pregnant') | Q(target_audience='both')
        )
        
        # Get all vaccine content (not filtered by trimester)
        vaccine_content = InfoContent.objects.filter(category='vaccine')
        
        # Get trimester-specific tips
        trimester_tips_content = {
            1: {
                'name': 'First Trimester',
                'weeks': 'Weeks 1-13',
                'tips': [
                    'Take prenatal vitamins with folic acid daily',
                    'Stay hydrated - drink 8-10 glasses of water',
                    'Get plenty of rest to combat fatigue',
                    'Avoid alcohol, smoking, and raw foods',
                    'Start gentle exercises like walking',
                ]
            },
            2: {
                'name': 'Second Trimester',
                'weeks': 'Weeks 14-26',
                'tips': [
                    'Continue prenatal vitamins and calcium',
                    'Increase protein intake for baby growth',
                    'Start pregnancy exercises and yoga',
                    'Begin preparing for breastfeeding',
                    'Plan your birth and hospital arrangements',
                ]
            },
            3: {
                'name': 'Third Trimester',
                'weeks': 'Weeks 27-40',
                'tips': [
                    'Rest frequently and sleep on your side',
                    'Eat smaller, frequent meals',
                    'Practice breathing exercises for labor',
                    'Pack your hospital bag',
                    'Know the signs of labor and when to go to hospital',
                ]
            }
        }
        
        # Update vaccination status based on due dates
        update_vaccination_status(vaccinations)
        
        # Get health recommendations for the latest checkup
        health_recommendations = []
        urgent_recommendation = None
        if checkups:
            latest_checkup = checkups.first()
            health_recommendations = latest_checkup.healthrecommendation_set.all()
            
            # Find the first urgent or high priority recommendation
            for recommendation in health_recommendations:
                if recommendation.severity in ['urgent', 'high']:
                    urgent_recommendation = recommendation
                    break
        
        context = {
            'profile': profile,
            'checkups': checkups,
            'vaccinations': vaccinations,
            'diet_content': diet_content,
            'exercise_content': exercise_content,
            'vaccine_content': vaccine_content,
            'pregnancy_dates': pregnancy_dates,
            'current_week': current_week,
            'current_month': current_month,
            'current_trimester': current_trimester,
            'trimester_info': trimester_tips_content.get(current_trimester, {}),
            'health_recommendations': health_recommendations,
            'urgent_recommendation': urgent_recommendation,
            'baby_size_fruit': baby_size_fruit,
            'baby_size_emoji': baby_size_emoji,
        }
        return render(request, 'core/pregnant_dashboard.html', context)
    except PregnantWomanProfile.DoesNotExist:
        messages.error(request, 'Pregnant woman profile not found.')
        return redirect('home')

@login_required
def update_pregnant_profile(request):
    profile = PregnantWomanProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PregnantWomanProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone number updated successfully!')
            return redirect('pregnant_dashboard')
    else:
        form = PregnantWomanProfileUpdateForm(instance=profile)
    return render(request, 'core/update_profile.html', {'form': form, 'profile_type': 'pregnant'})

@login_required
def update_mother_profile(request):
    profile = NewMotherProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = NewMotherProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone number updated successfully!')
            return redirect('mother_dashboard')
    else:
        form = NewMotherProfileUpdateForm(instance=profile)
    return render(request, 'core/update_profile.html', {'form': form, 'profile_type': 'mother'})

@login_required
def mother_dashboard(request):
    try:
        profile = NewMotherProfile.objects.get(user=request.user)
        checkups = CheckupProgress.objects.filter(mother_profile=profile).order_by('-created_at')
        vaccinations = VaccinationRecord.objects.filter(mother_profile=profile).order_by('due_date')
        
        # Get postpartum dates and stage for planning
        postpartum_dates = profile.get_postpartum_dates()
        postpartum_stage = profile.get_postpartum_stage()
        
        # Get postpartum stage-specific content using Q objects
        from django.db.models import Q
        
        # Filter breastfeeding content by postpartum stage
        breastfeeding_content = InfoContent.objects.filter(
            category='breastfeeding'
        ).filter(
            Q(postpartum_stage=postpartum_stage) | Q(postpartum_stage='all')
        ).filter(
            Q(target_audience='mother') | Q(target_audience='both')
        )
        
        # Filter mental health content by postpartum stage
        mental_content = InfoContent.objects.filter(
            category='mental'
        ).filter(
            Q(postpartum_stage=postpartum_stage) | Q(postpartum_stage='all')
        ).filter(
            Q(target_audience='mother') | Q(target_audience='both')
        )
        
        # Filter exercise content by postpartum stage
        exercise_content = InfoContent.objects.filter(
            category='exercise'
        ).filter(
            Q(postpartum_stage=postpartum_stage) | Q(postpartum_stage='all')
        ).filter(
            Q(target_audience='mother') | Q(target_audience='both')
        )
        
        # Filter diet content by postpartum stage
        diet_content = InfoContent.objects.filter(
            category='diet'
        ).filter(
            Q(postpartum_stage=postpartum_stage) | Q(postpartum_stage='all')
        ).filter(
            Q(target_audience='mother') | Q(target_audience='both')
        )
        
        # Get postpartum stage-specific tips
        stage_info = {
            'early': {
                'name': 'Early Recovery',
                'period': '0-6 weeks postpartum',
                'tips': [
                    'Rest as much as possible - your body is healing',
                    'Focus on breastfeeding and bonding with baby',
                    'Eat nutritious foods to support milk production',
                    'Gentle walking only - avoid strenuous exercise',
                    'Watch for signs of postpartum depression',
                ]
            },
            'mid': {
                'name': 'Mid Recovery',
                'period': '6 weeks - 3 months postpartum',
                'tips': [
                    'Gradually increase physical activity',
                    'Start light exercises with doctor approval',
                    'Continue nutritious diet for breastfeeding',
                    'Establish a sleep routine for you and baby',
                    'Connect with other new mothers for support',
                ]
            },
            'established': {
                'name': 'Established Recovery',
                'period': '3+ months postpartum',
                'tips': [
                    'Resume regular exercise routine',
                    'Consider starting solids for baby (after 6 months)',
                    'Focus on self-care and mental health',
                    'Plan for any work-life balance adjustments',
                    'Continue regular check-ups for you and baby',
                ]
            }
        }
        
        # Update vaccination status based on due dates
        update_vaccination_status(vaccinations)
        
        # Get health recommendations for the latest checkup
        health_recommendations = []
        urgent_recommendation = None
        if checkups:
            latest_checkup = checkups.first()
            health_recommendations = latest_checkup.healthrecommendation_set.all()
            
            # Find the first urgent or high priority recommendation
            for recommendation in health_recommendations:
                if recommendation.severity in ['urgent', 'high']:
                    urgent_recommendation = recommendation
                    break
        
        context = {
            'profile': profile,
            'checkups': checkups,
            'vaccinations': vaccinations,
            'breastfeeding_content': breastfeeding_content,
            'mental_content': mental_content,
            'exercise_content': exercise_content,
            'diet_content': diet_content,
            'postpartum_dates': postpartum_dates,
            'postpartum_stage': postpartum_stage,
            'stage_info': stage_info.get(postpartum_stage, {}),
            'health_recommendations': health_recommendations,
            'urgent_recommendation': urgent_recommendation,
        }
        return render(request, 'core/mother_dashboard.html', context)
    except NewMotherProfile.DoesNotExist:
        messages.error(request, 'Mother profile not found.')
        return redirect('home')

@login_required
def submit_story(request):
    # Only allow mothers or pregnant women
    is_mother = NewMotherProfile.objects.filter(user=request.user).exists()
    is_pregnant = PregnantWomanProfile.objects.filter(user=request.user).exists()
    if not (is_mother or is_pregnant):
        messages.error(request, 'Only registered mothers or pregnant women can submit a story.')
        return redirect('home')

    if request.method == 'POST':
        form = UserTestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.is_approved = True  # Show immediately
            testimonial.is_featured = False
            testimonial.save()
            messages.success(request, 'Your story has been submitted!')
            return redirect('success_stories')
    else:
        form = UserTestimonialForm()
    return render(request, 'core/submit_story.html', {'form': form})

@login_required
def give_birth(request):
    """Handle the transition from pregnant woman to new mother"""
    try:
        pregnant_profile = PregnantWomanProfile.objects.get(user=request.user)
    except PregnantWomanProfile.DoesNotExist:
        messages.error(request, 'You must be a registered pregnant woman to use this feature.')
        return redirect('home')
    
    if request.method == 'POST':
        form = GiveBirthForm(request.POST)
        if form.is_valid():
            actual_birth_date = form.cleaned_data['actual_birth_date']
            baby_name = form.cleaned_data.get('baby_name', '')
            birth_notes = form.cleaned_data.get('birth_notes', '')
            
            # Create new mother profile
            mother_profile = NewMotherProfile.objects.create(
                user=request.user,
                name=pregnant_profile.name,
                child_birth_date=actual_birth_date
            )
            
            # Create baby vaccination schedule based on actual birth date
            create_baby_vaccination_schedule(mother_profile)
            
            # Delete the pregnant profile (this will also delete pregnancy vaccination records)
            pregnant_profile.delete()
            
            messages.success(request, f'Congratulations! You have successfully transitioned to the New Mother portal. Your baby was born on {actual_birth_date.strftime("%B %d, %Y")}.')
            return redirect('mother_dashboard')
    else:
        form = GiveBirthForm()
    
    return render(request, 'core/give_birth.html', {
        'form': form,
        'pregnant_profile': pregnant_profile
    })

@login_required
def submit_checkup(request, profile_type):
    if request.method == 'POST':
        form = CheckupProgressForm(request.POST, profile_type=profile_type)
        if form.is_valid():
            checkup = form.save(commit=False)
            checkup.profile_type = profile_type
            
            if profile_type == 'pregnant':
                try:
                    profile = PregnantWomanProfile.objects.get(user=request.user)
                    checkup.pregnant_profile = profile
                except PregnantWomanProfile.DoesNotExist:
                    messages.error(request, 'Profile not found.')
                    return redirect('home')
            elif profile_type == 'mother':
                try:
                    profile = NewMotherProfile.objects.get(user=request.user)
                    checkup.mother_profile = profile
                except NewMotherProfile.DoesNotExist:
                    messages.error(request, 'Profile not found.')
                    return redirect('home')
            
            checkup.save()
            
            # Generate health recommendations based on checkup data
            try:
                recommendations = generate_health_recommendations(checkup)
                if recommendations:
                    messages.success(request, f'Checkup progress submitted successfully! Generated {len(recommendations)} personalized recommendations.')
                else:
                    messages.success(request, 'Checkup progress submitted successfully!')
            except Exception as e:
                messages.warning(request, f'Checkup submitted, but there was an issue generating recommendations: {str(e)}')
            
            if profile_type == 'pregnant':
                return redirect('pregnant_dashboard')
            else:
                return redirect('mother_dashboard')
    else:
        form = CheckupProgressForm(profile_type=profile_type)
    
    return render(request, 'core/submit_checkup.html', {
        'form': form,
        'profile_type': profile_type
    })

def update_vaccination_status(vaccinations):
    """Update vaccination status based on due dates"""
    today = date.today()
    for vaccination in vaccinations:
        if vaccination.status == 'pending' and vaccination.due_date < today:
            vaccination.status = 'overdue'
            vaccination.save()

@login_required
def vaccination_tracker(request):
    """Vaccination tracking page"""
    try:
        pregnant_profile = PregnantWomanProfile.objects.get(user=request.user)
        vaccinations = VaccinationRecord.objects.filter(pregnant_profile=pregnant_profile).order_by('due_date')
        profile_type = 'pregnant'
    except PregnantWomanProfile.DoesNotExist:
        try:
            mother_profile = NewMotherProfile.objects.get(user=request.user)
            vaccinations = VaccinationRecord.objects.filter(mother_profile=mother_profile).order_by('due_date')
            profile_type = 'mother'
        except NewMotherProfile.DoesNotExist:
            messages.error(request, 'Profile not found.')
            return redirect('home')
    
    # Update vaccination status
    update_vaccination_status(vaccinations)
    
    # Calculate statistics
    total_vaccinations = vaccinations.count()
    completed_vaccinations = vaccinations.filter(status='completed').count()
    pending_vaccinations = vaccinations.filter(status='pending').count()
    overdue_vaccinations = vaccinations.filter(status='overdue').count()
    
    # Calculate mother vs baby vaccine counts for mother profile
    mother_vaccines_count = 0
    baby_vaccines_count = 0
    processed_vaccinations = []
    
    for vaccination in vaccinations:
        if profile_type == 'mother':
            vaccine_name_lower = vaccination.vaccine_name.lower()
            if ('(Mother)' in vaccination.vaccine_name or 
                'tdap' in vaccine_name_lower or 
                'covid19' in vaccine_name_lower or 
                'influenza' in vaccine_name_lower):
                vaccination.is_mother_type = True
                mother_vaccines_count += 1
            else:
                vaccination.is_mother_type = False
                baby_vaccines_count += 1
        processed_vaccinations.append(vaccination)
    
    context = {
        'vaccinations': processed_vaccinations,
        'profile_type': profile_type,
        'total_vaccinations': total_vaccinations,
        'completed_vaccinations': completed_vaccinations,
        'pending_vaccinations': pending_vaccinations,
        'overdue_vaccinations': overdue_vaccinations,
        'mother_vaccines_count': mother_vaccines_count,
        'baby_vaccines_count': baby_vaccines_count,
    }
    return render(request, 'core/vaccination_tracker_v2.html', context)

@login_required
def update_vaccination(request, vaccination_id):
    """Update vaccination record"""
    vaccination = get_object_or_404(VaccinationRecord, id=vaccination_id)
    
    # Check if user owns this vaccination record
    if (vaccination.pregnant_profile and vaccination.pregnant_profile.user != request.user) or \
       (vaccination.mother_profile and vaccination.mother_profile.user != request.user):
        messages.error(request, 'You do not have permission to update this record.')
        return redirect('vaccination_tracker')
    
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST, instance=vaccination)
        if form.is_valid():
            vaccination = form.save(commit=False)
            
            # Handle status changes
            if vaccination.status == 'completed':
                if not vaccination.completed_date:
                    vaccination.completed_date = date.today()
            elif vaccination.status in ['pending', 'overdue', 'not_applicable']:
                vaccination.completed_date = None
            
            vaccination.save()
            messages.success(request, f'Vaccination record updated successfully! Status: {vaccination.get_status_display()}')
            return redirect('vaccination_tracker')
    else:
        form = VaccinationRecordForm(instance=vaccination)
    
    return render(request, 'core/update_vaccination.html', {
        'form': form,
        'vaccination': vaccination
    })

@login_required
def update_checkup(request, checkup_id):
    """Update a checkup progress record"""
    try:
        checkup = CheckupProgress.objects.get(id=checkup_id)
        
        # Check if user owns this checkup record
        if (checkup.pregnant_profile and checkup.pregnant_profile.user == request.user) or \
           (checkup.mother_profile and checkup.mother_profile.user == request.user):
            
            if request.method == 'POST':
                form = CheckupProgressForm(request.POST, instance=checkup, profile_type=checkup.profile_type)
                if form.is_valid():
                    updated_checkup = form.save()
                    
                    # Generate health recommendations based on updated checkup data
                    try:
                        recommendations = generate_health_recommendations(updated_checkup)
                        if recommendations:
                            messages.success(request, f'Checkup progress updated successfully! Generated {len(recommendations)} personalized recommendations.')
                        else:
                            messages.success(request, 'Checkup progress updated successfully!')
                    except Exception as e:
                        messages.warning(request, f'Checkup updated, but there was an issue generating recommendations: {str(e)}')
                    
                    # Redirect back to appropriate dashboard
                    if checkup.profile_type == 'pregnant':
                        return redirect('pregnant_dashboard')
                    else:
                        return redirect('mother_dashboard')
            else:
                form = CheckupProgressForm(instance=checkup, profile_type=checkup.profile_type)
            
            context = {
                'form': form,
                'checkup': checkup,
                'profile_type': checkup.profile_type,
            }
            return render(request, 'core/update_checkup.html', context)
        else:
            messages.error(request, 'You do not have permission to update this record.')
            return redirect('home')
            
    except CheckupProgress.DoesNotExist:
        messages.error(request, 'Checkup record not found.')
        return redirect('home')


@login_required
def delete_checkup(request, checkup_id):
    """Delete a checkup progress record"""
    try:
        checkup = CheckupProgress.objects.get(id=checkup_id)
        
        # Check if user owns this checkup record
        if (checkup.pregnant_profile and checkup.pregnant_profile.user == request.user) or \
           (checkup.mother_profile and checkup.mother_profile.user == request.user):
            
            if request.method == 'POST':
                checkup.delete()
                messages.success(request, 'Checkup progress deleted successfully.')
                
                # Redirect back to appropriate dashboard
                if checkup.profile_type == 'pregnant':
                    return redirect('pregnant_dashboard')
                else:
                    return redirect('mother_dashboard')
            
            # GET request - show confirmation page
            context = {
                'checkup': checkup,
                'profile_type': checkup.profile_type,
            }
            return render(request, 'core/delete_checkup_confirm.html', context)
        else:
            messages.error(request, 'You do not have permission to delete this record.')
            return redirect('home')
            
    except CheckupProgress.DoesNotExist:
        messages.error(request, 'Checkup record not found.')
        return redirect('home')

def content_detail(request, content_id):
    content = get_object_or_404(InfoContent, id=content_id)
    return render(request, 'core/content_detail.html', {'content': content})

def diet_plans(request):
    if request.user.is_authenticated:
        try:
            profile = PregnantWomanProfile.objects.get(user=request.user)
            current_week = profile.get_current_pregnancy_week()
            current_month = profile.get_current_pregnancy_month()
            current_trimester = profile.get_trimester()
            
            # Get personalized diet content
            all_diet_content = InfoContent.objects.filter(category='diet')
            personalized_diet = [content for content in all_diet_content if content.is_relevant_for_week(current_week)]
            
            context = {
                'diet_content': personalized_diet,
                'all_diet_content': all_diet_content,
                'current_week': current_week,
                'current_month': current_month,
                'current_trimester': current_trimester,
                'is_pregnant': True,
            }
        except PregnantWomanProfile.DoesNotExist:
            # User is not pregnant, show all content
            diet_content = InfoContent.objects.filter(category='diet')
            context = {
                'diet_content': diet_content,
                'all_diet_content': diet_content,
                'is_pregnant': False,
            }
    else:
        # Not logged in, show all content
        diet_content = InfoContent.objects.filter(category='diet')
        context = {
            'diet_content': diet_content,
            'all_diet_content': diet_content,
            'is_pregnant': False,
        }
    
    return render(request, 'core/diet_plans.html', context)

def vaccination_schedule(request):
    vaccine_content = InfoContent.objects.filter(category='vaccine')
    return render(request, 'core/vaccination_schedule.html', {'vaccine_content': vaccine_content})

def exercise_guidance(request):
    if request.user.is_authenticated:
        try:
            profile = PregnantWomanProfile.objects.get(user=request.user)
            current_week = profile.get_current_pregnancy_week()
            current_month = profile.get_current_pregnancy_month()
            current_trimester = profile.get_trimester()
            
            # Get personalized exercise content
            all_exercise_content = InfoContent.objects.filter(category='exercise')
            personalized_exercise = [content for content in all_exercise_content if content.is_relevant_for_week(current_week)]
            
            context = {
                'exercise_content': personalized_exercise,
                'all_exercise_content': all_exercise_content,
                'current_week': current_week,
                'current_month': current_month,
                'current_trimester': current_trimester,
                'is_pregnant': True,
            }
        except PregnantWomanProfile.DoesNotExist:
            # User is not pregnant, show all content
            exercise_content = InfoContent.objects.filter(category='exercise')
            context = {
                'exercise_content': exercise_content,
                'all_exercise_content': exercise_content,
                'is_pregnant': False,
            }
    else:
        # Not logged in, show all content
        exercise_content = InfoContent.objects.filter(category='exercise')
        context = {
            'exercise_content': exercise_content,
            'all_exercise_content': exercise_content,
            'is_pregnant': False,
        }
    
    return render(request, 'core/exercise_guidance.html', context)

def breastfeeding_support(request):
    breastfeeding_content = InfoContent.objects.filter(category='breastfeeding')
    return render(request, 'core/breastfeeding_support.html', {'breastfeeding_content': breastfeeding_content})

def mental_health_support(request):
    mental_content = InfoContent.objects.filter(category='mental')
    return render(request, 'core/mental_health_support.html', {'mental_content': mental_content})

def testimonials(request):
    """View for user testimonials and success stories"""
    approved_testimonials = UserTestimonial.objects.filter(is_approved=True).order_by('-is_featured', '-created_at')
    
    context = {
        'testimonials': approved_testimonials,
        'featured_count': approved_testimonials.filter(is_featured=True).count(),
        'total_count': approved_testimonials.count(),
    }
    return render(request, 'core/testimonials.html', context)

def success_stories(request):
    stories = UserTestimonial.objects.all().order_by('-created_at')
    return render(request, 'core/success_stories.html', {'stories': stories})

def health_experts(request):
    """View for health experts who validate content"""
    experts = HealthExpert.objects.filter(is_active=True).order_by('expert_type', 'name')
    
    context = {
        'experts': experts,
        'expert_types': HealthExpert.EXPERT_TYPE_CHOICES,
    }
    return render(request, 'core/health_experts.html', context)

def community_workers(request):
    """View for local community health workers"""
    workers = CommunityHealthWorker.objects.filter(is_active=True).order_by('worker_type', 'name')
    
    context = {
        'workers': workers,
        'worker_types': CommunityHealthWorker.WORKER_TYPE_CHOICES,
    }
    return render(request, 'core/community_workers.html', context)

def danger_signs(request):
    """View for pregnancy and postpartum danger signs"""
    danger_content = InfoContent.objects.filter(
        category='danger_signs',
        is_government_approved=True
    ).order_by('-created_at')
    
    context = {
        'danger_content': danger_content,
    }
    return render(request, 'core/danger_signs.html', context)

def about_trust(request):
    """About trust and credibility page"""
    # Get statistics
    gov_approved_content = InfoContent.objects.filter(is_government_approved=True).count()
    total_experts = HealthExpert.objects.filter(is_active=True).count()
    total_workers = CommunityHealthWorker.objects.filter(is_active=True).count()
    total_testimonials = UserTestimonial.objects.filter(is_approved=True).count()
    
    context = {
        'page_title': 'About Trust & Credibility',
        'gov_approved_content': gov_approved_content,
        'total_experts': total_experts,
        'total_workers': total_workers,
        'total_testimonials': total_testimonials,
    }
    
    return render(request, 'core/about_trust.html', context)

def trimester_tips(request):
    """View for trimester-specific pregnancy tips"""
    trimester = request.GET.get('trimester', None)
    
    # Get all active tips
    all_tips = PregnancyTip.objects.filter(
        is_active=True
    ).order_by('week_start', 'created_at')
    
    # Organize tips by trimester based on week_start
    def get_trimester(week_start):
        if week_start <= 13:
            return 1
        elif week_start <= 26:
            return 2
        else:
            return 3
    
    # Group tips by trimester
    trimester_tips = {
        1: {'do': [], 'dont': []},
        2: {'do': [], 'dont': []},
        3: {'do': [], 'dont': []}
    }
    
    # Categorize tips based on their content or title
    for tip in all_tips:
        trimester_num = get_trimester(tip.week_start)
        
        # Determine if it's a "do" or "dont" based on content analysis
        # Look for keywords in title and content
        title_lower = tip.title.lower()
        content_lower = tip.content.lower()
        
        # Keywords that suggest "don't" or negative advice
        dont_keywords = ['avoid', 'don\'t', 'do not', 'never', 'stop', 'limit', 'restrict', 'no', 'not', 'dangerous', 'harmful', 'risky']
        
        # Check if the tip contains "don't" keywords
        is_dont = any(keyword in title_lower or keyword in content_lower for keyword in dont_keywords)
        
        if is_dont:
            trimester_tips[trimester_num]['dont'].append(tip)
        else:
            trimester_tips[trimester_num]['do'].append(tip)
    
    # Statistics
    trimester_stats = {
        1: {'do_count': len(trimester_tips[1]['do']), 'dont_count': len(trimester_tips[1]['dont'])},
        2: {'do_count': len(trimester_tips[2]['do']), 'dont_count': len(trimester_tips[2]['dont'])},
        3: {'do_count': len(trimester_tips[3]['do']), 'dont_count': len(trimester_tips[3]['dont'])},
    }

    trimesters = [
        {"num": 1, "label": "First Trimester (Weeks 1-13)", "color": "success", "icon": "fa-seedling"},
        {"num": 2, "label": "Second Trimester (Weeks 14-26)", "color": "warning", "icon": "fa-sun"},
        {"num": 3, "label": "Third Trimester (Weeks 27-40)", "color": "danger", "icon": "fa-baby"},
    ]
    
    context = {
        'trimester_tips': trimester_tips,
        'all_tips': all_tips,  # Keep for backward compatibility
        'trimester_stats': trimester_stats,
        'selected_trimester': trimester,
        'page_title': 'Pregnancy Tips by Trimester',
        'trimesters': trimesters,
    }
    return render(request, 'core/trimester_tips.html', context)

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect users to their appropriate dashboard after login"""
        user = self.request.user
        
        # Check if user has a pregnant woman profile
        try:
            profile = PregnantWomanProfile.objects.get(user=user)
            # Check if profile is complete
            if profile.name and profile.age and profile.due_date and profile.phone_number:
                return '/dashboard/pregnant/'
            else:
                # Profile exists but is incomplete, redirect to completion page
                return '/complete-profile/pregnant/'
        except PregnantWomanProfile.DoesNotExist:
            pass
        
        # Check if user has a new mother profile
        try:
            profile = NewMotherProfile.objects.get(user=user)
            # Check if profile is complete
            if profile.name and profile.child_birth_date and profile.phone_number:
                return '/dashboard/mother/'
            else:
                # Profile exists but is incomplete, redirect to completion page
                return '/complete-profile/mother/'
        except NewMotherProfile.DoesNotExist:
            pass
        
        # If no profile found, redirect to home (this shouldn't happen with Google auth)
        return '/'

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'core/404.html', status=404)

def set_language(request):
    """Handle language switching"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in ['en', 'ne']:
            request.session[LANGUAGE_SESSION_KEY] = language
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def language_demo(request):
    """Demo page to show language switching functionality"""
    return render(request, 'core/language_demo.html')

def comprehensive_nutrition_pregnant(request):
    """Comprehensive nutrition table view for pregnant women"""
    if request.user.is_authenticated:
        try:
            profile = PregnantWomanProfile.objects.get(user=request.user)
            current_week = profile.get_current_pregnancy_week()
            current_month = profile.get_current_pregnancy_month()
            current_trimester = profile.get_trimester()
            
            # Get all nutrition content for pregnant women
            nutrition_content = InfoContent.objects.filter(category='diet').order_by('week_start')
            
            context = {
                'profile': profile,
                'current_week': current_week,
                'current_month': current_month,
                'current_trimester': current_trimester,
                'nutrition_content': nutrition_content,
                'is_pregnant': True,
            }
        except PregnantWomanProfile.DoesNotExist:
            messages.error(request, 'Pregnant woman profile not found.')
            return redirect('home')
    else:
        nutrition_content = InfoContent.objects.filter(category='diet').order_by('week_start')
        context = {
            'nutrition_content': nutrition_content,
            'is_pregnant': False,
        }
    
    return render(request, 'core/comprehensive_nutrition_pregnant.html', context)

def comprehensive_nutrition_mother(request):
    """Comprehensive nutrition table view for new mothers, with child details"""
    if request.user.is_authenticated:
        try:
            profile = NewMotherProfile.objects.get(user=request.user)
            postpartum_dates = profile.get_postpartum_dates()
            nutrition_content = InfoContent.objects.filter(category='breastfeeding').order_by('week_start')
            # Get latest checkup for child details
            latest_checkup = CheckupProgress.objects.filter(mother_profile=profile).order_by('-created_at').first()
            child_details = None
            if latest_checkup:
                child_details = {
                    'weight_kg': latest_checkup.child_weight_kg,
                    'height_cm': latest_checkup.child_height_cm,
                    'head_circumference_cm': latest_checkup.child_head_circumference_cm,
                    'feeding_status': latest_checkup.get_child_feeding_status_display() if latest_checkup.child_feeding_status else None,
                    'checkup_date': latest_checkup.created_at,
                }
            context = {
                'profile': profile,
                'postpartum_dates': postpartum_dates,
                'nutrition_content': nutrition_content,
                'is_mother': True,
                'child_details': child_details,
            }
        except NewMotherProfile.DoesNotExist:
            messages.error(request, 'Mother profile not found.')
            return redirect('home')
    else:
        nutrition_content = InfoContent.objects.filter(category='breastfeeding').order_by('week_start')
        context = {
            'nutrition_content': nutrition_content,
            'is_mother': False,
            'child_details': None,
        }
    return render(request, 'core/comprehensive_nutrition_mother.html', context)


def generate_health_recommendations(checkup):
    """Generate personalized health recommendations based on checkup data"""
    from .models import HealthRecommendation
    
    recommendations = []
    
    # Clear any existing recommendations for this checkup
    HealthRecommendation.objects.filter(checkup=checkup).delete()
    
    # For pregnant women
    if checkup.profile_type == 'pregnant' and checkup.pregnant_profile:
        profile = checkup.pregnant_profile
        current_week = profile.get_current_pregnancy_week()
        
        # Nutrition recommendations based on pregnancy week
        if current_week <= 13:  # First trimester
            rec = HealthRecommendation.objects.create(
                checkup=checkup,
                recommendation_type='nutrition',
                title='First Trimester Nutrition',
                description='Focus on folate-rich foods like leafy greens, citrus fruits, and fortified cereals. Take prenatal vitamins with folic acid daily.',
                calories_per_day=1800,
                protein_grams=60,
                iron_mg=27,
                calcium_mg=1000,
                severity='low'
            )
            recommendations.append(rec)
        elif current_week <= 26:  # Second trimester
            rec = HealthRecommendation.objects.create(
                checkup=checkup,
                recommendation_type='nutrition',
                title='Second Trimester Nutrition',
                description='Increase protein intake for baby growth. Include lean meats, fish, eggs, dairy, legumes, and nuts in your diet.',
                calories_per_day=2200,
                protein_grams=71,
                iron_mg=27,
                calcium_mg=1000,
                severity='low'
            )
            recommendations.append(rec)
        else:  # Third trimester
            rec = HealthRecommendation.objects.create(
                checkup=checkup,
                recommendation_type='nutrition',
                title='Third Trimester Nutrition',
                description='Focus on calcium and iron-rich foods. Include dairy products, dark leafy greens, and lean red meat.',
                calories_per_day=2400,
                protein_grams=71,
                iron_mg=27,
                calcium_mg=1000,
                severity='low'
            )
            recommendations.append(rec)
        
        # Analyze notes for symptoms
        if checkup.notes:
            notes_lower = checkup.notes.lower()
            symptom_alerts = []
            
            # Common pregnancy symptoms that require attention
            if 'bleeding' in notes_lower or 'blood' in notes_lower:
                symptom_alerts.append('Vaginal bleeding during pregnancy requires immediate medical attention.')
            
            if 'severe headache' in notes_lower or 'migraine' in notes_lower:
                symptom_alerts.append('Severe headaches can be a sign of preeclampsia. Monitor and report to your healthcare provider.')
            
            if 'vision' in notes_lower and ('blurry' in notes_lower or 'spots' in notes_lower or 'flashing' in notes_lower):
                symptom_alerts.append('Vision changes can indicate preeclampsia. Seek medical attention immediately.')
            
            if 'swelling' in notes_lower and ('face' in notes_lower or 'hands' in notes_lower):
                symptom_alerts.append('Facial or hand swelling can be a sign of preeclampsia. Contact your healthcare provider.')
            
            if 'contractions' in notes_lower and current_week < 37:
                symptom_alerts.append('Preterm contractions before 37 weeks require medical evaluation.')
            
            if 'decreased fetal movement' in notes_lower or 'baby not moving' in notes_lower:
                symptom_alerts.append('Decreased fetal movement should be evaluated by a healthcare provider immediately.')
            
            if 'severe nausea' in notes_lower or 'vomiting' in notes_lower:
                symptom_alerts.append('Severe nausea and vomiting (hyperemesis gravidarum) may require medical treatment.')
            
            if 'pain' in notes_lower:
                if 'abdominal' in notes_lower or 'stomach' in notes_lower:
                    symptom_alerts.append('Abdominal pain during pregnancy should be evaluated by a healthcare provider.')
                elif 'pelvic' in notes_lower:
                    symptom_alerts.append('Severe pelvic pain may indicate complications and requires medical attention.')
            
            # Create recommendation if symptoms detected
            if symptom_alerts:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Symptom Alert - Review Notes with Healthcare Provider',
                    description='Based on your notes, here are potential concerns that should be discussed with your healthcare provider: ' + ' '.join(symptom_alerts),
                    severity='high',
                    action_required=True,
                    follow_up_days=3
                )
                recommendations.append(rec)
        
        # Medicine recommendations based on symptoms
        if checkup.fever and checkup.fever_temperature:
            if checkup.fever_temperature >= 38.5:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medicine',
                    title='Fever Management',
                    description='High fever requires medical attention. Paracetamol 500mg can be taken as directed by your healthcare provider.',
                    medicine_name='Paracetamol',
                    dosage='500mg as needed',
                    duration='Until fever subsides',
                    severity='high',
                    action_required=True
                )
                recommendations.append(rec)
            elif checkup.fever_temperature >= 37.5:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medicine',
                    title='Mild Fever',
                    description='Monitor temperature. Stay hydrated and rest. Consult healthcare provider if fever persists.',
                    severity='medium',
                    action_required=False
                )
                recommendations.append(rec)
        
        # Blood pressure recommendations - Check for both high and low blood pressure
        if checkup.blood_pressure_systolic and checkup.blood_pressure_diastolic:
            systolic = checkup.blood_pressure_systolic
            diastolic = checkup.blood_pressure_diastolic
            
            # Check for Hypertensive Crisis (Emergency)
            if systolic >= 180 or diastolic >= 120:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Hypertensive Crisis - SEEK IMMEDIATE MEDICAL ATTENTION',
                    description='This is a medical emergency. Your blood pressure is dangerously high. Go to the emergency room or call emergency services immediately.',
                    severity='urgent',
                    action_required=True,
                    follow_up_days=0
                )
                recommendations.append(rec)
            
            # Check for Hypertension Stage 2
            elif systolic >= 140 or diastolic >= 90:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='High Blood Pressure (Hypertension Stage 2)',
                    description='Your blood pressure reading indicates stage 2 hypertension. Please consult your healthcare provider immediately for medication and treatment plan.',
                    severity='urgent',
                    action_required=True,
                    follow_up_days=1
                )
                recommendations.append(rec)
            
            # Check for Hypertension Stage 1
            elif systolic >= 130 or diastolic >= 80:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='lifestyle',
                    title='Elevated Blood Pressure (Hypertension Stage 1)',
                    description='Your blood pressure is elevated. Reduce salt intake, exercise regularly, manage stress, and monitor your readings closely.',
                    severity='high',
                    action_required=True,
                    follow_up_days=3
                )
                recommendations.append(rec)
            
            # Check for Low Blood Pressure (Hypotension)
            elif systolic < 90 or diastolic < 60:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Low Blood Pressure (Hypotension)',
                    description='Your blood pressure is lower than normal. If you experience dizziness, fainting, or fatigue, consult your healthcare provider.',
                    severity='medium',
                    action_required=False,
                    follow_up_days=7
                )
                recommendations.append(rec)
    
    # For new mothers
    elif checkup.profile_type == 'mother' and checkup.mother_profile:
        # Nutrition recommendations for breastfeeding
        rec = HealthRecommendation.objects.create(
            checkup=checkup,
            recommendation_type='nutrition',
            title='Breastfeeding Nutrition',
            description='Consume an additional 300-500 calories per day. Include protein-rich foods, whole grains, fruits, and vegetables.',
            calories_per_day=2500,
            protein_grams=71,
            calcium_mg=1000,
            severity='low'
        )
        recommendations.append(rec)
        
        # Analyze notes for symptoms in new mothers
        if checkup.notes:
            notes_lower = checkup.notes.lower()
            symptom_alerts = []
            
            # Common postpartum symptoms that require attention
            if 'bleeding' in notes_lower or 'blood' in notes_lower:
                if 'heavy' in notes_lower or 'soaking' in notes_lower:
                    symptom_alerts.append('Heavy vaginal bleeding (soaking more than one pad per hour) after delivery requires immediate medical attention.')
                else:
                    symptom_alerts.append('Any unusual vaginal bleeding postpartum should be reported to your healthcare provider.')
            
            if 'fever' in notes_lower:
                symptom_alerts.append('Fever after delivery can indicate infection. Contact your healthcare provider immediately.')
            
            if 'severe headache' in notes_lower or 'migraine' in notes_lower:
                symptom_alerts.append('Severe headaches postpartum can indicate complications. Seek medical attention.')
            
            if 'pain' in notes_lower:
                if 'incision' in notes_lower or 'stitches' in notes_lower or 'c-section' in notes_lower:
                    symptom_alerts.append('Increasing pain at incision site may indicate infection. Contact your healthcare provider.')
                elif 'chest' in notes_lower:
                    symptom_alerts.append('Chest pain can indicate serious complications like blood clots. Seek immediate medical attention.')
            
            if 'difficulty breathing' in notes_lower or 'shortness of breath' in notes_lower:
                symptom_alerts.append('Difficulty breathing can indicate serious complications like blood clots. Seek immediate medical attention.')
            
            if 'depression' in notes_lower or 'sad' in notes_lower or 'hopeless' in notes_lower or 'anxious' in notes_lower:
                symptom_alerts.append('Signs of postpartum depression or anxiety should be discussed with your healthcare provider immediately.')
            
            if 'swelling' in notes_lower and ('leg' in notes_lower or 'arm' in notes_lower):
                symptom_alerts.append('Swelling in legs or arms can indicate blood clots. Seek immediate medical attention.')
            
            if 'discharge' in notes_lower and ('foul' in notes_lower or 'smell' in notes_lower):
                symptom_alerts.append('Foul-smelling vaginal discharge can indicate infection. Contact your healthcare provider.')
            
            # Child-related symptoms in notes
            if 'baby' in notes_lower or 'child' in notes_lower:
                if 'not eating' in notes_lower or 'refusing feeds' in notes_lower:
                    symptom_alerts.append('If your baby is refusing feeds, contact your pediatrician.')
                
                if 'crying' in notes_lower and ('excessive' in notes_lower or 'constantly' in notes_lower):
                    symptom_alerts.append('Excessive crying in infants should be discussed with your pediatrician.')
                
                if 'rash' in notes_lower or 'skin' in notes_lower:
                    symptom_alerts.append('Skin rashes in babies should be evaluated by a pediatrician.')
            
            # Create recommendation if symptoms detected
            if symptom_alerts:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Symptom Alert - Review Notes with Healthcare Provider',
                    description='Based on your notes, here are potential concerns that should be discussed with your healthcare provider: ' + ' '.join(symptom_alerts),
                    severity='high',
                    action_required=True,
                    follow_up_days=3
                )
                recommendations.append(rec)
        
        # Child-related recommendations
        if checkup.child_weight_kg and checkup.child_height_cm:
            # Check if child weight is within normal range
            if checkup.child_weight_kg < 2.5:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Low Birth Weight',
                    description='Your baby\'s weight is below normal. Please consult your pediatrician for specialized care.',
                    severity='high',
                    action_required=True,
                    follow_up_days=3
                )
                recommendations.append(rec)
            
            # Check if child height is within normal range
            if checkup.child_height_cm < 45:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Short Length',
                    description='Your baby\'s length is below normal. Please consult your pediatrician for evaluation.',
                    severity='medium',
                    action_required=True,
                    follow_up_days=7
                )
                recommendations.append(rec)
        
        # Fever recommendations for mother
        if checkup.fever and checkup.fever_temperature:
            if checkup.fever_temperature >= 38.5:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medicine',
                    title='Fever Management',
                    description='High fever requires medical attention. Paracetamol 500mg can be taken as directed by your healthcare provider.',
                    medicine_name='Paracetamol',
                    dosage='500mg as needed',
                    duration='Until fever subsides',
                    severity='high',
                    action_required=True
                )
                recommendations.append(rec)
            elif checkup.fever_temperature >= 37.5:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medicine',
                    title='Mild Fever',
                    description='Monitor temperature. Stay hydrated and rest. Consult healthcare provider if fever persists.',
                    severity='medium',
                    action_required=False
                )
                recommendations.append(rec)
        
        # Blood pressure recommendations for mother - Check for both high and low blood pressure
        if checkup.blood_pressure_systolic and checkup.blood_pressure_diastolic:
            systolic = checkup.blood_pressure_systolic
            diastolic = checkup.blood_pressure_diastolic
            
            # Check for Hypertensive Crisis (Emergency)
            if systolic >= 180 or diastolic >= 120:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Hypertensive Crisis - SEEK IMMEDIATE MEDICAL ATTENTION',
                    description='This is a medical emergency. Your blood pressure is dangerously high. Go to the emergency room or call emergency services immediately.',
                    severity='urgent',
                    action_required=True,
                    follow_up_days=0
                )
                recommendations.append(rec)
            
            # Check for Hypertension Stage 2
            elif systolic >= 140 or diastolic >= 90:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='High Blood Pressure (Hypertension Stage 2)',
                    description='Your blood pressure reading indicates stage 2 hypertension. Please consult your healthcare provider immediately for medication and treatment plan.',
                    severity='urgent',
                    action_required=True,
                    follow_up_days=1
                )
                recommendations.append(rec)
            
            # Check for Hypertension Stage 1
            elif systolic >= 130 or diastolic >= 80:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='lifestyle',
                    title='Elevated Blood Pressure (Hypertension Stage 1)',
                    description='Your blood pressure is elevated. Reduce salt intake, exercise regularly, manage stress, and monitor your readings closely.',
                    severity='high',
                    action_required=True,
                    follow_up_days=3
                )
                recommendations.append(rec)
            
            # Check for Low Blood Pressure (Hypotension)
            elif systolic < 90 or diastolic < 60:
                rec = HealthRecommendation.objects.create(
                    checkup=checkup,
                    recommendation_type='medical_attention',
                    title='Low Blood Pressure (Hypotension)',
                    description='Your blood pressure is lower than normal. If you experience dizziness, fainting, or fatigue, consult your healthcare provider.',
                    severity='medium',
                    action_required=False,
                    follow_up_days=7
                )
                recommendations.append(rec)
    
    return recommendations


@login_required
def generate_pregnant_health_report_pdf(request):
    """Generate a PDF health report for pregnant women"""
    try:
        # Get the pregnant profile
        profile = PregnantWomanProfile.objects.get(user=request.user)
        
        # Get checkups ordered by date
        checkups = CheckupProgress.objects.filter(pregnant_profile=profile).order_by('-created_at')
        
        # Get health recommendations
        recommendations = []
        for checkup in checkups:
            recs = HealthRecommendation.objects.filter(checkup=checkup).order_by('-severity')
            recommendations.extend(recs)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="pregnancy_health_report_{profile.id}.pdf"'
        
        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph('AamCare Pregnancy Health Report', title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information
        patient_style = ParagraphStyle(
            'PatientInfo',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        story.append(Paragraph(f'<b>Patient Name:</b> {profile.name}', patient_style))
        story.append(Paragraph(f'<b>Age:</b> {profile.age}', patient_style))
        story.append(Paragraph(f'<b>Due Date:</b> {profile.due_date.strftime("%B %d, %Y")}', patient_style))
        story.append(Paragraph(f'<b>Current Week:</b> {profile.get_current_pregnancy_week()}', patient_style))
        story.append(Spacer(1, 20))
        
        # Checkups Section
        story.append(Paragraph('<b>Health Progress Records</b>', styles['Heading2']))
        
        if checkups.exists():
            # Create table data
            table_data = [['Date', 'Month', 'Weight (kg)', 'Blood Pressure', 'Notes']]
            
            for checkup in checkups[:10]:  # Limit to last 10 checkups
                bp = f'{checkup.blood_pressure_systolic}/{checkup.blood_pressure_diastolic}' if checkup.blood_pressure_systolic and checkup.blood_pressure_diastolic else 'N/A'
                notes = checkup.notes[:50] + '...' if checkup.notes and len(checkup.notes) > 50 else (checkup.notes or 'N/A')
                
                table_data.append([
                    checkup.created_at.strftime('%Y-%m-%d'),
                    str(checkup.month),
                    str(checkup.weight_kg) if checkup.weight_kg else 'N/A',
                    bp,
                    notes
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph('No health progress records found.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Recommendations Section
        story.append(Paragraph('<b>Health Recommendations</b>', styles['Heading2']))
        
        if recommendations:
            for rec in recommendations[:15]:  # Limit to 15 recommendations
                # Recommendation header with severity indicator
                severity_colors = {
                    'urgent': colors.red,
                    'high': colors.orange,
                    'medium': colors.yellow,
                    'low': colors.green
                }
                
                severity_color = severity_colors.get(rec.severity, colors.gray)
                rec_title = f'<font color="{severity_color.hexval()}">●</font> <b>{rec.title}</b> ({rec.get_severity_display()} Priority)'
                story.append(Paragraph(rec_title, styles['Normal']))
                
                # Recommendation details
                story.append(Paragraph(rec.description, styles['Normal']))
                
                # Special fields based on recommendation type
                if rec.recommendation_type == 'medicine' and rec.medicine_name:
                    med_info = f'<i>Medication:</i> {rec.medicine_name} - {rec.dosage}'
                    if rec.duration:
                        med_info += f' (Duration: {rec.duration})'
                    story.append(Paragraph(med_info, styles['Normal']))
                
                if rec.recommendation_type == 'nutrition' and rec.calories_per_day:
                    nutrition_info = f'<i>Nutrition Targets:</i> '
                    targets = []
                    if rec.calories_per_day:
                        targets.append(f'{rec.calories_per_day} kcal/day')
                    if rec.protein_grams:
                        targets.append(f'{rec.protein_grams}g protein')
                    if rec.iron_mg:
                        targets.append(f'{rec.iron_mg}mg iron')
                    if rec.calcium_mg:
                        targets.append(f'{rec.calcium_mg}mg calcium')
                    nutrition_info += ', '.join(targets)
                    story.append(Paragraph(nutrition_info, styles['Normal']))
                
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph('No health recommendations available.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph('Generated by AamCare - Your Virtual Health Assistant', footer_style))
        story.append(Paragraph(f'Report generated on: {timezone.now().strftime("%B %d, %Y at %I:%M %p")}', footer_style))
        
        # Build PDF
        doc.build(story)
        return response
        
    except PregnantWomanProfile.DoesNotExist:
        messages.error(request, 'Pregnant profile not found.')
        return redirect('pregnant_dashboard')
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('pregnant_dashboard')


@login_required
def generate_mother_health_report_pdf(request):
    """Generate a PDF health report for new mothers"""
    try:
        # Get the mother profile
        profile = NewMotherProfile.objects.get(user=request.user)
        
        # Get checkups ordered by date
        checkups = CheckupProgress.objects.filter(mother_profile=profile).order_by('-created_at')
        
        # Get health recommendations
        recommendations = []
        for checkup in checkups:
            recs = HealthRecommendation.objects.filter(checkup=checkup).order_by('-severity')
            recommendations.extend(recs)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="mother_health_report_{profile.id}.pdf"'
        
        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph('AamCare Mother & Baby Health Report', title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information
        patient_style = ParagraphStyle(
            'PatientInfo',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        story.append(Paragraph(f'<b>Mother Name:</b> {profile.name}', patient_style))
        story.append(Paragraph(f'<b>Baby Birth Date:</b> {profile.child_birth_date.strftime("%B %d, %Y")}', patient_style))
        story.append(Paragraph(f'<b>Postpartum Stage:</b> {profile.get_postpartum_stage()} months', patient_style))
        story.append(Spacer(1, 20))
        
        # Checkups Section
        story.append(Paragraph('<b>Recovery & Baby Progress Records</b>', styles['Heading2']))
        
        if checkups.exists():
            # Create table data
            table_data = [['Date', 'Month', 'Mom Weight (kg)', 'Blood Pressure', 'Baby Weight (kg)', 'Feeding Status', 'Notes']]
            
            for checkup in checkups[:10]:  # Limit to last 10 checkups
                bp = f'{checkup.blood_pressure_systolic}/{checkup.blood_pressure_diastolic}' if checkup.blood_pressure_systolic and checkup.blood_pressure_diastolic else 'N/A'
                notes = checkup.notes[:50] + '...' if checkup.notes and len(checkup.notes) > 50 else (checkup.notes or 'N/A')
                feeding_status = dict([(choice[0], choice[1]) for choice in CheckupProgress._meta.get_field('child_feeding_status').choices]).get(checkup.child_feeding_status, 'N/A')
                
                table_data.append([
                    checkup.created_at.strftime('%Y-%m-%d'),
                    str(checkup.month),
                    str(checkup.weight_kg) if checkup.weight_kg else 'N/A',
                    bp,
                    str(checkup.child_weight_kg) if checkup.child_weight_kg else 'N/A',
                    feeding_status,
                    notes
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph('No recovery progress records found.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Recommendations Section
        story.append(Paragraph('<b>Health Recommendations</b>', styles['Heading2']))
        
        if recommendations:
            for rec in recommendations[:15]:  # Limit to 15 recommendations
                # Recommendation header with severity indicator
                severity_colors = {
                    'urgent': colors.red,
                    'high': colors.orange,
                    'medium': colors.yellow,
                    'low': colors.green
                }
                
                severity_color = severity_colors.get(rec.severity, colors.gray)
                rec_title = f'<font color="{severity_color.hexval()}">●</font> <b>{rec.title}</b> ({rec.get_severity_display()} Priority)'
                story.append(Paragraph(rec_title, styles['Normal']))
                
                # Recommendation details
                story.append(Paragraph(rec.description, styles['Normal']))
                
                # Special fields based on recommendation type
                if rec.recommendation_type == 'medicine' and rec.medicine_name:
                    med_info = f'<i>Medication:</i> {rec.medicine_name} - {rec.dosage}'
                    if rec.duration:
                        med_info += f' (Duration: {rec.duration})'
                    story.append(Paragraph(med_info, styles['Normal']))
                
                if rec.recommendation_type == 'nutrition' and rec.calories_per_day:
                    nutrition_info = f'<i>Nutrition Targets:</i> '
                    targets = []
                    if rec.calories_per_day:
                        targets.append(f'{rec.calories_per_day} kcal/day')
                    if rec.protein_grams:
                        targets.append(f'{rec.protein_grams}g protein')
                    if rec.iron_mg:
                        targets.append(f'{rec.iron_mg}mg iron')
                    if rec.calcium_mg:
                        targets.append(f'{rec.calcium_mg}mg calcium')
                    nutrition_info += ', '.join(targets)
                    story.append(Paragraph(nutrition_info, styles['Normal']))
                
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph('No health recommendations available.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph('Generated by AamCare - Your Virtual Health Assistant', footer_style))
        story.append(Paragraph(f'Report generated on: {timezone.now().strftime("%B %d, %Y at %I:%M %p")}', footer_style))
        
        # Build PDF
        doc.build(story)
        return response
        
    except NewMotherProfile.DoesNotExist:
        messages.error(request, 'Mother profile not found.')
        return redirect('mother_dashboard')
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('mother_dashboard')

@login_required
def generate_pregnant_health_report_pdf(request):
    """Generate a PDF health report for pregnant women"""
    try:
        # Get the pregnant profile
        profile = PregnantWomanProfile.objects.get(user=request.user)
        
        # Get checkups ordered by date
        checkups = CheckupProgress.objects.filter(pregnant_profile=profile).order_by('-created_at')
        
        # Get health recommendations
        recommendations = []
        for checkup in checkups:
            recs = HealthRecommendation.objects.filter(checkup=checkup).order_by('-severity')
            recommendations.extend(recs)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="pregnancy_health_report_{profile.id}.pdf"'
        
        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph('AamCare Pregnancy Health Report', title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information
        patient_style = ParagraphStyle(
            'PatientInfo',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        story.append(Paragraph(f'<b>Patient Name:</b> {profile.name}', patient_style))
        story.append(Paragraph(f'<b>Age:</b> {profile.age}', patient_style))
        story.append(Paragraph(f'<b>Due Date:</b> {profile.due_date.strftime("%B %d, %Y")}', patient_style))
        story.append(Paragraph(f'<b>Current Week:</b> {profile.get_current_pregnancy_week()}', patient_style))
        story.append(Spacer(1, 20))
        
        # Checkups Section
        story.append(Paragraph('<b>Health Progress Records</b>', styles['Heading2']))
        
        if checkups.exists():
            # Create table data
            table_data = [['Date', 'Month', 'Weight (kg)', 'Blood Pressure', 'Notes']]
            
            for checkup in checkups[:10]:  # Limit to last 10 checkups
                bp = f'{checkup.blood_pressure_systolic}/{checkup.blood_pressure_diastolic}' if checkup.blood_pressure_systolic and checkup.blood_pressure_diastolic else 'N/A'
                notes = checkup.notes[:50] + '...' if checkup.notes and len(checkup.notes) > 50 else (checkup.notes or 'N/A')
                
                table_data.append([
                    checkup.created_at.strftime('%Y-%m-%d'),
                    str(checkup.month),
                    str(checkup.weight_kg) if checkup.weight_kg else 'N/A',
                    bp,
                    notes
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph('No health progress records found.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Recommendations Section
        story.append(Paragraph('<b>Health Recommendations</b>', styles['Heading2']))
        
        if recommendations:
            for rec in recommendations[:15]:  # Limit to 15 recommendations
                # Recommendation header with severity indicator
                severity_colors = {
                    'urgent': colors.red,
                    'high': colors.orange,
                    'medium': colors.yellow,
                    'low': colors.green
                }
                
                severity_color = severity_colors.get(rec.severity, colors.gray)
                rec_title = f'<font color="{severity_color.hexval()}">●</font> <b>{rec.title}</b> ({rec.get_severity_display()} Priority)'
                story.append(Paragraph(rec_title, styles['Normal']))
                
                # Recommendation details
                story.append(Paragraph(rec.description, styles['Normal']))
                
                # Special fields based on recommendation type
                if rec.recommendation_type == 'medicine' and rec.medicine_name:
                    med_info = f'<i>Medication:</i> {rec.medicine_name} - {rec.dosage}'
                    if rec.duration:
                        med_info += f' (Duration: {rec.duration})'
                    story.append(Paragraph(med_info, styles['Normal']))
                
                if rec.recommendation_type == 'nutrition' and rec.calories_per_day:
                    nutrition_info = f'<i>Nutrition Targets:</i> '
                    targets = []
                    if rec.calories_per_day:
                        targets.append(f'{rec.calories_per_day} kcal/day')
                    if rec.protein_grams:
                        targets.append(f'{rec.protein_grams}g protein')
                    if rec.iron_mg:
                        targets.append(f'{rec.iron_mg}mg iron')
                    if rec.calcium_mg:
                        targets.append(f'{rec.calcium_mg}mg calcium')
                    nutrition_info += ', '.join(targets)
                    story.append(Paragraph(nutrition_info, styles['Normal']))
                
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph('No health recommendations available.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph('Generated by AamCare - Your Virtual Health Assistant', footer_style))
        story.append(Paragraph(f'Report generated on: {timezone.now().strftime("%B %d, %Y at %I:%M %p")}', footer_style))
        
        # Build PDF
        doc.build(story)
        return response
        
    except PregnantWomanProfile.DoesNotExist:
        messages.error(request, 'Pregnant profile not found.')
        return redirect('pregnant_dashboard')
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('pregnant_dashboard')


@login_required
def generate_mother_health_report_pdf(request):
    """Generate a PDF health report for new mothers"""
    try:
        # Get the mother profile
        profile = NewMotherProfile.objects.get(user=request.user)
        
        # Get checkups ordered by date
        checkups = CheckupProgress.objects.filter(mother_profile=profile).order_by('-created_at')
        
        # Get health recommendations
        recommendations = []
        for checkup in checkups:
            recs = HealthRecommendation.objects.filter(checkup=checkup).order_by('-severity')
            recommendations.extend(recs)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="mother_health_report_{profile.id}.pdf"'
        
        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph('AamCare Mother & Baby Health Report', title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information
        patient_style = ParagraphStyle(
            'PatientInfo',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        story.append(Paragraph(f'<b>Mother Name:</b> {profile.name}', patient_style))
        story.append(Paragraph(f'<b>Baby Birth Date:</b> {profile.child_birth_date.strftime("%B %d, %Y")}', patient_style))
        story.append(Paragraph(f'<b>Postpartum Stage:</b> {profile.get_postpartum_stage()} months', patient_style))
        story.append(Spacer(1, 20))
        
        # Checkups Section
        story.append(Paragraph('<b>Recovery & Baby Progress Records</b>', styles['Heading2']))
        
        if checkups.exists():
            # Create table data
            table_data = [['Date', 'Month', 'Mom Weight (kg)', 'Blood Pressure', 'Baby Weight (kg)', 'Feeding Status', 'Notes']]
            
            for checkup in checkups[:10]:  # Limit to last 10 checkups
                bp = f'{checkup.blood_pressure_systolic}/{checkup.blood_pressure_diastolic}' if checkup.blood_pressure_systolic and checkup.blood_pressure_diastolic else 'N/A'
                notes = checkup.notes[:50] + '...' if checkup.notes and len(checkup.notes) > 50 else (checkup.notes or 'N/A')
                feeding_status = dict([(choice[0], choice[1]) for choice in CheckupProgress._meta.get_field('child_feeding_status').choices]).get(checkup.child_feeding_status, 'N/A')
                
                table_data.append([
                    checkup.created_at.strftime('%Y-%m-%d'),
                    str(checkup.month),
                    str(checkup.weight_kg) if checkup.weight_kg else 'N/A',
                    bp,
                    str(checkup.child_weight_kg) if checkup.child_weight_kg else 'N/A',
                    feeding_status,
                    notes
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph('No recovery progress records found.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Recommendations Section
        story.append(Paragraph('<b>Health Recommendations</b>', styles['Heading2']))
        
        if recommendations:
            for rec in recommendations[:15]:  # Limit to 15 recommendations
                # Recommendation header with severity indicator
                severity_colors = {
                    'urgent': colors.red,
                    'high': colors.orange,
                    'medium': colors.yellow,
                    'low': colors.green
                }
                
                severity_color = severity_colors.get(rec.severity, colors.gray)
                rec_title = f'<font color="{severity_color.hexval()}">●</font> <b>{rec.title}</b> ({rec.get_severity_display()} Priority)'
                story.append(Paragraph(rec_title, styles['Normal']))
                
                # Recommendation details
                story.append(Paragraph(rec.description, styles['Normal']))
                
                # Special fields based on recommendation type
                if rec.recommendation_type == 'medicine' and rec.medicine_name:
                    med_info = f'<i>Medication:</i> {rec.medicine_name} - {rec.dosage}'
                    if rec.duration:
                        med_info += f' (Duration: {rec.duration})'
                    story.append(Paragraph(med_info, styles['Normal']))
                
                if rec.recommendation_type == 'nutrition' and rec.calories_per_day:
                    nutrition_info = f'<i>Nutrition Targets:</i> '
                    targets = []
                    if rec.calories_per_day:
                        targets.append(f'{rec.calories_per_day} kcal/day')
                    if rec.protein_grams:
                        targets.append(f'{rec.protein_grams}g protein')
                    if rec.iron_mg:
                        targets.append(f'{rec.iron_mg}mg iron')
                    if rec.calcium_mg:
                        targets.append(f'{rec.calcium_mg}mg calcium')
                    nutrition_info += ', '.join(targets)
                    story.append(Paragraph(nutrition_info, styles['Normal']))
                
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph('No health recommendations available.', styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph('Generated by AamCare - Your Virtual Health Assistant', footer_style))
        story.append(Paragraph(f'Report generated on: {timezone.now().strftime("%B %d, %Y at %I:%M %p")}', footer_style))
        
        # Build PDF
        doc.build(story)
        return response
        
    except NewMotherProfile.DoesNotExist:
        messages.error(request, 'Mother profile not found.')
        return redirect('mother_dashboard')
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('mother_dashboard')
