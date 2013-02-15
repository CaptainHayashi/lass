from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from website.models import BannerCampaign, BannerTimeslot, SISComm
from grid.models import Grid
from website.models import Blog
from django.shortcuts import render, redirect
from django.utils import timezone


def front_page_banner(request, block_id=None):
    """
    Renders the current front page banner rotation.

    """
    now = timezone.now()
    campaigns = BannerCampaign.at(now)
    slots = (BannerTimeslot.objects
             .filter(campaign__in=campaigns)
             .filter(day=now.isoweekday(),
                     start_time__lte=now,
                     end_time__gt=now))
    return render(
        request,
        'website/banners/front_page.html',
        {
            'banners': [slot.campaign.banner for slot in slots]
        })


def send_message_form(request, block_id=None):
    """
    Renders the front page "send a message" form.

    """
    # TODO: remove me when the grid block changes to a generic one.
    return render(request, 'grid/send_message_form.html')


# NOTE: THE BELOW IS A TEMPORARY HACK
# PLEASE REPLACE WITH SOMETHING NICER

@require_POST
@csrf_exempt
def send_message(request):
    """
    Sends a message to the current show via the website.

    """
    # Current show
    timeslot = list.coming_up(quantity=1)[0]

    if 'comments' not in request.POST:
        result = render(
            request,
            'website/send-message-error.html',
            {'error': "You didn't specify a message."},
            status=403)
    elif not timeslot.can_be_messaged():
        result = render(
            request,
            'website/send-message-error.html',
            {'error': "This show isn't messagable."},
            status=403)
    else:
        message = request.POST['comments']

        spam = [
            '[url=',
            '<a href=',
            '&lt;a href='
        ]
        # Rudimentary spam check
        if True in (x in message for x in spam):
            result = render(
                request,
                'website/send-message-error.html',
                {'error':
                 'Your message has been detected as potential spam.'},
                status=403)
        else:
            # Check for possible computing words and warn presenters
            comp_words = [
                'fs1',
                'server',
                'icecast',
                'stream',
                'jukebox',
                'restart',
                'logger',
                'computing team',
                'compteam'
            ]
            if True in (x in message.lower() for x in comp_words):
                message = ''.join(("""
                <div class="ui-state-highlight">
                <span>
                    Computing Team will never ask you to switch to the
                    jukebox or otherwise disrupt your show using a SIS
                    message.
                </span>
                </div>
                """, message))

            # Find out where the sender is from
            location = (request.META['REMOTE_ADDR']
                        if 'HTTP_X_FORWARDED_FOR' not in request.META
                        else request.META['HTTP_X_FORWARDED_FOR'])

            message_comm = SISComm(
                commtypeid=3,  # Website communication
                sender='URY Website',
                timeslotid=timeslot.id,
                subject=message[:255],
                content=message,
                statusid=1,  # Unread
                comm_source=location)
            message_comm.save()

            result = redirect('index')
    return result


def blog_summary(request, block_id=None):
    """
    Outputs a summary of the blog corresponding to the grid block
    ID this view was called from.

    """
    return render(
        request,
        'website/blog_summary.html',
        {
            'blog': Blog.get(block_id)
        }
    )


def static_grid_block(request, block_id):
    """
    Outputs a static template as a grid block view.

    """
    return render(
        request,
        'grid/{0}.html'.format(block_id)
    )


def index(request):
    """
    Renders the home page.

    """
    return render(
        request,
        'website/index.html',
        {
            'grid': Grid.get_if_exists('index')
        }
    )
