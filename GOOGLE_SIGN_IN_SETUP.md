# Google Sign-In Setup Guide

## 📋 Prerequisites

Before implementing Google Sign-In, you'll need:

1. **Google Cloud Project** with billing enabled
2. **OAuth 2.0 Client ID** for web application
3. **Domain verification** (for production)

## 🔧 Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "Aamcare Health")
4. Click "Create"

### 2. Enable Google+ API

1. In Google Cloud Console, navigate to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Web application"
4. Enter name (e.g., "Aamcare Web App")
5. **Authorized JavaScript origins**:
   ```
   http://localhost:8000
   http://127.0.0.1:8000
   https://yourdomain.com (for production)
   ```
6. **Authorized redirect URIs**:
   ```
   http://localhost:8000/social-auth/complete/google-oauth2/
   http://127.0.0.1:8000/social-auth/complete/google-oauth2/
   https://yourdomain.com/social-auth/complete/google-oauth2/ (for production)
   ```
7. Click "Create"
8. Copy the **Client ID** and **Client Secret**

### 4. Configure Django Settings

Update your `aamcare/settings.py`:

```python
# Social Auth Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'YOUR_GOOGLE_CLIENT_ID'  # From step 3
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'  # From step 3
```

Replace:
- `YOUR_GOOGLE_CLIENT_ID` with your actual Client ID
- `YOUR_GOOGLE_CLIENT_SECRET` with your actual Client Secret

### 5. Update Base Template (Optional)

In `core/templates/core/base.html`, update the meta tag:

```html
<meta name="google-signin-client_id" content="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com">
```

## 🧪 Testing Google Sign-In

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to the login page: http://localhost:8000/login/

3. Click the "Sign in with Google" button

4. You should be redirected to Google's authentication page

5. After authentication, you'll be redirected back to your application

## 🛠️ Troubleshooting

### Common Issues:

1. **"redirect_uri_mismatch" Error**:
   - Ensure redirect URIs in Google Cloud Console exactly match your application's URLs
   - Include both `http://localhost:8000` and `http://127.0.0.1:8000` versions

2. **"invalid_client" Error**:
   - Verify Client ID and Client Secret are correctly entered in settings.py
   - Ensure no extra spaces or characters

3. **User Already Exists**:
   - System automatically detects existing users by email and logs them in
   - No duplicate accounts will be created

## 📊 User Experience Flow

1. **New User Registration**:
   - User clicks "Sign in with Google"
   - Google authenticates user
   - System creates new user account with Google profile data
   - User is redirected to appropriate dashboard based on registration type

2. **Existing User Login**:
   - User clicks "Sign in with Google"
   - Google authenticates user
   - System finds existing account by email
   - User is logged in and redirected to their dashboard

3. **Profile Creation**:
   - For new users, system creates appropriate profile (Pregnant Woman or New Mother)
   - Profile type determined by registration selection before Google Sign-In
   - Default to Pregnant Woman if no selection made

## 🔒 Security Considerations

1. **OAuth Tokens**:
   - Social Auth stores tokens securely
   - Tokens are used only for authentication, not for accessing Google services

2. **Email Verification**:
   - Google ensures email addresses are verified
   - No additional verification needed in the application

3. **Data Privacy**:
   - Only essential profile information is retrieved (name, email)
   - No access to Google contacts, calendar, or other services

## 🔄 Migration from Traditional Login

Users with existing accounts can:
1. Use traditional login with username/password
2. Later add Google Sign-In by connecting their Google account
3. System will match by email address

## 💡 Best Practices

1. **Clear Instructions**:
   - Explain benefits of Google Sign-In to users
   - Highlight security and convenience advantages

2. **Fallback Option**:
   - Keep traditional registration/login as alternative
   - Some users may prefer not to use Google

3. **Mobile Optimization**:
   - Google Sign-In works seamlessly on mobile browsers
   - Provides native app-like authentication experience

4. **Testing**:
   - Test with multiple Google accounts
   - Verify both new user registration and existing user login flows

## 📈 Analytics & Monitoring

The system logs:
- Successful Google authentications
- New user creations via Google
- Profile creation events
- Any authentication errors

Check Django logs for troubleshooting authentication issues.

## 🚀 Production Deployment

For production deployment:

1. **Update Authorized Origins**:
   - Add your production domain to Google Cloud Console
   - Remove localhost entries for security

2. **HTTPS Requirements**:
   - Ensure your site uses HTTPS
   - Google requires secure origins for OAuth

3. **Environment Variables**:
   - Store Client ID and Secret in environment variables
   - Never commit credentials to version control

4. **Monitoring**:
   - Set up error tracking for authentication failures
   - Monitor successful login rates

## 🆘 Support Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Django Social Auth Documentation](https://python-social-auth.readthedocs.io/)
- [Google Cloud Console](https://console.cloud.google.com/)

For issues with this implementation, check:
1. Django logs
2. Browser developer console
3. Google Cloud Console API metrics