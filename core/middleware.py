"""
Custom middleware for handling user authentication
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class GoogleOAuthOnboardingMiddleware:
    """
    Middleware to handle user authentication redirects
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view
        response = self.get_response(request)
        
        return response
