"""Models concerning URY schedule timeslots."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from schedule.models import BlockRangeRule
from schedule.models.season import Season
from schedule.models.metadata import Metadata, MetadataSubjectMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timedelta as td
from django.db.models import F, Q
import timedelta


class Range(object):
    """Class of the result of timeslots-in-range queries.

    Range is a thin wrapper around a QuerySet containing
    timeslot results that includes information about the start
    of the range, the end of the range, and which parameters were
    used in the making of the range.

    """
    def __init__(self,
                 data,
                 start,
                 end,
                 exclude_before_start=False,
                 exclude_after_end=False,
                 exclude_subsuming=False,
                 with_jukebox_entries=True):
        self.data = data
        self.start = start
        self.end = end
        self.timespan = end - start
        self.exclude_before_start = exclude_before_start
        self.exclude_after_end = exclude_after_end
        self.exclude_subsuming = exclude_subsuming
        self.with_jukebox_entries = with_jukebox_entries

    def __getattr__(self, attr):
        """Ensures that any attempts to get an attribute that isn't
        in the Range class are sent to the data object it wraps.

        """
        return self.data.__getattr__(attr)


class Timeslot(models.Model, MetadataSubjectMixin):
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
        get_latest_by = 'start_time'
        app_label = 'schedule'

    def metadata_set(self):
        """Provides the set of this timeslot's metadata."""
        return self.timeslotmetadata_set

    def metadata_parent(self):
        """Provides the metadata inheritance parent of this timeslot.

        """
        return self.season

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

            # Now we can do simple inequalities to match the
            # time-ranges, with the caveat that we'll have to check
            # against the slot projected forwards one day to make
            # sure that ranges starting the day before the show and
            # ending on the day of the show are considered correctly.
            block_range_matches = BlockRangeRule.objects.filter(
                Q(start_time__lte=slot_start,
                  end_time__gte=slot_end) |
                Q(start_time__lte=slot_start + td(days=1),
                  end_time__gte=slot_end + td(days=1))).order_by(
                      '-block__priority')
            if block_range_matches.exists():
                block = block_range_matches[0].block
            else:
                block = None
        else:
            block = season_block
        return block

    def __unicode__(self):
        """Provides a Unicode representation of this timeslot."""
        return "%s (%s to %s)" % (
            self.season,
            self.start_time,
            self.end_time())

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

    def by_line(self):
        """Returns a by-line for the timeslot (see Show.by_line for
        details).

        """
        return self.season.show.by_line(self.start_time)

    @classmethod
    def jukebox_entry(cls,
                      start_time,
                      end_time=None,
                      duration=None):
        """Creates a new timeslot that is bound to the URY Jukebox.

        """
        if duration is None:
            if end_time is None:
                raise ValueError('Specify end or duration.')
            else:
                duration = end_time - start_time
        elif end_time is not None:
            raise ValueError('Do not specify both end and duration.')

        return cls(
            season=Season.jukebox_season(),
            start_time=start_time,
            duration=duration)

    @classmethod
    def add_jukebox_entries(cls,
                            timeslots,
                            start,
                            end):
        """Fills any gaps in the given timeslot list with phantom
        "URY Jukebox" timeslots, such that the list is fully
        populated from the given start time to the given end time.

        Keyword arguments:
        timeslots -- the list of timeslots, may be empty
        start -- the start date/time
        end -- the end date/time"""
        if len(timeslots) == 0:
            timeslots = [cls.jukebox_entry(start, end)]
        else:
            # Start by filling in the ends
            if timeslots[0].start_time > start:
                timeslots.insert(
                    0,
                    cls.jukebox_entry(
                        start,
                        timeslots[0].start_time))
            if timeslots[-1].end_time() < end:
                timeslots.append(
                    cls.jukebox_entry(
                        timeslots[-1].end_time(),
                        end))
            # Next, fill in everything else
            # We're doing this by comparing two shows at a time to
            # see if they follow on from each other; if they don't
            # then we add a Jukebox in between them and make sure
            # the list indices we use reflect the growing list
            offset = 0
            for i in xrange(len(timeslots) - 1):
                left = timeslots[i + offset]
                right = timeslots[i + offset + 1]
                if left.end_time() < right.start_time:
                    timeslots.insert(
                        i + offset + 1,
                        cls.jukebox_entry(
                            left.end_time(),
                            right.start_time))
                    # The list has grown by one, so we'll need to
                    # factor that into the index calculations
                    offset += 1
        return timeslots

    @classmethod
    def timeslots_in_range(cls,
                           start,
                           end,
                           exclude_before_start=False,
                           exclude_after_end=False,
                           exclude_subsuming=False,
                           with_jukebox_entries=True):
        """Returns all the timeslots within a range defined by two
        datetime objects.

        Keyword arguments:
        start -- the start of the range, as a datetime
        end -- the end of the range, as a datetime
        exclude_before_start -- if True, the list will exclude all
            shows that start before the range, but end within it
            (default: False)
        exclude_after_end -- if True, the list will exclude all shows
            that start within the range, but end after it
            (default: False)
        exclude_subsuming -- if True, the list will exclude all shows
            that start before, but end after, the range (that is,
            they "subsume" the range)
            (default: False)
        with_jukebox_entries -- if True, gaps within the range will be
            filled with references to the URY Jukebox pseudo-show
            (default: True)

        """
        # THIS IS NOT A TRIVIAL FUNCTION!

        # We need the dates to be "timezone aware", because otherwise
        # Bad Things happen (the datetime stuff we'll be comparing
        # against is all timezone aware)
        start = timezone.make_aware(
            start,
            timezone.get_default_timezone())
        end = timezone.make_aware(
            end,
            timezone.get_default_timezone())

        # Start with ALL the timeslots (Django doesn't execute
        # database queries immediately so this is perfectly fine,
        # we'll be whittling this query down soon!
        timeslots = cls.objects.all()

        # ADVICE: Whenever you see an inequality on duration, just
        # mentally move the subtraction of 'start_time' over to
        # an addition on the other end, and replace duration +
        # start_time with end_time.  That should make sense hopefully

        # (this is because the model doesn't store end times in the
        # database)

        # Get rid of shows that start and end before the range
        # (diagrammatically, ##|  |  )
        timeslots = timeslots.exclude(
            start_time__lt=start,
            duration__lte=start - F('start_time')
        )
        # And start and end after the range
        # (diagrammatically,   |  |##)
        timeslots = timeslots.exclude(
            start_time__gte=end,
            duration__gt=end - F('start_time')
        )

        # This leaves:
        #   1) Shows that start and end inside the range
        #      - these will always be returned
        #        (diagrammatically,   |##|  )
        #   2) Shows that start before but end inside the range
        #      - these will be returned if exclude_before_start=False
        #        (diagrammatically, ##|##|  )
        #   3) Shows that start inside but end after the range
        #      - these will be returned if exclude_after_end=False
        #        (diagrammatically,   |##|##)
        #   4) Shows that completely subsume the range
        #      - these will be returned if exclude_subsuming=False
        #        (diagrammatically, ##|##|##)
        if exclude_before_start:  # 1)
            timeslots = timeslots.exclude(
                start_time__lt=start,
                duration__lte=end - F('start_time'))

        if exclude_after_end:  # 2)
            timeslots = timeslots.exclude(
                start_time__gte=start,
                duration__gt=end - F('start_time'))

        if exclude_subsuming:  # 3)
            timeslots = timeslots.exclude(
                start_time__lt=start,
                duration__gt=end - F('start_time'))

        # Of course, we want some form of ordering
        timeslots = timeslots.order_by("start_time")

        # And jukebox filling
        if with_jukebox_entries:
            # Can't do add_jukebox_entries if this is a queryset
            # so force it to be a list
            timeslots = cls.add_jukebox_entries(
                list(timeslots),
                start,
                end)

        # For all intents and purposes, this is just the queryset
        # with some added metadata on which range it actually
        # represents
        return Range(
            timeslots,
            start,
            end,
            exclude_before_start,
            exclude_after_end,
            exclude_subsuming,
            with_jukebox_entries)

    @classmethod
    def timeslots_in_offset(cls, date=None, offset=None, **keywords):
        """Lists all schedule timeslots occuring within a given
        duration of the given moment in time.

        That moment defaults to the current time.

        All keyword arguments beyond date (the aforementioned moment
        in time) and offset (the aforementioned time delta) are
        passed to 'timeslots_in_range' unmolested; see that
        function's docstring for details on what the allowed
        arguments are.

        """
        if date is None:
            date = datetime.now()
        if offset is None:  # Default to 0 (eg, get current show)
            offset = td.timedelta(days=0)

        return cls.timeslots_in_range(
            date,
            date + offset,
            **keywords)

    @classmethod
    def timeslots_in_day(cls, date=None, **keywords):
        """Lists all schedule timeslots occurring between the given
        moment in time and the moment exactly one day after it.

        All keyword arguments beyond date (the aforementioned moment
        in time) are passed to 'timeslots_in_offset' unmolested; see
        that function's docstring for details on what the allowed
        arguments are.

        'date' defaults to the current moment in time.

        """
        return cls.timeslots_in_offset(
            date,
            td(days=1),
            **keywords)

    @classmethod
    def timeslots_in_week(cls,
                          date=None,
                          split_days=False,
                          **keywords):
        """Lists all schedule timeslots occurring between the given
        moment in time and the moment exactly one week after it.

        All keyword arguments beyond date (the aforementioned moment
        in time) and split_days are passed to 'timeslots_in_offset'
        unmolested; see that function's docstring for details on what
        the allowed arguments are.

        If 'split_days' is True, the result will be equivalent to
        listing the result of 'timeslots_in_day' applied to each day
        of the week with the given arguments; otherwise the result
        will be 'timeslots_in_offset' where the offset is one week.

        'date' defaults to the current moment in time.

        """
        if split_days is True:
            result = map(
                lambda day: cls.timeslots_in_day(
                    date + td(days=day),
                    **keywords),
                xrange(0, 7))
        else:
            result = cls.timeslots_in_offset(
                date,
                td(weeks=1),
                **keywords)
        return result

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

    def attached_element():
        return timeslot

    id = exts.primary_key_from_meta(Meta)

    timeslot = Timeslot.make_foreign_key(Meta)
