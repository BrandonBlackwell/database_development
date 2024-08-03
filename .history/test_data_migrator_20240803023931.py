import unittest
import pymongo
from data_migrator import DataMigrator

class TestDataMigrator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Mongo connection
        client = pymongo.MongoClient("localhost", 27017)
        mongo_db = client.dev_dummy
        cls.collection = mongo_db.healthcare
        return super().setUpClass()
    
    def test_clean(self):
        dm = DataMigrator(self.collection.find_one({}))
        self.assertFalse(dm.clean())
        

if __name__ == "__main__":
    unittest.main(verbosity=2)