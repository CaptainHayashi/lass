"""Functions for manipulating and inserting filler timeslots.

Filler slots are fake timeslots, tied to a fake season (which is
assigned to a real show!), that are optionally used to pad out gaps
in timeslot ranges.

At the time of writing, the filler slots correspond to URY Jukebox
programming.

"""

# NOTE: A lot of this module involves subversion of the schedule
# system in order to make filler slots appear to be real shows to
# the higher levels of the website.  As always, improvements are
# very welcome.

from schedule.models import Term, Show, Season, Timeslot


def show(start_time, duration):
    """Retrieves a parent show usable for filler timeslots.

    Keyword arguments:
    start_time -- the start time of the filler timeslot being
        created, as an aware datetime
    duration -- the duration of the filler timeslot being
        created, as a timedelta
    """
    return Show.objects.get(pk=-1)


def term(start_time, duration):
    """Retrieves a university term that is usable for a filler slot
    with the given start time and duration (or, more specifically,
    the pseudo-season thereof).

    Keyword arguments:
    start_time -- the start time of the filler timeslot being
        created, as an aware datetime
    duration -- the duration of the filler timeslot being
        created, as a timedelta
    """
    return Term.of(start_time)


def season(start_time, duration):
    """Retrieves a parent season usable for filler timeslots.

    Keyword arguments:
    start_time -- the start time of the filler timeslot being
        created, as an aware datetime
    duration -- the duration of the filler timeslot being
        created, as a timedelta
    """
    this_term = term(start_time, duration)
    if this_term is None:
        raise ValueError(
            "Tried to create filler show outside a term.")
    return Season(
        show=show(start_time, duration),
        term=this_term,
        date_submitted=this_term.start)


def timeslot(start_time, end_time=None, duration=None):
    """Creates a new timeslot that is bound to the URY Jukebox.

    Keyword arguments:
    start_time -- the start time of the filler timeslot being
        created, as an aware datetime
    end_time -- the end time of the filler timeslot being
        created, as an aware datetime; this must be None if
        duration is used
    duration -- the duration of the filler timeslot being
        created, as a timedelta; this must be None if end_time
        is used
     """
    if duration is None:
        if end_time is None:
            raise ValueError('Specify end or duration.')
        else:
            duration = end_time - start_time
    elif end_time is not None:
        raise ValueError('Do not specify both end and duration.')

    return Timeslot(
        season=season(start_time, end_time),
        start_time=start_time,
        duration=duration)


## FILLING ALGORITHM

def fill(timeslots, start_time, end_time):
    """Fills any gaps in the given timeslot list with filler slots,
    such that the list is fully populated from the given start time
    to the given end time.

    Keyword arguments:
    timeslots -- the list of timeslots, may be empty
    start_time -- the start date/time
    end_time -- the end date/time

    """
    if len(timeslots) == 0:
        timeslots = [timeslot(start_time, end_time)]
    else:
        # Start by filling in the ends
        if timeslots[0].start_time > start_time:
            timeslots.insert(
                0,
                timeslot(
                    start_time,
                    timeslots[0].start_time))
        if timeslots[-1].end_time() < end_time:
            timeslots.append(
                timeslot(
                    timeslots[-1].end_time(),
                    end_time))
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
                    timeslot(
                        left.end_time(),
                        right.start_time))
                # The list has grown by one, so we'll need to
                # factor that into the index calculations
                offset += 1
    return timeslots
