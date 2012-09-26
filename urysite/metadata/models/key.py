"""The MetadataKey model, which forms the key in the metadata
key-value storage system.

"""
from django.db import models
from urysite import model_extensions as exts


class MetadataKey(models.Model):
    """A metadata key, which defines the semantics of a piece of
    metadata.

    """

    class Meta:
        db_table = 'metadata_key'  # in schema 'schedule'
        managed = False
        app_label = 'metadata'

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
