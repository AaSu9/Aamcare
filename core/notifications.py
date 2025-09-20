import os
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

def send_sms(to_number, message):
    # These should be set in your environment or Django settings
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', os.environ.get('TWILIO_ACCOUNT_SID'))
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', os.environ.get('TWILIO_AUTH_TOKEN'))
    from_number = getattr(settings, 'TWILIO_FROM_NUMBER', os.environ.get('TWILIO_FROM_NUMBER'))
    if not (account_sid and auth_token and from_number):
        raise Exception('Twilio credentials not set in environment or settings.')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

def send_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@aamcare.np'),
        [to_email],
        fail_silently=False,
    ) 