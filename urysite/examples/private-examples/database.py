"""
Sample database settings for LASS.

"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.psycopg2',
        'NAME': 'blah',
        'USER': 'a_user',
        'PASSWORD': 'a_password',
        'HOST': 'database.example.com',
        'PORT': '1350',
    }
}
