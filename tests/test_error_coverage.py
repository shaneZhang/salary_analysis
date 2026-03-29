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
        result = self.service.get_crosstab('gender', 'gender')
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
        result = self.service.get_trend_analysis('work_years', 'salary')
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
    
    def test_remove_duplicates_no_data(self):
        result = self.service.remove_duplicates()
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_no_data(self):
        result = self.service.handle_missing_values('drop')
        self.assertTrue(result['success'])
    
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
    
    def test_filter_data_no_data(self):
        result = self.service.filter_data({'gender': 'F'})
        self.assertTrue(result['success'])
    
    def test_convert_dtype_no_data(self):
        result = self.service.convert_dtype('salary', 'float')
        self.assertFalse(result['success'])
    
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
        result = self.service.create_trend_chart('work_years', 'salary')
        self.assertFalse(result['success'])


class TestDataServiceNoData(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = DataService(self.data_manager, self.config, self.logger)
    
    def test_load_file_invalid_path(self):
        result = self.service.load_file('/nonexistent/path/file.xlsx')
        self.assertFalse(result['success'])
    
    def test_get_preview_no_data(self):
        result = self.service.get_preview(10)
        self.assertIsNone(result)
    
    def test_export_data_no_data(self):
        result = self.service.export_data('/tmp/output.xlsx')
        self.assertFalse(result['success'])


class TestDataLoaderInvalidPath(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
    
    def test_load_excel_invalid_path(self):
        from src.exceptions import DataLoadError
        with self.assertRaises(DataLoadError):
            self.loader.load_excel('/nonexistent/path/file.xlsx')
    
    def test_get_sheet_names_invalid_path(self):
        from src.exceptions import DataLoadError
        with self.assertRaises(DataLoadError):
            self.loader.get_sheet_names('/nonexistent/path/file.xlsx')


class TestDataAnalyzerExtended(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20],
            'score': [1.5, 2.5, 3.5, 4.5, 5.5]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_correlation_with_multiple_columns(self):
        result = self.analyzer.get_correlation('age', 'salary')
        self.assertIn('pearson_r', result)
    
    def test_get_correlation_matrix_all_numeric(self):
        result = self.analyzer.get_correlation_matrix()
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_percentile_distribution_custom_percentiles(self):
        result = self.analyzer.get_percentile_distribution('salary', percentiles=[10, 25, 50, 75, 90])
        self.assertIsInstance(result, dict)
    
    def test_get_top_bottom_bottom(self):
        result = self.analyzer.get_top_bottom('salary', n=3, top=False)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_get_salary_distribution_custom_bins(self):
        result = self.analyzer.get_salary_distribution('salary', bins=[0, 15000, 30000, 50000])
        self.assertIsInstance(result, pd.DataFrame)


class TestDataProcessorWithMissing(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', None, 'David', 'Eve'],
            'age': [25, 30, 35, None, 45],
            'salary': [10000, 15000, 20000, 25000, None],
            'work_years': [2, 5, 10, 15, 20],
            'gender': ['F', 'M', 'M', 'M', 'F']
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_handle_missing_values_drop_with_missing(self):
        result = self.processor.handle_missing_values('drop')
        self.assertIsInstance(result, dict)
    
    def test_handle_missing_values_fill_forward(self):
        result = self.processor.handle_missing_values('fill_forward')
        self.assertIsInstance(result, dict)
    
    def test_handle_missing_values_fill_backward(self):
        result = self.processor.handle_missing_values('fill_backward')
        self.assertIsInstance(result, dict)
    
    def test_handle_missing_values_fill_constant(self):
        result = self.processor.handle_missing_values('fill_value', fill_value=0)
        self.assertIsInstance(result, dict)


class TestDataVisualizerWithCustomConfig(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
        self.visualizer.set_config({
            'figure_size': (10, 6),
            'dpi': 100,
            'title_fontsize': 14,
            'label_fontsize': 12,
            'tick_fontsize': 10,
            'legend_fontsize': 10,
            'colors': ['#FF0000', '#00FF00', '#0000FF']
        })
    
    def test_create_bar_chart_with_custom_config(self):
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Custom Config Bar'
        )
        self.assertIsNotNone(fig)
    
    def test_create_pie_chart_with_custom_colors(self):
        fig = self.visualizer.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Custom Colors Pie'
        )
        self.assertIsNotNone(fig)


if __name__ == '__main__':
    unittest.main()
