import unittest
from app.operations import DBManager
from app.db import init_db, Record

class TestDBManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.db_manager = DBManager(Record)

    def test_add_record(self):
        self.db_manager.add_record(column1="test1", column2="test2")
        records = self.db_manager.get_all_records()
        self.assertGreater(len(records), 0)

    def test_update_record(self):
        self.db_manager.add_record(column1="test1", column2="test2")
        records = self.db_manager.get_all_records()
        record_id = records[0].id
        self.db_manager.update_record(record_id, column1="updated_test1")
        updated_record = self.db_manager.get_record_by_id(record_id)
        self.assertEqual(updated_record.column1, "updated_test1")

    def test_remove_record(self):
        self.db_manager.add_record(column1="test1", column2="test2")
        records = self.db_manager.get_all_records()
        record_id = records[0].id
        self.db_manager.remove_record(record_id)
        records_after_removal = self.db_manager.get_all_records()
        self.assertEqual(len(records_after_removal), 0)

if __name__ == '__main__':
    unittest.main()