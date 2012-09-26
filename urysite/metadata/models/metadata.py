"""Models for the URY text metadata system.

To add metadata to a model, create a subclass of 'Metadata' for that
model, descend the model from 'MetadataSubjectMixin', and fill out
the methods identified in those two classes.

"""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from urysite import model_extensions as exts


class MetadataKey(models.Model):
    """A metadata key, which defines the semantics of a piece of
    metadata.

    """

    class Meta:
        db_table = 'metadata_key'  # in schema 'schedule'
        managed = False
        app_label = 'schedule'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=255,
        help_text="""A human-readable name for the metadata key.""")

    allow_multiple = models.BooleanField(
        default=False,
        help_text="""If True, multiple instances of this metadata key
            can be active at the same time (e.g. arbitrary tags).

            """)

    description = models.TextField(
        blank=True,
        help_text="""A human-readable description of the semantics
        (meaning) of this key, and where it is applicable.

        """)


class Metadata(models.Model):
    """An item of textual show metadata.

    """

    class Meta:
        abstract = True
        managed = False
        get_latest_by = 'effective_from'

    def __unicode__(self):
        """Returns a concise Unicode representation of the metadata.

        """
        return '%s -> %s (ef %s on %s)' % (
            self.metadata_key.name,
            self.metadata_value,
            self.effective_from,
            self.attached_element())

    def attached_element():
        """The element to which this metadatum is attached.

        This should be overridden in concrete models descending from
        Metadata.

        """
        pass

    # REMEMBER TO ADD THIS TO ANY DERIVING CLASSES!
    # id = exts.primary_key_from_meta(Meta)

    metadata_key = models.ForeignKey(
        MetadataKey,
        help_text="""The key, or type, of the metadata entry.""",
        db_column='metadata_key_id')

    metadata_value = models.TextField(
        help_text="""The value of this metadata entry.""")

    effective_from = models.DateTimeField(
        auto_now_add=True)

    # These two foreign keys have to have their models deferred
    # because otherwise there would be a cyclic dependency between
    # people and urysite over metadata.
    creator = models.ForeignKey(
        'people.Creator',
        help_text="""The person who created this metadata entry.""",
        db_column='memberid',
        related_name='%(app_label)s_%(class)s_created_set')

    approver = models.ForeignKey(
        'people.Approver',
        help_text="""The person who approved this metadata entry,
            if it has indeed been approved.

            """,
        null=True,
        db_column='approvedid',
        related_name='%(app_label)s_%(class)s_approved_set')


class MetadataSubjectMixin(object):
    """Mixin granting the ability to access metadata.

    """

    # Don't forget to override this!
    def metadata_set(self):
        """Returns the QuerySet that provides the metadata.

        This should invariably be overridden in mixin users.

        """
        pass

    # Also override this, if relevant
    def metadata_parent(self):
        """Returns an object that metadata should be inherited from
        if not assigned for this object.

        This can return None if no inheriting should be done.

        """
        return None

    ## COMMON METADATA KEYS ##

    def title(self):
        """Provides the current title of the item.

        The title is extracted from the item metadata.

        """
        return self.current_metadatum('title')

    def title_image(self):
        """Provides the path (within the image directory) of an
        image that can be used in place of this item's 'title'
        metadatum in headings, if such an image exists.

        This is extracted from the item metadata.

        """
        return self.current_metadatum('title_image')

    def description(self):
        """Provides the current description of the item.

        The description is extracted from the item metadata.

        """
        return self.current_metadatum('description')

    def metadatum_at_date(self, date, key, inherit=True):
        """Returns the value of the given metadata key that was
        in effect at the given date.

        The value returned is the most recently effected value
        that is approved and not made effective after the given
        date.

        If no such item exists, and inherit is True, the metadatum
        request will propagate up to the parent if it exists.

        """
        key_id = MetadataKey.objects.get(name=key).id
        try:
            result = self.metadata_set().filter(
                metadata_key__pk=key_id,
                approver__isnull=False,
                effective_from__lte=date).order_by(
                    '-effective_from').latest().metadata_value
        except ObjectDoesNotExist:
            if inherit is True and self.metadata_parent() is not None:
                result = self.metadata_parent().current_metadatum(
                    key,
                    inherit)
            else:
                result = None
        return result

    def current_metadatum(self, key, inherit=True):
        """Retrieves the current value of the given metadata key.

        The current value is the most recently effected value that
        is approved and not in the future.

        If no such item exists, and inherit is True, the metadatum
        request will propagate up to the parent if it exists.

        """
        return self.metadatum_at_date(timezone.now(), key, inherit)
