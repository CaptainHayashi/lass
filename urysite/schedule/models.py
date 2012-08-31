"""Models for the URY schedule.

Except where explicitly stated otherwise, the database tables in
this module are in the 'schedule' schema in URY.

"""

from datetime import datetime
from django.db import models
from people.models import Person
from urysite import model_extensions as exts
import timedelta


####################
## Person proxies ##
####################

# These two models are used to make the case where multiple people
# are associated with a model (in different ways- for example creator
# of a data item, approver of that item, etc) less ambiguous.


class Creator(Person):
    """A creator of show data."""
    class Meta:
        proxy = True


class Approver(Person):
    """A person who has approved a schedule change."""
    class Meta:
        proxy = True


#################################
## Schedule entity ABCs/mixins ## 
#################################

class ScheduleEntity(models.Model):
    """Abstract class for all creatable schedule entities.

    This class captures the common features of all creatable
    schedule entities, namely the inclusion of creator and approver
    links.

    """

    class Meta:
        abstract = True

    # Override this when implementing this ABC
    entity_name = 'schedule entity'

    creator = models.ForeignKey(
        Creator,
        db_column='memberid',
        help_text='The creator of this %s.' % entity_name)

    approver = models.ForeignKey(
        Approver,
        null = True,
        db_column='approverid',
        help_text="""The approver of this %s.

        If not specified, the entity has not been approved.

        """ % entity_name)


class MetadataSubjectMixin(object):
    """Mixin granting the ability to access schedule metadata.

    """

    # Don't forget to override this! 
    def metadata_set(self):
        """Returns the QuerySet that provides the metadata.

        This should invariably be overridden in mixin users.

        """
        pass

    def title(self):
        """Provides the current title of the show.

        The show title is extracted from the show metadata.

        """
        return self.current_metadatum('title')

    def description(self):
        """Provides the current description of the show.

        The show description is extracted from the show metadata.

        """
        return self.current_metadatum('description')

    def current_metadatum(self, key):
        """Retrieves the current value of the given metadata key.

        The current value is the most recently effected value that
        is approved and not in the future.

        """
        key_id = MetadataKey.objects.get(name=key).id
        return self.metadata_set().filter(
            metadata_key__pk=key_id).exclude(
            effective_from__gte=datetime.now()).order_by(
            '-effective_from').latest().metadata_value


###########
## Terms ##
###########

class Term(models.Model):
    """An entry in the URY university terms set."""

    class Meta:
        db_table = 'terms'  # In public schema
        managed = False

    def __unicode__(self):
        return '%s Term (%s -> %s)' % (self.name,
            self.start, self.end)

    id = exts.primary_key('termid')

    start = models.DateTimeField()

    end = models.DateTimeField(
        db_column='finish')

    name = models.CharField(
        max_length=20,
        db_column='descr')


###########
## Shows ##
###########

class ShowType(models.Model):
    """A type of show in the URY schedule.

    """

    class Meta:
        db_table = 'show_type'  # in schema "schedule"
        managed = False  # Can't manage, in non-public schema

    def __unicode__(self):
        return self.name


    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=30,
        db_column='name')

    public = models.BooleanField(
        default=True,
        db_column='public')


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

    def __unicode__(self):
        return '%s (%s)' % (self.title(), self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('show_detail', [str(self.id)])

    def metadata_set(self):
        return self.showmetadata_set
 
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

    @staticmethod
    def get_shows_for_day(day):
        """Retrieves a list of all shows that lie within a day."""


class Season(models.Model, MetadataSubjectMixin):
    """A season of a URY show.

    Seasons map onto terms of scheduled timeslots for a show. 

    """

    class Meta:
        db_table = 'show_season'  # In schema 'schedule'
        managed = False
        verbose_name = 'show season'

    def __unicode__(self):
        return '[%s] -> %s' % (self.show, self.term)

    def metadata_set(self):
        return self.seasonmetadata_set

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


##############
## Metadata ##
##############

class MetadataKey(models.Model):
    """A metadata key, which defines the semantics of a piece of 
    metadata.

    """

    class Meta:
        db_table = 'metadata_key'  # in schema 'schedule'
        managed = False

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=255,
        help_text="""A human-readable name for the metadata key.""")


class Metadata(models.Model):
    """An item of textual show metadata.

    """

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'effective_from'

    def __unicode__(self):
        """Returns a concise Unicode representation of the metadata.

        """
        return '%s -> %s (ef %s on %s)' % (self.metadata_key.name,
             self.metadata_value,
             self.effective_from,
             self.attached_element())

    def attached_element():
        """The element to which this metadatum is attached.

        This should be overridden in concrete models descending from
        Metadata.

        """
        pass

    # REMEMBER TO ADD THIS TO ANY DERIVING CLASSES!
    # id = exts.primary_key_from_meta(Meta)

    metadata_key = models.ForeignKey(
        MetadataKey,
        help_text="""The key, or type, of the metadata entry.""",
        db_column='metadata_key_id')


    metadata_value = models.TextField(
        help_text="""The value of this metadata entry.""")

    effective_from = models.DateTimeField(
        auto_now_add=True)

    creator = models.ForeignKey(
        Creator,
        help_text="""The person who created this metadata entry.""",
        db_column='memberid',
        related_name='%(app_label)s_%(class)s_created_set')

    approver = models.ForeignKey(
        'people.Person',
        help_text="""The person who approved this metadata entry,
            if it has indeed been approved.

            """,
        null=True,
        db_column='approvedid',
        related_name='%(app_label)s_%(class)s_approved_set')


