from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import date, timedelta

class PregnantWomanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    due_date = models.DateField()
    medical_history = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name
    
    def get_current_pregnancy_week(self):
        """Calculate current pregnancy week based on due date"""
        today = date.today()
        # Pregnancy is typically 40 weeks, so conception date is 40 weeks before due date
        conception_date = self.due_date - timedelta(weeks=40)
        weeks_pregnant = (today - conception_date).days // 7
        return max(1, min(40, weeks_pregnant))

    def get_current_pregnancy_month(self):
        """Calculate current pregnancy month based on due date"""
        weeks = self.get_current_pregnancy_week()
        return (weeks // 4) + 1
    
    def get_trimester(self):
        """Get current trimester (1, 2, or 3)"""
        weeks = self.get_current_pregnancy_week()
        if weeks <= 13:
            return 1
        elif weeks <= 26:
            return 2
        else:
            return 3
    
    def get_pregnancy_dates(self):
        """Get important pregnancy dates for planning"""
        today = date.today()
        conception_date = self.due_date - timedelta(weeks=40)
        current_week = self.get_current_pregnancy_week()
        
        # Calculate important dates
        dates = {
            'conception_date': conception_date,
            'first_trimester_end': conception_date + timedelta(weeks=13),
            'second_trimester_end': conception_date + timedelta(weeks=26),
            'third_trimester_start': conception_date + timedelta(weeks=27),
            'current_date': today,
            'weeks_remaining': 40 - current_week,
            'days_remaining': (self.due_date - today).days,
        }
        
        # Calculate week-specific dates for the next 4 weeks
        dates['next_weeks'] = []
        for i in range(1, 5):
            week_date = conception_date + timedelta(weeks=current_week + i - 1)
            if week_date <= self.due_date:
                dates['next_weeks'].append({
                    'week': current_week + i,
                    'date': week_date,
                    'days_from_now': (week_date - today).days
                })
        
        return dates

class NewMotherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    child_birth_date = models.DateField()
    current_health_status = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name
    
    def get_postpartum_dates(self):
        """Get important postpartum dates for planning"""
        today = date.today()
        birth_date = self.child_birth_date
        days_since_birth = (today - birth_date).days
        
        # Calculate important postpartum dates
        dates = {
            'birth_date': birth_date,
            'days_since_birth': days_since_birth,
            'weeks_since_birth': days_since_birth // 7,
            'months_since_birth': days_since_birth // 30,
            'current_date': today,
        }
        
        # Calculate upcoming milestone dates
        dates['milestones'] = []
        milestones = [
            (7, '1 week postpartum'),
            (14, '2 weeks postpartum'),
            (30, '1 month postpartum'),
            (42, '6 weeks postpartum'),
            (60, '2 months postpartum'),
            (90, '3 months postpartum'),
            (180, '6 months postpartum'),
            (365, '1 year postpartum'),
        ]
        
        for days, description in milestones:
            milestone_date = birth_date + timedelta(days=days)
            if milestone_date >= today:
                dates['milestones'].append({
                    'date': milestone_date,
                    'description': description,
                    'days_from_now': (milestone_date - today).days
                })
        
        return dates
    
    def get_postpartum_stage(self):
        """Get current postpartum recovery stage (early, mid, established)"""
        days_since_birth = (date.today() - self.child_birth_date).days
        if days_since_birth <= 42:  # 0-6 weeks
            return 'early'
        elif days_since_birth <= 90:  # 6 weeks - 3 months
            return 'mid'
        else:  # 3+ months
            return 'established'

class CheckupProgress(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('pregnant', 'Pregnant Woman'),
        ('mother', 'New Mother'),
    )
    profile_type = models.CharField(max_length=10, choices=PROFILE_TYPE_CHOICES)
    pregnant_profile = models.ForeignKey(PregnantWomanProfile, on_delete=models.CASCADE, null=True, blank=True)
    mother_profile = models.ForeignKey(NewMotherProfile, on_delete=models.CASCADE, null=True, blank=True)
    month = models.PositiveIntegerField()
    
    # Mother's health information
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Mother's weight in kilograms")
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True, help_text="Mother's systolic blood pressure (top number)")
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True, help_text="Mother's diastolic blood pressure (bottom number)")
    fever = models.BooleanField(default=False, help_text="Does mother have fever?")
    fever_temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Fever temperature in Celsius")
    
    # Newborn child information (for mother profiles)
    child_weight_kg = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Child's weight in kilograms")
    child_height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Child's height in centimeters")
    child_head_circumference_cm = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Child's head circumference in centimeters")
    child_feeding_status = models.CharField(max_length=20, choices=[
        ('breastfeeding', 'Breastfeeding'),
        ('formula', 'Formula Feeding'),
        ('mixed', 'Mixed Feeding'),
        ('weaning', 'Weaning'),
    ], blank=True, help_text="Child's current feeding method")
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.profile_type == 'pregnant' and self.pregnant_profile:
            return f"{self.pregnant_profile.name} - Month {self.month}"
        elif self.profile_type == 'mother' and self.mother_profile:
            return f"{self.mother_profile.name} - Month {self.month}"
        return f"Checkup Progress - Month {self.month}"

