from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_ANALYTICS_TRACKING_ID': settings.GOOGLE_ANALYTICS_TRACKING_ID,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL
    }