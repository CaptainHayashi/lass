"""In which a mixin that allows attached metadata on a model to be
accessed in a common manner is described.

"""

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from metadata.models.key import MetadataKey


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
