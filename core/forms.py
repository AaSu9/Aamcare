from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from .models import PregnantWomanProfile, NewMotherProfile, CheckupProgress, VaccinationRecord, UserTestimonial

class PregnantWomanRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(min_value=13, max_value=100, required=True)
    due_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    phone_number = forms.CharField(max_length=15, required=True, help_text='Enter your phone number for SMS notifications')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 20:
            raise forms.ValidationError("Registration is only allowed for women aged 20 or above.")
        return age

class NewMotherRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    child_birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    current_health_status = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    age = forms.IntegerField(min_value=13, max_value=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True, help_text='Enter your phone number for SMS notifications')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 20:
            raise forms.ValidationError("Registration is only allowed for mothers aged 20 or above.")
        return age

class CheckupProgressForm(forms.ModelForm):
    class Meta:
        model = CheckupProgress
        fields = [
            'month', 
            'weight_kg', 
            'blood_pressure_systolic', 
            'blood_pressure_diastolic', 
            'fever',
            'fever_temperature',
            'child_weight_kg',
            'child_height_cm',
            'child_head_circumference_cm',
            'child_feeding_status',
            'notes'
        ]
        widgets = {
            'weight_kg': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'placeholder': 'e.g., 65.5'}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'min': '0', 'max': '300', 'placeholder': 'e.g., 120'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'min': '0', 'max': '200', 'placeholder': 'e.g., 80'}),
            'fever_temperature': forms.NumberInput(attrs={'step': '0.1', 'min': '35', 'max': '45', 'placeholder': 'e.g., 38.5'}),
            'child_weight_kg': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': 'e.g., 3.2'}),
            'child_height_cm': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'placeholder': 'e.g., 50.5'}),
            'child_head_circumference_cm': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'placeholder': 'e.g., 35.2'}),
            'child_feeding_status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        profile_type = kwargs.pop('profile_type', None)
        super().__init__(*args, **kwargs)
        
        # Set labels
        self.fields['weight_kg'].label = "Mother's Weight (kg)"
        self.fields['blood_pressure_systolic'].label = "Mother's Blood Pressure - Systolic"
        self.fields['blood_pressure_diastolic'].label = "Mother's Blood Pressure - Diastolic"
        self.fields['fever'].label = "Does mother have fever?"
        self.fields['fever_temperature'].label = "Fever Temperature (°C)"
        self.fields['child_weight_kg'].label = "Child's Weight (kg)"
        self.fields['child_height_cm'].label = "Child's Height (cm)"
        self.fields['child_head_circumference_cm'].label = "Child's Head Circumference (cm)"
        self.fields['child_feeding_status'].label = "Child's Feeding Method"
        
        # Show/hide fields based on profile type
        if profile_type == 'pregnant':
            # Hide child-related fields for pregnant women
            self.fields['child_weight_kg'].widget = forms.HiddenInput()
            self.fields['child_height_cm'].widget = forms.HiddenInput()
            self.fields['child_head_circumference_cm'].widget = forms.HiddenInput()
            self.fields['child_feeding_status'].widget = forms.HiddenInput()
        elif profile_type == 'mother':
            # Show all fields for new mothers
            pass
        else:
            # Default: show all fields
            pass

    def clean(self):
        cleaned_data = super().clean()
        fever = cleaned_data.get('fever')
        fever_temperature = cleaned_data.get('fever_temperature')
        
        # If fever is True but no temperature provided, set a default
        if fever and not fever_temperature:
            cleaned_data['fever_temperature'] = 38.0
        
        return cleaned_data

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['status', 'completed_date', 'notes']
        widgets = {
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make completed_date required when status is completed
        if self.instance and self.instance.status == 'completed':
            self.fields['completed_date'].required = True
        else:
            self.fields['completed_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completed_date = cleaned_data.get('completed_date')
        
        if status == 'completed' and not completed_date:
            cleaned_data['completed_date'] = date.today()
        
        return cleaned_data 

class UserTestimonialForm(forms.ModelForm):
    class Meta:
        model = UserTestimonial
        fields = ['title', 'story', 'outcome', 'village_district']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'story': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Share your story...'}),
            'outcome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g., 'Safe delivery', 'Healthy baby', 'Recovery'"}),
            'village_district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village and district'}),
        } 

class GiveBirthForm(forms.Form):
    actual_birth_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Enter the actual date when you gave birth"
    )
    baby_name = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Baby\'s name (optional)'}),
        help_text="Optional: Enter your baby's name"
    )
    birth_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any notes about the birth (optional)'}),
        required=False,
        help_text="Optional: Any notes about the birth experience"
    )

    def clean_actual_birth_date(self):
        birth_date = self.cleaned_data.get('actual_birth_date')
        if birth_date and birth_date > date.today():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return birth_date 

class PregnantWomanProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PregnantWomanProfile
        fields = ['phone_number']

class NewMotherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = NewMotherProfile
        fields = ['phone_number'] 