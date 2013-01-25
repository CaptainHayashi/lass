from django.contrib import admin

from metadata.admin_base import TextMetadataInline
from metadata.admin_base import ImageMetadataInline

from lass_lerouge.models import Role
from lass_lerouge.models import RoleTextMetadata
from lass_lerouge.models import RoleImageMetadata
from lass_lerouge.models import GroupRootRole


## RoleMetadata ##

class RoleTextMetadataInline(TextMetadataInline):
    model = RoleTextMetadata


class RoleImageMetadataInline(ImageMetadataInline):
    model = RoleImageMetadata


## Role ##

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias', 'title')
    inlines = [
        RoleTextMetadataInline,
        RoleImageMetadataInline
    ]

    # These are needed because title and description are pseudo
    # attributes exported through the metadata system.

    def title(self, obj):
        return obj.title

    def description(self, obj):
        return obj.description


admin.site.register(Role, RoleAdmin)


## GroupRootRole ##

class GroupRootRoleAdmin(RoleAdmin):
    list_display = (
        'id',
        'group_root_id',
        'alias',
        'title',
        'group_type'
    )


admin.site.register(GroupRootRole, GroupRootRoleAdmin)
