import os, sys

if __name__ == "__main__":
    # CHANGED manage.py will use development settings by default. 
    # Change the DJANGO_SETTINGS_MODULE environment variable for using the environment specific settings file.
    if os.environ.get('DJANGO_DEVELOPMENT') == 'True':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chinese.settings.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chinese.settings.production')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

