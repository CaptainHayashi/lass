"""
The master Django settings module for LASS.

Most of the settings that could change from site to site are imported
from an array of modules in the `urysite.private` package, which will
likely not exist in a fresh copy of LASS.  An example configuration
is provided in ``(project root)/urysite/examples/private``.

"""

import os
import yaml

from glob import glob
from urysite import django_apps, contrib_apps


PROOT = os.path.dirname(__file__)


######################################################################
## OVERRIDABLE BLOCK

## LOGGING

# Defaults for overridable settings
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend'
)
MIDDLEWARE_PRE_CLASSES = []
MIDDLEWARE_POST_CLASSES = []
SEARCH_INDEX_PATH = None
INTERNAL_IPS = ('127.0.0.1')

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

# Import in private settings
for fname in sorted(glob(os.path.join(PROOT, 'private', '*.yml'))):
    try:
        with open(fname) as f:
            globals().update(yaml.load(f.read()))
    except IOError:
        pass

# Slightly hacky method of allowing the settings file to specify it
# wants to get its database configuration programmatically.
if globals().get('DATABASES', None) == 'use-external':
    from urysite.private import database
    DATABASES = database.DATABASES

######################################################################
## NON-OVERRIDABLE BLOCK


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'website.context.broadcast_info',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_PRE_CLASSES

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE_CLASSES += MIDDLEWARE_POST_CLASSES

ROOT_URLCONF = 'urysite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'urysite.wsgi.application'

INSTALLED_APPS = django_apps.INSTALLED_APPS
INSTALLED_APPS += contrib_apps.INSTALLED_APPS

INSTALLED_APPS += (
    ## LASS APPS ##
    'lass_utils',
    'people',
    'uryplayer',
    'schedule',
    'search',
    'getinvolved',
    'metadata',
    'music',
    'laconia',
    'grid',
    'website',
)

##############
## HAYSTACK ##
##############

# Haystack 1 configuration

# Use me for Haystack 2:
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
#        'PATH': os.path.join(PROOT, 'xapian_index'),
#    },
#}
