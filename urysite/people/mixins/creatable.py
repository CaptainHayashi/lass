"""Mixin for items that track their creator."""

from django.db import models


class CreatableMixin(models.Model):
    """Mixin for items that track their creator.

    """

    class Meta:
        abstract = True

    creator = models.ForeignKey(
        'people.Creator',
        null=True,
        db_column='memberid',
        help_text='The person who created this item, if any.',
        related_name='created_%(app_label)s_%(class)s_set')
