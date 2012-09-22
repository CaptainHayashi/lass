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
        get_latest_by = 'start'

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
    def of(cls, date):
        """Returns the term of the given date, or None if the date
        does not lie in any known term.

        """
        query = cls.objects.filter(
            start__lte=date,
            end__gt=date)
        return query.latest() if query.exists() else None

    @classmethod
    def before(cls, date):
        """Assuming the given date does not belong in a term, returns
        the last term to occur before the date.

        This can be used to find out which holiday the date is in,
        if any.

        """
        query = cls.objects.filter(
            start__lte=date,
            end__lte=date)
        return query.latest() if query.exists() else None
