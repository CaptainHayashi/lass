from website.models import Banner, BannerCategory
from django.contrib import admin


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'filename', 'uri')


class BannerInline(admin.TabularInline):
    model = Banner


class BannerCategoryAdmin(admin.ModelAdmin):
    inlines = [BannerInline]

admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerCategory, BannerCategoryAdmin)
