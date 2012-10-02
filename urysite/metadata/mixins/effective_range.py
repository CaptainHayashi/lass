"""A partial implementation of DateRangeMixin's interface by which
the date range is fulfilled by an 'effective from' and an 'effective
to' pair of fields.

"""

from django.db import models
from metadata.mixins.date_range import DateRangeMixin


class EffectiveRangeMixin(models.Model, DateRangeMixin):
    """Mixin adding an 'effective from' and 'effective to' pair of
    fields that implement DateRangeMixin.

    """

    class Meta:
        abstract = True

    effective_from = models.DateTimeField(
        db_column='effective_from',
        null=True,
        blank=True,
        help_text="""The date from which this item applies.
            If this is not given, then the item is inert, which
            is usually the case when it has not been approved.

            """)

    effective_to = models.DateTimeField(
        db_column='effective_to',
        null=True,
        blank=True,
        help_text="""The date on which this credit ceases to apply,
            if any.

            """)

    def range_start(self):
        return self.effective_from

    def range_end(self):
        return self.effective_to
