"""Models pertaining to LeRouge roles"""

from django.db import models
from urysite.models import Metadata, MetadataSubjectMixin
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


class Role(models.Model, MetadataSubjectMixin):
    """A role in the URY roles system.

    A role is a group of people, used to delineate privileges
    as well as route email and implement team groupings.

    """
    class Meta:
        db_table = 'role'  # in schema 'people'
        managed = False
        app_label = 'people'

    def __unicode__(self):
        return self.alias

    def metadata_set(self):
        return self.rowmetadata_set

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

    parents = models.ManyToManyField(
            'self',
            symmetrical=False,
            through='RoleInheritance')

    @staticmethod
    def make_foreign_key(src_meta, db_column='role_id'):
        """Shortcut for creating a field that links to a role, given
        the source model's metadata class.

        """
        return exts.foreign_key(src_meta, 'Role', db_column, 'role')


class RoleMetadata(Metadata):
    """An item of textual role metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'role_metadata'  # in schema 'people'
        verbose_name = 'role metadatum'
        verbose_name_plural = 'role metadata'
        app_label = 'people'

    def attached_element(self):
        return self.role

    id = exts.primary_key_from_meta(Meta)

    role = Role.make_foreign_key(Meta)


class RoleInheritance(models.Model):
    """A parent-child inheritance relationship between roles.

    The role inheritance system causes children to inherit their
    privileges from parents, as well as making children of group
    roots become identified as part of the group (team) the group
    root defines.

    """
    class Meta:
        db_table = 'role_inheritance'  # in schema 'people'
        managed = False
        verbose_name = 'role inheritance'
        verbose_name_plural = 'role inheritances'
        app_label = 'people'

    def __unicode__(self):
        return '{0} --|> {1}', self.child, self.parent

    id = exts.primary_key_from_meta(Meta)

    parent = models.ForeignKey(
        Role,
        db_column='parent_id',
        related_name='role_children_set')

    child = models.ForeignKey(
        Role,
        db_column='child_id',
        related_name='role_parents_set')
