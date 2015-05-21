import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Job(models.Model):
    title = models.CharField(max_length=200)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # hourly_rate = models.DecimalField(decimal_places=2, max_digits=5)
    hourly_rate = models.FloatField(
        validators=[MinValueValidator(0.01)]
    )
    # tax_rate = models.DecimalField(decimal_places=2, max_digits=2)
    tax_rate = models.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)]
    )
    date_added = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return unicode(self.title)


class TimeEntry(models.Model):
    total_time = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    date = models.DateTimeField(default=timezone.now)
    summary = models.TextField()
    job = models.ForeignKey(Job)

    def __unicode__(self):
        return unicode(self.date)
