from django.conf.urls import patterns, url


urlpatterns = patterns(
    'grid.views',
    url(r'^raw/(?P<block_id>[a-zA-Z-_]+)$',
        'block_raw',
        name='block_raw'),
)
