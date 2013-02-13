"""
Context processors used in the LASS project.

"""

import datetime

from django.conf import settings
from django.utils import timezone

from schedule import models

from website.models import Website


def website(request):
    """
    Provides the Website object so that data attached to the website
    can be accessed.

    """
    return {
        'website': Website(request)
    }


def broadcast_info(request):
    """
    Adds information about whether the radio station is currently
    broadcasting into the template context, as well as the currently
    broadcasting shows.

    """
    now = timezone.now()

    # If any other ways of discerning whether broadcasting is
    # occurring, add them here!
    term = models.Term.of(now)
    if not term:
        preterm = models.Term.before(now)

    return {
        'shows': models.Timeslot.objects.public().in_range(
            now,
            now + datetime.timedelta(days=1)
        ),
        # broadcasting is intended to be true when a schedule is
        # in play.
        'broadcasting': getattr(
            settings,
            'BROADCASTING',
            (term is not None)
        ),
        # transmitting is intended to be a stronger form of
        # broadcasting, in that it represents times when the station
        # is technically on air but not necessarily working to a
        # schedule.
        'transmitting': getattr(
            settings,
            'TRANSMITTING',
            (
                term is not None
                or (preterm is not None and preterm.name.lower() != 'summer')
            )
        ),
    }
