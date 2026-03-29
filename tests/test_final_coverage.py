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
from src.events.event_bus import EventBus


class TestEventBusExtended(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus.get_instance()
        self.bus.clear()
    
    def test_publish_no_handlers(self):
        self.bus.publish('nonexistent_event', 'data')
    
    def test_multiple_handlers(self):
        results = []
        
        def handler1(data):
            results.append(('handler1', data))
        
        def handler2(data):
            results.append(('handler2', data))
        
        self.bus.subscribe('test', handler1)
        self.bus.subscribe('test', handler2)
        self.bus.publish('test', 'test_data')
        
        self.assertEqual(len(results), 2)
    
    def test_clear(self):
        def handler(data):
            pass
        self.bus.subscribe('test', handler)
        self.bus.clear()
        self.assertFalse(self.bus.has_handlers('test'))


class TestAppStateExtended(unittest.TestCase):
    def setUp(self):
        self.state = AppState.get_instance()
        self.state.reset()
    
    def test_subscribe(self):
        notified = []
        
        def observer(state):
            notified.append(True)
        
        self.state.subscribe(observer)
        self.state.set_status(AppStateStatus.LOADING)
        self.assertEqual(len(notified), 1)
    
    def test_unsubscribe(self):
        notified = []
        
        def observer(state):
            notified.append(True)
        
        self.state.subscribe(observer)
        self.state.unsubscribe(observer)
        self.state.set_status(AppStateStatus.LOADING)
        self.assertEqual(len(notified), 0)


class TestDataManagerExtended(unittest.TestCase):
    def setUp(self):
        self.dm = DataManager()
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000]
        })
    
    def test_update_data(self):
        self.dm.set_data(self.test_data)
        self.dm.update_data(lambda df: df[df['age'] > 25])
        result = self.dm.get_data()
        self.assertEqual(len(result), 2)
    
    def test_update_data_no_data(self):
        self.dm.update_data(lambda df: df)
        result = self.dm.get_data()
        self.assertIsNone(result)


class TestDataLoaderExtended(unittest.TestCase):
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
    
    def test_validate_data_no_data(self):
        is_valid, errors = self.loader.validate_data()
        self.assertFalse(is_valid)
        self.assertIn('没有加载数据', errors)


class TestDataProcessorExtended(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000],
            'work_years': [2, 5, 10],
            'gender': ['F', 'M', 'M']
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_remove_duplicates_no_data(self):
        processor = DataProcessor()
        result = processor.remove_duplicates()
        self.assertEqual(result, 0)
    
    def test_handle_missing_values_no_data(self):
        processor = DataProcessor()
        result = processor.handle_missing_values('drop')
        self.assertEqual(result, {})
    
    def test_detect_outliers_no_data(self):
        processor = DataProcessor()
        result = processor.detect_outliers('salary')
        self.assertTrue(result.empty)
    
    def test_create_age_group_custom_bins(self):
        result = self.processor.create_age_group('age', bins=[0, 30, 100], labels=['年轻', '中年'])
        self.assertTrue(result)
    
    def test_create_salary_group_custom_bins(self):
        result = self.processor.create_salary_group('salary', bins=[0, 15000, 999999], labels=['低', '高'])
        self.assertTrue(result)
    
    def test_create_experience_group_custom_bins(self):
        result = self.processor.create_work_experience_group('work_years', bins=[0, 5, 999], labels=['新手', '老手'])
        self.assertTrue(result)


class TestDataAnalyzerExtended(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_frequency_analysis_no_data(self):
        analyzer = DataAnalyzer()
        result = analyzer.get_frequency_analysis('gender')
        self.assertTrue(result.empty)
    
    def test_get_crosstab_no_data(self):
        analyzer = DataAnalyzer()
        result = analyzer.get_crosstab('gender', 'gender')
        self.assertTrue(result.empty)
    
    def test_get_correlation_matrix_no_data(self):
        analyzer = DataAnalyzer()
        result = analyzer.get_correlation_matrix(['age', 'salary'])
        self.assertTrue(result.empty)
    
    def test_get_boxplot_data_no_data(self):
        analyzer = DataAnalyzer()
        result = analyzer.get_boxplot_data('gender', 'salary')
        self.assertEqual(result, {})


class TestDataVisualizerExtended(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
    
    def test_create_bar_chart_horizontal(self):
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Horizontal Bar',
            horizontal=True
        )
        self.assertIsNotNone(fig)
    
    def test_create_histogram_with_kde(self):
        fig = self.visualizer.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
            bins=5,
            title='Test Histogram with KDE',
            kde=True
        )
        self.assertIsNotNone(fig)
    
    def test_create_pie_chart_autopct(self):
        fig = self.visualizer.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie with Autopct',
            autopct='%1.1f%%'
        )
        self.assertIsNotNone(fig)


class TestProcessingServiceExtended(unittest.TestCase):
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
    
    def test_handle_missing_values_fill_constant(self):
        result = self.service.handle_missing_values('fill_constant', fill_value=0)
        self.assertTrue(result['success'])


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
    
    def test_get_crosstab_normalized(self):
        result = self.service.get_crosstab('gender', 'gender', normalize=True)
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()
