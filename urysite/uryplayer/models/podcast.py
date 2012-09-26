# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from metadata.models import Metadata, MetadataSubjectMixin
from urysite import model_extensions as exts
from people.models import Person


class Podcast(models.Model, MetadataSubjectMixin):
    """A podcast in the URY player.

    """

    class Meta:
        db_table = 'podcast'  # in schema "uryplayer"
        ordering = ['-date_submitted']
        managed = False
        app_label = 'uryplayer'

    def __unicode__(self):
        return '%s (%s)' % (self.title(), self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_detail', [str(self.id)])

    def metadata_set(self):
        return self.podcastmetadata_set

    def credits_at(self, time):
        """Returns a list of all credits for people who worked on this
        podcast at the given instant in time.

        """
        # Why excludes?  Because effective_to might be NULL
        # and we don't want to throw away results where it is
        # as this entails indefinite effectiveness.
        return self.podcastcredit_set.exclude(
            effective_from__gt=time).exclude(
                effective_to__lt=time).exclude(
                    approver__isnull=True)

    def by_line(self, time):
        """Returns a by-line for the podcast- a human-readable summary
        of all the presenters, co-presenters and other important
        people who worked on the podcast at the given instant in time.

        The by-line does not include a 'with' or 'by' prefix.
        If nobody worked on the podcast, the empty string is returned.

        """
        credits = list(self.credits_at(time))
        if len(credits) == 0:
            by_line = ''
        elif len(credits) == 1:
            by_line = credits[0].person.full_name()
        else:
            by_line = u' and '.join((
                u', '.join(
                    map(
                        lambda x: x.person.full_name(),
                        credits[:-1])),
                credits[-1].person.full_name()))
        return by_line

    id = exts.primary_key_from_meta(Meta)

    date_submitted = models.DateTimeField(
        auto_now_add=True,
        db_column='submitted')

    people = models.ManyToManyField(
        Person,
        through='PodcastCredit')

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

    def attached_element():
        return podcast

    id = exts.primary_key_from_meta(Meta)

    podcast = Podcast.make_foreign_key(Meta)
