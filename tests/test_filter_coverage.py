import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_manager import DataManager
from src.models.config_manager import ConfigManager
from src.models.logger import AppLogger
from src.services.processing_service import ProcessingService
from src.core.data_processor import DataProcessor


class TestProcessingServiceFilter(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = ProcessingService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_filter_data(self):
        conditions = {'age': {'min': 30}}
        result = self.service.filter_data(conditions)
        self.assertTrue(result['success'])
    
    def test_filter_data_multiple_conditions(self):
        conditions = {'age': {'min': 25, 'max': 40}}
        result = self.service.filter_data(conditions)
        self.assertTrue(result['success'])
    
    def test_reset_data(self):
        result = self.service.reset_data()
        self.assertTrue(result['success'])
    
    def test_get_data_summary(self):
        result = self.service.get_data_summary()
        self.assertIsNotNone(result)


class TestDataProcessorFilter(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_apply_filter(self):
        conditions = {'age': {'min': 30}}
        result = self.processor.apply_filter(conditions)
        self.assertIsInstance(result, int)
    
    def test_get_current_data(self):
        result = self.processor.get_current_data()
        self.assertIsNotNone(result)
    
    def test_get_data_summary(self):
        result = self.processor.get_data_summary()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
