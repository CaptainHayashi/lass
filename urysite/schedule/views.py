from django.shortcuts import render
from datetime import datetime, timedelta
from schedule.models import Timeslot


class ScheduleTable(object):
    """A weekly schedule, in tabular form and ready to be outputted
    in a template.

    """

    class Row(object):
        """A row in a schedule table."""
        class IncorrectlySizedRowException(Exception):
            """Exception thrown when an add operation that would make
            a row too large occurs, or when a read operation on a row
            that is insufficiently sized happens."""
            pass

        class Entry(object):
            """An entry in a schedule table row.
            
            Schedule table entries depict part of a show timeslot
            that airs inside the time period of its parent row.
            
            The booleans is_start and is_end state whether this entry
            marks the start and/or the end of the referenced show
            respectively.
            
            """
            def __init__(self, is_start, is_end):
                self.is_start = is_start
                self.is_end = is_end

        def __init__(self, time):
            self.time = time
            self.shows = []

        def add(self, show, is_start, is_end):
            if len(self.shows) == 7:
                # We don't want more than seven days!
                raise IncorrectlySizedRowException
            else:
                self.shows.append(Entry(show, is_start, is_end))

    @classmethod
    def tabulate_week_lists(cls, weeks, start_date):
        """Creates a schedule week table from a group of seven lists.

        You should generally use 'tabulate' instead of directly
        invoking this.

        """
        pass           

    @classmethod
    def tabulate(cls, range_list):
        """Creates a schedule week table.

        Keyword arguments:
        range_list -- the list of seven schedule ranges that
            constitute the schedule week to tabulate, as outputted by
            (for example) Timeslot.timeslots_in_week with split_days
            set to True

        """
        # Sanity check the data
        # The range needs to have very specific properties in order
        # for the schedule tabulator to work right now.
        if type(range_list) != list:
            raise ValueError(
                "Schedule table data list must be an actual list.")
        elif len(range_list) != 7:
            raise ValueError(
                """Schedule table data list must contain 7 ranges.
                Instead got {0} ranges""".format(len(range_list)))
        # Extract data while sanity checking
        range_list_pure = []
        for range_data in range_list:
            if range_data.with_jukebox_entries is False:
                raise ValueError(
                    "Schedule column data must include Jukebox.")
            elif range_data.timespan != timedelta(days=1):
                raise ValueError(
                    "Schedule column data must span one day each.")
            elif range_data.exclude_before_start:
                raise ValueError(
                    "Schedule column data must include-before-start.")
            elif range_data.exclude_after_end:
                raise ValueError(
                    "Schedule column data must include-after-end.")
            elif range_data.exclude_subsuming:
                raise ValueError(
                    "Schedule column data must include-subsuming.")
            range_list_pure.append(range_data.data)
        return cls.tabulate_week_lists(
            range_list_pure,
            range_list[0].start)

def get_week_day(year, week, day, ury_start_hour=7):
    """Given a year, a week number inside that year and a day number
    inside that day (from 1 to 7), finds the corresponding time
    period that represents the start of that URY day.

    See the C89 definition of strptime formats for details on how
    this function works.

    """
    # Note: the modulo 7 is to convert a day in the form 1-7 where
    # 1=Monday, 7=Sunday to the form 0-6 where 0=Sunday, 6=Saturday.
    # Why?  This is how strptime wants it, for some daft reason.
    day = int(day) % 7

    # If anyone can find an easier way of converting year/week to a
    # datetime, replace the following:
    week_start_str = '{0} {1} {2} {3}'.format(
        year, week, day, ury_start_hour)
    return datetime.strptime(week_start_str, '%Y %W %w %H')


def get_week_start(year, week):
    """Given a year and a week number inside that year, finds the
    date of the Monday of that week.

    See get_week_day for details on how this function works.

    """
    return get_week_day(year, week, 1)


def schedule_week_from_date(request, week_start):
    """The week-at-a-glance schedule view, with the week specified
    by a date object denoting its starting day.

    """
    next_start = week_start + timedelta(weeks=1)
    next_year, next_week, next_day = next_start.isocalendar()

    prev_start = week_start - timedelta(weeks=1)
    prev_year, prev_week, prev_day = prev_start.isocalendar()

    schedule = ScheduleTable.tabulate(
        Timeslot.timeslots_in_week(
            week_start,
            split_days=True,
            exclude_before_start=False,
            exclude_after_end=False,
            exclude_subsuming=False,
            with_jukebox_entries=True))

    return render(
        request,
        'schedule/schedule-week.html',
        {'week_start': week_start,
            'next_start': next_start,
            'next_year': next_year,
            'next_week': next_week,
            'prev_start': prev_start,
            'prev_year': prev_year,
            'prev_week': prev_week})


def to_monday(date):
    """Given a date, find the date of the Monday of its week."""
    days_after_monday = date.weekday()
    return date - timedelta(days=days_after_monday)


def index(request):
    """The view that gets brought up if you navigate to 'schedule'.

    Currently this just gets the weekly schedule for the current
    week.
    """
    return schedule_week_from_date(
        request,
        to_monday(datetime.today()))


def schedule_week(request, year, week):
    """The week-at-a-glance schedule view.

    """
    # WEEK STARTS
    return schedule_week_from_date(
        request, 
        get_week_start(year, week))

def schedule_day_from_date(request, day_start):
    """The week-at-a-glance schedule view, with the week specified
    by a date object denoting its starting day.

    """
    next_start = day_start + timedelta(days=1)
    next_year, next_week, next_day = next_start.isocalendar()

    prev_start = day_start - timedelta(days=1)
    prev_year, prev_week, prev_day = prev_start.isocalendar()

    return render(
        request,
        'schedule/schedule-day.html',
        {'day_start': day_start,
            'next_start': next_start,
            'next_year': next_year,
            'next_week': next_week,
            'next_day': next_day,
            'prev_start': prev_start,
            'prev_year': prev_year,
            'prev_week': prev_week,
            'prev_day': prev_day,
            'schedule': Timeslot.timeslots_in_day(
                day_start,
                exclude_before_start=False,
                exclude_after_end=False,
                exclude_subsuming=False,
                with_jukebox_entries=True).data})

def schedule_day(request, year, week, day):
    """The day-in-detail schedule view.

    """
    return schedule_day_from_date(
        request,
        get_week_day(year, week, day))
