"""
URLconf for the music microsite.

"""

from django.conf.urls import patterns, url
from django.views.generic import DetailView

from music.models import ChartType


urlpatterns = patterns(
    'music.views',
    url(r'^charts/(?P<slug>[A-Za-z_-]$',
        DetailView.as_view(
            slug_field='name',
            model=ChartType
        ),
        name='charttype_detail'),
)
