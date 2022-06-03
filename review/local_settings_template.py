import os

STATIC_URL = '/static/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # i.e. "../"

STATIC_ROOT = "/var/www/..." # unused for dev server, unless you run collectstatic
STATICFILES_DIRS = (os.path.join(BASE_DIR, "web/static/web"),)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/www/...',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '...'

ALLOWED_HOSTS = ['<FQDN>'] # can use ['*'] for development

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
