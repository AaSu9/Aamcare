from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/pregnant/', views.register_pregnant_woman, name='register_pregnant_woman'),
    path('register/mother/', views.register_new_mother, name='register_new_mother'),
    path('dashboard/pregnant/', views.pregnant_dashboard, name='pregnant_dashboard'),
    path('dashboard/mother/', views.mother_dashboard, name='mother_dashboard'),
    path('story/submit/', views.submit_story, name='submit_story'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('give-birth/', views.give_birth, name='give_birth'),
    path('checkup/submit/<str:profile_type>/', views.submit_checkup, name='submit_checkup'),
    path('checkup/delete/<int:checkup_id>/', views.delete_checkup, name='delete_checkup'),
    path('vaccination/tracker/', views.vaccination_tracker, name='vaccination_tracker'),
    path('vaccination/update/<int:vaccination_id>/', views.update_vaccination, name='update_vaccination'),
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),
    path('diet-plans/', views.diet_plans, name='diet_plans'),
    path('vaccination-schedule/', views.vaccination_schedule, name='vaccination_schedule'),
    path('exercise-guidance/', views.exercise_guidance, name='exercise_guidance'),
    path('breastfeeding-support/', views.breastfeeding_support, name='breastfeeding_support'),
    path('mental-health-support/', views.mental_health_support, name='mental_health_support'),
    
    # Trust-building features
    path('testimonials/', views.testimonials, name='testimonials'),
    path('health-experts/', views.health_experts, name='health_experts'),
    path('community-workers/', views.community_workers, name='community_workers'),
    path('danger-signs/', views.danger_signs, name='danger_signs'),
    path('about-trust/', views.about_trust, name='about_trust'),
    path('trimester-tips/', views.trimester_tips, name='trimester_tips'),
    path('comprehensive-nutrition/pregnant/', views.comprehensive_nutrition_pregnant, name='comprehensive_nutrition_pregnant'),
    path('comprehensive-nutrition/mother/', views.comprehensive_nutrition_mother, name='comprehensive_nutrition_mother'),
    path('set-language/', views.set_language, name='set_language'),
    path('language-demo/', views.language_demo, name='language_demo'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/update/pregnant/', views.update_pregnant_profile, name='update_pregnant_profile'),
    path('profile/update/mother/', views.update_mother_profile, name='update_mother_profile'),
    path('complete-profile/pregnant/', views.complete_pregnant_profile, name='complete_pregnant_profile'),
    path('complete-profile/mother/', views.complete_mother_profile, name='complete_mother_profile'),
] 