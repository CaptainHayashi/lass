"""Models concerning URY show seasons."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from schedule.models.term import Term
from schedule.models.show import Show
from metadata.models import Metadata
from metadata.mixins import MetadataSubjectMixin
from metadata.mixins import SubmittableMixin
from people.mixins import CreditableMixin


class Season(MetadataSubjectMixin,
             SubmittableMixin,
             CreditableMixin):
    """A season of a URY show.

    Seasons map onto terms of scheduled timeslots for a show.

    """

    class Meta:
        db_table = 'show_season'  # In schema 'schedule'
        verbose_name = 'show season'
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    show = models.ForeignKey(
        Show,
        db_column='show_id',
        help_text='The show associated with this season.')

    term = models.ForeignKey(
        Term,
        db_column='termid',
        help_text='The term this season is scheduled for.')

    ## MAGIC METHODS ##

    def __unicode__(self):
        return '[{0}] -> {1}'.format(self.show, self.term)

    ## OVERRIDES ##

    def metadata_set(self):
        return self.seasonmetadata_set

    def metadata_parent(self):
        return self.show

    def credits_set(self):
        """Provides the set of this season's credits."""
        return self.show.credits_set()

    @models.permalink
    def get_absolute_url(self):
        """Retrieves the absolute URL through which a timeslot can be
        found on the website.

        """
        return ('season_detail', (), {
            'pk': self.show.id,
            'season_num': self.number()})

    ## ADDITIONAL METHODS ##

    def number(self):
        """Returns the relative number of this season, with the first
        season of the attached show returning a number of 1.

        """
        number = None
        for index, season in enumerate(self.show.season_set.all()):
            if season.id == self.id:
                number = index + 1  # Note that this can never be 0
                break
        assert number, "Season not in its show's season set."
        return number

    def block(self):
        """Returns the block that the season is in, if any.

        This will return a Block object if a block is matched, or
        None if there wasn't one (one can associate to Block.default()
        in this case, if a block is needed).

        For timeslots, use their block() methods instead so as to pull
        in timeslot specific matching rules.

        """
        # Show rules take precedence
        show_block = self.show.block()
        if show_block is None:
            # TODO: add direct rules for season
            # Now do season based checks
            #block_show_matches = self.blockshowrule_set.filter(
            #    show=self).order_by('-priority')
            #if block_show_matches.exists():
            #block = block_show_matches[0]
            #else:
            block = None
        else:
            block = show_block
        return block

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

    id = exts.primary_key_from_meta(Meta)

    season = Season.make_foreign_key(Meta)

    ## OVERRIDES ##

    def attached_element(self):
        return self.season
