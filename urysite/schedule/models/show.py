"""Models concerning URY shows."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite.models.metadata import Metadata, MetadataSubjectMixin
from urysite import model_extensions as exts
from people.models import Person


class ShowType(models.Model):
    """A type of show in the URY schedule.

    """

    class Meta:
        db_table = 'show_type'  # in schema "schedule"
        managed = False  # Can't manage, in non-public schema
        app_label = 'schedule'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=30,
        db_column='name')

    public = models.BooleanField(
        default=True,
        db_column='public')

    is_real_show = models.BooleanField(
        default=True)


class Show(models.Model, MetadataSubjectMixin):
    """A show in the URY schedule.

    URY show objects represent the part of a show that is constant
    across any time-slots it is scheduled into: the show's type,
    creation date, credited people, and so on.

    """

    class Meta:
        db_table = 'show'  # in schema "schedule"
        ordering = ['show_type', '-date_submitted']
        managed = False
        app_label = 'schedule'

    def __unicode__(self):
        return '%s (%s)' % (self.title(), self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('show_detail', [str(self.id)])

    def metadata_set(self):
        return self.showmetadata_set

    def credits_at(self, time):
        """Returns a list of all credits for people who worked on this
        show at the given instant in time.

        """
        # Why excludes?  Because effective_to might be NULL
        # and we don't want to throw away results where it is
        # as this entails indefinite effectiveness.
        return self.showcredit_set.exclude(
            effective_from__gt=time).exclude(
                effective_to__lt=time).exclude(
                    approver__isnull=True)

    def by_line(self, time):
        """Returns a by-line for the show- a human-readable summary
        of all the presenters, co-presenters and other important
        people who worked on the show at the given instant in time.

        The by-line does not include a 'with' or 'by' prefix.
        If nobody worked on the show, the empty string is returned.

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

    def is_real_show(self):
        """Returns True if this show constitutes a "real show".

        A real show is technically any show whose type defines it
        to be; the flag denotes that the show constitutes an actually
        scheduled event and not an automatically created filler show
        such as URY Jukebox.

        """
        return self.show_type.is_real_show

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
        if (len(block_matches)) > 0:
            block = block_matches[0].block
        else:
            block = None
        return block

    id = exts.primary_key_from_meta(Meta)

    show_type = models.ForeignKey(
        ShowType,
        help_text="""The show type, which affects whether or not the
            show appears in the public schedule, amongst other things.
            """,
        db_column='show_type_id')

    date_submitted = models.DateTimeField(
        auto_now_add=True,
        db_column='submitted')

    people = models.ManyToManyField(
        Person,
        through='ShowCredit')

    @staticmethod
    def make_foreign_key(src_meta, db_column='show_id'):
        """Shortcut for creating a field that links to a show, given the
        source model's metadata class.

        """
        return exts.foreign_key(src_meta, 'Show', db_column, 'show')


class ShowMetadata(Metadata):
    """An item of textual show metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'show_metadata'  # in schema 'schedule'
        verbose_name = 'show metadatum'
        verbose_name_plural = 'show metadata'
        app_label = 'schedule'

    def attached_element():
        return show

    id = exts.primary_key_from_meta(Meta)

    show = Show.make_foreign_key(Meta)
