"""Mixin for items that must be approved before becoming usable."""

from django.db import models


class ApprovableMixin(models.Model):
    """Mixin for items that must be approved before becoming usable.

    """

    class Meta:
        abstract = True

    approver = models.ForeignKey(
        'people.Approver',
        null=True,
        blank=True,
        db_column='approvedid',
        help_text='The person who approved this item, if any.',
        related_name='approved_%(app_label)s_%(class)s_set')
