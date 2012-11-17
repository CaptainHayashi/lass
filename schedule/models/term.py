"""Models concerning URY terms."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts


class Term(models.Model):
    """
    A university term.

    Because University Radio York is a student radio station, its
    timetables are organised along University of York term
    boundaries.  This means that seasons are delineated by the
    terms that they cover, which are represented in the database
    using this model.

    """

    class Meta:
        db_table = 'terms'  # In public schema
        app_label = 'schedule'
        get_latest_by = 'start_date'

    def __unicode__(self):
        """
        Returns a human-readable representation of this term.

        The representation is of the form "NAME Term YEAR", where
        Name is Autumn, Spring or Summer and YEAR is the academic
        year in nnnn/nn+1 format, for example 2011/12.

        """
        year = self.academic_year()
        return u'{0} Term {1}/{2}'.format(
            self.name,
            year,
            (year + 1) % 100
        )

    def academic_year(self):
        """Returns the academic year of this term.

        """
        # Heuristic: if a term starts before September, then
        # it'll be the Spring or Summer of the academic year
        # that started the previous year.
        return (self.start_date.year
                if self.start_date.month >= 9
                else self.start_date.year - 1)

    id = exts.primary_key('termid')

    start_date = models.DateTimeField(
        db_column='start')

    end_date = models.DateTimeField(
        db_column='finish')

    name = models.CharField(
        max_length=10,
        db_column='descr')

    @classmethod
    def of(cls, date):
        """
        Returns the term of the given date, or None if the date
        does not lie in any known term.

        """
        query = cls.objects.filter(
            start_date__lte=date,
            end_date__gt=date
        )
        try:
            result = query.latest()
        except Term.DoesNotExist:
            result = None
        return result

    @classmethod
    def before(cls, date):
        """Assuming the given date does not belong in a term, returns
        the last term to occur before the date.

        This can be used to find out which holiday the date is in,
        if any.

        """
        query = cls.objects.filter(
            start_date__lte=date,
            end_date__lte=date
        )
        try:
            result = query.latest()
        except Term.DoesNotExist:
            result = None
        return result
