from django.db import models
from urysite import model_extensions as exts
from lass_utils.models import Type
from lass_utils.mixins import SubmittableMixin


class ChartType(Type):
    """A type of chart, for example recommended listening or
    URY Chart.

    """
    def latest_release(self):
        """
        Returns the latest chart release for this type, if one
        exists.

        Raises `ChartRelease.DoesNotExist` if the given chart has no
        releases.

        """
        return self.chartreleases_set.latest()

    class Meta(Type.Meta):
        db_table = 'chart_type'

    id = exts.primary_key_from_meta(Meta)


class ChartRelease(SubmittableMixin):
    """A chart release, into which chart rows are entered."""

    class Meta(SubmittableMixin.Meta):
        db_table = 'chart_release'
        get_latest_by = 'date_submitted'
        ordering = ['date_submitted']

    id = exts.primary_key_from_meta(Meta)

    type = models.ForeignKey(
        ChartType,
        db_column='chart_type_id')


class ChartRow(models.Model):
    """A row in a chart."""

    class Meta:
        db_table = 'chart_row'
        ordering = ['position']
        unique_together = ('id', 'position')

    id = exts.primary_key_from_meta(Meta)

    chart = models.ForeignKey(
        ChartRelease,
        db_column='chart_release_id')

    position = models.PositiveSmallIntegerField()

    track = models.CharField(max_length=255)

    artist = models.CharField(max_length=255)

    def last_position(self):
        """Gets the position of this item in the chart published
        before the one this item belongs to.

        Returns None if the item was not on the chart last time.

        """
        prev_charts = ChartType.objects.filter(
            date_submitted__lt=self.chart.date_submitted
        )
        if prev_charts:
            prev_chart = prev_charts.latest()
            try:
                last_position = prev_chart.chartrow_set.get(
                    track__exact=self.track,
                    artist__exact=self.position).position
            except ChartRow.DoesNotExist:
                last_position = None
        else:
            last_position = None
        return last_position
