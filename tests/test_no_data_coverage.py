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
from src.core.data_analyzer import DataAnalyzer
from src.core.data_processor import DataProcessor
from src.core.visualizer import DataVisualizer


class TestAnalysisServiceNoData(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = AnalysisService(self.data_manager, self.config, self.logger)
    
    def test_get_descriptive_stats_no_data(self):
        result = self.service.get_descriptive_stats('salary')
        self.assertTrue(result['success'])
    
    def test_get_grouped_stats_no_data(self):
        result = self.service.get_grouped_stats('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis_no_data(self):
        result = self.service.get_frequency_analysis('gender')
        self.assertTrue(result['success'])
    
    def test_get_crosstab_no_data(self):
        result = self.service.get_crosstab('gender', 'department')
        self.assertTrue(result['success'])
    
    def test_compare_by_dimension_no_data(self):
        result = self.service.compare_by_dimension('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_matrix_no_data(self):
        result = self.service.get_correlation_matrix(['age', 'salary'])
        self.assertTrue(result['success'])
    
    def test_get_correlation_no_data(self):
        result = self.service.get_correlation('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_trend_analysis_no_data(self):
        result = self.service.get_trend_analysis('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_salary_distribution_no_data(self):
        result = self.service.get_salary_distribution('salary')
        self.assertTrue(result['success'])
    
    def test_get_summary_report_no_data(self):
        result = self.service.get_summary_report('salary')
        self.assertTrue(result['success'])
    
    def test_get_dimensions_analysis_no_data(self):
        result = self.service.get_dimensions_analysis(['gender'], 'salary')
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data_no_data(self):
        result = self.service.get_boxplot_data('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom_no_data(self):
        result = self.service.get_top_bottom('salary', n=3, top=True)
        self.assertTrue(result['success'])
    
    def test_get_percentile_distribution_no_data(self):
        result = self.service.get_percentile_distribution('salary')
        self.assertTrue(result['success'])


class TestProcessingServiceNoData(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = ProcessingService(self.data_manager, self.config, self.logger)
    
    def test_detect_outliers_no_data(self):
        result = self.service.detect_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_remove_outliers_no_data(self):
        result = self.service.remove_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_create_age_group_no_data(self):
        result = self.service.create_age_group('age')
        self.assertFalse(result['success'])
    
    def test_create_salary_group_no_data(self):
        result = self.service.create_salary_group('salary')
        self.assertFalse(result['success'])
    
    def test_create_experience_group_no_data(self):
        result = self.service.create_experience_group('work_years')
        self.assertFalse(result['success'])
    
    def test_convert_dtype_no_data(self):
        result = self.service.convert_dtype('salary', 'float')
        self.assertFalse(result['success'])
    
    def test_handle_missing_values_no_data(self):
        result = self.service.handle_missing_values('mean')
        self.assertTrue(result['success'])
    
    def test_encode_categorical_no_data(self):
        result = self.service.encode_categorical(columns=['gender'])
        self.assertTrue(result['success'])


class TestVisualizationServiceNoData(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = VisualizationService(self.data_manager, self.config, self.logger)
    
    def test_create_salary_distribution_chart_no_data(self):
        result = self.service.create_salary_distribution_chart('salary')
        self.assertFalse(result['success'])
    
    def test_create_comparison_chart_no_data(self):
        result = self.service.create_comparison_chart('gender', 'salary')
        self.assertFalse(result['success'])
    
    def test_create_trend_chart_no_data(self):
        result = self.service.create_trend_chart('age', 'salary')
        self.assertFalse(result['success'])
    
    def test_create_bar_chart_no_data(self):
        result = self.service.create_bar_chart('gender', 'salary')
        self.assertIn('success', result)
    
    def test_create_scatter_chart_no_data(self):
        result = self.service.create_scatter_chart('age', 'salary')
        self.assertIn('success', result)


class TestDataAnalyzerNoData(unittest.TestCase):
    def setUp(self):
        self.analyzer = DataAnalyzer()
    
    def test_get_descriptive_stats_no_data(self):
        result = self.analyzer.get_descriptive_stats('salary')
        self.assertEqual(result, {})
    
    def test_get_grouped_stats_no_data(self):
        result = self.analyzer.get_grouped_stats('gender', 'salary')
        self.assertTrue(result.empty)
    
    def test_get_frequency_analysis_no_data(self):
        result = self.analyzer.get_frequency_analysis('gender')
        self.assertTrue(result.empty)
    
    def test_get_correlation_no_data(self):
        result = self.analyzer.get_correlation('age', 'salary')
        self.assertEqual(result, {})
    
    def test_get_trend_analysis_no_data(self):
        result = self.analyzer.get_trend_analysis('age', 'salary')
        self.assertTrue(result.empty)
    
    def test_get_salary_distribution_no_data(self):
        result = self.analyzer.get_salary_distribution('salary')
        self.assertTrue(result.empty)
    
    def test_get_top_bottom_no_data(self):
        result = self.analyzer.get_top_bottom('salary', n=3, top=True)
        self.assertTrue(result.empty)
    
    def test_get_percentile_distribution_no_data(self):
        result = self.analyzer.get_percentile_distribution('salary')
        self.assertEqual(result, {})


class TestDataProcessorNoData(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
    
    def test_detect_outliers_no_data(self):
        result = self.processor.detect_outliers('salary')
        self.assertTrue(result.empty)
    
    def test_remove_outliers_no_data(self):
        result = self.processor.remove_outliers('salary')
        self.assertEqual(result, 0)
    
    def test_create_age_group_no_data(self):
        result = self.processor.create_age_group('age')
        self.assertFalse(result)
    
    def test_create_salary_group_no_data(self):
        result = self.processor.create_salary_group('salary')
        self.assertFalse(result)
    
    def test_create_work_experience_group_no_data(self):
        result = self.processor.create_work_experience_group('work_years')
        self.assertFalse(result)
    
    def test_convert_dtype_no_data(self):
        result = self.processor.convert_dtype('salary', 'float')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
