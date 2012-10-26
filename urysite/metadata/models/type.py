"""Common base class for type-of models."""

from django.db import models
from django.core.cache import cache


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

    ## CLASS METHODS ##

    @classmethod
    def get(cls, identifier):
        """User-friendly type get function.

        If the input is an integer, it will be treated as the target
        type's primary key.

        If the input is a string, it will be treated as the target
        type's name (case-insensitively).

        If the input is an instance of cls itself, it will simply be
        returned.

        Else, TypeError will be raised.

        """
        cache_key = u'type-{0}-{1}-{2}'.format(
            cls._meta.app_label,
            cls._meta.object_name,
            identifier.replace('-', '--').replace(' ', '-')
            # ^-- Memcached refuses keys with spaces
        )
        cached = cache.get(cache_key)
        if cached:
            result = cached
        else:
            if isinstance(identifier, cls):
                result = identifier
            elif isinstance(identifier, int):
                result = cls.objects.get(pk=identifier)
            elif isinstance(identifier, basestring):
                result = cls.objects.get(name__iexact=identifier)
            else:
                raise TypeError(
                    "Input of incorrect type (see docstring)."
                )
            cache.set(cache_key, result, 60 * 60)
        return result
