from website.models import BannerCampaign, BannerTimeslot
from django.shortcuts import render
from django.utils import timezone


def front_page_banner(request):
    now = timezone.now()
    campaigns = BannerCampaign.at(now)
    slots = (BannerTimeslot.objects
             .filter(campaign__in=campaigns)
             .filter(day=now.weekday(),
                     start_time__lte=now,
                     end_time__gt=now))
    return render(
        request,
        'website/banners/front_page.html',
        {
            'banners': [slot.campaign.banner for slot in slots]
        })


def index(request):
    return render(request, 'website/index.html')
