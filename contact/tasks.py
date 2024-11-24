from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_contact_email(name, email, message):
    try:
        send_mail(
            subject=f'New Contact from {name}',
            message=f"Message:\n{message}\n\nEmail: {email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending email: {e}")
