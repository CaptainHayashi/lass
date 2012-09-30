"""Models for the URY text metadata system.

To add metadata to a model, create a subclass of 'Metadata' for that
model, descend the model from 'MetadataSubjectMixin', and fill out
the methods identified in those two classes.

"""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from metadata.models.key import MetadataKey
from people.mixins import CreatableMixin
from people.mixins import ApprovableMixin
from metadata.mixins import EffectiveRangeMixin


class Metadata(ApprovableMixin,
               CreatableMixin,
               EffectiveRangeMixin):
    """An item of textual show metadata.

    """

    class Meta(EffectiveRangeMixin.Meta):
        abstract = True
        get_latest_by = 'effective_from'

    def __unicode__(self):
        """Returns a concise Unicode representation of the metadata.

        """
        return '{0} -> {1} (ef {2}->{3} on {4})' % (
            self.metadata_key.name,
            self.metadata_value,
            self.effective_from,
            self.effective_to,
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
