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
        dm = DataMigrator(json)
        return super().setUpClass()
    def test_clean(self, json_obj):
        self.assertFalse(dm.migrate(json_obj))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)