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


class TestAnalysisServiceSimple(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = AnalysisService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F', 'M'],
            'age': [25, 30, 35, 40, 45, 50],
            'salary': [10000, 15000, 20000, 25000, 30000, 35000],
            'work_years': [2, 5, 10, 15, 20, 25],
            'department': ['HR', 'IT', 'IT', 'Finance', 'HR', 'Finance']
        })
        self.data_manager.set_data(self.test_data)
    
    def test_get_descriptive_stats(self):
        result = self.service.get_descriptive_stats('salary')
        self.assertTrue(result['success'])
    
    def test_get_grouped_stats(self):
        result = self.service.get_grouped_stats('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis(self):
        result = self.service.get_frequency_analysis('gender')
        self.assertTrue(result['success'])
    
    def test_get_crosstab(self):
        result = self.service.get_crosstab('gender', 'department')
        self.assertTrue(result['success'])
    
    def test_compare_by_dimension(self):
        result = self.service.compare_by_dimension('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_matrix(self):
        result = self.service.get_correlation_matrix(['age', 'salary', 'work_years'])
        self.assertTrue(result['success'])
    
    def test_get_correlation(self):
        result = self.service.get_correlation('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_trend_analysis(self):
        result = self.service.get_trend_analysis('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_salary_distribution(self):
        result = self.service.get_salary_distribution('salary')
        self.assertTrue(result['success'])
    
    def test_get_summary_report(self):
        result = self.service.get_summary_report('salary')
        self.assertTrue(result['success'])
    
    def test_get_dimensions_analysis(self):
        result = self.service.get_dimensions_analysis(['gender', 'department'], 'salary')
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data(self):
        result = self.service.get_boxplot_data('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom(self):
        result = self.service.get_top_bottom('salary', n=3, top=True)
        self.assertTrue(result['success'])
    
    def test_get_percentile_distribution(self):
        result = self.service.get_percentile_distribution('salary')
        self.assertTrue(result['success'])


class TestProcessingServiceSimple(unittest.TestCase):
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
    
    def test_detect_outliers(self):
        result = self.service.detect_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_remove_outliers(self):
        result = self.service.remove_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_create_age_group(self):
        result = self.service.create_age_group('age')
        self.assertTrue(result['success'])
    
    def test_create_salary_group(self):
        result = self.service.create_salary_group('salary')
        self.assertTrue(result['success'])
    
    def test_create_experience_group(self):
        result = self.service.create_experience_group('work_years')
        self.assertTrue(result['success'])
    
    def test_convert_dtype(self):
        result = self.service.convert_dtype('salary', 'float')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_mean(self):
        result = self.service.handle_missing_values('mean')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_median(self):
        result = self.service.handle_missing_values('median')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_mode(self):
        result = self.service.handle_missing_values('mode')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_drop(self):
        result = self.service.handle_missing_values('drop')
        self.assertTrue(result['success'])
    
    def test_encode_categorical(self):
        result = self.service.encode_categorical(columns=['gender'])
        self.assertTrue(result['success'])


class TestVisualizationServiceSimple(unittest.TestCase):
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
    
    def test_create_salary_distribution_chart(self):
        result = self.service.create_salary_distribution_chart('salary')
        self.assertTrue(result['success'])
    
    def test_create_comparison_chart(self):
        result = self.service.create_comparison_chart('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_trend_chart(self):
        result = self.service.create_trend_chart('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_bar_chart(self):
        result = self.service.create_bar_chart('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_scatter_chart(self):
        result = self.service.create_scatter_chart('age', 'salary')
        self.assertIn('success', result)


class TestDataAnalyzerSimple(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F', 'M'],
            'age': [25, 30, 35, 40, 45, 50],
            'salary': [10000, 15000, 20000, 25000, 30000, 35000],
            'work_years': [2, 5, 10, 15, 20, 25],
            'department': ['HR', 'IT', 'IT', 'Finance', 'HR', 'Finance']
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_descriptive_stats(self):
        result = self.analyzer.get_descriptive_stats('salary')
        self.assertIn('mean', result)
    
    def test_get_grouped_stats(self):
        result = self.analyzer.get_grouped_stats('gender', 'salary')
        self.assertFalse(result.empty)
    
    def test_get_frequency_analysis(self):
        result = self.analyzer.get_frequency_analysis('gender')
        self.assertFalse(result.empty)
    
    def test_get_crosstab(self):
        result = self.analyzer.get_crosstab('gender', 'department')
        self.assertFalse(result.empty)
    
    def test_compare_by_dimension(self):
        result = self.analyzer.compare_by_dimension('gender', 'salary')
        self.assertFalse(result.empty)
    
    def test_get_correlation_matrix(self):
        result = self.analyzer.get_correlation_matrix(['age', 'salary', 'work_years'])
        self.assertFalse(result.empty)
    
    def test_get_correlation(self):
        result = self.analyzer.get_correlation('age', 'salary')
        self.assertIn('pearson_r', result)
    
    def test_get_trend_analysis(self):
        result = self.analyzer.get_trend_analysis('age', 'salary')
        self.assertFalse(result.empty)
    
    def test_get_salary_distribution(self):
        result = self.analyzer.get_salary_distribution('salary')
        self.assertFalse(result.empty)
    
    def test_get_top_bottom(self):
        result = self.analyzer.get_top_bottom('salary', n=3, top=True)
        self.assertEqual(len(result), 3)
    
    def test_get_percentile_distribution(self):
        result = self.analyzer.get_percentile_distribution('salary')
        self.assertIn('p25', result)
    
    def test_get_boxplot_data(self):
        result = self.analyzer.get_boxplot_data('gender', 'salary')
        self.assertIn('F', result)


class TestDataProcessorSimple(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_detect_outliers(self):
        result = self.processor.detect_outliers('salary')
        self.assertFalse(result.empty)
    
    def test_remove_outliers(self):
        result = self.processor.remove_outliers('salary')
        self.assertIsInstance(result, int)
    
    def test_create_age_group(self):
        result = self.processor.create_age_group('age')
        self.assertTrue(result)
    
    def test_create_salary_group(self):
        result = self.processor.create_salary_group('salary')
        self.assertTrue(result)
    
    def test_create_work_experience_group(self):
        result = self.processor.create_work_experience_group('work_years')
        self.assertTrue(result)
    
    def test_convert_dtype(self):
        result = self.processor.convert_dtype('salary', 'float')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
