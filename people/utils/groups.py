"""Functions concerning role groups, which typically correspond to
station teams.

"""

from people.models import GroupRootRole, GroupType


## GROUP TYPES ##


## GROUP ROOTS ##

def roots(active_only=True):
    """Retrieves all currently active group root roles or, if
    active_only is set to False, all group roles currently stored.

    The return value is a queryset and can thus be filtered further
    (for example, filtering by visibility).

    Keyword arguments:
    active_only -- if True, only active group roots are retrieved;
        if False, all group roots stored in the system are retrieved
        (default: True)
    """
    roots = GroupRootRole.objects.all()
    return roots.filter(is_active=True) if active_only else roots


# Canned group root queries
# (Many of these will be specific to URY)

def roots_of_type(group_type, *args, **kwargs):
    """A filtered counterpart to group_roots that retrieves only
    group roots in the given group type.

    A practical example in the radio station context would be to
    find all teams (group roots) that are on-air teams (group type).

    Any arguments other than group_type are passed to group_roots, so
    see also the documentation of that function.

    If group_type is a string, it will be taken as the name of the
    group type instead of a reference to the actual object.

    """
    if isinstance(group_type, basestring):
        group_type = GroupType.objects.get(name=group_type)

    return group_roots(*args, **kwargs).filter(group_type)
