import pytest
from analyze_platform.operations import DBManager
from django.db import models

@pytest.mark.django_db
class TestModel(models.Model):
    column1 = models.CharField(max_length=100)
    column2 = models.CharField(max_length=100)

    class Meta:
        app_label = 'analyze_platform'  # Specify the app label

@pytest.fixture
def db_manager():
    return DBManager(TestModel)

@pytest.mark.django_db
def test_add_record(db_manager):
    db_manager.add_record(column1="value1", column2="value2")
    assert TestModel.objects.count() == 1

@pytest.mark.django_db
def test_update_record(db_manager):
    db_manager.add_record(column1="value1", column2="value2")
    db_manager.update_record(1, column1="updated_value1")
    record = TestModel.objects.get(pk=1)
    assert record.column1 == "updated_value1"

@pytest.mark.django_db
def test_remove_record(db_manager):
    db_manager.add_record(column1="value1", column2="value2")
    db_manager.remove_record(1)
    assert TestModel.objects.count() == 0
