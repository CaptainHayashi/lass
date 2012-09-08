"""Models pertaining to LeRouge roles"""

from django.db import models
from urysite import model_extensions as exts

class RoleVisibility(models.Model):
    class Meta:
        db_table = 'visibilities'
        managed = False
        app_label = 'people'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(max_length=100)

    description = models.TextField()


###########
## Roles ##
###########

class Role(models.Model):
    class Meta:
        db_table = 'roles'  # in schema 'people'
        managed = False
        app_label = 'people'

    def __unicode__(self):
        return self.alias

    id = exts.primary_key_from_meta(Meta)

    alias = models.CharField(max_length=100)

    visibility_level = models.ForeignKey(
        RoleVisibility,
        db_column='visibilitylevel')

    is_group_root = models.BooleanField(
        db_column='isgrouproot')

    is_active = models.BooleanField(
        db_column='isactive')

    ordering = models.IntegerField()
