# WhatsApp Business API Implementation Plan for Aamcare

## Current Issues Identified

1. **Authentication Failure**: Twilio credentials are not working for API calls
2. **Sandbox Limitation**: Using Twilio Sandbox (+14155238886) which requires manual opt-in
3. **No Automatic Messaging**: Cannot send messages to users who haven't manually opted in

## Root Causes

1. **Credential Issue**: The provided credentials may be incorrect or expired
2. **Sandbox Restriction**: Twilio Sandbox only allows messaging to users who have manually sent "join" message
3. **Account Status**: The account may be in trial mode with restrictions

## Immediate Fix - Credential Verification

First, we need to verify and update the Twilio credentials:

### Step 1: Verify Current Credentials
```bash
# Check if credentials work with Twilio CLI (if installed)
twilio api:core:accounts:fetch --sid=ACcd8a206b626859f47e411bf8c8f67674
```

### Step 2: Update Settings (if credentials are wrong)
In `aamcare/settings.py`:
```python
# Update with correct credentials
TWILIO_ACCOUNT_SID = 'YOUR_CORRECT_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_CORRECT_AUTH_TOKEN'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Keep Sandbox for now
```

## Long-term Solution - WhatsApp Business API Migration

### Phase 1: Account Upgrade
1. Upgrade Twilio account from Trial to Paid ($0-20/month)
2. This removes sandbox restrictions

### Phase 2: Get Local Nepal Number
1. Purchase a Nepal phone number (+977) through Twilio
2. Configure it for WhatsApp Business API

### Phase 3: Facebook Business Verification
1. Create Facebook Business Manager account
2. Complete WhatsApp Business registration through Facebook
3. Submit message templates for approval

## Temporary Workaround - Sandbox Opt-in Process

Until WhatsApp Business API is implemented, users must manually opt-in:

### For Each User:
1. Save +14155238886 as "Aamcare Health" in WhatsApp
2. Send "join aamcare" to that number
3. Only then will they receive messages

### Automate Opt-in Instructions:
Create a dashboard alert showing these instructions to users who haven't opted in yet.

## Implementation Steps

### 1. Fix Authentication Issue
```python
# In notifications.py, improve error handling:
def send_sms(to_number, message):
    try:
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', os.environ.get('TWILIO_ACCOUNT_SID'))
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', os.environ.get('TWILIO_AUTH_TOKEN'))
        from_number = getattr(settings, 'TWILIO_FROM_NUMBER', os.environ.get('TWILIO_FROM_NUMBER'))
        
        if not (account_sid and auth_token and from_number):
            raise Exception('Twilio credentials not set in environment or settings.')
            
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        return {'success': True, 'sid': message.sid}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### 2. Add Retry Logic
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def send_whatsapp_with_retry(client, from_, to, body):
    # Same as send_whatsapp but with retry logic
    pass
```

### 3. Implement User Opt-in Tracking
Add a field to user profiles to track WhatsApp opt-in status:
```python
# In models.py
class PregnantWomanProfile(models.Model):
    # ... existing fields ...
    whatsapp_opted_in = models.BooleanField(default=False)
    whatsapp_opt_in_date = models.DateTimeField(null=True, blank=True)
```

## Next Steps Recommendation

### Immediate (Today):
1. [ ] Verify Twilio credentials are correct
2. [ ] Manually opt-in all 4 users (rita, Sita Sharma, nita, sita)
3. [ ] Test message sending after opt-in

### Short-term (This Week):
1. [ ] Upgrade Twilio account from Trial to Paid
2. [ ] Begin Facebook Business verification process
3. [ ] Research Nepal phone numbers on Twilio

### Long-term (This Month):
1. [ ] Complete WhatsApp Business API migration
2. [ ] Get local Nepal phone number
3. [ ] Submit message templates for approval

## Benefits of WhatsApp Business API

1. **No Manual Opt-in**: Message all users automatically
2. **Local Number**: Use +977 Nepal number for better recognition
3. **Professional Branding**: Official business messaging
4. **Unlimited Scale**: Support thousands/millions of users
5. **Higher Delivery Rates**: Better message deliverability

## Cost Estimation

### Twilio Costs (Monthly):
- Account Fee: $0-20 (depends on plan)
- WhatsApp Messages: $0.005-0.01 per message
- Nepal Number: $1-3/month
- Estimated Monthly Cost: $50-200 (for 10,000 messages)

## Support Contacts

### Twilio Support:
- Website: https://support.twilio.com
- Email: support@twilio.com

### Aamcare Development:
- Repository: https://github.com/AaSu9/Aamcare