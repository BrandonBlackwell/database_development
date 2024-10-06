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
    {
        "_id": "ObjectId(66ac7d476d18e2d62dcf5bc3)",
        "Name": 'Name',
        ' Age': 'Age',
        ' Gender': 'Gender',
        ' Blood Type': 'Blood Type',
        ' Medical Condition': 'Medical Condition',
        ' Date of Admission': 'Date of Admission',
        ' Doctor': 'Doctor',
        ' Hospital': 'Hospital',
        ' Insurance Provider': 'Insurance Provider',
        ' Billing Amount': 'Billing Amount',
        ' Room Number': 'Room Number',
        ' Admission Type': 'Admission Type',
        ' Disharge Date': 'Discharge Date',
        ' Medication': 'Medication',
        ' Test Results': 'Test Results'
    }

        expected = {}
        dm = DataMigrator()
        json_obj = self.collection.find_one({})
        self.assertFalse(dm.clean(json_obj))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)