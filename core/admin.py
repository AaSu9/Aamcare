from django.contrib import admin
from .models import (
    PregnantWomanProfile, NewMotherProfile, CheckupProgress, 
    InfoContent, VaccinationRecord, HealthExpert, UserTestimonial, 
    CommunityHealthWorker, PregnancyTip, VaccinationNotificationLog
)

@admin.register(HealthExpert)
class HealthExpertAdmin(admin.ModelAdmin):
    list_display = ['name', 'expert_type', 'institution', 'years_experience', 'is_active']
    list_filter = ['expert_type', 'is_active', 'years_experience']
    search_fields = ['name', 'institution', 'qualification']
    readonly_fields = ['created_at']

@admin.register(UserTestimonial)
class UserTestimonialAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'outcome', 'village_district', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['is_approved', 'is_featured', 'outcome', 'created_at']
    search_fields = ['user__username', 'title', 'story', 'village_district']
    readonly_fields = ['created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    list_editable = ['is_approved', 'is_featured']
    list_display_links = ['title']
    
    # Add bulk actions for better management
    actions = [
        'approve_testimonials',
        'unapprove_testimonials',
        'feature_testimonials',
        'unfeature_testimonials',
        'delete_selected_testimonials'
    ]
    
    # Fieldsets for better organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'story', 'outcome', 'village_district')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_featured'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} testimonials have been approved.')
    approve_testimonials.short_description = "Approve selected testimonials"

    def feature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} testimonials have been featured.')
    feature_testimonials.short_description = "Feature selected testimonials"
    
    def unapprove_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} testimonials have been unapproved.')
    unapprove_testimonials.short_description = "Unapprove selected testimonials"
    
    def unfeature_testimonials(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} testimonials have been unfeatured.')
    unfeature_testimonials.short_description = "Unfeature selected testimonials"
    
    def delete_selected_testimonials(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} testimonials have been permanently deleted.')
    delete_selected_testimonials.short_description = "Delete selected testimonials permanently"
    
    # Custom delete confirmation
    def delete_model(self, request, obj):
        self.message_user(request, f'Success story "{obj.title}" has been permanently deleted.')
        obj.delete()

@admin.register(CommunityHealthWorker)
class CommunityHealthWorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'worker_type', 'village_district', 'years_experience', 'is_verified', 'is_active']
    list_filter = ['worker_type', 'is_verified', 'is_active', 'years_experience']
    search_fields = ['name', 'village_district', 'phone_number']
    readonly_fields = ['created_at']

@admin.register(CheckupProgress)
class CheckupProgressAdmin(admin.ModelAdmin):
    list_display = [
        'profile_type', 'month', 'weight_kg', 'blood_pressure_systolic', 
        'blood_pressure_diastolic', 'fever', 'child_weight_kg', 'child_height_cm', 'created_at'
    ]
    list_filter = ['profile_type', 'month', 'fever', 'child_feeding_status', 'created_at']
    search_fields = ['pregnant_profile__name', 'mother_profile__name', 'notes']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('profile_type', 'pregnant_profile', 'mother_profile', 'month')
        }),
        ('Mother\'s Health', {
            'fields': ('weight_kg', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'fever', 'fever_temperature')
        }),
        ('Child\'s Information', {
            'fields': ('child_weight_kg', 'child_height_cm', 'child_head_circumference_cm', 'child_feeding_status'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(InfoContent)
class InfoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'source', 'is_government_approved', 'is_culturally_sensitive', 'reviewed_by']
    list_filter = ['category', 'source', 'is_government_approved', 'is_culturally_sensitive', 'created_at']
    search_fields = ['title', 'body', 'cultural_context']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'body', 'week_start', 'week_end')
        }),
        ('Trust & Validation', {
            'fields': ('source', 'source_reference', 'reviewed_by', 'review_date', 'is_government_approved')
        }),
        ('Cultural Sensitivity', {
            'fields': ('is_culturally_sensitive', 'cultural_context', 'local_language_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PregnancyTip)
class PregnancyTipAdmin(admin.ModelAdmin):
    list_display = ['tip_type', 'title', 'week_start', 'week_end', 'is_active', 'created_at']
    list_filter = ['tip_type', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tip_type', 'title', 'content')
        }),
        ('Week Range', {
            'fields': ('week_start', 'week_end')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PregnantWomanProfile)
class PregnantWomanProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'age', 'due_date', 'phone_number', 'get_current_week', 'get_trimester_display']
    list_filter = ['due_date']
    search_fields = ['name', 'user__username', 'phone_number']
    readonly_fields = ['get_current_week', 'get_trimester_display', 'get_pregnancy_info']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'age', 'phone_number')
        }),
        ('Pregnancy Details', {
            'fields': ('due_date', 'medical_history')
        }),
        ('Current Status', {
            'fields': ('get_current_week', 'get_trimester_display', 'get_pregnancy_info'),
            'classes': ('collapse',)
        })
    )
    
    def get_current_week(self, obj):
        return f"Week {obj.get_current_pregnancy_week()}"
    get_current_week.short_description = 'Current Week'
    
    def get_trimester_display(self, obj):
        return f"Trimester {obj.get_trimester()}"
    get_trimester_display.short_description = 'Trimester'
    
    def get_pregnancy_info(self, obj):
        dates = obj.get_pregnancy_dates()
        return f"Days remaining: {dates['days_remaining']}, Weeks remaining: {dates['weeks_remaining']}"
    get_pregnancy_info.short_description = 'Pregnancy Info'

