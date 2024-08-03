import unittest
import pymongo
from data_migrator import DataMigrator

class TestDataMigrator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Mongo connection
        client = pymongo.MongoClient("localhost", 27017)
        mongo_db = client.dev_dummy
        collection = mongo_db.healthcare
        
        return super().setUpClass()
    def test_clean(self, json_obj):
        self.setUpClass()
        dm = DataMigrator(self.json)
        self.assertFalse(dm.clean(json_obj))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)