"""Models concerning URY show seasons."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from schedule.models.term import Term
from schedule.models.show import Show
from schedule.models.metadata import Metadata, MetadataSubjectMixin
from datetime import datetime


class Season(models.Model, MetadataSubjectMixin):
    """A season of a URY show.

    Seasons map onto terms of scheduled timeslots for a show.

    """

    class Meta:
        db_table = 'show_season'  # In schema 'schedule'
        managed = False
        verbose_name = 'show season'
        app_label = 'schedule'

    def __unicode__(self):
        return '[%s] -> %s' % (self.show, self.term)

    def metadata_set(self):
        return self.seasonmetadata_set

    def metadata_parent(self):
        return self.show

    id = exts.primary_key_from_meta(Meta)

    show = models.ForeignKey(
        Show,
        db_column='show_id',
        help_text='The show associated with this season.')

    term = models.ForeignKey(
        Term,
        db_column='termid',
        help_text='The term this season is scheduled for.')

    date_submitted = models.DateTimeField(
        null=True,
        db_column='submitted',
        help_text='The date the season was submitted, if any.')

    @classmethod
    def jukebox_season(cls):
        """Returns the pseudo-season associated with URY Jukebox."""
        return cls(
            show=Show.objects.get(pk=-1),
            term=Term.jukebox_term(),
            date_submitted=datetime.fromtimestamp(0))


    @staticmethod
    def make_foreign_key(src_meta, db_column='show_season_id'):
        """Shortcut for creating a field that links to a season,
        given the source model's metadata class.

        """
        return exts.foreign_key(
            src_meta,
            'Season',
            db_column,
            'season')


class SeasonMetadata(Metadata):
    """An item of textual season metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'season_metadata'  # in schema 'schedule'
        verbose_name = 'season metadatum'
        verbose_name_plural = 'season metadata'
        app_label = 'schedule'

    def attached_element():
        return season

    id = exts.primary_key_from_meta(Meta)

    season = Season.make_foreign_key(Meta)


