from django.db import models
from django.utils import timezone

class DataRecord(models.Model):
    id = models.AutoField(primary_key=True)
    column1 = models.CharField(max_length=50)
    column2 = models.CharField(max_length=50)

    class Meta:
        abstract = False

class DataStatus(models.Model):
    update_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Last update: {self.update_time}"
