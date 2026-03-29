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
from src.models.app_state import AppState, AppStateStatus
from src.services.data_service import DataService
from src.services.processing_service import ProcessingService
from src.services.analysis_service import AnalysisService
from src.services.visualization_service import VisualizationService
from src.core.data_loader import DataLoader
from src.core.data_processor import DataProcessor
from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer


class TestVisualizationServiceMore(unittest.TestCase):
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
    
    def test_create_scatter_chart(self):
        result = self.service.create_scatter_chart(
            x_data=[1, 2, 3, 4],
            y_data=[10, 20, 30, 40],
            title='Test Scatter'
        )
        self.assertTrue(result['success'])
    
    def test_create_boxplot(self):
        result = self.service.create_boxplot(
            data_dict={'A': [1, 2, 3], 'B': [4, 5, 6]},
            title='Test Boxplot'
        )
        self.assertTrue(result['success'])
    
    def test_create_heatmap(self):
        result = self.service.create_heatmap(
            data=pd.DataFrame([[1, 2], [3, 4]]),
            title='Test Heatmap'
        )
        self.assertTrue(result['success'])
    
    def test_save_chart(self):
        self.service.create_bar_chart(['A'], [1], 'Test')
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.close()
        result = self.service.save_chart(temp_file.name)
        self.assertTrue(result['success'])
        os.unlink(temp_file.name)
    
    def test_set_figure_size(self):
        result = self.service.set_figure_size(12, 8)
        self.assertIsNone(result)
    
    def test_set_dpi(self):
        result = self.service.set_dpi(150)
        self.assertIsNone(result)
    
    def test_set_color_scheme(self):
        result = self.service.set_color_scheme(['#FF0000', '#00FF00'])
        self.assertIsNone(result)


class TestAnalysisServiceMore(unittest.TestCase):
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
    
    def test_get_trend_analysis(self):
        result = self.service.get_trend_analysis('work_years', 'salary')
        self.assertTrue(result['success'])
    
    def test_get_salary_distribution(self):
        result = self.service.get_salary_distribution('salary')
        self.assertTrue(result['success'])
    
    def test_get_dimensions_analysis(self):
        result = self.service.get_dimensions_analysis(['gender'], 'salary')
        self.assertTrue(result['success'])


class TestProcessingServiceMore(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.config = ConfigManager()
        self.logger = AppLogger.get_instance()
        self.service = ProcessingService(self.data_manager, self.config, self.logger)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000],
            'work_years': [2, 5, 10],
            'gender': ['F', 'M', 'M']
        })
        self.data_manager.set_data(self.test_data)
    
    def test_convert_dtype(self):
        result = self.service.convert_dtype('salary', 'float')
        self.assertTrue(result['success'])
    
    def test_filter_data(self):
        result = self.service.filter_data({'gender': 'F'})
        self.assertTrue(result['success'])
    
    def test_encode_categorical(self):
        result = self.service.encode_categorical(columns=['gender'])
        self.assertTrue(result['success'])


class TestDataServiceMore(unittest.TestCase):
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
    
    def test_get_sheet_names_service(self):
        result = self.service.get_sheet_names(self.excel_path)
        self.assertIsInstance(result, list)
    
    def test_export_data(self):
        self.service.load_file(self.excel_path)
        export_path = os.path.join(self.temp_dir, 'export.xlsx')
        result = self.service.export_data(export_path)
        self.assertTrue(result['success'])
    
    def test_get_preview(self):
        self.service.load_file(self.excel_path)
        preview = self.service.get_preview(2)
        self.assertIsNotNone(preview)
    
    def test_apply_field_mapping(self):
        self.service.load_file(self.excel_path)
        result = self.service.apply_field_mapping({'姓名': 'employee_name'})
        self.assertTrue(result['success'])


class TestDataLoaderMore(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
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
    
    def test_load_excel_with_multiple_sheets(self):
        with pd.ExcelWriter(self.excel_path, engine='openpyxl') as writer:
            self.test_data.to_excel(writer, sheet_name='Sheet1', index=False)
            self.test_data.to_excel(writer, sheet_name='Sheet2', index=False)
        
        result = self.loader.load_excel(self.excel_path, sheet_name='Sheet2')
        self.assertEqual(len(result), 3)


class TestDataProcessorMore(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000],
            'work_years': [2, 5, 10],
            'gender': ['F', 'M', 'M']
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_handle_outliers(self):
        result = self.processor.handle_outliers('salary', strategy='remove')
        self.assertIsNotNone(result)
    
    def test_convert_dtype_invalid_column(self):
        result = self.processor.convert_dtype('nonexistent', 'float')
        self.assertFalse(result)
    
    def test_create_calculated_field_valid(self):
        result = self.processor.create_calculated_field('double_salary', lambda df: df['salary'] * 2)
        self.assertTrue(result)


class TestDataAnalyzerMore(unittest.TestCase):
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
    
    def test_get_correlation_invalid_columns(self):
        result = self.analyzer.get_correlation('nonexistent', 'salary')
        self.assertEqual(result, {})


class TestDataVisualizerMore(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
    
    def test_create_line_chart_multiple_series(self):
        fig = self.visualizer.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30], [5, 10, 15]],
            labels=['Series1', 'Series2'],
            title='Test Multi-Line'
        )
        self.assertIsNotNone(fig)
    
    def test_create_pie_chart_with_colors(self):
        fig = self.visualizer.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie',
            colors=['#FF0000', '#00FF00', '#0000FF']
        )
        self.assertIsNotNone(fig)
    
    def test_create_bar_chart_with_labels(self):
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Bar',
            labels=['10%', '20%', '30%']
        )
        self.assertIsNotNone(fig)


class TestConfigManagerMore(unittest.TestCase):
    def test_get_default_field_mapping(self):
        config = ConfigManager()
        mapping = config.get_field_mapping()
        self.assertIn('姓名', mapping)
        self.assertEqual(mapping['姓名'], 'name')
    
    def test_get_default_salary_bins(self):
        config = ConfigManager()
        bins = config.get_salary_bins()
        self.assertTrue(len(bins) > 0)
    
    def test_get_default_chart_colors(self):
        config = ConfigManager()
        colors = config.get_chart_colors()
        self.assertTrue(len(colors) > 0)
    
    def test_get_app_config(self):
        config = ConfigManager()
        app_config = config.get_app_config()
        self.assertIsNotNone(app_config)


if __name__ == '__main__':
    unittest.main()
