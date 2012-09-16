from django.shortcuts import render
from datetime import date, time, datetime, timedelta
from schedule.models import Timeslot
from django.utils import timezone


# Changing this will change the starting time of the schedule
# views.
# NOTE: This time is taken to be in local time, NOT UTC!
URY_START = time(
    hour=7,
    minute=0,
    second=0)


def ury_start_on_date(date):
    """Returns a new datetime representing the nominal start of URY
    programming on the given date (timezone-aware).

    """
    return timezone.make_aware(
        datetime.combine(date, URY_START),
        timezone.get_current_timezone())


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
            def __init__(self, timeslot):
                self.row_span = 1
                self.timeslot = timeslot 

        def __init__(self, start_time, duration):
            self.start_time = start_time
            self.entries = []
            self.see_above = []
            self.duration = duration

        def add(self, timeslot):
            """Adds a timeslot to the row.
            
            No inter-row compressing is done at this stage.
            
            """
            if len(self.entries) == 7:
                # We don't want more than seven days!
                raise IncorrectlySizedRowException
            else:
                self.entries.append(
                    ScheduleTable.Row.Entry(
                        timeslot))

        def real_column(self, column):
            """Returns the actual index of a given column in the row. 

            The reason the column number and entries index may be
            different is because of row compression.

            """
            return column - \
                len([x for x in self.see_above if x < column])

        def get(self, column):
            """Gets the entry at the given column.

            If the row has been compressed (some of its contents
            removed due to being referenced in rows above it in the
            table), this method will return the item that would
            normally be in the column, or None if the column in
            question has been thus affected.

            """
            if column in self.see_above:
                # Column has been removed due to compression
                return None
            else:
                return self.entries[self.real_column(column)]

        def inc_row_span(self, column):
            """Increases the row span count of the given (logical)
            column.

            This should be used when compressing the row below this
            one in the table.
            """
            self.get(column).row_span += 1

    def __init__(self):
        self.rows = []

    def add(self, row):
        """Adds a new row, compressing it in the process.

        If any row entry is defined as not being the show start, and
        an entry for the same show appears in the same column of the
        previous row, then the show is deleted from the inserted row
        and the row span of the other entry is incremented.

        """
        if type(row) == ScheduleTable.Row:
            entries = row.entries
            # Compress row by merging where possible with above
            # row
            if len(self.rows) > 0:
                for col, show in enumerate(row.entries[:]):
                    slot = show.timeslot
                    # If the show was in the previous two rows, the
                    # row above will already have been compressed, and
                    # this manifests itself in the above show being
                    # None.
                    # We need to keep going through the rows until we
                    # hit an actual show, then see if it's the same
                    # as the one we're adding, to decide whether to
                    # compress the entry in this row too.
                    for above_row in reversed(self.rows):
                        above_show = above_row.get(col)
                        if above_show is None: 
                            continue
                        elif slot is above_row.get(col).timeslot:
                            # Compress by adding span to previous row
                            row.entries.remove(show)
                            row.see_above.append(col)
                            above_row.inc_row_span(col)
        
            self.rows.append(row)
        else:
            raise TypeError("Cannot add things other than Rows.")

    @classmethod
    def tabulate_week_lists(cls,
                            week,
                            start_date,
                            align_to_hour=True):
        """Creates a schedule week table from a group of seven lists.

        You should generally use 'tabulate' instead of directly
        invoking this.

        """
        assert len(week) == 7, "Must be 7 days in the week list."
        assert False not in [len(day) > 0 for day in week], \
            "All week lists must be populated."

        row_date = start_date
        time_remaining_on_shows = [day[0].duration for day in week]
        table = ScheduleTable()

        # Assuming that either all weeks are populated or none are
        while True in [len(day) > 0 for day in week]:
            assert False not in [len(day) > 0 for day in week], \
                "All days must be of equal length."
            assert timedelta(seconds=0) not in \
                time_remaining_on_shows, \
                """A time remaining on show entry is zero.
                This show should have been dropped off the stack
                already.
                """

            # If any of the current shows' remaining durations would
            # send the schedule over 24 hours, then we take drastic
            # action by culling its remaining duration and cancelling
            # all the subsequent shows.
            # This is so each day is the same length.
            # (Note that Jukebox filling ensures each day is AT LEAST
            # 24 hours long)
            for day_index in range(len(time_remaining_on_shows)):
                if (row_date + time_remaining_on_shows[day_index]) \
                    - start_date > timedelta(days=1):
                    time_remaining_on_shows[day_index] = \
                        (start_date + timedelta(days=1)) - row_date
                    week[day_index] = week[day_index][0:1]

            # Decide where to split the row, initially we'll use the
            # shortest remaining show time
            shortest_duration = min(time_remaining_on_shows)
            # However, if we're aligning to hours, we'll need to
            # prematurely split the row to accomodate it
            if align_to_hour:
                time_until_next_hour = timedelta(hours=1) - \
                    timedelta(
                        minutes=row_date.minute,
                        seconds=row_date.second,
                        microseconds=row_date.microsecond)
                row_duration = min(
                    shortest_duration,
                    time_until_next_hour)
            else:
                row_duration = shortest_duration

            row = ScheduleTable.Row(row_date, row_duration)
            # Now shove shows into the row
            for day_index, day in enumerate(week):
                # Decide whether this row entry contains the start
                # of the show (all time remaining) or the end of the
                # show (time remaining will hit 0 after this row is
                # done)
                is_end = (time_remaining_on_shows[day_index] == \
                    row_duration)
                # Because we pick either the shortest remaining show
                # duration or something shorter than it as the row
                # duration, these assertions should hold
                assert time_remaining_on_shows[day_index] >= \
                    row_duration, """Row must never be bigger than
                    the amount of time remaining for a show in the
                    queue."""
                assert day[0].duration >= row_duration, \
                    """Row must never be bigger than a show's
                    duration."""

                row.add(day[0])

                # Push spent shows off the day stacks, deduct
                # row duration from time remaining on unspent ones
                if is_end:
                    del day[0]
                    if len(day) > 0:
                        time_remaining_on_shows[day_index] = \
                            day[0].duration
                    else:
                        time_remaining_on_shows[day_index] = \
                            None
                else:
                    time_remaining_on_shows[day_index] -= \
                        row_duration
                assert time_remaining_on_shows[day_index] is None \
                    or time_remaining_on_shows[day_index] > \
                    timedelta(seconds=0), """No time remaining on
                    unpopped show."""

            # Get ready for next row
            row_date += row_duration
            table.add(row)
        return table

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
            range_list_pure.append(range_data.data[:])
        return cls.tabulate_week_lists(
            range_list_pure,
            range_list[0].start)