class HealthExpert(models.Model):
    """Model for health experts who validate content"""
    EXPERT_TYPE_CHOICES = (
        ('doctor', 'Medical Doctor'),
        ('midwife', 'Midwife'),
        ('nurse', 'Nurse'),
        ('nutritionist', 'Nutritionist'),
        ('psychologist', 'Psychologist'),
        ('anm', 'Auxiliary Nurse Midwife (ANM)'),
        ('fchv', 'Female Community Health Volunteer (FCHV)'),
    )
    
    name = models.CharField(max_length=100)
    expert_type = models.CharField(max_length=20, choices=EXPERT_TYPE_CHOICES)
    qualification = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    years_experience = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='experts/', null=True, blank=True)
    bio = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.get_expert_type_display()}"

class InfoContent(models.Model):
    CATEGORY_CHOICES = (
        ('diet', 'Diet'),
        ('vaccine', 'Vaccine'),
        ('exercise', 'Exercise'),
        ('mental', 'Mental Health'),
        ('breastfeeding', 'Breastfeeding'),
        ('danger_signs', 'Danger Signs'),
        ('cultural', 'Cultural Guidance'),
    )
    
    SOURCE_CHOICES = (
        ('who', 'World Health Organization (WHO)'),
        ('nepal_mohp', 'Nepal Ministry of Health and Population'),
        ('local_expert', 'Local Health Expert'),
        ('community', 'Community Health Worker'),
        ('research', 'Medical Research'),
    )
    
    TRIMESTER_CHOICES = (
        ('1', 'First Trimester (Weeks 1-13)'),
        ('2', 'Second Trimester (Weeks 14-26)'),
        ('3', 'Third Trimester (Weeks 27-40)'),
        ('all', 'All Trimesters'),
    )
    
    POSTPARTUM_STAGE_CHOICES = (
        ('early', 'Early Recovery (0-6 weeks)'),
        ('mid', 'Mid Recovery (6 weeks - 3 months)'),
        ('established', 'Established (3+ months)'),
        ('all', 'All Stages'),
    )
    
    TARGET_AUDIENCE_CHOICES = (
        ('pregnant', 'Pregnant Women'),
        ('mother', 'New Mothers'),
        ('both', 'Both'),
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    title_ne = models.CharField(max_length=200, blank=True, null=True, help_text="Title in Nepali")
    body = models.TextField()
    body_ne = models.TextField(blank=True, null=True, help_text="Body in Nepali")
    week_start = models.PositiveIntegerField(null=True, blank=True, help_text="Start week for this content (1-40)")
    week_end = models.PositiveIntegerField(null=True, blank=True, help_text="End week for this content (1-40)")
    
    # Trust and validation fields
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='local_expert')
    source_reference = models.CharField(max_length=500, blank=True, help_text="Specific reference or document number")
    reviewed_by = models.ForeignKey(HealthExpert, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    is_government_approved = models.BooleanField(default=False)
    is_culturally_sensitive = models.BooleanField(default=True)
    
    # Cultural context
    cultural_context = models.TextField(blank=True, help_text="How this information relates to Nepali culture and traditions")
    local_language_available = models.BooleanField(default=False, help_text="Available in local languages (Nepali, Maithili, etc.)")
    
    # Trimester and postpartum targeting
    trimester = models.CharField(max_length=5, choices=TRIMESTER_CHOICES, default='all', help_text="Relevant trimester for pregnant women")
    postpartum_stage = models.CharField(max_length=20, choices=POSTPARTUM_STAGE_CHOICES, default='all', help_text="Relevant postpartum stage for new mothers")
    target_audience = models.CharField(max_length=10, choices=TARGET_AUDIENCE_CHOICES, default='both', help_text="Target audience for this content")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def is_relevant_for_week(self, week):
        """Check if this content is relevant for a specific pregnancy week"""
        if self.week_start is None or self.week_end is None:
            return True  # General content is always relevant
        return self.week_start <= week <= self.week_end

class UserTestimonial(models.Model):
    """Model for user success stories and testimonials"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    title_ne = models.CharField(max_length=200, blank=True, null=True, help_text="Title in Nepali")
    story = models.TextField()
    story_ne = models.TextField(blank=True, null=True, help_text="Story in Nepali")
    outcome = models.CharField(max_length=100, help_text="e.g., 'Safe delivery', 'Healthy baby', 'Recovery'")
    village_district = models.CharField(max_length=100, help_text="Village and district")
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class CommunityHealthWorker(models.Model):
    """Model for local health workers who contribute to the app"""
    WORKER_TYPE_CHOICES = (
        ('anm', 'Auxiliary Nurse Midwife (ANM)'),
        ('fchv', 'Female Community Health Volunteer (FCHV)'),
        ('asha', 'Accredited Social Health Activist (ASHA)'),
        ('local_doctor', 'Local Doctor'),
    )
    
    name = models.CharField(max_length=100)
    worker_type = models.CharField(max_length=20, choices=WORKER_TYPE_CHOICES)
    village_district = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    years_experience = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_worker_type_display()} ({self.village_district})"

class VaccinationRecord(models.Model):
    VACCINE_CHOICES = (
        ('tdap', 'Tdap (Tetanus, Diphtheria, Pertussis)'),
        ('influenza', 'Influenza Vaccine'),
        ('covid19', 'COVID-19 Vaccine'),
        ('hepb_birth', 'Hepatitis B (Birth)'),
        ('dtap_2m', 'DTaP (2 months)'),
        ('hib_2m', 'Hib (2 months)'),
        ('pcv13_2m', 'PCV13 (2 months)'),
        ('ipv_2m', 'IPV (2 months)'),
        ('rotavirus_2m', 'Rotavirus (2 months)'),
        ('dtap_4m', 'DTaP (4 months)'),
        ('hib_4m', 'Hib (4 months)'),
        ('pcv13_4m', 'PCV13 (4 months)'),
        ('ipv_4m', 'IPV (4 months)'),
        ('rotavirus_4m', 'Rotavirus (4 months)'),
        ('dtap_6m', 'DTaP (6 months)'),
        ('hib_6m', 'Hib (6 months)'),
        ('pcv13_6m', 'PCV13 (6 months)'),
        ('ipv_6m', 'IPV (6 months)'),
        ('rotavirus_6m', 'Rotavirus (6 months)'),
        ('hepb_6m', 'Hepatitis B (6 months)'),
        ('mmr_12m', 'MMR (12 months)'),
        ('varicella_12m', 'Varicella (12 months)'),
        ('hepa_12m', 'Hepatitis A (12 months)'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('not_applicable', 'Not Applicable'),
    )
    
    pregnant_profile = models.ForeignKey(PregnantWomanProfile, on_delete=models.CASCADE, null=True, blank=True)
    mother_profile = models.ForeignKey(NewMotherProfile, on_delete=models.CASCADE, null=True, blank=True)
    vaccine_name = models.CharField(max_length=20, choices=VACCINE_CHOICES)
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.pregnant_profile:
            return f"{self.pregnant_profile.name} - {self.get_vaccine_name_display()}"
        elif self.mother_profile:
            return f"{self.mother_profile.name} - {self.get_vaccine_name_display()}"
        return f"Vaccination - {self.get_vaccine_name_display()}"

class PregnancyTip(models.Model):
    """Model for pregnancy tips and advice"""
    tip_type = models.CharField(max_length=20, choices=[
        ('general', 'General'),
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise'),
        ('safety', 'Safety'),
        ('emotional', 'Emotional Health'),
        ('medical', 'Medical'),
    ], default='general')
    title = models.CharField(max_length=200)
    title_ne = models.CharField(max_length=200, blank=True, null=True, help_text="Title in Nepali")
    content = models.TextField()
    content_ne = models.TextField(blank=True, null=True, help_text="Content in Nepali")
    week_start = models.IntegerField(help_text="Starting week of pregnancy")
    week_end = models.IntegerField(help_text="Ending week of pregnancy")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['week_start', 'created_at']

    def __str__(self):
        return f"{self.title} (Week {self.week_start}-{self.week_end})"

class VaccinationNotificationLog(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("sms", "SMS"),
        ("email", "Email"),
        ("whatsapp", "WhatsApp"),
    ]
    STATUS_CHOICES = [
        ("success", "Success"),
        ("failure", "Failure"),
    ]
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, null=True, blank=True,
        help_text="The user who received the notification (if applicable)."
    )
    pregnant_woman = models.ForeignKey(
        'PregnantWomanProfile', on_delete=models.CASCADE, null=True, blank=True,
        help_text="Pregnant woman profile if applicable."
    )
    mother = models.ForeignKey(
        'NewMotherProfile', on_delete=models.CASCADE, null=True, blank=True,
        help_text="New mother profile if applicable."
    )
    vaccination_record = models.ForeignKey(
        'VaccinationRecord', on_delete=models.CASCADE, null=True, blank=True,
        help_text="The vaccination record related to this notification."
    )
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES)
    sent_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.TextField(blank=True, help_text="The message content or error details.")

    def __str__(self):
        target = self.pregnant_woman or self.mother or self.user
        return f"{self.get_notification_type_display()} to {target} at {self.sent_at}"


class HealthRecommendation(models.Model):
    """Model for storing personalized health recommendations based on checkup data"""
    RECOMMENDATION_TYPE_CHOICES = [
        ("nutrition", "Nutrition"),
        ("medicine", "Medicine"),
        ("lifestyle", "Lifestyle"),
        ("exercise", "Exercise"),
        ("medical_attention", "Medical Attention Required"),
    ]
    
    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]
    
    checkup = models.ForeignKey(CheckupProgress, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="low")
    
    # Medicine specific fields
    medicine_name = models.CharField(max_length=100, blank=True)
    dosage = models.CharField(max_length=100, blank=True, help_text="e.g., '500mg twice daily'")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '7 days'")
    
    # Nutrition specific fields
    calories_per_day = models.PositiveIntegerField(null=True, blank=True)
    protein_grams = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    iron_mg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    calcium_mg = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    
    # Action items
    action_required = models.BooleanField(default=False, help_text="Does this require immediate action?")
    follow_up_days = models.PositiveIntegerField(null=True, blank=True, help_text="Days until follow-up recommended")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_recommendation_type_display()}: {self.title}"
    
    class Meta:
        ordering = ['-severity', '-created_at']
