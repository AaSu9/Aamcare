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

admin.site.register(PregnantWomanProfile)
admin.site.register(NewMotherProfile)
admin.site.register(VaccinationRecord)
admin.site.register(VaccinationNotificationLog)
