# This is an example settings_local.py file.
# Copy it and add your local settings here.

# For absolute urls
DOMAIN = "127.0.0.1"
PROTOCOL = "http://"
PORT = 8000

SITE_URL = '%s%s:%d' % (PROTOCOL, DOMAIN, PORT)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mozillians.db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    },
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


#Serve Profile Photos from django
UPLOAD_URL = '/media/uploads'

# Statsd Defaults -- adjust as needed
STATSD_HOST = 'localhost'
STATSD_PORT = 8125
STATSD_PREFIX = 'mozillians'

## Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DEBUG = TEMPLATE_DEBUG = True

# ElasticSearch
ES_DISABLED = False
ES_HOSTS = ['127.0.0.1:9200']

CELERY_ALWAYS_EAGER = True

JAVA_BIN = '/usr/bin/java'

SESSION_COOKIE_SECURE = False

CACHES = {}

#STATSD_CLIENT = 'django_statsd.clients.log'

# Basket
BASKET_URL = None
BASKET_NEWSLETTER = 'mozilla-phone'
BASKET_MANAGERS = None # or list of email addresses.

import logging
logging.disable(logging.INFO)

GA_ACCOUNT_CODE = 'papari'
LESS_PREPROCESS = True