## These next two functions were purloined from
## http://stackoverflow.com/q/304256

def iso_year_start(iso_year):
    """The gregorian calendar date of the first day of the given ISO
    year.
    
    """
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 


def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Gregorian calendar date for the given ISO year, week
    and day.
    
    """
    year_start = iso_year_start(iso_year)
    return year_start + timedelta(
        days=iso_day-1,
        weeks=iso_week-1)

## End unoriginal code


def get_week_day(year, week, day):
    """Given a year, a week number inside that year and a day number
    inside that day (from 1 to 7), finds the corresponding time
    period that represents the start of that URY day.

    """
    return ury_start_on_date(iso_to_gregorian(year, week, day))


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
            'prev_week': prev_week,
            'schedule': schedule})


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
        ury_start_on_date(to_monday(datetime.utcnow())))


def schedule_week(request, year, week):
    """The week-at-a-glance schedule view.

    """
    # WEEK STARTS
    return schedule_week_from_date(
        request, 
        get_week_start(int(year), int(week)))


# DAY SCHEDULES 

def schedule_day_from_date(request, day_start):
    """The day-at-a-glance schedule view, with the day specfied by
    a date object (including the start time of the schedule).

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


def schedule_weekday(request, year, week, weekday):
    """The day-in-detail schedule view, with the day provided in
    Year/Week/Day format.

    """
    return schedule_day_from_date(
        request,
        get_week_day(int(year), int(week), int(weekday)))


def schedule_day(request, year, month, day):
    """The day-in-detail schedule view, with the day provided in
    Year/Month/Day format.

    """
    return schedule_day_from_date(
        request,
        ury_start_on_date(date(
            year=int(year),
            month=int(month),
            day=int(day))))


def today(request): 
    """A view that shows the day schedule for today."""
    return schedule_day_from_date(
        request,
        ury_start_on_date(timezone.now()))

