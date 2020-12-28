"""
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from django.urls import reverse_lazy
from os.path import dirname, join, exists, abspath

# Use 12factor inspired environment variables or from a file
import environ
env = environ.Env()

# Ideally move env file should be outside the git repo, i.e. BASE_DIR.parent.parent
env_file = join(dirname(__file__), 'local.env')
if exists(env_file):
    environ.Env.read_env(str(env_file))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# ALLOWED_HOSTS
ALLOWED_HOSTS = eval(env('ALLOWED_HOSTS'))

# Sitemaps
# Need to update database table: django_site manual from example.com to domain name, which match record ID=1
SITE_ID = 1
SITE_NAME = 'django_chinese'
SITE_URL = 'https://django_chinese.com/' 

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

# Local - Build paths inside the project like this: join(BASE_DIR, 'directory')
STATICFILES_FINDERS = (                                 # For Django-Compressor
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter', 
    'compressor.filters.cssmin.rCSSMinFilter'
]
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
COMPRESS_JS_FILTERS = [     # Only compress javascript in production
    'compressor.filters.jsmin.JSMinFilter'
]

# Define Local Server MEDIA_ROOT for User-uploaded files like profile pics need to be served
STATIC_URL = '/static/'                 # Local
MEDIA_URL = '/media/'                 # Local

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Use PBKDF2 algorithm with a SHA256 hash
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
# https://docs.djangoproject.com/en/3.0/topics/auth/passwords/#password-validation
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
# ]

# django-allauth settings
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of django-allauth
    'django.contrib.auth.backends.ModelBackend',

    # django-allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {
    'signup': 'django_chinese.forms.AllauthSignupForm',
    'login': 'django_chinese.forms.AllauthLoginForm',
    'reset_password': 'django_chinese.forms.AllauthResetPasswordForm',
    'reset_password_from_key': 'django_chinese.forms.AllauthResetPasswordKeyForm',
    'change_password': 'django_chinese.forms.AllauthChangePasswordForm',
    'set_password': 'django_chinese.forms.AllauthSetPasswordForm',
}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
LOGIN_REDIRECT_URL = reverse_lazy('profiles:show_self')     # Redirect after sign 
# LOGIN_REDIRECT_URL = '/'        
ACCOUNT_LOGOUT_ON_GET = True                                # Logout without confirm
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy('home')
ACCOUNT_SESSION_REMEMBER = True
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_PROVIDERS = dict
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_AUTH_CLIENT_ID'),
            'secret': env('GOOGLE_AUTH_SECRET'),
            'key': env('GOOGLE_AUTH_KEY'),
        }
    }
}

# Email Server Settings
EMAIL_CONFIG = env.email_url('EMAIL_URL', default='consolemail://')
if 'smtp' in EMAIL_CONFIG['EMAIL_BACKEND']:
    EMAIL_USE_TLS = EMAIL_CONFIG['EMAIL_USE_TLS']
    EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
    EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']
    EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD']
else:
    # For developing, email sent to console
    # Commen local.env "EMAIL_URL" to use console Email backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'     

WEBMASTER_1 = env('WEBMASTER_1')
WEBMASTER_2 = env('WEBMASTER_2')

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                
                # django-allauth needs this from django
                'django.template.context_processors.request',

                # global settings for templates. Need update django_chinese to project folder name
                'django_chinese.context_processors.global_settings',
            ],
        },
    },
]

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
  
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'compressor',
    'crispy_forms',
    'dbbackup',
    'captcha',

    'profiles',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'django_chinese.urls'
WSGI_APPLICATION = 'django_chinese.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db()
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

# Default data format: 2000-02-18
USE_L10N = False
DATE_FORMAT = 'Y年m月d'
DATETIME_FORMAT = 'Y年m月d日 H:i'
USE_I18N = True
USE_TZ = True
TIME_ZONE = 'Asia/Shanghai'


# Crispy Form Theme - Bootstrap 4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# For Bootstrap 4, change error alert to 'danger'
from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Google Analytics
GOOGLE_ANALYTICS_TRACKING_ID = env('GOOGLE_ANALYTICS_TRACKING_ID')
