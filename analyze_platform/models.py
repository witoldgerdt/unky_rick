from django.db import models

class DataRecord(models.Model):
    id = models.AutoField(primary_key=True)
    column1 = models.CharField(max_length=50)
    column2 = models.CharField(max_length=50)

    class Meta:
        abstract = False
