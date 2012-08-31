from people.models import Role, Person
from django.contrib import admin


## Person ##

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_joined')
    exclude = ('password',)


admin.site.register(Person, PersonAdmin)


## Role ##

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias')


admin.site.register(Role, RoleAdmin)
