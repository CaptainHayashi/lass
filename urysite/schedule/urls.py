from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from schedule.models import Show

##
# SCHEDULE VIEWS
##

# Partial regular expressions
year_regex = r'(?P<year>\d+)'
week_regex = r'[wW](eek)?(?P<week>([0-4]?\d|5[0-3]))'
weekday_regex = r'[dD]?(ay)?(?P<weekday>[1-7])'
month_regex = r'(?P<month>(0?\d|1[12]))'
day_regex = r'(?P<day>([0-2]?\d|3[01]))'

# Full URL expressions in terms of the above
schedule_week_regex, \
    schedule_weekday_regex, \
    schedule_day_regex = (
        r'^{0}/$'.format('/'.join(x))
        for x in (
            (year_regex, week_regex),
            (year_regex, week_regex, weekday_regex),
            (year_regex, month_regex, day_regex),
        )
    )

##
# SHOW DATABASE VIEWS
##

# Partial regular expressions
show_regex = r'(?P<pk>(-1|\d+))'
season_regex = r'(?P<season_num>[1-9]\d*)'
timeslot_regex = r'(?P<timeslot_num>[1-9]\d*)'

# Full URL expressions in terms of the above
showdb_show_regex, \
    showdb_season_regex, \
    showdb_timeslot_regex = (
        r'^shows/{0}/$'.format('/'.join(x))
        for x in (
            (show_regex,),
            (show_regex, season_regex),
            (show_regex, season_regex, timeslot_regex),
        )
    )

urlpatterns = patterns(
    'schedule.views',
    url(r'^$',
        'index',
        name='schedule_index'),
    url(r'^today/',
        'today',
        name='today'),
    url(schedule_week_regex,
        'schedule_week',
        name='schedule_week'),
    url(schedule_weekday_regex,
        'schedule_weekday',
        name='schedule_weekday'),
    url(schedule_day_regex,
        'schedule_day',
        name='schedule_day'),
    url(r'^shows/$',
        ListView.as_view(
            queryset=Show.objects.filter(
                show_type__has_showdb_entry=True)),
        name='show_index'),
    url(showdb_show_regex,
        DetailView.as_view(
            queryset=Show.objects.filter(
                show_type__has_showdb_entry=True)),
        name='show_detail'),
    url(showdb_season_regex,
        'season_detail',
        name='season_detail'),
    url(showdb_timeslot_regex,
        'timeslot_detail',
        name='timeslot_detail'),
)
