import unittest
from data_migrator import DataMigrator

class TestDataMigrator(unittest.TestCase):
    @classmethod
    def test_clean(self, json_obj):
        self.assertFalse(migrate(json_obj))
        

if __name__ == "__main__":
    unittest.main(verbosity=2)