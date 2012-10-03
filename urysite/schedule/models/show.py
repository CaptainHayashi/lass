"""Models concerning URY shows."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from metadata.models import Metadata
from people.models import Person
from metadata.mixins import MetadataSubjectMixin
from metadata.mixins import SubmittableMixin
from people.mixins import CreditableMixin


class ShowType(models.Model):
    """A type of show in the URY schedule.

    """

    class Meta:
        db_table = 'show_type'  # in schema "schedule"
        app_label = 'schedule'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=30)

    public = models.BooleanField(
        default=True)

    has_showdb_entry = models.BooleanField(
        default=True)


class Show(MetadataSubjectMixin,
           SubmittableMixin,
           CreditableMixin):
    """A show in the URY schedule.

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

    @staticmethod
    def make_foreign_key(src_meta, db_column='show_id'):
        """Shortcut for creating a field that links to a show, given the
        source model's metadata class.

        """
        return exts.foreign_key(src_meta, 'Show', db_column, 'show')

    ## OVERRIDES ##

    def __unicode__(self):
        return '{0} ({1})'.format(self.title(), self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('show_detail', [str(self.id)])

    def metadata_set(self):
        return self.showmetadata_set

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
        db_table = 'show_metadata'  # in schema 'schedule'
        verbose_name = 'show metadatum'
        verbose_name_plural = 'show metadata'
        app_label = 'schedule'

    def attached_element(self):
        return self.show

    id = exts.primary_key_from_meta(Meta)

    show = Show.make_foreign_key(Meta)
