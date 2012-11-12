from people.models.role import Role, RoleMetadata
from people.models import Person, CreditType
from people.models import GroupRootRole
from django.contrib import admin


## Person ##

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_joined')
    exclude = ('password',)


admin.site.register(Person, PersonAdmin)


## RoleMetadata ##

class RoleMetadataInline(admin.StackedInline):
    model = RoleMetadata
    list_display = ('metadata_key', 'metadata_value')


## GroupRootRole ##

class GroupRootRoleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group_root_id',
        'alias',
        'title',
        'group_type')
    inlines = [RoleMetadataInline]


admin.site.register(GroupRootRole, GroupRootRoleAdmin)


## Role ##

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias', 'title')
    inlines = [RoleMetadataInline]


admin.site.register(Role, RoleAdmin)


## CreditType ##

admin.site.register(CreditType)
