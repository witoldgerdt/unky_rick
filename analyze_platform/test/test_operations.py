import pytest
from analyze_platform.models import TestModel
from analyze_platform.operations import DBManager

@pytest.fixture
def db_manager():
    return DBManager(TestModel)

@pytest.mark.django_db
def test_add_record(db_manager):
    db_manager.add_record(column1="value1", column2="value2")
    assert TestModel.objects.count() == 1

@pytest.mark.django_db
def test_update_record(db_manager):
    record = db_manager.add_record(column1="value1", column2="value2")
    db_manager.update_record(record.pk, column1="updated_value1")
    updated_record = TestModel.objects.get(pk=record.pk)
    assert updated_record.column1 == "updated_value1"

@pytest.mark.django_db
def test_remove_record(db_manager):
    record = db_manager.add_record(column1="value1", column2="value2")
    db_manager.remove_record(record.pk)
    assert TestModel.objects.count() == 0
