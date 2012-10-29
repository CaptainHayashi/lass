"""
Sample local debug settings for LASS.

"""

DEBUG = True
TEMPLATE_DEBUG = DEBUG


def debug_toolbar_callback(request):
    """
    The callback used to decide whether or not to show the debug
    toolbar.

    """
    return (
        DEBUG
        and request.META['SERVER_PORT'] == '8000'
    )
