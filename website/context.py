"""
Context processors used in the LASS project.

"""

from django.conf import settings
from django.utils import timezone

from schedule.models.term import Term


def broadcast_info(request):
    """
    Adds information about whether the radio station is currently
    broadcasting into the template context.

    """
    # If any other ways of discerning whether broadcasting is
    # occurring, add them here!
    term = Term.of(timezone.now())
    return {
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
            (term is not None
             or Term.before(timezone.now()).name.lower() != 'summer')
        ),
    }
