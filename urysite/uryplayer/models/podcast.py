# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from metadata.models import Metadata
from urysite import model_extensions as exts
from people.models import Person
from metadata.mixins import MetadataSubjectMixin
from metadata.mixins import SubmittableMixin
from people.mixins import CreditableMixin


class Podcast(MetadataSubjectMixin,
              SubmittableMixin,
              CreditableMixin):
    """A podcast in the URY player.

    """

    class Meta:
        db_table = 'podcast'  # in schema "uryplayer"
        ordering = ['-date_submitted']
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    people = models.ManyToManyField(
        Person,
        through='PodcastCredit')

    ## MAGIC METHODS ##

    def __unicode__(self):
        return '%s (%s)' % (self.title(), self.id)

    ## OVERRIDES ##

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_detail', [str(self.id)])

    def metadata_set(self):
        return self.podcastmetadata_set

    def credits_set(self):
        return self.podcastcredit_set

    ## ADDITIONAL METHODS ##

    @staticmethod
    def make_foreign_key(src_meta, db_column='podcast_id'):
        """Shortcut for creating a field that links to a podcast, given the
        source model's metadata class.

        """
        return exts.foreign_key(src_meta, 'Podcast', db_column, 'podcast')


class PodcastMetadata(Metadata):
    """An item of textual podcast metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'podcast_metadata'  # in schema 'schedule'
        verbose_name = 'podcast metadatum'
        verbose_name_plural = 'podcast metadata'
        app_label = 'uryplayer'

    def attached_element(self):
        return self.podcast

    id = exts.primary_key_from_meta(Meta)

    podcast = Podcast.make_foreign_key(Meta)