@admin.register(NewMotherProfile)
class NewMotherProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'child_birth_date', 'phone_number', 'get_days_since_birth', 'get_postpartum_stage_display']
    list_filter = ['child_birth_date']
    search_fields = ['name', 'user__username', 'phone_number']
    readonly_fields = ['get_days_since_birth', 'get_postpartum_stage_display', 'get_postpartum_info']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'phone_number')
        }),
        ('Child Information', {
            'fields': ('child_birth_date', 'current_health_status')
        }),
        ('Current Status', {
            'fields': ('get_days_since_birth', 'get_postpartum_stage_display', 'get_postpartum_info'),
            'classes': ('collapse',)
        })
    )
    
    def get_days_since_birth(self, obj):
        dates = obj.get_postpartum_dates()
        return f"{dates['days_since_birth']} days ({dates['weeks_since_birth']} weeks)"
    get_days_since_birth.short_description = 'Time Since Birth'
    
    def get_postpartum_stage_display(self, obj):
        return obj.get_postpartum_stage().title()
    get_postpartum_stage_display.short_description = 'Postpartum Stage'
    
    def get_postpartum_info(self, obj):
        dates = obj.get_postpartum_dates()
        return f"Months since birth: {dates['months_since_birth']}"
    get_postpartum_info.short_description = 'Postpartum Info'

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['get_profile_name', 'vaccine_name', 'due_date', 'completed_date', 'status', 'created_at']
    list_filter = ['status', 'vaccine_name', 'due_date', 'created_at']
    search_fields = ['pregnant_profile__name', 'mother_profile__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Profile Information', {
            'fields': ('pregnant_profile', 'mother_profile')
        }),
        ('Vaccination Details', {
            'fields': ('vaccine_name', 'due_date', 'completed_date', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_profile_name(self, obj):
        if obj.pregnant_profile:
            return f"{obj.pregnant_profile.name} (Pregnant)"
        elif obj.mother_profile:
            return f"{obj.mother_profile.name} (Mother)"
        return "No Profile"
    get_profile_name.short_description = 'Profile'
    get_profile_name.admin_order_field = 'pregnant_profile__name'

@admin.register(VaccinationNotificationLog)
class VaccinationNotificationLogAdmin(admin.ModelAdmin):
    list_display = ['get_recipient', 'notification_type', 'sent_at', 'status', 'get_vaccination']
    list_filter = ['notification_type', 'status', 'sent_at']
    search_fields = ['user__username', 'pregnant_woman__name', 'mother__name', 'message']
    readonly_fields = ['sent_at']
    date_hierarchy = 'sent_at'
    
    fieldsets = (
        ('Recipient Information', {
            'fields': ('user', 'pregnant_woman', 'mother')
        }),
        ('Notification Details', {
            'fields': ('notification_type', 'vaccination_record', 'sent_at', 'status')
        }),
        ('Message', {
            'fields': ('message',),
            'classes': ('collapse',)
        })
    )
    
    def get_recipient(self, obj):
        target = obj.pregnant_woman or obj.mother or obj.user
        return str(target) if target else "Unknown"
    get_recipient.short_description = 'Recipient'
    
    def get_vaccination(self, obj):
        if obj.vaccination_record:
            return obj.vaccination_record.get_vaccine_name_display()
        return "N/A"
    get_vaccination.short_description = 'Vaccine'
