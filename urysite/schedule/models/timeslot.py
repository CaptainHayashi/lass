"""Models concerning URY schedule timeslots."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from schedule.models import BlockRangeRule
from schedule.models.season import Season
from schedule.models.metadata import Metadata, MetadataSubjectMixin
from django.utils import timezone
from datetime import timedelta as td
from django.db.models import Q
import timedelta


class Timeslot(models.Model, MetadataSubjectMixin):
    """A slot in the URY schedule allocated to a show.

    URY timeslots can overlap, because not all timeslots represent
    on-air shows (the schedule system is used to schedule demos,
    in-studio recordings, and outside broadcasts as well as in-studio
    shows).  Because of this, a timeslot CANNOT safely be uniquely
    identified from its show and time range - use the timeslot ID.
    """

    class Meta:
        db_table = 'show_season_timeslot'
        managed = False
        verbose_name = 'show timeslot'
        get_latest_by = 'start_time'
        app_label = 'schedule'

    def metadata_set(self):
        """Provides the set of this timeslot's metadata."""
        return self.timeslotmetadata_set

    def metadata_parent(self):
        """Provides the metadata inheritance parent of this timeslot.

        """
        return self.season

    def block(self):
        """Returns the block that the timeslot is in, if any.

        This will return a Block object if a block is matched, or
        None if there wasn't one (one can associate to Block.default()
        in this case, if a block is needed).

        """
        # Season rules take precedence
        season_block = self.season.block()
        if season_block is None:
            # TODO: add direct rules for timeslot
            # Now do season based checks
            #block_show_matches = self.blockshowrule_set.filter(
            #    show=self).order_by('-priority')
            #if block_show_matches.exists():
            #block = block_show_matches[0]
            #else:
            # TODO: add time-range rules for timeslot

            # Get start as distance from midnight, and end as
            # distance plus duration
            slot_start = self.start_time - self.start_time.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0)
            slot_end = slot_start + self.duration
            assert slot_start < slot_end, "Slot starts after end."

            # Because the block range is in local time and the slot
            # dates are in UTC, we'll need to subtract the local
            # time's UTC offset in the calculations.
            utc = self.start_time.astimezone(
                timezone.get_current_timezone()).utcoffset()
            day = td(days=1)

            # Now we can do simple inequalities to match the
            # time-ranges, with the caveat that we'll have to check
            # against the slot projected forwards one day to make
            # sure that ranges starting the day before the show and
            # ending on the day of the show are considered correctly.
            block_range_matches = BlockRangeRule.objects.filter(
                Q(start_time__lte=slot_start + utc,
                  end_time__gte=slot_end + utc) |
                Q(start_time__lte=slot_start + utc + day,
                  end_time__gte=slot_end + utc + day)).order_by(
                      '-block__priority')
            if block_range_matches.exists():
                block = block_range_matches[0].block
            else:
                block = None
        else:
            block = season_block
        return block

    def __unicode__(self):
        """Provides a Unicode representation of this timeslot."""
        return "%s (%s to %s)" % (
            self.season,
            self.start_time,
            self.end_time())

    id = exts.primary_key_from_meta(Meta)

    season = Season.make_foreign_key(Meta)

    start_time = models.DateTimeField(
        db_column='start_time',
        help_text='The date and time of the start of this timeslot.')

    duration = timedelta.TimedeltaField(
        db_column='duration',
        help_text='The duration of the timeslot.')

    def end_time(self):
        """Calculates the end time of this timeslot."""
        return self.start_time + self.duration

    def by_line(self):
        """Returns a by-line for the timeslot (see Show.by_line for
        details).

        """
        return self.season.show.by_line(self.start_time)

    def is_real_show(self):
        """Returns True if the timeslot references a real show.

        For example, this will return False if the timeslot is for
        the Jukebox.

        """
        return self.season.is_real_show()

    @staticmethod
    def make_foreign_key(src_meta,
                         db_column='show_season_timeslot_id'):
        """Shortcut for creating a field that links to a timeslot,
        given the source model's metadata class.

        """
        return exts.foreign_key(
            src_meta,
            'Timeslot',
            db_column,
            'timeslot')


class TimeslotMetadata(Metadata):
    """An item of textual Timeslot metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'timeslot_metadata'  # in schema 'schedule'
        verbose_name = 'timeslot metadatum'
        verbose_name_plural = 'timeslot metadata'
        app_label = 'schedule'

    def attached_element(self):
        return self.timeslot

    id = exts.primary_key_from_meta(Meta)

    timeslot = Timeslot.make_foreign_key(Meta)
