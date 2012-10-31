from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from website.models import BannerCampaign, BannerTimeslot, SISComm
from website.models import Grid
from django.shortcuts import render, redirect
from django.utils import timezone
from schedule.utils import list


def front_page_banner(request):
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


@cache_page(60, key_prefix="front_page_send_message")
def send_message_form(request):
    """
    Renders the front page "send a message" form.

    """
    return (render(request, 'website/send_message_form.html')
            if (list.coming_up(quantity=1)[0]
                .show_type().can_be_messaged)
            else render(request, 'website/send_message_deny.html'))


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
                statusid=2,  # No other statuses
                comm_source=location)
            message_comm.save()

            result = redirect('index')
    return result


def index(request):
    """
    Renders the home page.

    """
    return render(
        request,
        'website/index.html',
        {
            'grid': Grid.get('index')
        }
    )
