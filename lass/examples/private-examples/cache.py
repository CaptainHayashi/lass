"""
Example caching setup for LASS.

DO NOT PUT THESE IN A PUBLIC GIT REPOSITORY!

"""

_DEFAULT = {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
}

CACHES = {
    'default': _DEFAULT,
}
