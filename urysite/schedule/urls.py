from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from schedule.models import Show
from schedule.views import schedule_week

urlpatterns = patterns(
    'schedule.views',
    #url(r'^$', 'index'),
    url(r'^(?P<year>\d\d\d\d)/(?P<week>[wW]([01234]?\d|5[0123]))/$',
        schedule_week,
        name='schedule_week'), 
    url(r'^shows/$',
        ListView.as_view(model=Show),
        name='show_list'),
    url(r'^shows/(?P<pk>(-1|\d+))/$',
        DetailView.as_view(model=Show),
        name='show_detail'),
)
