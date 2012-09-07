from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from schedule.models import Show
from schedule.views import schedule_week, schedule_day, index

year_regex = r'(?P<year>\d+)'
week_regex = r'[wW](eek)?(?P<week>([01234]?\d|5[0123]))'
day_regex = r'[dD]?(ay)?(?P<day>[1234567])'

schedule_week_regex = '/'.join((year_regex, week_regex))
schedule_day_regex = '/'.join((year_regex, week_regex, day_regex))

urlpatterns = patterns(
    'schedule.views',
    url(r'^$',
        index,
        name='schedule_index'),
    url(r'^' + schedule_week_regex + '/$',
        schedule_week,
        name='schedule_week'),
    url(r'^' + schedule_day_regex + '/$',
        schedule_day,
        name='schedule_day'),
    url(r'^shows/$',
        ListView.as_view(model=Show),
        name='show_list'),
    url(r'^shows/(?P<pk>(-1|\d+))/$',
        DetailView.as_view(model=Show),
        name='show_detail'),
)
