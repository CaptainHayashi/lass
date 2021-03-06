from django.db.models.loading import get_model
from metadata.utils.date_range import in_range
from django.shortcuts import render
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.conf import settings

from schedule.utils import range as s_range

import csv
import json


# This is used to limit range_XYZ requests to prevent them from
# DoSing URY accidentally.
MAX_RANGE_LENGTH = 10 * 24 * 60 * 60  # Ten days


def laconia_error(request, message, status=403):
    """
    Throws an error from the laconia interface.

    The default status code emitted is 403 Forbidden.

    """
    return render(
        request,
        'laconia/error.txt',
        {'message': message},
        content_type='text/plain',
        status=status
    )


def current_show_location_and_time(request):
    """Sends the current show location, time and show ID as text."""
    # This just expects the current show to be given by context processors now.
    return render(
        request,
        'laconia/current-show-location-and-time.txt',
        content_type="text/plain"
    )


def current_show_and_next(request):
    """Sends info about the current show as JSON."""
    # In case the worst happens and the schedule doesn't come back with
    # two items, we're very cautious about the size of day.
    day = list(s_range.day(limit=2))

    json_data = {}
    if len(day) >= 1:
        on_air = day[0]
        if on_air.player_image:
            image = on_air.player_image.url
        else:
            image = settings.STATIC_URL + "img/default_show_player.png"
        json_data.update(
            {
                "onAir": on_air.title,
                "onAirDesc": on_air.description,
                "onAirPres": on_air.by_line(),
                "onAirTime": '{:%H:%M} - {:%H:%M}'.format(
                    on_air.start_time, on_air.end_time
                ),
                "onAirImg": image,
            }
        )
    if len(day) >= 2:
        up_next = day[1]
        json_data.update(
            {
                "upNext": up_next.title,
                "upNextDesc": up_next.description,
                "upNextPres": up_next.by_line(),
                "upNextTime": '{:%H:%M} - {:%H:%M}'.format(
                    up_next.start_time, up_next.end_time
                )
            }
        )
    return HttpResponse(
        simplejson.dumps(json_data), content_type="application/json"
    )


def range_querystring(request, appname, modelname, format='json'):
    """
    Wrapper to `range` that expects its date range in the query
    string.

    Since this view mainly exists to accommodate FullCalendar, which
    expects its output in JSON, the default format is JSON as opposed
    to CSV.

    """
    if 'start' not in request.GET or 'end' not in request.GET:
        raise Http404
    return range(
        request,
        appname,
        modelname,
        request.GET['start'],
        request.GET['end'],
        format
    )


def range(request, appname, modelname, start, end, format='csv'):
    """
    Retrieves a summary about any items in the given model that fall
    within the given range.

    Items are returned if any time within their own time range falls
    within the given range.

    If format is 'csv', the result is delivered as a CSV if the given
    model exists and supports range queries, or a HTTP 404 if not.
    The CSV may be empty.

    If format is 'fullcal', the result is instead a JSON list
    corresponding to the schema at http://arshaw.com/fullcalendar -
    again if the given model cannot be queried for range a HTTP 404
    will be emitted.

    If the model supports metadata queries, the 'title' and
    'description' metadata will be pulled if it exists.

    If the model supports credit queries, the by-line will also be
    added.

    """
    model = get_model(appname, modelname)
    if model is None:
        raise Http404

    start = int(start)
    end = int(end)

    # Request sanity checking
    if (end - start) < 0:
        response = laconia_error(
            request,
            'Requested range is negative.'
        )
    elif (end - start) > MAX_RANGE_LENGTH:
        response = laconia_error(
            request,
            'Requested range is too long (max: {0} seconds)'.format(
                MAX_RANGE_LENGTH
            )
        )
    else:
        try:
            items = in_range(model, start, end)
        except AttributeError:
            # Assuming this means the model can't do range-based ops
            raise Http404

        filename = u'{0}-{1}-{2}-{3}'.format(
            appname,
            modelname,
            start,
            end
        )

        if format == 'csv':
            f = range_csv
        elif format == 'json':
            f = range_json
        else:
            raise ValueError('Invalid format specifier.')
        response = f(filename, items)
    return response


def range_csv(filename, items):
    """
    Returns a range query result in CSV format.

    The order of items in the CSV rows are:

    1) Primary key
    2) Start time as UNIX timestamp
    3) End time as UNIX timestamp
    4) 'title' from default metadata strand, if metadata exists;
       else blank
    5) 'description' from default metadata strand, if metadata exists;
       else blank
    6) By-line, if credits exist; else blank

    """
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = (
        u'attachment; filename="{0}.csv"'.format(filename)
    )
    writer = csv.writer(response)

    for item in items:
        writer.writerow([
            item.pk,
            item.range_start_unix(),
            item.range_end_unix(),
            getattr(item, 'title', ''),
            getattr(item, 'description', ''),
            getattr(item, 'by_line', lambda x: '')()
        ])

    return response


def range_item_title(item):
    """
    Returns the most sensible human-readable title for the item.

    This is either the 'text'/'title' metadatum if the item supports
    metadata, or the empty string (for loggerng compatibility
    purposes, primarily).

    """
    return getattr(item, 'title', '')


def range_item_dict(item):
    """
    Returns a dictionary representing the information from a given
    range item that is pertinent to a range query.

    """
    return {
        'id': item.pk,
        'title': range_item_title(item),
        'start': item.range_start_unix(),
        'end': item.range_end_unix(),
    }


def range_json(filename, items):
    """
    Returns a range query in JSON (full-calendar) format.

    The format used is described in
    http://arshaw.com/fullcalendar/docs/event_data/Event_Object

    If the range item supports metadata, the 'title' attribute will
    correspond to the 'text'/'title' metadatum if it exists for the
    start time of the item; else the item's Unicode representation
    will be returned.

    """
    return HttpResponse(
        json.dumps(map(range_item_dict, items)),
        mimetype='application/json'
    )
