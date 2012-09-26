from urysite.models import MetadataKey
from django.contrib import admin


## MetadataKey ##

class MetadataKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'allow_multiple')

admin.site.register(MetadataKey, MetadataKeyAdmin)
