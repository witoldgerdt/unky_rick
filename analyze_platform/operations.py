from analyze_platform.models import DataRecord
from django.db import transaction

class DBManager:
    def __init__(self, model):
        self.model = model

    @transaction.atomic
    def add_record(self, **kwargs):
        """
        Add a record to the database.
        """
        return self.model.objects.create(**kwargs)

    @transaction.atomic
    def update_record(self, pk, **kwargs):
        """
        Update a record in the database.
        """
        record = self.model.objects.get(pk=pk)
        for key, value in kwargs.items():
            setattr(record, key, value)
        record.save()
        return record

    @transaction.atomic
    def remove_record(self, pk):
        """
        Remove a record from the database.
        """
        record = self.model.objects.get(pk=pk)
        record.delete()