class ShowMetadata(Metadata):
    """An item of textual show metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'show_metadata'  # in schema 'schedule'
        verbose_name='show metadatum'
        verbose_name_plural='show metadata'

    def attached_element():
        return show

    id = exts.primary_key_from_meta(Meta)

    show = Show.make_foreign_key(Meta) 


class SeasonMetadata(Metadata):
    """An item of textual season metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'season_metadata'  # in schema 'schedule'
        verbose_name='season metadatum'
        verbose_name_plural='season metadata'

    def attached_element():
        return season

    id = exts.primary_key_from_meta(Meta)

    season = Season.make_foreign_key(Meta) 

   
class ShowCreditType(models.Model):
    """A type of show credit, as used in ShowCredit.

    Types of show credit might include "presenter", "director",
    "reporter" and so on.

    """

    class Meta:
        db_table = 'show_credit_type'  # in schema 'schedule'
        managed = False  # have to do this due to schema, probably

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=255,
        help_text='Human-readable, singular name for the type.')

    plural = models.CharField(
        max_length=255,
        help_text='Human readable plural for the type.')

    # More to come here eventually


class ShowCredit(models.Model):
    """The intermediate model for the Show<->Person relationship.

    The rationale for the naming is that a ShowCredit is a "credit"
    (in the "film credits" sense) for a person's role on a given
    show.

    """

    class Meta:
        db_table = 'show_credit'  # In schema "schedule"
        managed = False  # Can't manage, in non-public schema

        ordering = ['credit_type__name']

    def __unicode__(self):
        return self.person.full_name()


    id = exts.primary_key_from_meta(Meta)

    show = models.ForeignKey(
        Show,
        db_column='show_id',
        help_text='The show that the person is being credited for.')

    person = models.ForeignKey(
        Person,
        db_column='creditid',
        help_text='The person being credited for working on a show.',
        related_name='credits_set')

    creator = models.ForeignKey(
        Creator,
        db_column='memberid',
        help_text='The person who created the credit.',
        related_name='created_credits_set')

    credit_type = models.ForeignKey(
        ShowCreditType,
        db_column='credit_type_id',
        help_text='The type of credit the person is assigned.')


class Timeslot(models.Model):
    """A slot in the URY schedule allocated to a show.

    URY timeslots can overlap, because not all timeslots represent
    on-air shows (the schedule system is used to schedule demos,
    in-studio recordings, and outside broadcasts as well as in-studio
    shows).  Because of this, a timeslot CANNOT safely be uniquely
    identified from its show and time range - use the timeslot ID.
    """

    class Meta:
        db_table = 'show_season_timeslot'
        managed = False
        verbose_name = 'show timeslot'


    id = exts.primary_key_from_meta(Meta)

    season = Season.make_foreign_key(Meta)

    start_time = models.DateTimeField(
        db_column='start_time',
        help_text='The date and time of the start of this timeslot.')

    duration = timedelta.TimedeltaField(
        db_column='duration',
        help_text='The duration of the timeslot.')

    def end_time(self):
        """Calculates the end time of this timeslot."""
        return self.start_time + self.duration 

############
## BLOCKS ##
############

class Block(models.Model):
    """A block of programming.

    Schedule blocks group together related shows, such as specialist
    music and flagship blocks, by time or by common naming
    conventions.

    """

    class Meta:
        db_table = 'block'  # In schema 'schedule'
        managed = False  # It's in another schema, so can't manage
        ordering = ('priority',)

    def __unicode__(self):
        return self.name


    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=255,
        help_text='The publicly viewable name for this block.')

    tag = models.CharField(
        max_length=100,
        help_text="""The machine-readable string identifier used, for
            example, as the prefix of the CSS classes used to colour
            this block.

            """)

    priority = models.IntegerField(
        help_text="""The priority of this block when deciding which
            block a show falls into.

            A lower number indicates a higher priority.

            """) 

    is_listable = models.BooleanField(
        default=False,
        help_text="""If true, the block appears in lists of blocks,
            allowing people to find shows in that block.

            """)


# Block matching rules #


class BlockNameRule(models.Model):
    """A name-based matching rule for blocks.

    A block matching rule that matches shows whose names match the
    given regular expression.

    """

    class Meta:
        db_table = 'block_name_rule'  # In schema 'schedule'
        managed = False  # It's in another schema, so can't manage

    def __unicode__(self):
        return "%s -> %s" % (self.regex, self.block)


    id = exts.primary_key_from_meta(Meta)

    block = models.ForeignKey(
        Block,
        help_text='The block this rule matches against.')

    regex = models.CharField(
        max_length=255,
        help_text="""The Perl-compatible regular expression that
            show names must match in order to match this block.

        """)


class BlockShowRule(models.Model):
    """A show-based matching rule for blocks.

    A block matching rule that matches the attached show only.

    This rule takes precedence over all other rules, except any
    directly matching timeslots.

    """

    class Meta:
        db_table = 'block_show_rule'  # In schema 'schedule'
        managed = False  # It's in another schema, so can't manage

    def __unicode__(self):
        return "%s -> %s" % (self.show, self.block)


    id = exts.primary_key_from_meta(Meta)

    block = models.ForeignKey(
        Block,
        help_text='The block this rule matches against.')

    show = models.ForeignKey(
        Show,
        help_text='The show this rule assigns a block to.')
