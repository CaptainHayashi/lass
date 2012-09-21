"""A class representing a contiguous, linear chunk of programming,
and also containing various methods for extracting said chunks from
the schedule.

"""

from schedule.models import Timeslot
from schedule.utils import filler
from django.db.models import F
from datetime import timedelta
from django.utils import timezone


class ScheduleRange(object):
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

    def __repr__(self):
        """Returns a debug representation of the range."""
        return self.data.__repr__()

    def __getattr__(self, attr):
        """Ensures that any attempts to get an attribute that isn't
        in the Range class are sent to the data object it wraps.

        """
        return self.data.__getattr__(attr)

    @classmethod
    def between(cls,
                start,
                end,
                exclude_before_start=False,
                exclude_after_end=False,
                exclude_subsuming=False,
                with_filler_timeslots=True):
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
        with_filler_timeslots -- if True, gaps within the range will be
            filled with references to the filler pseudo-show
            (default: True)

        """
        # THIS IS NOT A TRIVIAL FUNCTION!

        # Start with ALL the timeslots (Django doesn't execute
        # database queries immediately so this is perfectly fine,
        # we'll be whittling this query down soon!
        timeslots = Timeslot.objects.all()

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
        if with_filler_timeslots:
            # Can't do add_filler_timeslots if this is a queryset
            # so force it to be a list
            timeslots = filler.fill(
                list(timeslots),
                start,
                end)

        # For all intents and purposes, this is just the queryset
        # with some added metadata on which range it actually
        # represents
        return cls(
            timeslots,
            start,
            end,
            exclude_before_start,
            exclude_after_end,
            exclude_subsuming,
            with_filler_timeslots)

    @classmethod
    def within(cls, date=None, offset=None, **keywords):
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
            date = timezone.now()
        if offset is None:  # Default to 0 (eg, get current show)
            offset = timedelta.timedelta(days=0)

        return cls.between(
            date,
            date + offset,
            **keywords)

    @classmethod
    def day(cls, date=None, **keywords):
        """Lists all schedule timeslots occurring between the given
        moment in time and the moment exactly one day after it.

        All keyword arguments beyond date (the aforementioned moment
        in time) are passed to 'timeslots_in_offset' unmolested; see
        that function's docstring for details on what the allowed
        arguments are.

        'date' defaults to the current moment in time.

        """
        return cls.within(
            date,
            timedelta(days=1),
            **keywords)

    @classmethod
    def week(cls, date=None, split_days=False, **keywords):
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
            result = [cls.day(
                date + timedelta(days=day),
                **keywords) for day in xrange(0, 7)]
        else:
            result = cls.within(
                date,
                timedelta(weeks=1),
                **keywords)
        return result
