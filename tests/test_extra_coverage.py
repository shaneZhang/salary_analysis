import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import format_number, get_column_type, safe_divide, truncate_string
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


class TestHelpers(unittest.TestCase):
    def test_format_number_int(self):
        result = format_number(1000)
        self.assertEqual(result, '1,000')
    
    def test_format_number_float(self):
        result = format_number(1234.5678, decimal_places=2)
        self.assertEqual(result, '1,234.57')
    
    def test_format_number_none(self):
        result = format_number(None)
        self.assertEqual(result, '')
    
    def test_format_number_string(self):
        result = format_number('test')
        self.assertEqual(result, 'test')
    
    def test_get_column_type_numeric(self):
        series = pd.Series([1, 2, 3])
        result = get_column_type(series)
        self.assertEqual(result, 'numeric')
    
    def test_get_column_type_text(self):
        series = pd.Series(['a', 'b', 'c'])
        result = get_column_type(series)
        self.assertEqual(result, 'text')
    
    def test_safe_divide_normal(self):
        result = safe_divide(10, 2)
        self.assertEqual(result, 5.0)
    
    def test_safe_divide_zero(self):
        result = safe_divide(10, 0)
        self.assertEqual(result, 0.0)
    
    def test_safe_divide_custom_default(self):
        result = safe_divide(10, 0, default=-1.0)
        self.assertEqual(result, -1.0)
    
    def test_truncate_string_short(self):
        result = truncate_string('short', max_length=10)
        self.assertEqual(result, 'short')
    
    def test_truncate_string_long(self):
        result = truncate_string('this is a very long string', max_length=10)
        self.assertEqual(len(result), 10)
    
    def test_truncate_string_none(self):
        result = truncate_string(None)
        self.assertEqual(result, '')


class TestAnalysisServiceExtra(unittest.TestCase):
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
    
    def test_compare_by_dimension(self):
        result = self.service.compare_by_dimension('gender', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_crosstab(self):
        result = self.service.get_crosstab('gender', 'gender')
        self.assertTrue(result['success'])
    
    def test_get_summary_report(self):
        result = self.service.get_summary_report('salary')
        self.assertTrue(result['success'])
    
    def test_get_top_bottom(self):
        result = self.service.get_top_bottom('salary', n=3, top=True)
        self.assertTrue(result['success'])
    
    def test_get_boxplot_data(self):
        result = self.service.get_boxplot_data('gender', 'salary')
        self.assertTrue(result['success'])


class TestVisualizationServiceExtra(unittest.TestCase):
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
    
    def test_create_salary_distribution_chart(self):
        result = self.service.create_salary_distribution_chart('value')
        self.assertTrue(result['success'])
    
    def test_create_comparison_chart(self):
        result = self.service.create_comparison_chart('category', 'value')
        self.assertTrue(result['success'])


class TestDataAnalyzerExtra(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_compare_by_dimension(self):
        result = self.analyzer.compare_by_dimension('gender', 'salary')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_trend_analysis(self):
        result = self.analyzer.get_trend_analysis('work_years', 'salary')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_percentile_distribution(self):
        result = self.analyzer.get_percentile_distribution('salary')
        self.assertIsInstance(result, dict)
    
    def test_get_salary_distribution(self):
        result = self.analyzer.get_salary_distribution('salary')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_top_bottom(self):
        result = self.analyzer.get_top_bottom('salary', n=3, top=True)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_summary_report(self):
        result = self.analyzer.get_summary_report('salary')
        self.assertIsInstance(result, dict)
    
    def test_get_dimensions_analysis(self):
        result = self.analyzer.get_dimensions_analysis(['gender'], 'salary')
        self.assertIsInstance(result, dict)
    
    def test_calculate_growth_rate(self):
        result = self.analyzer.calculate_growth_rate('work_years', 'salary')
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_current_data(self):
        result = self.analyzer.get_current_data()
        self.assertIsInstance(result, pd.DataFrame)


class TestDataVisualizerExtra(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
    
    def test_create_boxplot(self):
        fig = self.visualizer.create_boxplot(
            data_dict={'A': [1, 2, 3], 'B': [4, 5, 6]},
            title='Test Boxplot'
        )
        self.assertIsNotNone(fig)
    
    def test_create_heatmap(self):
        fig = self.visualizer.create_heatmap(
            data=pd.DataFrame([[1, 2], [3, 4]]),
            title='Test Heatmap'
        )
        self.assertIsNotNone(fig)
    
    def test_save_figure(self):
        import tempfile
        fig = self.visualizer.create_bar_chart(['A'], [1], 'Test')
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.close()
        fig.savefig(temp_file.name)
        self.assertTrue(os.path.exists(temp_file.name))
        os.unlink(temp_file.name)


class TestDataProcessorExtra(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000],
            'work_years': [2, 5, 10],
            'gender': ['F', 'M', 'M']
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_create_age_group(self):
        result = self.processor.create_age_group('age')
        self.assertTrue(result)
    
    def test_create_salary_group(self):
        result = self.processor.create_salary_group('salary')
        self.assertTrue(result)
    
    def test_create_work_experience_group(self):
        result = self.processor.create_work_experience_group('work_years')
        self.assertTrue(result)
    
    def test_filter_data(self):
        result = self.processor.filter_data({'gender': 'F'})
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_data(self):
        result = self.processor.data
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_statistics(self):
        result = self.processor.data.describe()
        self.assertIsInstance(result, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
