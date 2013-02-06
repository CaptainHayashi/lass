"""
Temporary glue code for the old URY site blogs system.

"""

from metadata.models import Type
from django.db import models
from urysite import model_extensions as exts


class Blog(Type):
    """
    A blog in the old URY site blogs system.

    """
    id = exts.primary_key('blogid')
    rss_uri = models.TextField()
    blog_uri = models.TextField()

    class Meta(Type.Meta):
        db_table = 'blog'
        app_label = 'website'
