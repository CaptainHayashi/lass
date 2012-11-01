"""
Adminstration system hooks for the `website` model set.

"""

from website.models import Banner, BannerType
from website.models import BannerCampaign, BannerLocation
from website.models import Grid, GridBlock, GridBlockInstance
from website.models import GridBlockMetadata
from website.models import BannerTimeslot
from metadata.admin_base import MetadataAdmin, MetadataInline
from django.contrib import admin


class GridBlockInstanceAdmin(admin.ModelAdmin):
    """
    An administration snap-in for grid block instances.

    """
    list_display = (
        'grid_block',
        'grid',
        'x',
        'y'
    )

admin.site.register(GridBlockInstance, GridBlockInstanceAdmin)


class GridBlockInstanceInline(admin.TabularInline):
    """
    An inline administration snap-in for grid block instances.

    """
    model = GridBlockInstance


class GridBlockMetadataInline(MetadataInline):
    """
    An inline administration snap-in for grid block metadata.

    """
    model = GridBlockMetadata


admin.site.register(GridBlockMetadata, MetadataAdmin)


class GridBlockAdmin(admin.ModelAdmin):
    """
    An administration snap-in for grid blocks.

    This snap-in also includes an inline snap-in for in-grid
    instances of the administered grid blocks.

    """
    list_display = (
        'name',
        'description',
        'width',
        'height'
    )
    inlines = [
        GridBlockInstanceInline,
        GridBlockMetadataInline
    ]

admin.site.register(GridBlock, GridBlockAdmin)


class GridAdmin(admin.ModelAdmin):
    """
    An administration snap-in for grids.

    This snap-in also includes an inline snap-in for editing
    instances bound to this grid.

    """
    list_display = (
        'name',
        'description',
        'width',
        'height'
    )
    inlines = [GridBlockInstanceInline]

admin.site.register(Grid, GridAdmin)


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
