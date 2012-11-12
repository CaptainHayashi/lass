"""Models concerning URY schedule timeslots."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from django.utils import timezone
from datetime import timedelta as td
from django.db.models import F, Q
import timedelta
from schedule.models import BlockRangeRule
from schedule.models import ShowLocation
from schedule.models import Season
from metadata.models import Metadata
from metadata.mixins import MetadataSubjectMixin
from metadata.mixins import DateRangeMixin
from people.mixins import ApprovableMixin
from people.mixins import CreditableMixin
from people.mixins import CreatableMixin


class Timeslot(MetadataSubjectMixin,
               CreatableMixin,
               ApprovableMixin,
               CreditableMixin,
               DateRangeMixin):
    """
    A slot in the URY schedule allocated to a show.

    URY timeslots can overlap, because not all timeslots represent
    on-air shows (the schedule system is used to schedule demos,
    in-studio recordings, and outside broadcasts as well as in-studio
    shows).  Because of this, a timeslot CANNOT safely be uniquely
    identified from its show and time range - use the timeslot ID.

    """

    class Meta:
        db_table = 'show_season_timeslot'
        verbose_name = 'show timeslot'
        get_latest_by = 'start_time'
        ordering = ['start_time']
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    season = Season.make_foreign_key(Meta)

    start_time = models.DateTimeField(
        db_column='start_time',
        help_text='The date and time of the start of this timeslot.')

    duration = timedelta.TimedeltaField(
        db_column='duration',
        default='1:00:00',
        help_text='The duration of the timeslot.')

    ## MAGIC METHODS ##

    def __unicode__(self):
        """Provides a Unicode representation of this timeslot."""
        return u'{0} ({1} to {2})'.format(
            self.season,
            self.start_time,
            self.end_time())

    ## OVERRIDES ##

    # MetadataSubjectMixin

    def metadata_strands(self):
        """Provides the sets of this timeslot's metadata."""
        return {
            'text': self.timeslotmetadata_set
        }

    def metadata_parent(self):
        """Provides the metadata inheritance parent of this timeslot.

        """
        return self.season

    # CreditableMixin

    def credits_set(self):
        """Provides the set of this timeslot's credits."""
        return self.season.credits_set()

    # DateRangeMixin

    def range_start(self):
        """Retrieves the start of this timeslot's date range."""
        return self.start_time

    def range_end(self):
        """Retrieves the end of this timeslot's date range."""
        return self.end_time()

    def range_duration(self):
        """Retrieves the duration of this timeslot's date range."""
        return self.duration

    @classmethod
    def range_start_filter_arg(cls, inequality, value):
        """Given a filter inequality and a value to compare against,
        returns a tuple of the keyword argument and value that can
        be used to represent that inequality against the range start
        time in a filter.

        """
        return u'start_time__{0}'.format(inequality), value

    @classmethod
    def range_end_filter_arg(cls, inequality, value):
        """Given a filter inequality and a value to compare against,
        returns a tuple of the keyword argument and value that can
        be used to represent that inequality against the range end
        time in a filter.

        """
        return (u'duration__{0}'.format(inequality),
                value - F('start_time'))

    # Model

    @models.permalink
    def get_absolute_url(self):
        """Retrieves the absolute URL through which a timeslot can be
        found on the website.

        """
        return ('timeslot_detail', (), {
            'pk': self.season.show.id,
            'season_num': self.season.number(),
            'timeslot_num': self.number()})

    ## ADDITIONAL METHODS ##

    def can_be_messaged(self):
        """
        Returns whether this timeslot is messagable via the website.

        """
        return self.show_type().can_be_messaged

    def show_type(self):
        """Shortcut to return the type of the show this timeslot is
        attached to.

        """
        return self.season.show.show_type

    def location(self):
        """Returns the location the timeslot was broadcasted from.

        If no location is on file for the timeslot's time, None is
        returned.

        """
        locations = ShowLocation.at(
            self.start_time,
            queryset=self.season.show.showlocation_set.all())
        return (locations.latest().location
                if locations.exists()
                else None)

    def block(self):
        """Returns the block that the timeslot is in, if any.

        This will return a Block object if a block is matched, or
        None if there wasn't one (one can associate to Block.default()
        in this case, if a block is needed).

        """
        # Season rules take precedence
        season_block = self.season.block()
        if season_block is None:
            # TODO: add direct rules for timeslot
            # Now do season based checks
            #block_show_matches = self.blockshowrule_set.filter(
            #    show=self).order_by('-priority')
            #if block_show_matches.exists():
            #block = block_show_matches[0]
            #else:
            # TODO: add time-range rules for timeslot

            # Get start as distance from midnight, and end as
            # distance plus duration
            slot_start = self.start_time - self.start_time.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0)
            slot_end = slot_start + self.duration
            assert slot_start < slot_end, "Slot starts after end."

            # Because the block range is in local time and the slot
            # dates are in UTC, we'll need to subtract the local
            # time's UTC offset in the calculations.
            utc = self.start_time.astimezone(
                timezone.get_current_timezone()).utcoffset()
            day = td(days=1)

            # Now we can do simple inequalities to match the
            # time-ranges, with the caveat that we'll have to check
            # against the slot projected forwards one day to make
            # sure that ranges starting the day before the show and
            # ending on the day of the show are considered correctly.
            block_range_matches = BlockRangeRule.objects.filter(
                Q(start_time__lte=slot_start + utc,
                  end_time__gte=slot_end + utc) |
                Q(start_time__lte=slot_start + utc + day,
                  end_time__gte=slot_end + utc + day)).order_by(
                      '-block__priority')
            block = (block_range_matches[0].block
                     if block_range_matches
                     else None)
        else:
            block = season_block
        return block

    def end_time(self):
        """Calculates the end time of this timeslot."""
        return self.start_time + self.duration

    def number(self):
        """Returns the relative number of this timeslot, with the
        first timeslot of the attached season returning a number of 1.

        """
        number = None
        for index, timeslot in enumerate(self.season.timeslot_set.all()):
            if timeslot.id == self.id:
                number = index + 1  # Note that this can never be 0
                break
        assert number, "Timeslot not in its season's timeslot set."
        return number

    @staticmethod
    def make_foreign_key(src_meta,
                         db_column='show_season_timeslot_id'):
        """Shortcut for creating a field that links to a timeslot,
        given the source model's metadata class.

        """
        return exts.foreign_key(
            src_meta,
            'Timeslot',
            db_column,
            'timeslot')


class TimeslotMetadata(Metadata):
    """An item of textual Timeslot metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'timeslot_metadata'  # in schema 'schedule'
        verbose_name = 'timeslot metadatum'
        verbose_name_plural = 'timeslot metadata'
        app_label = 'schedule'

    id = exts.primary_key_from_meta(Meta)

    element = Timeslot.make_foreign_key(Meta)
