## Master URLconf for URY Website ##

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import schedule.admin
import uryplayer.admin
import metadata.admin
import people.admin


# This is required for Django Admin to work
admin.autodiscover()
schedule.admin.register(admin.site)
uryplayer.admin.register(admin.site)
metadata.admin.register(admin.site)
people.admin.register(admin.site)


# General website pages (dynamic ones; static website pages
# use the flatpages system):

urlpatterns = patterns(
    'website.views',
    url(r'^index$', 'index', name='index-explicit'),
    url(r'^$',  'index', name='index'),
    url(r'^send-message$', 'send_message', name='send_message'),
)


# Website applications

urlpatterns += patterns(
    '',
    # URY apps
    url(r'^schedule/', include('schedule.urls')),
    url(r'^uryplayer/', include('uryplayer.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^getinvolved/', include('getinvolved.urls')),
    url(r'^laconia/', include('laconia.urls')),
    url(r'^grid/', include('grid.urls')),

    url(r'^admin/orderedmove/(?P<direction>up|down)/'
        '(?P<model_type_id>\d+)/(?P<model_id>\d+)/$',
        'urysite.views.admin_move_ordered_model',
        name="admin-move"),

    # Django apps
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('zinnia.urls')),
    url(r'^news/', include('zinnia.urls')),
    url(r'^speech/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
