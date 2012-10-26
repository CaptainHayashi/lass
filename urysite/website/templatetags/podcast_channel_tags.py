"""Template tags for dealing with podcast channels."""

from django import template
from uryplayer.models import PodcastChannel
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def channel_singular(channel_name):
    """Replaces an internal channel name with the channel's
    singular noun metadatum.

    """
    return (PodcastChannel
            .get(channel_name)
            .metadata()['text']['singular'])
