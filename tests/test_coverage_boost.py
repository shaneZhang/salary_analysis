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


class TestVisualizationServiceFull(unittest.TestCase):
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
    
    def test_create_bar_chart_with_data(self):
        result = self.service.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Bar',
            xlabel='Category',
            ylabel='Value'
        )
        self.assertTrue(result['success'])
    
    def test_create_line_chart_with_data(self):
        result = self.service.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30]],
            title='Test Line',
            labels=['Series1']
        )
        self.assertTrue(result['success'])
    
    def test_create_pie_chart_with_data(self):
        result = self.service.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie'
        )
        self.assertTrue(result['success'])
    
    def test_create_histogram_with_data(self):
        result = self.service.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
            bins=5,
            title='Test Histogram'
        )
        self.assertTrue(result['success'])
    
    def test_get_current_figure(self):
        self.service.create_bar_chart(['A'], [1], 'Test')
        fig = self.service.get_current_figure()
        self.assertIsNotNone(fig)


class TestAnalysisServiceFull(unittest.TestCase):
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
    
    def test_get_descriptive_stats(self):
        result = self.service.get_descriptive_stats('salary')
        self.assertTrue(result['success'])
    
    def test_get_grouped_stats(self):
        result = self.service.get_grouped_stats('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_correlation_matrix(self):
        result = self.service.get_correlation_matrix(['age', 'salary', 'work_years'])
        self.assertTrue(result['success'])
    
    def test_get_frequency_analysis(self):
        result = self.service.get_frequency_analysis('gender')
        self.assertTrue(result['success'])
    
    def test_get_correlation(self):
        result = self.service.get_correlation('age', 'salary')
        self.assertTrue(result['success'])


class TestProcessingServiceFull(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = ProcessingService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Alice'],
            'age': [25, 30, 35, 25],
            'salary': [10000, 15000, 20000, 10000],
            'work_years': [2, 5, 10, 2],
            'gender': ['F', 'M', 'M', 'F']
        })
        self.data_manager.set_data(self.test_data)
    
    def test_remove_duplicates(self):
        result = self.service.remove_duplicates()
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_drop(self):
        result = self.service.handle_missing_values('drop')
        self.assertTrue(result['success'])
    
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
    
    def test_reset_data(self):
        result = self.service.reset_data()
        self.assertTrue(result['success'])


class TestDataServiceFull(unittest.TestCase):
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
        
        self.temp_dir = tempfile.mkdtemp()
        self.excel_path = os.path.join(self.temp_dir, 'test_data.xlsx')
        self.test_data.to_excel(self.excel_path, index=False)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_file(self):
        result = self.service.load_file(self.excel_path)
        self.assertTrue(result['success'])
    
    def test_get_data_info(self):
        self.service.load_file(self.excel_path)
        result = self.service.get_data_info()
        self.assertIn('rows', result)
    
    def test_validate_current_data(self):
        self.service.load_file(self.excel_path)
        is_valid, errors = self.service.validate_current_data()
        self.assertTrue(is_valid)
    
    def test_get_field_mapping(self):
        result = self.service.get_field_mapping()
        self.assertIn('姓名', result)


class TestDataProcessorFull(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Alice'],
            'age': [25, 30, 35, 25],
            'salary': [10000, 15000, 20000, 10000],
            'work_years': [2, 5, 10, 2],
            'gender': ['F', 'M', 'M', 'F']
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_remove_duplicates_processor(self):
        count = self.processor.remove_duplicates()
        self.assertGreaterEqual(count, 0)
    
    def test_handle_missing_values_drop(self):
        result = self.processor.handle_missing_values('drop')
        self.assertIsInstance(result, dict)
    
    def test_handle_missing_values_fill_mean(self):
        result = self.processor.handle_missing_values('fill_mean')
        self.assertIsInstance(result, dict)
    
    def test_handle_missing_values_fill_median(self):
        result = self.processor.handle_missing_values('fill_median')
        self.assertIsInstance(result, dict)
    
    def test_handle_missing_values_fill_mode(self):
        result = self.processor.handle_missing_values('fill_mode')
        self.assertIsInstance(result, dict)
    
    def test_detect_outliers_iqr(self):
        result = self.processor.detect_outliers('salary', method='iqr')
        self.assertIsInstance(result, pd.Series)
    
    def test_detect_outliers_zscore(self):
        result = self.processor.detect_outliers('salary', method='zscore')
        self.assertIsInstance(result, pd.Series)
    
    def test_remove_outliers_iqr(self):
        result = self.processor.remove_outliers('salary', method='iqr')
        self.assertIsInstance(result, int)
    
    def test_remove_outliers_zscore(self):
        result = self.processor.remove_outliers('salary', method='zscore')
        self.assertIsInstance(result, int)


class TestDataAnalyzerFull(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_descriptive_stats(self):
        result = self.analyzer.get_descriptive_stats('salary')
        self.assertIn('mean', result)
    
    def test_get_grouped_stats(self):
        result = self.analyzer.get_grouped_stats('gender', 'salary')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_correlation_matrix(self):
        result = self.analyzer.get_correlation_matrix(['age', 'salary', 'work_years'])
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_frequency_analysis(self):
        result = self.analyzer.get_frequency_analysis('gender')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_crosstab(self):
        result = self.analyzer.get_crosstab('gender', 'gender')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_boxplot_data(self):
        result = self.analyzer.get_boxplot_data('gender', 'salary')
        self.assertIsInstance(result, dict)


class TestDataVisualizerFull(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
    
    def test_create_bar_chart_basic(self):
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Bar'
        )
        self.assertIsNotNone(fig)
    
    def test_create_line_chart_basic(self):
        fig = self.visualizer.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30]],
            title='Test Line'
        )
        self.assertIsNotNone(fig)
    
    def test_create_pie_chart_basic(self):
        fig = self.visualizer.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie'
        )
        self.assertIsNotNone(fig)
    
    def test_create_scatter_chart_basic(self):
        fig = self.visualizer.create_scatter_chart(
            x_data=[1, 2, 3],
            y_data=[10, 20, 30],
            title='Test Scatter'
        )
        self.assertIsNotNone(fig)
    
    def test_create_histogram_basic(self):
        fig = self.visualizer.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
            bins=5,
            title='Test Histogram'
        )
        self.assertIsNotNone(fig)
    
    def test_set_config(self):
        self.visualizer.set_config({
            'figure_size': (12, 8),
            'dpi': 100
        })
    
    def test_set_data(self):
        self.visualizer.set_data(pd.DataFrame({'A': [1, 2, 3]}))


if __name__ == '__main__':
    unittest.main()
