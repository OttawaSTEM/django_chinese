from django.conf import settings
from django.core.mail import send_mail

import logging
logger = logging.getLogger('project')

def SendEmail(subject, message, to=None, files=None):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.WEBMASTER_1, settings.WEBMASTER_2],
            fail_silently=False,
        )    
    except Exception as e:
        logger.info('Error - send_email: {} - '.format(e, subject))
        send_mail(
            f'Error - {subject}',
            message,
            settings.EMAIL_HOST_USER,
            [settings.WEBMASTER_1, settings.WEBMASTER_2],
            fail_silently=False,
        )    
