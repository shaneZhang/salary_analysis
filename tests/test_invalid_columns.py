import unittest
import pandas as pd
import numpy as np
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.config_manager import ConfigManager
from src.models.data_manager import DataManager
from src.models.logger import AppLogger
from src.services.data_service import DataService
from src.services.processing_service import ProcessingService
from src.services.analysis_service import AnalysisService
from src.services.visualization_service import VisualizationService
from src.core.data_loader import DataLoader
from src.core.data_processor import DataProcessor
from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer


class TestAnalysisServiceWithInvalidColumns(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = AnalysisService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_get_descriptive_stats_invalid_column(self):
        result = self.service.get_descriptive_stats('nonexistent')
        self.assertTrue(result['success'])
    
    def test_get_grouped_stats_invalid_columns(self):
        result = self.service.get_grouped_stats('nonexistent', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis_invalid_column(self):
        result = self.service.get_frequency_analysis('nonexistent')
        self.assertTrue(result['success'])
    
    def test_get_crosstab_invalid_columns(self):
        result = self.service.get_crosstab('nonexistent', 'gender')
        self.assertFalse(result['success'])
    
    def test_compare_by_dimension_invalid_column(self):
        result = self.service.compare_by_dimension('nonexistent', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_matrix_invalid_columns(self):
        result = self.service.get_correlation_matrix(['nonexistent1', 'nonexistent2'])
        self.assertFalse(result['success'])
    
    def test_get_correlation_invalid_columns(self):
        result = self.service.get_correlation('nonexistent', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_trend_analysis_invalid_columns(self):
        result = self.service.get_trend_analysis('nonexistent', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_salary_distribution_invalid_column(self):
        result = self.service.get_salary_distribution('nonexistent')
        self.assertTrue(result['success'])
    
    def test_get_summary_report_invalid_column(self):
        result = self.service.get_summary_report('nonexistent')
        self.assertTrue(result['success'])
    
    def test_get_dimensions_analysis_invalid_columns(self):
        result = self.service.get_dimensions_analysis(['nonexistent'], 'salary')
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data_invalid_columns(self):
        result = self.service.get_boxplot_data('nonexistent', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom_invalid_column(self):
        result = self.service.get_top_bottom('nonexistent', n=3, top=True)
        self.assertTrue(result['success'])
    
    def test_get_percentile_distribution_invalid_column(self):
        result = self.service.get_percentile_distribution('nonexistent')
        self.assertTrue(result['success'])


class TestProcessingServiceWithInvalidColumns(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = ProcessingService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_detect_outliers_invalid_column(self):
        result = self.service.detect_outliers('nonexistent')
        self.assertTrue(result['success'])
    
    def test_remove_outliers_invalid_column(self):
        result = self.service.remove_outliers('nonexistent')
        self.assertTrue(result['success'])
    
    def test_create_age_group_invalid_column(self):
        result = self.service.create_age_group('nonexistent')
        self.assertFalse(result['success'])
    
    def test_create_salary_group_invalid_column(self):
        result = self.service.create_salary_group('nonexistent')
        self.assertFalse(result['success'])
    
    def test_create_experience_group_invalid_column(self):
        result = self.service.create_experience_group('nonexistent')
        self.assertFalse(result['success'])
    
    def test_convert_dtype_invalid_column(self):
        result = self.service.convert_dtype('nonexistent', 'float')
        self.assertFalse(result['success'])
    
    def test_handle_missing_values_invalid_strategy(self):
        result = self.service.handle_missing_values('invalid_strategy')
        self.assertTrue(result['success'])


class TestVisualizationServiceWithInvalidColumns(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = VisualizationService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_create_salary_distribution_chart_invalid_column(self):
        result = self.service.create_salary_distribution_chart('nonexistent')
        self.assertFalse(result['success'])
    
    def test_create_comparison_chart_invalid_columns(self):
        result = self.service.create_comparison_chart('nonexistent', 'salary')
        self.assertFalse(result['success'])
    
    def test_create_trend_chart_invalid_columns(self):
        result = self.service.create_trend_chart('nonexistent', 'salary')
        self.assertFalse(result['success'])


class TestDataAnalyzerWithInvalidColumns(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_descriptive_stats_invalid_column(self):
        result = self.analyzer.get_descriptive_stats('nonexistent')
        self.assertEqual(result, {})
    
    def test_get_grouped_stats_invalid_columns(self):
        result = self.analyzer.get_grouped_stats('nonexistent', 'salary')
        self.assertTrue(result.empty)
    
    def test_get_frequency_analysis_invalid_column(self):
        result = self.analyzer.get_frequency_analysis('nonexistent')
        self.assertTrue(result.empty)
    
    def test_get_crosstab_invalid_columns(self):
        with self.assertRaises(KeyError):
            self.analyzer.get_crosstab('nonexistent', 'gender')
    
    def test_compare_by_dimension_invalid_column(self):
        result = self.analyzer.compare_by_dimension('nonexistent', 'salary')
        self.assertTrue(result.empty)
    
    def test_get_correlation_matrix_invalid_columns(self):
        with self.assertRaises(KeyError):
            self.analyzer.get_correlation_matrix(['nonexistent1', 'nonexistent2'])
    
    def test_get_correlation_invalid_columns(self):
        result = self.analyzer.get_correlation('nonexistent', 'salary')
        self.assertEqual(result, {})
    
    def test_get_trend_analysis_invalid_columns(self):
        result = self.analyzer.get_trend_analysis('nonexistent', 'salary')
        self.assertTrue(result.empty)
    
    def test_get_salary_distribution_invalid_column(self):
        result = self.analyzer.get_salary_distribution('nonexistent')
        self.assertTrue(result.empty)
    
    def test_get_top_bottom_invalid_column(self):
        result = self.analyzer.get_top_bottom('nonexistent', n=3, top=True)
        self.assertTrue(result.empty)
    
    def test_get_percentile_distribution_invalid_column(self):
        result = self.analyzer.get_percentile_distribution('nonexistent')
        self.assertEqual(result, {})
    
    def test_get_boxplot_data_invalid_columns(self):
        result = self.analyzer.get_boxplot_data('nonexistent', 'salary')
        self.assertEqual(result, {})


class TestDataProcessorWithInvalidColumns(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_detect_outliers_invalid_column(self):
        result = self.processor.detect_outliers('nonexistent')
        self.assertTrue(result.empty)
    
    def test_remove_outliers_invalid_column(self):
        result = self.processor.remove_outliers('nonexistent')
        self.assertEqual(result, 0)
    
    def test_create_age_group_invalid_column(self):
        result = self.processor.create_age_group('nonexistent')
        self.assertFalse(result)
    
    def test_create_salary_group_invalid_column(self):
        result = self.processor.create_salary_group('nonexistent')
        self.assertFalse(result)
    
    def test_create_work_experience_group_invalid_column(self):
        result = self.processor.create_work_experience_group('nonexistent')
        self.assertFalse(result)
    
    def test_convert_dtype_invalid_column(self):
        result = self.processor.convert_dtype('nonexistent', 'float')
        self.assertFalse(result)
    
    def test_create_calculated_field_invalid(self):
        from src.exceptions import DataProcessingError
        with self.assertRaises(DataProcessingError):
            self.processor.create_calculated_field('new_field', lambda df: df['nonexistent'] * 2)


if __name__ == '__main__':
    unittest.main()
