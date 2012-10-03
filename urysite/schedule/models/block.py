"""Models concerning schedule blocks."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
import timedelta


###########
## Block ##
###########

class Block(models.Model):
    """A block of programming.

    Schedule blocks group together related shows, such as specialist
    music and flagship blocks, by time or by common naming
    conventions.

    """

    class Meta:
        db_table = 'block'  # In schema 'schedule'
        ordering = ('priority',)
        app_label = 'schedule'

    def __unicode__(self):
        return self.name

    id = exts.primary_key_from_meta(Meta)

    name = models.CharField(
        max_length=255,
        help_text='The publicly viewable name for this block.')

    tag = models.CharField(
        max_length=100,
        help_text="""The machine-readable string identifier used, for
            example, as the prefix of the CSS classes used to colour
            this block.

            """)

    priority = models.IntegerField(
        help_text="""The priority of this block when deciding which
            block a show falls into.

            A lower number indicates a higher priority.

            """)

    is_listable = models.BooleanField(
        default=False,
        help_text="""If true, the block appears in lists of blocks,
            allowing people to find shows in that block.

            """)


class BlockRangeRule(models.Model):
    """Block rules that associate timeslots falling into given ranges
    with corresponding blocks.

    This is the lowest priority rule type.

    """

    class Meta:
        db_table = 'block_range_rule'  # In schema 'schedule'
        app_label = 'schedule'

    def __unicode__(self):
        return "{0} to {1} -> {2}".format(
            self.start_time,
            self.end_time,
            self.block)

    id = exts.primary_key_from_meta(Meta)

    block = models.ForeignKey(
        Block,
        help_text='The block this rule matches against.')

    start_time = timedelta.TimedeltaField(
        help_text='The start of the range defining this block.')

    end_time = timedelta.TimedeltaField(
        help_text='The end of the range defining this block.')
