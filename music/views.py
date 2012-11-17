"""Views used in the music app."""

from django.shortcuts import render
from music.models import ChartType, ChartRelease


def home_chart(request, block_id, show_position=True):
    """Renders a view of the given chart for the home page.

    chart_type can be any item that can be used by ChartType.get to
    retrieve a type.

    Due to issues getting embedded view tags to pass booleans in,
    show_position will accept the strings 'True' and 'False' as
    True and False respectively.

    """
    # If anyone can make this not necessary, please do
    if show_position == 'True':
        show_position = True
    elif show_position == 'False':
        show_position = False

    # Quickfix that should be deleted once the
    # chart types are renamed
    try:
        chart_type = ChartType.get(block_id)
    except ChartType.DoesNotExist:
        if block_id == 'chart':
            chart_type = ChartType.get('URY Chart')
        elif block_id == 'music':
            chart_type = ChartType.get('Recommended Listening')

    try:
        chart = ChartRelease.objects.filter(
            type__exact=chart_type).latest()
    except ChartRelease.DoesNotExist:
        chart = None
    return render(
        request,
        'music/home-chart.html',
        {
            'chart': chart,
            'chart_type': chart_type,
            'show_position': show_position
        })
