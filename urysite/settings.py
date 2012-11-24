"""
The master Django settings module for LASS.

Most of the settings that could change from site to site are imported
from an array of modules in the `urysite.private` package, which will
likely not exist in a fresh copy of LASS.  An example configuration
is provided in ``(project root)/urysite/examples/private``.

"""

import os
from urysite import django_apps, contrib_apps

## PRIVATE SETTINGS AREA ##
# Place site-specific settings in the modules imported here.
# They will be ignored by the standard gitignore.
from urysite.private import admin, debug, locale, content, key, sites
from urysite.private import database, cache, auth, middleware

PROJECT_ROOT = os.path.dirname(__file__)

## Settings defined in the private area ##
ADMINS = admin.ADMINS
MANAGERS = admin.MANAGERS
DEBUG = debug.DEBUG
TEMPLATE_DEBUG = debug.TEMPLATE_DEBUG
TIME_ZONE = locale.TIME_ZONE
LANGUAGE_CODE = locale.LANGUAGE_CODE
USE_I18N = locale.USE_I18N
USE_L10N = locale.USE_L10N
USE_TZ = locale.USE_TZ
SECRET_KEY = key.SECRET_KEY
SITE_ID = sites.SITE_ID
MEDIA_ROOT = content.MEDIA_ROOT
MEDIA_URL = content.MEDIA_URL
STATIC_ROOT = content.STATIC_ROOT
STATIC_URL = content.STATIC_URL
TEMPLATE_DIRS = content.TEMPLATE_DIRS
LOCALE_PATHS = content.LOCALE_DIRS
STATICFILES_DIRS = content.STATICFILES_DIRS
SEARCH_INDEX_PATH = content.SEARCH_INDEX_PATH

DATABASES = database.DATABASES

if hasattr(database, 'CREDIT_TYPE_DB_TABLE'):
    CREDIT_TYPE_DB_TABLE = database.CREDIT_TYPE_DB_TABLE
if hasattr(database, 'CREDIT_TYPE_DB_ID_COLUMN'):
    CREDIT_TYPE_DB_ID_COLUMN = database.CREDIT_TYPE_DB_ID_COLUMN
if hasattr(database, 'PERSON_DB_TABLE'):
    PERSON_DB_TABLE = database.PERSON_DB_TABLE
if hasattr(database, 'PERSON_DB_ID_COLUMN'):
    PERSON_DB_ID_COLUMN = database.PERSON_DB_ID_COLUMN

AUTHENTICATION_BACKENDS = auth.AUTHENTICATION_BACKENDS

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'zinnia.context_processors.version'
)

MIDDLEWARE_CLASSES = middleware.PRE_CLASSES
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
MIDDLEWARE_CLASSES += middleware.POST_CLASSES

ROOT_URLCONF = 'urysite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'urysite.wsgi.application'

INSTALLED_APPS = django_apps.INSTALLED_APPS
INSTALLED_APPS += contrib_apps.INSTALLED_APPS

INSTALLED_APPS += (
    ## LASS APPS ##
    'grid',
    'website',
    'people',
    'uryplayer',
    'schedule',
    'search',
    'getinvolved',
    'metadata',
    'music',
    'laconia',
)

##############
## HAYSTACK ##
##############

# Haystack 1 configuration
HAYSTACK_SITECONF = 'urysite.search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_XAPIAN_PATH = SEARCH_INDEX_PATH

# Use me for Haystack 2:
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
#        'PATH': os.path.join(PROJECT_ROOT, 'xapian_index'),
#    },
#}


#############
## LOGGING ##
#############

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

########
# LESS #
########

LESS_OUTPUT_DIR = 'LESS_CACHE'

##############
# COMPRESSOR #
##############

INTERNAL_IPS = ('127.0.0.1')

#########
# CACHE #
#########

CACHES = cache.CACHES

#################
# DEBUG TOOLBAR #
#################

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': debug.debug_toolbar_callback
}
