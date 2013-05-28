"""
Example paths to the media and static locations on this copy of LASS.

"""

_BASE = '/path/to/content'


def path(subdir, topdir=_BASE):
    return '/'.join((topdir, subdir))

STATICFILES_DIRS = (
    path('static-in'),
)
TEMPLATE_DIRS = (
    path('templates'),
)

LOCALE_DIRS = (
    path('locale'),
)

SEARCH_INDEX_PATH = path('index')

MEDIA_ROOT = path('media/')
MEDIA_URL = '/media/'

STATIC_ROOT = path('static/')
STATIC_URL = '/static/'
