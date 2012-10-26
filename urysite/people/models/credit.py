"""Models concerning crediting URY members for the existence of data.

"""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from people.models import Person
from people.mixins import CreatableMixin
from people.mixins import ApprovableMixin
from metadata.mixins import EffectiveRangeMixin


class CreditType(models.Model):
    """A type of credit, as used in ShowCredit.

    Types of show credit might include "presenter", "director",
    "reporter" and so on.

    """

    class Meta:
        ordering = ['name']
        db_table = 'credit_type'  # in schema 'people'
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


class Credit(ApprovableMixin,
             CreatableMixin,
             EffectiveRangeMixin):
    """Abstract base class for credit models."""

    class Meta(EffectiveRangeMixin.Meta):
        ordering = ['person']
        abstract = True

    credit_type = models.ForeignKey(
        CreditType,
        db_column='credit_type_id',
        help_text='The type of credit the person is assigned.')

    person = models.ForeignKey(
        Person,
        db_column='creditid',
        help_text='The person being credited.',
        related_name='credited_%(app_label)s_%(class)s_set')

    ## MAGIC METHODS ##

    def __unicode__(self):
        return self.person.full_name()
