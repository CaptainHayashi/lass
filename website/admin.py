"""
Adminstration system hooks for the `website` model set.

"""

from website.models import Banner, BannerType
from website.models import BannerCampaign, BannerLocation
from website.models import BannerTimeslot
from website.models import WebsitePackageEntry
from website.models import WebsiteImageMetadata
from website.models import WebsiteTextMetadata
from django.contrib import admin


class BannerTimeslotAdmin(admin.ModelAdmin):
    """
    An administration snap-in for banner timeslots.

    """
    list_display = (
        'campaign',
        'day',
        'start_time',
        'end_time'
    )

admin.site.register(BannerTimeslot, BannerTimeslotAdmin)


class BannerTimeslotInline(admin.TabularInline):
    """
    An inline administration snap-in for banner timeslots.

    """
    model = BannerTimeslot


class BannerCampaignAdmin(admin.ModelAdmin):
    """
    An administration snap-in for banner campaigns.

    This snap-in includes an inline snap-in for timeslots that
    are part of campaigns.

    """
    list_display = (
        'banner',
        'location',
        'effective_from',
        'effective_to'
    )
    inlines = [BannerTimeslotInline]


admin.site.register(BannerCampaign, BannerCampaignAdmin)


class BannerCampaignInline(admin.StackedInline):
    """
    An inline adminstration snap-in for banner campaigns.

    """
    model = BannerCampaign


class BannerLocationAdmin(admin.ModelAdmin):
    """
    An administration snap-in for banner locations.

    This snap-in includes an inline snap-in for banner campaigns
    concerning the administered locations.

    """
    list_display = ('name', 'description')
    inlines = [BannerCampaignInline]


admin.site.register(BannerLocation, BannerLocationAdmin)


class BannerAdmin(admin.ModelAdmin):
    """
    An administration snap-in for banners.

    This snap-in includes an inline snap-in for banner campaigns
    that dictate when and where the banner appears.

    """
    list_display = ('alt', 'type', 'image', 'target')
    inlines = [BannerCampaignInline]

admin.site.register(Banner, BannerAdmin)


class BannerInline(admin.TabularInline):
    """
    An inline administration snap-in for banners.

    """
    model = Banner


class BannerTypeAdmin(admin.ModelAdmin):
    """
    An administration snap-in for banner types.

    This snap-in includes an inline snap-in for banners that are
    of the administered types.

    """
    inlines = [BannerInline]

admin.site.register(BannerType, BannerTypeAdmin)

admin.site.register(WebsiteTextMetadata)
admin.site.register(WebsiteImageMetadata)
admin.site.register(WebsitePackageEntry)
