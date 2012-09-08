"""Models concerning crediting URY members for the existence of data.

"""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from people.models import Person, Creator, Approver


class CreditType(models.Model):
    """A type of credit, as used in ShowCredit.

    Types of show credit might include "presenter", "director",
    "reporter" and so on.

    """

    class Meta:
        db_table = 'credit_type'  # in schema 'people'
        managed = False  # have to do this due to schema, probably
        app_label = 'people'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=255,
        help_text='Human-readable, singular name for the type.')

    plural = models.CharField(
        max_length=255,
        help_text='Human readable plural for the type.')

    is_in_byline = models.BooleanField(
        default=False,
        help_text='If true, credits of this type appear in by-lines.')

    # More to come here eventually
