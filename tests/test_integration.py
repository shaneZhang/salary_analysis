import unittest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_manager import DataManager
from src.models.config_manager import ConfigManager
from src.models.logger import AppLogger
from src.services.data_service import DataService
from src.services.processing_service import ProcessingService
from src.services.analysis_service import AnalysisService
from src.services.visualization_service import VisualizationService


class TestDataService(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = DataService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            '姓名': ['张三', '李四', '王五'],
            '性别': ['男', '女', '男'],
            '年龄': [25, 30, 35],
            '税前薪资': [10000, 15000, 20000]
        })
    
    def test_get_data_info(self):
        info = self.service.get_data_info()
        self.assertFalse(info.get('has_data', False))
    
    def test_get_field_mapping(self):
        mapping = self.service.get_field_mapping()
        self.assertIn('姓名', mapping)
    
    def test_validate_current_data(self):
        is_valid, errors = self.service.validate_current_data()
        self.assertFalse(is_valid)


class TestProcessingService(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = ProcessingService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Alice'],
            'age': [25, 30, 35, 25],
            'salary': [10000, 15000, 20000, 10000],
            'work_years': [2, 5, 10, 2]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_remove_duplicates(self):
        result = self.service.remove_duplicates()
        self.assertTrue(result['success'])
        self.assertEqual(result['removed_count'], 1)
    
    def test_handle_missing_values(self):
        result = self.service.handle_missing_values('drop')
        self.assertTrue(result['success'])
    
    def test_detect_outliers(self):
        result = self.service.detect_outliers('salary')
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
    
    def test_reset_data(self):
        self.service.remove_duplicates()
        result = self.service.reset_data()
        self.assertTrue(result['success'])
    
    def test_get_data_summary(self):
        summary = self.service.get_data_summary()
        self.assertEqual(summary['total_rows'], 4)


class TestAnalysisService(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = AnalysisService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David'],
            'gender': ['F', 'M', 'M', 'M'],
            'age': [25, 30, 35, 40],
            'salary': [10000, 15000, 20000, 25000]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_get_descriptive_stats(self):
        result = self.service.get_descriptive_stats('salary')
        self.assertTrue(result['success'])
        self.assertIn('stats', result)
    
    def test_get_grouped_stats(self):
        result = self.service.get_grouped_stats('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis(self):
        result = self.service.get_frequency_analysis('gender')
        self.assertTrue(result['success'])
    
    def test_get_crosstab(self):
        result = self.service.get_crosstab('gender', 'gender')
        self.assertTrue(result['success'])
    
    def test_compare_by_dimension(self):
        result = self.service.compare_by_dimension('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_matrix(self):
        result = self.service.get_correlation_matrix(['age', 'salary'])
        self.assertTrue(result['success'])
    
    def test_get_correlation(self):
        result = self.service.get_correlation('age', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_summary_report(self):
        result = self.service.get_summary_report('salary')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom(self):
        result = self.service.get_top_bottom('salary', n=2, top=True)
        self.assertTrue(result['success'])
    
    def test_get_percentile_distribution(self):
        result = self.service.get_percentile_distribution('salary')
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data(self):
        result = self.service.get_boxplot_data('gender', 'salary')
        self.assertTrue(result['success'])


class TestVisualizationService(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = VisualizationService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D'],
            'value': [10, 20, 30, 40]
        })
        self.data_manager.set_data(self.test_data)
    
    def test_create_bar_chart(self):
        result = self.service.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Bar Chart'
        )
        self.assertTrue(result['success'])
    
    def test_create_line_chart(self):
        result = self.service.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30]],
            title='Test Line Chart'
        )
        self.assertTrue(result['success'])
    
    def test_create_pie_chart(self):
        result = self.service.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie Chart'
        )
        self.assertTrue(result['success'])
    
    def test_create_histogram(self):
        result = self.service.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
            title='Test Histogram'
        )
        self.assertTrue(result['success'])
    
    def test_create_salary_distribution_chart(self):
        result = self.service.create_salary_distribution_chart('value')
        self.assertTrue(result['success'])
    
    def test_create_comparison_chart(self):
        result = self.service.create_comparison_chart('category', 'value')
        self.assertTrue(result['success'])
    
    def test_get_current_figure(self):
        self.service.create_bar_chart(['A'], [1], 'Test')
        fig = self.service.get_current_figure()
        self.assertIsNotNone(fig)


if __name__ == '__main__':
    unittest.main()
