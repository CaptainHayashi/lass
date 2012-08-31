from django.conf.urls import patterns, include, url
from django.views.generic import DetailView
#from uryplayer.models import Podcast

urlpatterns = patterns(
    'uryplayer.views',
    #url(r'^$', 'index'),
    #url(r'^podcasts/(?P<pk>\d+)/$',
    #    DetailView.as_view(
    #        model=Podcast,
    #        template_name='uryplayer/podcast.html')),
)
