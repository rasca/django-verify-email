import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'verify_email',
    'verify_email.tests',
)

ROOT_URLCONF = 'verify_email.tests.urls'

DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

TEMPLATE_DIRS = (
    os.path.join(os.getcwd(), 'templates/'),
)
