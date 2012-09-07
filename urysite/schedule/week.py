"""The Week class, which represents a week of scheduled programming,
and provides various functions for transforming weekly views of the
schedule.

"""

class Week(object):
    """A view of one week of the URY schedule."""
    def __init__(self,
                 start_date,
                 data,
                 ):
        """Initialises a Week.

        Keyword arguments:
        start-date -- the date on which this week starts (need not
            be a Monday)
        data -- the list that populates the schedule; there
            must be eight constituent lists if has_extra_day is set,
            or seven if it is not
        has_extra_day -- whether or not the week data contains an
            additional day for use when shifting the 

