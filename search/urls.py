"""URLconf for the URY site searching system."""

from django.conf.urls import patterns, include, url
from search.views import sitewide_search_view_factory

urlpatterns = patterns(
    'search.views',
    url(r'^$',
        sitewide_search_view_factory(),
        name='search'),
)
