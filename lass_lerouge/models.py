"""Models pertaining to LeRouge roles"""

from django.conf import settings
from django.db import models

from metadata.models import TextMetadata
from metadata.models import ImageMetadata
from metadata.mixins import MetadataSubjectMixin
from urysite import model_extensions as exts


class RoleVisibility(models.Model):
    class Meta:
        db_table = 'role_visibility'
        app_label = 'lass_lerouge'

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
        if hasattr(settings, 'ROLE_DB_TABLE'):
            db_table = settings.ROLE_DB_TABLE
        app_label = 'lass_lerouge'

    def __unicode__(self):
        return self.alias

    def metadata_strands(self):
        return {
            'text': self.roletextmetadata_set,
            'image': self.roleimagemetadata_set,
        }

    def email(self):
        """Retrieves the email address that can be used to reach
        members of this role, if any.

        """
        # TODO: Only publicly emailable roles should return here
        return '@'.join((self.alias, 'ury.org.uk'))

    if hasattr(settings, 'ROLE_DB_ID_COLUMN'):
        id = models.AutoField(
            primary_key=True,
            db_column=settings.ROLE_DB_ID_COLUMN
        )

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

    @classmethod
    def make_foreign_key(cls):
        """
        Shortcut for creating a field that links to a role.

        """
        _FKEY_KWARGS = {}
        if hasattr(settings, 'ROLE_DB_FKEY_COLUMN'):
            _FKEY_KWARGS['db_column'] = settings.ROLE_DB_FKEY_COLUMN
        return models.ForeignKey(
            cls,
            help_text='The role associated with this item.',
            **_FKEY_KWARGS
        )


class GroupType(models.Model):
    """A type of role group.

    """
    class Meta:
        db_table = 'group_type'  # in schema 'lass_lerouge'
        app_label = 'lass_lerouge'

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
        app_label = 'lass_lerouge'

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
    'lass_lerouge',
    'RoleTextMetadata',
    getattr(
        settings, 'ROLE_TEXT_METADATA_DB_TABLE',
        None
    ),
    getattr(
        settings, 'ROLE_TEXT_METADATA_DB_ID_COLUMN',
        None
    ),
    fkey=Role.make_foreign_key(),
)


RoleImageMetadata = ImageMetadata.make_model(
    Role,
    'lass_lerouge',
    'RoleImageMetadata',
    getattr(
        settings, 'ROLE_IMAGE_METADATA_DB_TABLE',
        None
    ),
    getattr(
        settings, 'ROLE_IMAGE_METADATA_DB_ID_COLUMN',
        None
    ),
    fkey=Role.make_foreign_key(),
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
        app_label = 'lass_lerouge'

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
