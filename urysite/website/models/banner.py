"""Models used for the banner rotation system.

"""

from django.db import models
from urysite import model_extensions as exts
from metadata.models import Type
from urysite.models import OrderedModel
from people.mixins import ApprovableMixin
from people.mixins import CreatableMixin
from metadata.mixins import EffectiveRangeMixin
from datetime import time
from django.utils import timezone


class BannerType(Type):
    class Meta(Type.Meta):
        db_table = 'banner_type'
        verbose_name = 'banner type'
        verbose_name_plural = 'banner types'
        app_label = 'website'

    id = exts.primary_key_from_meta(Meta)


class Banner(models.Model):
    class Meta:
        db_table = 'banner'
        app_label = 'website'

    def __unicode__(self):
        return self.alt

    id = exts.primary_key_from_meta(Meta)

    alt = models.TextField(
        help_text="""The text used as alt text/mouseover text on this
            banner; it should serve the same purpose as the banner
            image for presenting information or describing the target
            link.

            """)

    filename = models.ImageField(
        upload_to='banners')

    target = models.URLField(
        blank=True,
        help_text="""The URI that the banner links to when clicked;
            if this is empty, the banner will not be clickable.

            """)

    type = models.ForeignKey(
        BannerType,
        db_column='banner_type_id',
        help_text="""The banner type, which is generally used to
            decide where the banner appears on the website (front
            page, team blogs, etc.)
            """)


class BannerLocation(Type):
    """A location on the website that a banner campaign can be run
    in.

    """
    class Meta(Type.Meta):
        db_table = 'banner_location'
        app_label = 'website'

    id = exts.primary_key_from_meta(Meta)


class BannerCampaign(ApprovableMixin,
                     CreatableMixin,
                     EffectiveRangeMixin):
    """A run of a banner on a website location, into which multiple
    banner slots can be entered.

    """
    class Meta:
        db_table = 'banner_campaign'
        app_label = 'website'

    id = exts.primary_key_from_meta(Meta)

    location = models.ForeignKey(
        BannerLocation,
        db_column='banner_location_id',
        help_text="""The location on the website the banner will
            appear in.

            """)

    banner = models.ForeignKey(
        Banner,
        db_column='banner_id',
        help_text="""The banner this campaign is being run with.""")

    ## MAGIC METHODS ##

    def __unicode__(self):
        return "{0} ({1}, {2}->{3})".format(self.banner.alt,
                                           self.location,
                                           self.effective_from,
                                           self.effective_to)


class BannerTimeslot(OrderedModel,
                     ApprovableMixin,
                     CreatableMixin):
    """A timeslot on a banner campaign, marking a period of time on
    a given weekday for the banner to appear in the campaign
    rotation.

    """
    class Meta:
        db_table = 'banner_timeslot'
        app_label = 'website'

    campaign = models.ForeignKey(
        BannerCampaign,
        db_column='banner_campaign_id')

    day = models.PositiveSmallIntegerField(
        help_text="""The day of the week on which this banner slot
            will run, with Monday as day 1 and Sunday as day 7.
            """,
        choices=(
            (1, 'Mondays'),
            (2, 'Tuesdays'),
            (3, 'Wednesdays'),
            (4, 'Thursdays'),
            (5, 'Fridays'),
            (6, 'Saturdays'),
            (7, 'Sundays')
        ))

    from_time = models.TimeField(
        help_text="""The time of day when the banner will start
            rotating.
            """,
        default=time(
            hour=0,
            minute=0,
            second=0,
            tzinfo=timezone.get_current_timezone()))

    to_time = models.TimeField(
        help_text="""The time of day when the banner will stop
            rotating.
            """,
        default=time(
            hour=23,
            minute=59,
            second=59,
            tzinfo=timezone.get_current_timezone()))
