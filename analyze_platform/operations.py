from django.db import models

class DBManager:
    """Class to manage database operations."""

    def __init__(self, model):
        self.model = model

    def add_record(self, **kwargs):
        """Add a new record to the database."""
        self.model.objects.create(**kwargs)

    def update_record(self, pk, **kwargs):
        """Update an existing record in the database."""
        obj = self.model.objects.get(pk=pk)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()

    def remove_record(self, pk):
        """Remove a record from the database."""
        self.model.objects.get(pk=pk).delete()
