"""Common base class for type-of models."""

from django.db import models


class Type(models.Model):
    class Meta:
        abstract = True

    # Remember to add this
    # id = exts.primary_key_from_meta(Meta)

    name = models.SlugField(
        help_text="""The short name of this type entry, which should
            be used to identify it in code.

            """)

    description = models.TextField(
        help_text="""A human-readable description of this type entry
            and its semantics.

            """)

    ## MAGIC METHODS ##

    def __unicode__(self):
        return self.name
