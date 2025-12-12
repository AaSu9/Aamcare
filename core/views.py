from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.views import LoginView
from .forms import PregnantWomanRegistrationForm, NewMotherRegistrationForm, CheckupProgressForm, VaccinationRecordForm, UserTestimonialForm, GiveBirthForm, PregnantWomanProfileUpdateForm, NewMotherProfileUpdateForm
from .models import (
    PregnantWomanProfile, NewMotherProfile, CheckupProgress, InfoContent, 
    VaccinationRecord, HealthExpert, UserTestimonial, CommunityHealthWorker, PregnancyTip
)
from django.contrib.auth.models import User
# Custom language session key
LANGUAGE_SESSION_KEY = 'django_language'

def home(request):
    # Get featured testimonials for the homepage
    featured_testimonials = UserTestimonial.objects.filter(is_approved=True, is_featured=True)[:3]
    
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
            messages.success(request, 'Checkup progress submitted successfully!')
            
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
            PregnantWomanProfile.objects.get(user=user)
            return '/dashboard/pregnant/'
        except PregnantWomanProfile.DoesNotExist:
            pass
        
        # Check if user has a new mother profile
        try:
            NewMotherProfile.objects.get(user=user)
            return '/dashboard/mother/'
        except NewMotherProfile.DoesNotExist:
            pass
        
        # If no profile found, redirect to home
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
