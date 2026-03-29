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


class TestAnalysisServiceEdgeCases(unittest.TestCase):
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
    
    def test_get_descriptive_stats_with_all_same_values(self):
        df = pd.DataFrame({'salary': [10000, 10000, 10000, 10000, 10000]})
        self.data_manager.set_data(df)
        result = self.service.get_descriptive_stats('salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_with_single_column(self):
        df = pd.DataFrame({'salary': [10000, 15000, 20000]})
        self.data_manager.set_data(df)
        result = self.service.get_correlation_matrix(['salary'])
        self.assertTrue(result['success'])
    
    def test_get_grouped_stats_with_single_group(self):
        df = pd.DataFrame({
            'gender': ['F', 'F', 'F', 'F', 'F'],
            'salary': [10000, 15000, 20000, 25000, 30000]
        })
        self.data_manager.set_data(df)
        result = self.service.get_grouped_stats('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis_with_all_unique(self):
        df = pd.DataFrame({'id': [1, 2, 3, 4, 5]})
        self.data_manager.set_data(df)
        result = self.service.get_frequency_analysis('id')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom_with_n_larger_than_data(self):
        result = self.service.get_top_bottom('salary', n=100, top=True)
        self.assertTrue(result['success'])
    
    def test_get_top_bottom_bottom(self):
        result = self.service.get_top_bottom('salary', n=3, top=False)
        self.assertTrue(result['success'])
    
    def test_get_dimensions_analysis_with_single_dimension(self):
        result = self.service.get_dimensions_analysis(['gender'], 'salary')
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data_with_many_groups(self):
        df = pd.DataFrame({
            'department': ['HR', 'IT', 'Finance', 'Sales', 'Marketing'],
            'salary': [10000, 15000, 20000, 25000, 30000]
        })
        self.data_manager.set_data(df)
        result = self.service.get_boxplot_data('department', 'salary')
        self.assertTrue(result['success'])


class TestProcessingServiceEdgeCases(unittest.TestCase):
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
    
    def test_detect_outliers_with_no_outliers(self):
        df = pd.DataFrame({'salary': [10000, 10000, 10000, 10000, 10000]})
        self.data_manager.set_data(df)
        result = self.service.detect_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_remove_outliers_with_no_outliers(self):
        df = pd.DataFrame({'salary': [10000, 10000, 10000, 10000, 10000]})
        self.data_manager.set_data(df)
        result = self.service.remove_outliers('salary')
        self.assertTrue(result['success'])
    
    def test_create_age_group_with_young_ages(self):
        df = pd.DataFrame({'age': [18, 20, 22, 24, 26]})
        self.data_manager.set_data(df)
        result = self.service.create_age_group('age')
        self.assertTrue(result['success'])
    
    def test_create_salary_group_with_low_salaries(self):
        df = pd.DataFrame({'salary': [1000, 2000, 3000, 4000, 5000]})
        self.data_manager.set_data(df)
        result = self.service.create_salary_group('salary')
        self.assertTrue(result['success'])
    
    def test_create_experience_group_with_low_experience(self):
        df = pd.DataFrame({'work_years': [0, 1, 2, 3, 4]})
        self.data_manager.set_data(df)
        result = self.service.create_experience_group('work_years')
        self.assertTrue(result['success'])
    
    def test_convert_dtype_to_int(self):
        result = self.service.convert_dtype('salary', 'int')
        self.assertTrue(result['success'])
    
    def test_convert_dtype_to_str(self):
        result = self.service.convert_dtype('salary', 'str')
        self.assertTrue(result['success'])
    
    def test_encode_categorical_with_multiple_columns(self):
        df = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'department': ['HR', 'IT', 'IT', 'Finance', 'HR']
        })
        self.data_manager.set_data(df)
        result = self.service.encode_categorical(columns=['gender', 'department'])
        self.assertTrue(result['success'])


class TestVisualizationServiceEdgeCases(unittest.TestCase):
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
    
    def test_create_salary_distribution_chart_with_bins(self):
        result = self.service.create_salary_distribution_chart('salary')
        self.assertTrue(result['success'])
    
    def test_create_comparison_chart_with_multiple_groups(self):
        df = pd.DataFrame({
            'department': ['HR', 'IT', 'Finance', 'Sales', 'Marketing'],
            'salary': [10000, 15000, 20000, 25000, 30000]
        })
        self.data_manager.set_data(df)
        result = self.service.create_comparison_chart('department', 'salary')
        self.assertTrue(result['success'])
    
    def test_create_trend_chart_with_single_point(self):
        df = pd.DataFrame({
            'age': [25],
            'salary': [10000]
        })
        self.data_manager.set_data(df)
        result = self.service.create_trend_chart('age', 'salary')
        self.assertIn('success', result)
    
    def test_create_bar_chart_with_single_group(self):
        df = pd.DataFrame({
            'gender': ['F', 'F', 'F'],
            'salary': [10000, 15000, 20000]
        })
        self.data_manager.set_data(df)
        result = self.service.create_bar_chart('gender', 'salary')
        self.assertTrue(result['success'])


class TestDataAnalyzerEdgeCases(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_descriptive_stats_with_all_same_values(self):
        df = pd.DataFrame({'salary': [10000, 10000, 10000, 10000, 10000]})
        analyzer = DataAnalyzer(df)
        result = analyzer.get_descriptive_stats('salary')
        self.assertEqual(result['std'], 0)
    
    def test_get_correlation_with_perfect_correlation(self):
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10]
        })
        analyzer = DataAnalyzer(df)
        result = analyzer.get_correlation('a', 'b')
        self.assertEqual(result['pearson_r'], 1.0)
    
    def test_get_top_bottom_with_empty_result(self):
        df = pd.DataFrame({'salary': []})
        analyzer = DataAnalyzer(df)
        result = analyzer.get_top_bottom('salary', n=3, top=True)
        self.assertTrue(result.empty)


class TestDataProcessorEdgeCases(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_detect_outliers_with_all_same_values(self):
        df = pd.DataFrame({'salary': [10000, 10000, 10000, 10000, 10000]})
        processor = DataProcessor(df)
        result = processor.detect_outliers('salary')
        self.assertFalse(result.empty)
    
    def test_remove_outliers_with_all_same_values(self):
        df = pd.DataFrame({'salary': [10000, 10000, 10000, 10000, 10000]})
        processor = DataProcessor(df)
        result = processor.remove_outliers('salary')
        self.assertEqual(result, 0)
    
    def test_create_age_group_with_extreme_ages(self):
        df = pd.DataFrame({'age': [18, 65, 70, 75, 80]})
        processor = DataProcessor(df)
        result = processor.create_age_group('age')
        self.assertTrue(result)
    
    def test_create_salary_group_with_extreme_salaries(self):
        df = pd.DataFrame({'salary': [1000, 100000, 200000, 300000, 400000]})
        processor = DataProcessor(df)
        result = processor.create_salary_group('salary')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
