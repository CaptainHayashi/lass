"""Interoperation with legacy SIS messaging."""

# NOTE: THIS IS SUPPOSED TO BE TEMPORARY CODE #

# This should probably live somewhere else.

from django.db import models
from urysite import model_extensions as exts


class SISComm(models.Model):
    """An entry in the SIS communication system."""

    class Meta:
        db_table = 'messages'
        managed = False

    id = exts.primary_key('commid')

    # This should be a fkey to season_timeslot
    # but due to old schema compatibility reasons it isn't.
    timeslotid = models.IntegerField()

    commtypeid = models.IntegerField()

    sender = models.CharField(max_length=64)

    date = models.DateTimeField(auto_now_add=True)

    subject = models.CharField(max_length=255)

    content = models.TextField()

    statusid = models.IntegerField()

    comm_source = models.IPAddressField()
