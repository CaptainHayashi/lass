"""
Administration system registrations for the grid system.

"""

from grid.models import Grid, GridBlock, GridBlockInstance
from grid.models import GridBlockTextMetadata
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


class GridBlockTextMetadataInline(MetadataInline):
    """
    An inline administration snap-in for grid block metadata.

    """
    model = GridBlockTextMetadata


admin.site.register(GridBlockTextMetadata, MetadataAdmin)


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
        GridBlockTextMetadataInline
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
