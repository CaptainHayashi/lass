from django.shortcuts import render
from datetime import datetime, timedelta


def get_week_start(year, week):
    """Given a year and a week number inside that year, finds the
    date of the Monday of that week.

    See the C89 definition of strptime formats for details on how
    this function works.

    """
    # If anyone can find an easier way of converting year/week to a
    # datetime, replace the following:
    week_start_str = '%s %s 1' % (year, week)
    return datetime.strptime(week_start_str, '%Y %W %w')


def schedule_week_from_date(request, week_start):
    """The week-at-a-glance schedule view, with the week specified
    by a date object denoting its starting day.

    """
    next_start = week_start + timedelta(weeks=1)
    next_year, next_week, next_day = next_start.isocalendar()

    prev_start = week_start - timedelta(weeks=1)
    prev_year, prev_week, prev_day = prev_start.isocalendar()

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
