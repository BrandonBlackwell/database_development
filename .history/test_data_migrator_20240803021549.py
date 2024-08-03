import unittest
from data_migrator import DataMigrator

class TestDataMigrator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        json = {
        "icUnit"           : "ic",
        "jcUnit"           : "jc",
        "normalizedRnUnit" : "normalized_rn"
    }
        
        return super().setUpClass()
    def test_clean(self, json_obj):
        self.setUpClass()
        dm = DataMigrator(self.json)
        self.assertFalse(dm.clean(json_obj))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)