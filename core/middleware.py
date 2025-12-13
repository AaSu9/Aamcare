"""
Custom middleware for handling Google OAuth user onboarding
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class GoogleOAuthOnboardingMiddleware:
    """
    Middleware to redirect newly Google authenticated users to profile completion page
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view
        response = self.get_response(request)
        
        # Check if user is authenticated and needs profile completion
        if request.user.is_authenticated:
            if request.session.get('needs_profile_completion', False):
                # Clear the flag
                needs_completion = request.session.pop('needs_profile_completion', False)
                profile_type = request.session.pop('profile_completion_type', 'pregnant')
                
                if needs_completion:
                    # Add a message to inform the user
                    messages.info(request, 'Please complete your profile information.')
                    
                    # Redirect to appropriate profile completion page
                    if profile_type == 'pregnant':
                        return redirect('complete_pregnant_profile')
                    elif profile_type == 'mother':
                        return redirect('complete_mother_profile')
        
        return response