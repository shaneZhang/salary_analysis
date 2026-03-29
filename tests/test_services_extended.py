import unittest
import pandas as pd
import numpy as np
import os
import sys
import tempfile
import shutil
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.config_manager import ConfigManager
from src.models.data_manager import DataManager
from src.models.logger import AppLogger
from src.models.app_state import AppState, AppStateStatus
from src.services.data_service import DataService
from src.services.processing_service import ProcessingService
from src.services.analysis_service import AnalysisService
from src.services.visualization_service import VisualizationService


class TestConfigManagerExtended(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        
        self.config_data = {
            "field_mapping": {
                "姓名": "name",
                "性别": "gender",
                "年龄": "age"
            },
            "salary_bins": [0, 5000, 10000, 15000, 20000],
            "salary_labels": ["5千以下", "5千-1万", "1万-1.5万", "1.5万-2万"],
            "chart_colors": ["#FF0000", "#00FF00", "#0000FF"]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, ensure_ascii=False)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_config_from_file(self):
        config = ConfigManager(self.config_path)
        field_mapping = config.get_field_mapping()
        self.assertEqual(field_mapping['姓名'], 'name')
    
    def test_get_salary_bins(self):
        config = ConfigManager(self.config_path)
        bins = config.get_salary_bins()
        self.assertEqual(len(bins), 5)
    
    def test_get_salary_labels(self):
        config = ConfigManager(self.config_path)
        labels = config.get_salary_labels()
        self.assertEqual(len(labels), 4)
    
    def test_get_chart_colors(self):
        config = ConfigManager(self.config_path)
        colors = config.get_chart_colors()
        self.assertEqual(len(colors), 3)
    
    def test_get_age_bins(self):
        config = ConfigManager()
        bins = config.get_age_bins()
        self.assertIsInstance(bins, list)
    
    def test_get_age_labels(self):
        config = ConfigManager()
        labels = config.get_age_labels()
        self.assertIsInstance(labels, list)
    
    def test_get_experience_bins(self):
        config = ConfigManager()
        bins = config.get_experience_bins()
        self.assertIsInstance(bins, list)
    
    def test_get_experience_labels(self):
        config = ConfigManager()
        labels = config.get_experience_labels()
        self.assertIsInstance(labels, list)
    
    def test_get_figure_size(self):
        config = ConfigManager()
        size = config.get_figure_size()
        self.assertIsInstance(size, tuple)
    
    def test_get_dpi(self):
        config = ConfigManager()
        dpi = config.get_dpi()
        self.assertIsInstance(dpi, int)
    
    def test_get_font_sizes(self):
        config = ConfigManager()
        title_size = config._app_config.title_fontsize
        label_size = config._app_config.label_fontsize
        self.assertIsInstance(title_size, int)
        self.assertIsInstance(label_size, int)


class TestDataServiceExtended(unittest.TestCase):
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
    
    def test_load_file_success(self):
        result = self.service.load_file(self.excel_path)
        self.assertTrue(result['success'])
        self.assertEqual(result['rows'], 3)
    
    def test_load_file_invalid(self):
        result = self.service.load_file('/nonexistent/file.xlsx')
        self.assertFalse(result['success'])
    
    def test_load_folder_success(self):
        result = self.service.load_folder(self.temp_dir)
        self.assertTrue(result['success'])
    
    def test_load_folder_invalid(self):
        result = self.service.load_folder('/nonexistent/folder')
        self.assertFalse(result['success'])
    
    def test_load_multiple_files_success(self):
        result = self.service.load_multiple_files([self.excel_path])
        self.assertTrue(result['success'])
    
    def test_get_data_info(self):
        self.service.load_file(self.excel_path)
        info = self.service.get_data_info()
        self.assertTrue(info['has_data'])
    
    def test_get_field_mapping(self):
        mapping = self.service.get_field_mapping()
        self.assertIn('姓名', mapping)
    
    def test_validate_current_data(self):
        self.service.load_file(self.excel_path)
        is_valid, errors = self.service.validate_current_data()
        self.assertTrue(is_valid)


class TestProcessingServiceExtended(unittest.TestCase):
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
    
    def test_handle_missing_values_fill_mean(self):
        result = self.service.handle_missing_values('fill_mean')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_fill_median(self):
        result = self.service.handle_missing_values('fill_median')
        self.assertTrue(result['success'])
    
    def test_handle_missing_values_fill_mode(self):
        result = self.service.handle_missing_values('fill_mode')
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
        self.service.remove_duplicates()
        result = self.service.reset_data()
        self.assertTrue(result['success'])
    
    def test_get_data_summary(self):
        summary = self.service.get_data_summary()
        self.assertIn('total_rows', summary)


class TestAnalysisServiceExtended(unittest.TestCase):
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


class TestVisualizationServiceExtended(unittest.TestCase):
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


class TestAppStateExtended(unittest.TestCase):
    def setUp(self):
        self.state = AppState.get_instance()
        self.state.reset()
    
    def test_set_get_status(self):
        self.state.set_status(AppStateStatus.LOADING)
        self.assertEqual(self.state.get_status(), AppStateStatus.LOADING)
    
    def test_set_get_current_file(self):
        self.state.set_current_file('/path/to/file.xlsx')
        self.assertEqual(self.state.get_current_file(), '/path/to/file.xlsx')
    
    def test_set_error(self):
        self.state.set_error('Test error')
        self.assertEqual(self.state.get_error(), 'Test error')
        self.assertEqual(self.state.get_status(), AppStateStatus.ERROR)
    
    def test_clear_error(self):
        self.state.set_error('Test error')
        self.state.clear_error()
        self.assertIsNone(self.state.get_error())
        self.assertEqual(self.state.get_status(), AppStateStatus.IDLE)
    
    def test_set_get_state(self):
        self.state.set_state('custom_key', 'custom_value')
        self.assertEqual(self.state.get_state()['custom_key'], 'custom_value')


if __name__ == '__main__':
    unittest.main()
