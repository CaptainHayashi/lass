from django.conf.urls import patterns, url
from getinvolved.views import index

urlpatterns = patterns(
    'getinvolved.views',
    url(r'^$',
        index,
        name='getinvolved_index'),
)
