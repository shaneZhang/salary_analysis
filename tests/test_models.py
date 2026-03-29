import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_manager import DataManager
from src.models.config_manager import ConfigManager
from src.models.app_state import AppState, AppStateStatus
from src.events.event_bus import EventBus
from src.exceptions import (
    AppException, DataException, DataLoadError, 
    DataValidationError, DataProcessingError,
    AnalysisException, AnalysisError,
    VisualizationException, VisualizationError,
    ConfigurationException, ConfigurationError
)


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.dm = DataManager()
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000]
        })
    
    def test_set_and_get_data(self):
        self.dm.set_data(self.test_data)
        result = self.dm.get_data()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
    
    def test_get_data_info(self):
        self.dm.set_data(self.test_data)
        info = self.dm.get_data_info()
        self.assertEqual(info['rows'], 3)
        self.assertEqual(info['columns'], 3)
        self.assertTrue(info['has_data'])
    
    def test_has_data(self):
        self.assertFalse(self.dm.has_data())
        self.dm.set_data(self.test_data)
        self.assertTrue(self.dm.has_data())
    
    def test_subscribe_notify(self):
        notified = []
        
        def observer(data):
            notified.append(data)
        
        self.dm.subscribe(observer)
        self.dm.set_data(self.test_data)
        self.assertEqual(len(notified), 1)
    
    def test_unsubscribe(self):
        notified = []
        
        def observer(data):
            notified.append(data)
        
        self.dm.subscribe(observer)
        self.dm.unsubscribe(observer)
        self.dm.set_data(self.test_data)
        self.assertEqual(len(notified), 0)
    
    def test_reset(self):
        self.dm.set_data(self.test_data)
        self.dm.update_data(lambda df: df[df['age'] > 30])
        self.assertEqual(len(self.dm.get_data()), 1)
        
        self.dm.reset()
        self.assertEqual(len(self.dm.get_data()), 3)
    
    def test_clear(self):
        self.dm.set_data(self.test_data)
        self.dm.clear()
        self.assertFalse(self.dm.has_data())


class TestConfigManager(unittest.TestCase):
    def test_default_config(self):
        config = ConfigManager()
        field_mapping = config.get_field_mapping()
        self.assertIn('姓名', field_mapping)
        self.assertEqual(field_mapping['姓名'], 'name')
    
    def test_get_salary_bins(self):
        config = ConfigManager()
        bins = config.get_salary_bins()
        self.assertIsInstance(bins, list)
        self.assertTrue(len(bins) > 0)
    
    def test_get_chart_colors(self):
        config = ConfigManager()
        colors = config.get_chart_colors()
        self.assertIsInstance(colors, list)
        self.assertTrue(len(colors) > 0)
    
    def test_get_set_value(self):
        config = ConfigManager()
        config.set('test_key', 'test_value')
        self.assertEqual(config.get('test_key'), 'test_value')
        self.assertEqual(config.get('nonexistent', 'default'), 'default')


class TestAppState(unittest.TestCase):
    def setUp(self):
        self.state = AppState()
        self.state.reset()
    
    def test_singleton(self):
        state2 = AppState.get_instance()
        self.assertIs(self.state, state2)
    
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


class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.bus.clear()
    
    def test_singleton(self):
        bus2 = EventBus.get_instance()
        self.assertIs(self.bus, bus2)
    
    def test_subscribe_publish(self):
        results = []
        
        def handler(data):
            results.append(data)
        
        self.bus.subscribe('test_event', handler)
        self.bus.publish('test_event', 'test_data')
        self.assertEqual(results, ['test_data'])
    
    def test_unsubscribe(self):
        results = []
        
        def handler(data):
            results.append(data)
        
        self.bus.subscribe('test_event', handler)
        self.bus.unsubscribe('test_event', handler)
        self.bus.publish('test_event', 'test_data')
        self.assertEqual(results, [])
    
    def test_has_handlers(self):
        self.assertFalse(self.bus.has_handlers('test_event'))
        self.bus.subscribe('test_event', lambda x: x)
        self.assertTrue(self.bus.has_handlers('test_event'))


class TestExceptions(unittest.TestCase):
    def test_app_exception(self):
        exc = AppException('Test message')
        self.assertEqual(str(exc), 'Test message')
    
    def test_app_exception_with_details(self):
        exc = AppException('Test message', 'Additional details')
        self.assertIn('Test message', str(exc))
        self.assertIn('Additional details', str(exc))
    
    def test_data_load_error(self):
        exc = DataLoadError('Load failed')
        self.assertIsInstance(exc, DataException)
        self.assertIsInstance(exc, AppException)
    
    def test_data_validation_error(self):
        exc = DataValidationError('Validation failed')
        self.assertIsInstance(exc, DataException)
    
    def test_analysis_error(self):
        exc = AnalysisError('Analysis failed')
        self.assertIsInstance(exc, AnalysisException)
    
    def test_visualization_error(self):
        exc = VisualizationError('Viz failed')
        self.assertIsInstance(exc, VisualizationException)
    
    def test_configuration_error(self):
        exc = ConfigurationError('Config failed')
        self.assertIsInstance(exc, ConfigurationException)


if __name__ == '__main__':
    unittest.main()
