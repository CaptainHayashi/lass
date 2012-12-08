"""Models pertaining to LeRouge roles"""

from django.db import models
from metadata.models import TextMetadata
from metadata.mixins import MetadataSubjectMixin
from urysite import model_extensions as exts


class RoleVisibility(models.Model):
    class Meta:
        db_table = 'role_visibility'
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
        app_label = 'people'

    def __unicode__(self):
        return self.alias

    def metadata_strands(self):
        return {
            'text': self.roletextmetadata_set
        }

    def email(self):
        """Retrieves the email address that can be used to reach
        members of this role, if any.

        """
        # TODO: Only publicly emailable roles should return here
        return '@'.join((self.alias, 'ury.org.uk'))

    id = exts.primary_key_from_meta(Meta)

    alias = models.CharField(max_length=100)

    visibility_level = models.ForeignKey(
        RoleVisibility,
        db_column='visibilitylevel')

    is_active = models.BooleanField(
        db_column='isactive')

    ordering = models.IntegerField()

    parents = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='RoleInheritance'
    )

    @staticmethod
    def make_foreign_key(src_meta, db_column='role_id'):
        """Shortcut for creating a field that links to a role, given
        the source model's metadata class.

        """
        return exts.foreign_key(src_meta, 'Role', db_column, 'role')


class GroupType(models.Model):
    """A type of role group.

    """
    class Meta:
        db_table = 'group_type'  # in schema 'people'
        app_label = 'people'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=20,
        help_text="A human-friendly name for the group type.")


class GroupRootRole(Role):
    """A group root is a role that defines a role group,
    consisting of itself and all roles inheriting from it.

    Group roots are usually used to define 'teams' of roles.

    """
    class Meta:
        db_table = 'group_root_role'  # in schema 'people'
        app_label = 'people'

    group_root_id = exts.primary_key_from_meta(Meta)

    role_id = models.OneToOneField(
        Role,
        parent_link=True)

    group_type = models.ForeignKey(
        GroupType)

    group_leader = models.ForeignKey(
        Role,
        null=True,
        blank=True,
        related_name='led_groups_set',
        help_text="""An optional link to a role who is considered to
            represent the "leader" of the group, if any.  For
            example, if there is a Computing Team, the Head of
            Computing role would be the group leader.

            """)

RoleTextMetadata = TextMetadata.make_model(
    Role,
    'schedule',
    'RoleTextMetadata',
    'role_metadata',
    'role_metadata_id',
    'role_id'
)


class RoleInheritance(models.Model):
    """A parent-child inheritance relationship between roles.

    The role inheritance system causes children to inherit their
    privileges from parents, as well as making children of group
    roots become identified as part of the group (team) the group
    root defines.

    """
    class Meta:
        db_table = 'role_inheritance'  # in schema 'people'
        verbose_name = 'role inheritance'
        verbose_name_plural = 'role inheritances'
        app_label = 'people'

    def __unicode__(self):
        return '{0} --|> {1}'.format(self.child, self.parent)

    id = exts.primary_key_from_meta(Meta)

    parent = models.ForeignKey(
        Role,
        db_column='parent_id',
        related_name='role_children_set')

    child = models.ForeignKey(
        Role,
        db_column='child_id',
        related_name='role_parents_set')
