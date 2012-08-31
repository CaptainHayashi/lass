from django.db import models


# BANNERS #

class BannerCategory(models.Model):
    class Meta:
        db_table = 'banner_category'
        verbose_name = 'banner category'
        verbose_name_plural = 'banner categories'
        managed = False

    def __unicode__(self):
        return self.descr

    id = models.AutoField(
        primary_key=True,
        db_column='categoryid')
    descr = models.TextField()


class Banner(models.Model):
    class Meta:
        db_table = 'banner'
        ordering = ['ordering']
        managed = False

    def __unicode__(self):
        return self.name

    id = models.AutoField(
        primary_key=True,
        db_column='bannerid')
    name = models.TextField()
    filename = models.TextField()
    uri = models.URLField()
    days = models.TextField()
    category = models.ForeignKey(
        BannerCategory,
        db_column='categoryid')
    ordering = models.IntegerField()
