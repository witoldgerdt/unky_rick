from django.db import models

class DataRecord(models.Model):
    column1 = models.CharField(max_length=255)
    column2 = models.TextField()
