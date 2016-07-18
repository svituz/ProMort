from django.db import models
from django.contrib.auth.models import User
from slides_manager.models import Slide


class Slice(models.Model):
    label = models.CharField(max_length=10, blank=False)
    slide = models.ForeignKey(Slide, on_delete=models.PROTECT,
                              blank=False, related_name='slices')
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False)
    creation_data = models.DateTimeField(auto_now_add=True)
    roi_json = models.TextField(blank=False)
    total_cores = models.IntegerField(blank=False, default=0)
    positive_cores = models.IntegerField(blank=False, default=0)

    class Meta:
        unique_together = ('label', 'slide')


class Core(models.Model):
    label = models.CharField(max_length=10, blank=False)
    slice = models.ForeignKey(Slice, on_delete=models.PROTECT,
                              blank=False, related_name='cores')
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    roi_json = models.TextField(blank=False)
    length = models.FloatField(blank=False, default=0.0)
    area = models.FloatField(blank=False, default=0.0)

    class Meta:
        unique_together = ('label', 'slice')


class CellularFocus(models.Model):
    label = models.CharField(max_length=10, blank=False)
    core = models.ForeignKey(Core, on_delete=models.PROTECT,
                             blank=False, related_name='cellular_focuses')
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    roi_json = models.TextField(blank=False)
    length = models.FloatField(blank=False, default=0.0)
    area = models.FloatField(blank=False, default=0-0)
    tumor_area = models.BooleanField(blank=False)

    class Meta:
        unique_together = ('label', 'core')
