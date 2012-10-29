"""
Example local administration settings for LASS.

"""

_DOMAIN = 'example.com'


def email(local, domain=_DOMAIN):
    return '@'.join((local, domain))


ADMINS = (
    (
        'Admin Person',
        email('admin.person')
    ),
    (
        'Webmaster',
        email('webmaster')
    )
)
MANAGERS = ADMINS
SERVER_EMAIL = email('lass-noreply')
