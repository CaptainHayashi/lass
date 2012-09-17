from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from schedule.models import Show
from schedule.views import schedule_week
from schedule.views import schedule_weekday
from schedule.views import schedule_day
from schedule.views import index
from schedule.views import today

year_regex = r'(?P<year>\d+)'
week_regex = r'[wW](eek)?(?P<week>([01234]?\d|5[0123]))'
weekday_regex = r'[dD]?(ay)?(?P<weekday>[1234567])'
month_regex = r'(?P<month>(0?\d|1[12]))'
day_regex = r'(?P<day>([012]?\d|3[01]))'

schedule_week_regex, schedule_weekday_regex, schedule_day_regex = \
    ['/'.join(x) for x in
        [(year_regex, week_regex),
         (year_regex, week_regex, weekday_regex),
         (year_regex, month_regex, day_regex)]]

urlpatterns = patterns(
    'schedule.views',
    url(r'^$',
        index,
        name='schedule_index'),
    url(r'^today/',
        today,
        name='today'),
    url(r'^{0}/$'.format(schedule_week_regex),
        schedule_week,
        name='schedule_week'),
    url(r'^{0}/$'.format(schedule_weekday_regex),
        schedule_weekday,
        name='schedule_weekday'),
    url(r'^{0}/$'.format(schedule_day_regex),
        schedule_day,
        name='schedule_day'),
    url(r'^shows/$',
        ListView.as_view(model=Show),
        name='show_list'),
    url(r'^shows/(?P<pk>(-1|\d+))/$',
        DetailView.as_view(model=Show),
        name='show_detail'),
)
