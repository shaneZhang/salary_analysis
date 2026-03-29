import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_manager import DataManager
from src.models.config_manager import ConfigManager
from src.models.logger import AppLogger
from src.services.analysis_service import AnalysisService
from src.services.processing_service import ProcessingService
from src.services.visualization_service import VisualizationService


class TestAnalysisServiceExtra(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = AnalysisService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_get_descriptive_stats_with_valid_data(self):
        result = self.service.get_descriptive_stats('salary')
        self.assertTrue(result['success'])
    
    def test_get_grouped_stats_with_valid_data(self):
        result = self.service.get_grouped_stats('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis_with_valid_data(self):
        result = self.service.get_frequency_analysis('gender')
        self.assertTrue(result['success'])
    
    def test_get_crosstab_with_valid_data(self):
        result = self.service.get_crosstab('gender', 'gender')
        self.assertTrue(result['success'])
    
    def test_compare_by_dimension_with_valid_data(self):
        result = self.service.compare_by_dimension('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_matrix_with_valid_data(self):
        result = self.service.get_correlation_matrix(['age', 'salary'])
        self.assertTrue(result['success'])
    
    def test_get_correlation_with_valid_data(self):
        result = self.service.get_correlation('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_trend_analysis_with_valid_data(self):
        result = self.service.get_trend_analysis('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_salary_distribution_with_valid_data(self):
        result = self.service.get_salary_distribution('salary')
        self.assertTrue(result['success'])
    
    def test_get_summary_report_with_valid_data(self):
        result = self.service.get_summary_report('salary')
        self.assertTrue(result['success'])
    
    def test_get_dimensions_analysis_with_valid_data(self):
        result = self.service.get_dimensions_analysis(['gender'], 'salary')
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data_with_valid_data(self):
        result = self.service.get_boxplot_data('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom_with_valid_data(self):
        result = self.service.get_top_bottom('salary', n=3, top=True)
        self.assertTrue(result['success'])
    
    def test_get_percentile_distribution_with_valid_data(self):
        result = self.service.get_percentile_distribution('salary')
        self.assertTrue(result['success'])


class TestProcessingServiceExtra(unittest.TestCase):
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
    
    def test_detect_outliers_with_valid_data(self):
        result = self.service.detect_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_remove_outliers_with_valid_data(self):
        result = self.service.remove_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_create_age_group_with_valid_data(self):
        result = self.service.create_age_group('age')
        self.assertTrue(result['success'])
    
    def test_create_salary_group_with_valid_data(self):
        result = self.service.create_salary_group('salary')
        self.assertTrue(result['success'])
    
    def test_create_experience_group_with_valid_data(self):
        result = self.service.create_experience_group('work_years')
        self.assertTrue(result['success'])
    
    def test_convert_dtype_with_valid_data(self):
        result = self.service.convert_dtype('salary', 'float')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_with_valid_data(self):
        result = self.service.handle_missing_values('mean')
        self.assertTrue(result['success'])
    
    def test_encode_categorical_with_valid_data(self):
        result = self.service.encode_categorical(columns=['gender'])
        self.assertTrue(result['success'])


class TestVisualizationServiceExtra(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = VisualizationService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_create_salary_distribution_chart_with_valid_data(self):
        result = self.service.create_salary_distribution_chart('salary')
        self.assertTrue(result['success'])
    
    def test_create_comparison_chart_with_valid_data(self):
        result = self.service.create_comparison_chart('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_trend_chart_with_valid_data(self):
        result = self.service.create_trend_chart('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_bar_chart_with_valid_data(self):
        result = self.service.create_bar_chart('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_scatter_chart_with_valid_data(self):
        result = self.service.create_scatter_chart('age', 'salary')
        self.assertIn('success', result)


if __name__ == '__main__':
    unittest.main()
