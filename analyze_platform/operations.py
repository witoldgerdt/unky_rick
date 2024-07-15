from analyze_platform.models import TestModel

class DBManager:
    def __init__(self, model):
        self.model = model

    def add_record(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update_record(self, pk, **kwargs):
        record = self.model.objects.get(pk=pk)
        for key, value in kwargs.items():
            setattr(record, key, value)
        record.save()

    def remove_record(self, pk):
        self.model.objects.get(pk=pk).delete()
