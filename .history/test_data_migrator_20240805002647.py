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
        #  _id: ObjectId("66ac7d476d18e2d62dcf5bd6"),
        {
            "name": 'LuKE BuRgEss',
            ' age': 34,
            ' gender': 'Female',
            ' blood_type': 'A-',
            ' medical_condition': 'Hypertension',
            ' date_of_admission': '2021-03-04',
            ' Doctor': 'Justin Moore Jr.',
            ' Hospital': 'Houston PLC',
            ' Insurance Provider': 'Blue Cross',
            ' Billing Amount': 18843.02301783416,
            ' Room Number': 260,
            ' Admission Type': 'Elective',
            ' Disharge Date': '2021-03-14',
            ' Medication': 'Aspirin',
            ' Test Results': 'Abnormal'
        }


        expected = {}
        dm = DataMigrator()
        json_obj = self.collection.find_one({})
        self.assertFalse(dm.clean(json_obj))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)