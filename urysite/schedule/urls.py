from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from schedule.models import Show
from schedule.views import schedule_week
from schedule.views import schedule_weekday
from schedule.views import schedule_day
from schedule.views import index
from schedule.views import today
from schedule.views import season_detail, timeslot_detail

year_regex = r'(?P<year>\d+)'
week_regex = r'[wW](eek)?(?P<week>([01234]?\d|5[0123]))'
weekday_regex = r'[dD]?(ay)?(?P<weekday>[1234567])'
month_regex = r'(?P<month>(0?\d|1[12]))'
day_regex = r'(?P<day>([012]?\d|3[01]))'

schedule_week_regex, schedule_weekday_regex, schedule_day_regex = \
    [r'^{0}/$'.format('/'.join(x)) for x in
        [(year_regex, week_regex),
         (year_regex, week_regex, weekday_regex),
         (year_regex, month_regex, day_regex)]]

show_regex = r'(?P<pk>(-1|\d+))'
season_regex = r'(?P<season_num>[1-9]\d*)'
timeslot_regex = r'(?P<timeslot_num>[1-9]\d*)'
showdb_show_regex, showdb_season_regex, showdb_timeslot_regex = \
    [r'^shows/{0}/$'.format('/'.join(x)) for x in
        [(show_regex,),
         (show_regex, season_regex),
         (show_regex, season_regex, timeslot_regex)]]

urlpatterns = patterns(
    'schedule.views',
    url(r'^$',
        index,
        name='schedule_index'),
    url(r'^today/',
        today,
        name='today'),
    url(schedule_week_regex,
        schedule_week,
        name='schedule_week'),
    url(schedule_weekday_regex,
        schedule_weekday,
        name='schedule_weekday'),
    url(schedule_day_regex,
        schedule_day,
        name='schedule_day'),
    url(r'^shows/$',
        ListView.as_view(model=Show),
        name='show_list'),
    url(showdb_show_regex,
        DetailView.as_view(model=Show),
        name='show_detail'),
    url(showdb_season_regex,
        season_detail,
        name='season_detail'),
    url(showdb_timeslot_regex,
        timeslot_detail,
        name='timeslot_detail'),
)
