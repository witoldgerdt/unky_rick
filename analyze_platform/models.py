from django.db import models

# Create your models here.
from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

class Record(BaseModel):
    column1 = models.CharField(max_length=50)
    column2 = models.CharField(max_length=50)
