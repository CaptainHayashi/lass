"""Base admin classes for metadata administration."""

from django.contrib import admin


class MetadataAdmin(admin.ModelAdmin):
    """Base class for metadata admin-lets."""

    date_hierarchy = 'effective_from'
    list_display = (
        'element',
        'key',
        'value',
        'creator',
        'approver',
        'effective_from',
        'effective_to',
    )


class MetadataInline(admin.TabularInline):
    """Base inline class for metadata inline admin-lets."""

    pass
