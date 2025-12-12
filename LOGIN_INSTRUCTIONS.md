# Login and Registration Instructions

## Existing User Accounts

You can log in with any of these existing accounts:

### Regular Users
1. **rita** (pregnant woman)
   - Username: `rita`
   - Password: (you'll need to set this)
   
2. **sita** (new mother)
   - Username: `sita`
   - Password: (you'll need to set this)
   
3. **demo_mom** (pregnant woman)
   - Username: `demo_mom`
   - Password: (you'll need to set this)

### Admin User
- Username: `admin`
- Password: `admin123`

## Setting Passwords for Regular Users

Since passwords weren't set for the regular users, you'll need to set them first:

1. Access the admin panel: http://127.0.0.1:8000/admin/
2. Log in with admin credentials (admin/admin123)
3. Navigate to "Users" section
4. Click on each user (rita, sita, demo_mom)
5. In the "Password" field, click "Reset password"
6. Follow the prompts to set a new password

## Alternative: Create New User Accounts

You can also register new accounts:

1. **Register as Pregnant Woman**: http://127.0.0.1:8000/register/pregnant/
2. **Register as New Mother**: http://127.0.0.1:8000/register/mother/

## Login Process

1. Visit: http://127.0.0.1:8000/login/
2. Enter your username and password
3. You'll be redirected to your appropriate dashboard:
   - Pregnant women go to: http://127.0.0.1:8000/pregnant/dashboard/
   - New mothers go to: http://127.0.0.1:8000/mother/dashboard/

## Troubleshooting

### If you can't log in:
1. Make sure you've set passwords for existing users via admin panel
2. Check that the server is running (http://127.0.0.1:8000/)
3. Verify the URLs are correct

### If redirected incorrectly:
1. The system automatically detects your profile type
2. If you have no profile, you'll be redirected to the home page

## Testing the Automated Twilio Registration

When you register a new user:
1. Their phone number is automatically registered with Twilio
2. They receive a welcome message
3. They're ready to receive daily health tips at 7 AM

The system now works correctly with:
✅ Fixed login redirection URLs
✅ Proper user profile detection
✅ Automated Twilio phone number registration
✅ Welcome messages for new registrations