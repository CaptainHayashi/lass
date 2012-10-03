from website.models import Banner, BannerType
from website.models import BannerCampaign, BannerLocation
from website.models import BannerTimeslot
from django.contrib import admin


class BannerTimeslotAdmin(admin.ModelAdmin):
    list_display = (
        'campaign',
        'day',
        'start_time',
        'end_time'
    )

admin.site.register(BannerTimeslot, BannerTimeslotAdmin)


class BannerTimeslotInline(admin.TabularInline):
    model = BannerTimeslot


class BannerCampaignAdmin(admin.ModelAdmin):
    list_display = (
        'banner',
        'location',
        'effective_from',
        'effective_to'
    )
    inlines = [BannerTimeslotInline]


admin.site.register(BannerCampaign, BannerCampaignAdmin)


class BannerCampaignInline(admin.StackedInline):
    model = BannerCampaign


class BannerLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [BannerCampaignInline]


admin.site.register(BannerLocation, BannerLocationAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt', 'type', 'image', 'target')
    inlines = [BannerCampaignInline]


class BannerInline(admin.TabularInline):
    model = Banner


class BannerTypeAdmin(admin.ModelAdmin):
    inlines = [BannerInline]

admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerType, BannerTypeAdmin)
