from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model to include common fields or methods
    """
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

class Record(BaseModel):
    """
    Model representing a record with two columns.
    """
    column1 = models.CharField(max_length=50)
    column2 = models.CharField(max_length=50)

    def __str__(self):
        return f"Record {self.id}: {self.column1}, {self.column2}"
