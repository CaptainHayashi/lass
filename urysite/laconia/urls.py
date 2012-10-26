from django.conf.urls import patterns, url

APP_MODEL_REGEX = r'(?P<appname>.+)/(?P<modelname>.+)'

urlpatterns = patterns(
    'laconia.views',
    url(r'^current-show-location-and-time/$',
        'current_show_location_and_time',
        name='current_show_location_and_time'),
    url(r'^range/{0}/(?P<start>[0-9]+)/(?P<end>[0-9]+.)/$'
        .format(APP_MODEL_REGEX),
        'range',
        name='range'),
    url(r'^range/{0}/$'
        .format(APP_MODEL_REGEX),
        'range_querystring',
        name='range_querystring'),
)
