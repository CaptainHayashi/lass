"""
Models for the home page grid system.
"""

from django.conf import settings
from django.db import models

from lass_utils.models import Type
from metadata.models.text import TextMetadata
from metadata.mixins import MetadataSubjectMixin
from uryplayer.models import PodcastChannel
from urysite import model_extensions as exts


class GridBlock(Type, MetadataSubjectMixin):
    """
    A block in the home page grid.

    Grid blocks are akin to widgets or dashboard items in other
    analogous systems.

    A `GridBlock` does not contain any positioning information; the
    `GridBlockInstance` and `Grid` models are concerned with this.

    """
    if hasattr(settings, 'GRID_BLOCK_DB_ID_COLUMN'):
        id = models.AutoField(
            primary_key=True,
            db_column=getattr(settings, 'GRID_BLOCK_DB_ID_COLUMN')
        )
    width = models.IntegerField(
        default=1,
        help_text='The width of this block, in multiples of one '
        'regularly sized block.'
    )
    height = models.IntegerField(
        default=1,
        help_text='The height of this block, in multiples of one '
        'regularly sized block.'
    )
    view_name = models.CharField(
        max_length=255,
        help_text='The name of the view to embed in this block.'
    )
    cache_duration = models.IntegerField(
        default=0,
        help_text='The duration, in seconds, that this block should '
        'be cached for.'
    )
    more_url = models.CharField(
        max_length=255,
        blank=True,
        help_text='If given, the name of a Django URL to link to '
        'in the block footer as a source of more information '
        'on the subject of the contents of this block. '
    )
    is_more_url_absolute = models.BooleanField(
        default=False,
        help_text='If True, the More URL is interpreted as a raw URL;'
        ' otherwise it is parsed as a Django URL name.'
    )
    podcast_channel = models.ForeignKey(
        PodcastChannel,
        null=True,
        blank=True,
        help_text='If given, a podcast channel that should be linked '
        'to this block.'
    )
    ajax_poll_duration = models.IntegerField(
        default=0,
        help_text='The number of seconds between each AJAX poll if '
        'an `ajax_url` is provided.  If 0, AJAX is disabled.'
    )

    ## OVERRIDES ##

    def metadata_strands(self):
        """
        Returns the set of metadata strands available for this grid
        block.

        """
        return {
            'text': self.gridblocktextmetadata_set
        }

    ## ADDITIONAL METHODS ##

    @classmethod
    def make_foreign_key(cls):
        """
        Shortcut for creating a field that links to a grid.

        """
        _FKEY_KWARGS = {}
        if hasattr(settings, 'GRID_BLOCK_DB_FKEY_COLUMN'):
            _FKEY_KWARGS['db_column'] = (
                settings.GRID_BLOCK_DB_FKEY_COLUMN
            )
        return models.ForeignKey(
            cls,
            help_text='The grid associated with this item.',
            **_FKEY_KWARGS
        )

    class Meta(Type.Meta):
        if hasattr(settings, 'GRID_BLOCK_DB_TABLE'):
            db_table = getattr(settings, 'GRID_BLOCK_DB_TABLE')
        app_label = 'grid'

GridBlockTextMetadata = TextMetadata.make_model(
    GridBlock,
    'grid',
    'GridBlockTextMetadata',
    getattr(settings, 'GRID_BLOCK_TEXT_METADATA_DB_TABLE', None),
    getattr(settings, 'GRID_BLOCK_TEXT_METADATA_DB_ID_COLUMN', None),
    fkey=GridBlock.make_foreign_key()
)


class Grid(Type):
    """
    An object representing a grid of `GridBlock`s.

    """

    width = models.IntegerField(
        default=3,
        help_text='The maximum width, in multiples of one standard'
        'block, that this grid will allow.'
    )
    height = models.IntegerField(
        default=6,
        help_text='The maximum height, in multiples of one standard'
        'block, that this grid will allow.'
    )
    blocks = models.ManyToManyField(
        GridBlock,
        through='GridBlockInstance'
    )

    def ordered_list(self):
        """Returns a list of blocks active on this grid, ordered to render.

        Provides all the blocks
        This grid has instances for
        Ordered Y then X
        """
        return GridBlock.objects.in_bulk(
            self.gridblockinstance_set.all().values_list(
                'grid_block', flat=True
            )
        ).values()

    class Meta(Type.Meta):
        db_table = 'grid'
        app_label = 'grid'

    id = exts.primary_key_from_meta(Meta)


class GridBlockInstance(models.Model):
    """
    An instance of a grid block within a grid.

    """

    x = models.IntegerField(
        help_text='The X position, starting from 0, of this block in'
        'its grid.'
    )
    y = models.IntegerField(
        help_text='The Y position, starting from 0, of this block in'
        'its grid.'
    )
    grid = models.ForeignKey(
        Grid,
        help_text='The grid to assign this block to.'
    )
    grid_block = models.ForeignKey(
        GridBlock,
        help_text='The grid block to assign to a grid.'
    )

    class Meta:
        db_table = 'grid_block_instance'
        app_label = 'grid'
        unique_together = ('grid', 'x', 'y')
        ordering = ('y', 'x')

    id = exts.primary_key_from_meta(Meta)
