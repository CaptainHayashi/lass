## Master URLconf for URY Website ##

from django.conf.urls import patterns, include, url
from django.contrib import admin

# This is required for Django Admin to work
admin.autodiscover()


# General website pages (dynamic ones; static website pages
# use the flatpages system):

urlpatterns = patterns(
    'website.views',
    url(r'^index$', 'index', name='index-explicit'),
    url(r'^$',  'index', name='index'),
)


# Website applications

urlpatterns += patterns(
    '',
    # URY apps
    url(r'^schedule/', include('schedule.urls')),
    url(r'^uryplayer/', include('uryplayer.urls')),
    url(r'^search/', include('search.urls')),

    # Django apps
    url(r'^admin/', include(admin.site.urls)),
)
