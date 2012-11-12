"""Models concerning URY shows."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

# All tables here, unless explicitly stated, are in the 'schedule'
# schema in URY.

from django.db import models
from urysite import model_extensions as exts
from metadata.models import Type
from metadata.models import Metadata
from people.models import Person
from uryplayer.models import PodcastLink
from metadata.mixins import MetadataSubjectMixin
from metadata.mixins import SubmittableMixin
from metadata.mixins import EffectiveRangeMixin
from people.mixins import ApprovableMixin
from people.mixins import CreatableMixin
from people.mixins import CreditableMixin
from schedule.models import Location


class ShowType(Type):
    """
    A type of show in the URY schedule.

    """

    class Meta(Type.Meta):
        db_table = 'show_type'  # in schema "schedule"
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    public = models.BooleanField(
        default=True)

    has_showdb_entry = models.BooleanField(
        default=True)

    can_be_messaged = models.BooleanField(
        default=False,
        help_text="""If this is True, then the show can be messaged
            through the main page message form.

            """)


class ShowLocation(EffectiveRangeMixin,
                   CreatableMixin,
                   ApprovableMixin):
    """
    A mapping of shows to their locations.

    """

    class Meta(EffectiveRangeMixin.Meta):
        db_table = 'show_location'
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    show = models.ForeignKey(
        'Show',
        db_column='show_id')

    location = models.ForeignKey(
        Location,
        db_column='location_id')


class Show(MetadataSubjectMixin,
           SubmittableMixin,
           CreatableMixin,
           CreditableMixin):
    """
    A show in the URY schedule.

    URY show objects represent the part of a show that is constant
    across any time-slots it is scheduled into: the show's type,
    creation date, credited people, and so on.

    """

    class Meta:
        db_table = 'show'  # in schema "schedule"
        ordering = ['show_type', '-date_submitted']
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    show_type = models.ForeignKey(
        ShowType,
        help_text="""The show type, which affects whether or not the
            show appears in the public schedule, amongst other things.
            """,
        db_column='show_type_id')

    people = models.ManyToManyField(
        Person,
        through='ShowCredit')

    locations = models.ManyToManyField(
        Location,
        through=ShowLocation)

    @staticmethod
    def make_foreign_key(src_meta, db_column='show_id'):
        """
        Shortcut for creating a field that links to a show, given the
        source model's metadata class.

        """
        return exts.foreign_key(src_meta, 'Show', db_column, 'show')

    ## OVERRIDES ##

    def __unicode__(self):
        return u'{0} ({1})'.format(self.title(), self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('show_detail', [str(self.id)])

    def metadata_strands(self):
        return {
            'text': self.showmetadata_set
        }

    def credits_set(self):
        return self.showcredit_set

    def block(self):
        """Returns the block that the show is in, if any.

        This will return a Block object if a block is matched, or
        None if there wasn't one (one can associate to Block.default()
        in this case, if a block is needed).

        For seasons and timeslots, use their block() methods instead
        so as to pull in season and timeslot specific matching rules.

        """
        # Show rules take precedence
        block_matches = self.blockshowrule_set.order_by(
            '-block__priority')
        if block_matches.exists():
            block = block_matches[0].block
        else:
            block = None
        return block


class ShowMetadata(Metadata):
    """An item of textual show metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'show_metadata'
        verbose_name = 'show metadatum'
        verbose_name_plural = 'show metadata'
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    element = Show.make_foreign_key(Meta)


class ShowPodcastLink(PodcastLink):
    """A link between a show and a podcast."""

    class Meta(PodcastLink.Meta):
        db_table = 'show_podcast_link'
        app_label = 'schedule'
