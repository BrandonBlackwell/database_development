from pandas import DataFrame
import unittest
from datetime import datetime

data_map = {"testdate": "test_date", "operator": "operator",
            "testtype": "test_type", "program": "program", "continuity": "continuity",
            "temperature": "temperature", "names": "names",
            "mask name": "mask", "lot": "lot", "chip": "chip", "wafer": "wafer", "fabrow": "row", 
            "fabcol": "column", "imagedata": "image_data", "test version": "test_version", 
            "icunit": "ic"}

metrics_list = ["icunit", "jcunit"]

def clean(record: dict) -> dict:
  updated_record = {"metrics": [], "units": [], "values": []}
  for field, value in record.items():
    column = data_map.get(field.lower(), field)
    if column in metrics_list:
      metrics += column
      units   += value
      value   += record[f"{column}Value"]
    updated_record.update({column: value})

class TestDataCleaner(unittest.TestCase):
    """Data transformation and cleansing class
    1. Columns are properly mapped
    2. Metric columns are properly mapped
    3. Metrics that have units are properly handled
      a. No metrics at all
      b. No unit
      c. No metric
      d. No value
    4. Metrics with no units are properly handled
    
    Args:
        unittest (_type_): _description_
    """
    
    def test_column_mappings(self):
        """Mongo columns are mapped to Maria columns
        """
        actual_record =  {"TestDate": datetime.today(), "operator": "John Doe",
                          "testType": "type 1", "program": "program 1", "continuity": "pass",
                          "temperature": 2.5, "Names": "the_brown,fox jumped, over_moon",
                          "Mask Name": "G999", "lot": 99, "Chip": 9, "Wafer": "6969", "fabRow": 1, "fabCol": 2,
                          "ImageData": "bytes".encode(), "Test Version": "A_1", "icUnit": "uA", "icValue": 0.9897}
        
        expected_record = {"metrics": [], "units": [], "values": [],
                           "test_date": datetime.today(), "operator": "John Doe",
                           "test_type": "type 1", "program": "program 1", "continuity": "pass",
                           "temperature": 2.5, "names": "the_brown,fox jumped, over_moon",
                           "mask": "G999", "lot": 99, "chip": 9, "wafer": "6969", "row": 1, "col": 2,
                           "image_data": "bytes".encode(), "test_version": "A_1"}
        self.maxDiff = None
        self.assertEqual(expected_record, actual_record)
        
    def test_metric_mappings(self):
      expected_record = {"metrics": ["ic"], "units": ["uA"], "values": [1.0]}
      actual_record   = {}
      
      self.assertEqual(expected_record, actual_record)
      
    def test_missing_unit(self):
      """Test result with a missing unit is flagged.
      """
      # data = {"icUnit": "uA", "icValue": 1.0}
      data = {"icValue": 1.0}
      expected_record = {"metrics": ["ic"], "units": ["dummy"], "values": [1.0]}
      actual_record = clean(data)
      
      self.assertEqual(expected_record, actual_record)
      
    def test_missing_metric(self):
      """Test result with a missing metric is flagged.
      """
      expected_record = {"metrics": ["ic"], "units": ["uA"], "values": [1.0]}
      actual_record   = {}
      
      self.assertEqual(expected_record, actual_record)
      
    def test_missing_metric_value(self):
      """Test result with a missing metric is flagged.
      """
      expected_record = {"metrics": ["ic"], "units": ["uA"], "values": [1.0]}
      actual_record   = {}
      
      self.assertEqual(expected_record, actual_record)
      
    def test_no_metric_unit_value(self):
      """Test result with no metrics is flagged.
      """
      expected_record = {"metrics": ["ic"], "units": ["uA"], "values": [1.0]}
      actual_record   = {}
      
      self.assertEqual(expected_record, actual_record)