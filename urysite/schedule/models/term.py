"""Models concerning URY terms."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from datetime import datetime


class Term(models.Model):
    """An entry in the URY university terms set."""

    class Meta:
        db_table = 'terms'  # In public schema
        managed = False
        app_label = 'schedule'

    def __unicode__(self):
        return '{0} Term ({1} -> {2})'.format(
            self.name,
            datetime.date(self.start),
            datetime.date(self.end))

    id = exts.primary_key('termid')

    start = models.DateTimeField()

    end = models.DateTimeField(
        db_column='finish')

    name = models.CharField(
        max_length=10,
        db_column='descr')

    @classmethod
    def jukebox_term(cls):
        """Returns a fake term usable by Jukebox seasons."""
        return cls(
            start=datetime.fromtimestamp(0),
            end=datetime.fromtimestamp(0),
            name="Jukebox")
