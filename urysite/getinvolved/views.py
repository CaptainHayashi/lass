from django.shortcuts import render
from people.utils import group


def index(request):
    """The get involved page index view.

    """

    return render(
        request,
        'getinvolved/index.html',
        {'on_air_teams': group.roots_of_type('On-Air Teams'),
            'support_teams': group.roots_of_type('Support Teams')})
