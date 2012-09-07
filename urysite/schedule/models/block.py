"""Models concerning schedule blocks."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from schedule.models.show import Show


class Block(models.Model):
    """A block of programming.

    Schedule blocks group together related shows, such as specialist
    music and flagship blocks, by time or by common naming
    conventions.

    """

    class Meta:
        db_table = 'block'  # In schema 'schedule'
        managed = False  # It's in another schema, so can't manage
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


# Block matching rules #


class BlockNameRule(models.Model):
    """A name-based matching rule for blocks.

    A block matching rule that matches shows whose names match the
    given regular expression.

    """

    class Meta:
        db_table = 'block_name_rule'  # In schema 'schedule'
        managed = False  # It's in another schema, so can't manage
        app_label = 'schedule'

    def __unicode__(self):
        return "%s -> %s" % (self.regex, self.block)

    id = exts.primary_key_from_meta(Meta)

    block = models.ForeignKey(
        Block,
        help_text='The block this rule matches against.')

    regex = models.CharField(
        max_length=255,
        help_text="""The Perl-compatible regular expression that
            show names must match in order to match this block.

        """)


class BlockShowRule(models.Model):
    """A show-based matching rule for blocks.

    A block matching rule that matches the attached show only.

    This rule takes precedence over all other rules, except any
    directly matching timeslots.

    """

    class Meta:
        db_table = 'block_show_rule'  # In schema 'schedule'
        managed = False  # It's in another schema, so can't manage
        app_label = 'schedule'

    def __unicode__(self):
        return "%s -> %s" % (self.show, self.block)

    id = exts.primary_key_from_meta(Meta)

    block = models.ForeignKey(
        Block,
        help_text='The block this rule matches against.')

    show = models.ForeignKey(
        Show,
        help_text='The show this rule assigns a block to.')
