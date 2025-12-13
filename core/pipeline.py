"""
Custom pipeline for handling Google OAuth2 authentication
"""
from django.contrib.auth.models import User
from core.models import PregnantWomanProfile, NewMotherProfile
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """Create or get user from Google OAuth2 data"""
    if user:
        return {'is_new': False}

    # Extract user information from Google
    email = details.get('email')
    first_name = details.get('first_name', '')
    last_name = details.get('last_name', '')
    username = details.get('username') or email.split('@')[0]
    
    # Check if user already exists
    try:
        user = User.objects.get(email=email)
        return {'is_new': False, 'user': user}
    except User.DoesNotExist:
        pass
    
    # Create new user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=User.objects.make_random_password()  # Random password since they'll use Google auth
        )
        
        logger.info(f"Created new user from Google OAuth: {user.username}")
        return {'is_new': True, 'user': user}
    except Exception as e:
        logger.error(f"Error creating user from Google OAuth: {str(e)}")
        return None

def create_profile(strategy, details, backend, user=None, is_new=False, *args, **kwargs):
    """Create user profile based on session data or default to pregnant woman"""
    if not user:
        return
    
    # If user is not new, don't create profile (already exists)
    if not is_new:
        return
    
    # Try to get user type from session (set during registration)
    user_type = strategy.session_get('user_type', 'pregnant')
    
    try:
        if user_type == 'pregnant':
            profile = PregnantWomanProfile.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip(),
                phone_number='',  # Will be added later
                created_by_google=True
            )
            logger.info(f"Created PregnantWomanProfile for Google user: {user.username}")
            # Store in session for post-processing
            strategy.session_set('newly_created_profile_id', profile.id)
            strategy.session_set('newly_created_profile_type', 'pregnant')
        elif user_type == 'mother':
            profile = NewMotherProfile.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip(),
                phone_number='',  # Will be added later
                created_by_google=True
            )
            logger.info(f"Created NewMotherProfile for Google user: {user.username}")
            # Store in session for post-processing
            strategy.session_set('newly_created_profile_id', profile.id)
            strategy.session_set('newly_created_profile_type', 'mother')
        else:
            # Default to pregnant woman if no type specified
            profile = PregnantWomanProfile.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip(),
                phone_number='',
                created_by_google=True
            )
            logger.info(f"Created default PregnantWomanProfile for Google user: {user.username}")
            # Store in session for post-processing
            strategy.session_set('newly_created_profile_id', profile.id)
            strategy.session_set('newly_created_profile_type', 'pregnant')
            
    except Exception as e:
        logger.error(f"Error creating profile for Google user {user.username}: {str(e)}")

def redirect_to_profile_completion(strategy, details, backend, user=None, is_new=False, *args, **kwargs):
    """Redirect newly created Google users to profile completion page"""
    if not user or not is_new:
        return
    
    # Check if this is a newly created Google user
    profile_type = strategy.session_get('newly_created_profile_type')
    profile_id = strategy.session_get('newly_created_profile_id')
    
    if profile_type and profile_id:
        # Set a flag in session to indicate user needs to complete profile
        strategy.session_set('needs_profile_completion', True)
        strategy.session_set('profile_completion_type', profile_type)
        strategy.session_set('profile_completion_id', profile_id)
        
        # Clean up temporary session data
        strategy.session_pop('newly_created_profile_type', None)
        strategy.session_pop('newly_created_profile_id', None)
        
        # Note: We can't do actual redirect here as this is in pipeline
        # The redirect will be handled in a custom middleware or view