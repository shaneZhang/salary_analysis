"""
模型层单元测试
"""

import unittest
import pandas as pd
import numpy as np
import tempfile
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_manager import DataManager
from src.models.config_manager import ConfigManager, AppConfig
from src.models.app_state import AppStatusManager, AppState, SelectionManager
from src.events.event_bus import EventBus, EVENT_TYPES


class TestDataManager(unittest.TestCase):
    """DataManager测试"""
    
    def setUp(self):
        self.dm = DataManager()
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000]
        })
    
    def test_set_and_get_data(self):
        """测试设置和获取数据"""
        self.dm.set_data(self.test_data)
        
        result = self.dm.get_data()
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
    
    def test_has_data(self):
        """测试数据存在检查"""
        self.assertFalse(self.dm.has_data())
        
        self.dm.set_data(self.test_data)
        self.assertTrue(self.dm.has_data())
    
    def test_get_data_info(self):
        """测试获取数据信息"""
        self.dm.set_data(self.test_data)
        
        info = self.dm.get_data_info()
        
        self.assertEqual(info['rows'], 3)
        self.assertEqual(info['columns'], 3)
        self.assertIn('name', info['column_names'])
    
    def test_get_column_names(self):
        """测试获取列名"""
        self.dm.set_data(self.test_data)
        
        all_cols = self.dm.get_column_names()
        self.assertEqual(len(all_cols), 3)
        
        numeric_cols = self.dm.get_column_names('numeric')
        self.assertEqual(len(numeric_cols), 2)
        
        categorical_cols = self.dm.get_column_names('categorical')
        self.assertEqual(len(categorical_cols), 1)
    
    def test_update_data(self):
        """测试更新数据"""
        self.dm.set_data(self.test_data)
        
        self.dm.update_data(lambda df: df[df['age'] > 25])
        
        result = self.dm.get_data()
        self.assertEqual(len(result), 2)
    
    def test_reset(self):
        """测试重置数据"""
        self.dm.set_data(self.test_data)
        self.dm.update_data(lambda df: df[df['age'] > 25])
        
        self.dm.reset()
        
        result = self.dm.get_data()
        self.assertEqual(len(result), 3)
    
    def test_clear(self):
        """测试清除数据"""
        self.dm.set_data(self.test_data)
        self.dm.clear()
        
        self.assertFalse(self.dm.has_data())
    
    def test_observer_pattern(self):
        """测试观察者模式"""
        notified = []
        
        def observer(data):
            notified.append(data)
        
        self.dm.subscribe(observer)
        self.dm.set_data(self.test_data)
        
        self.assertEqual(len(notified), 1)
        
        self.dm.unsubscribe(observer)
        self.dm.update_data(lambda df: df)
        
        self.assertEqual(len(notified), 1)


class TestConfigManager(unittest.TestCase):
    """ConfigManager测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ConfigManager()
        
        self.assertIsNotNone(config.get_field_mapping())
        self.assertIsNotNone(config.get_salary_bins())
        self.assertIsNotNone(config.get_chart_colors())
    
    def test_get_config_value(self):
        """测试获取配置值"""
        config = ConfigManager()
        
        title = config.get('app_title', 'Default')
        self.assertEqual(title, '园区白领薪资数据分析工具')
        
        unknown = config.get('unknown_key', 'default_value')
        self.assertEqual(unknown, 'default_value')
    
    def test_set_config_value(self):
        """测试设置配置值"""
        config = ConfigManager()
        
        config.set('custom_key', 'custom_value')
        
        result = config.get('custom_key')
        self.assertEqual(result, 'custom_value')
    
    def test_save_and_load_config(self):
        """测试保存和加载配置"""
        config = ConfigManager()
        config.set('test_key', 'test_value')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            config.save(temp_path)
            
            new_config = ConfigManager(temp_path)
            
            result = new_config.get('test_key', 'default')
            self.assertEqual(result, 'test_value')
        finally:
            os.unlink(temp_path)


class TestAppStatusManager(unittest.TestCase):
    """AppStatusManager测试"""
    
    def setUp(self):
        self.sm = AppStatusManager()
    
    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.sm.state, AppState.IDLE)
        self.assertEqual(self.sm.message, '就绪')
    
    def test_set_state(self):
        """测试设置状态"""
        self.sm.set_state(AppState.LOADING, '加载中...', 50)
        
        self.assertEqual(self.sm.state, AppState.LOADING)
        self.assertEqual(self.sm.message, '加载中...')
        self.assertEqual(self.sm.progress, 50.0)
    
    def test_convenience_methods(self):
        """测试便捷方法"""
        self.sm.set_loading('测试加载')
        self.assertEqual(self.sm.state, AppState.LOADING)
        
        self.sm.set_processing('测试处理')
        self.assertEqual(self.sm.state, AppState.PROCESSING)
        
        self.sm.set_error('测试错误')
        self.assertEqual(self.sm.state, AppState.ERROR)
        
        self.sm.set_idle('就绪')
        self.assertEqual(self.sm.state, AppState.IDLE)
    
    def test_is_busy(self):
        """测试忙碌状态检查"""
        self.assertFalse(self.sm.is_busy())
        
        self.sm.set_loading()
        self.assertTrue(self.sm.is_busy())
        
        self.sm.set_idle()
        self.assertFalse(self.sm.is_busy())
    
    def test_observer_pattern(self):
        """测试观察者模式"""
        notified = []
        
        def observer(status_info):
            notified.append(status_info)
        
        self.sm.subscribe(observer)
        self.sm.set_loading('测试')
        
        self.assertEqual(len(notified), 1)
        self.assertEqual(notified[0].state, AppState.LOADING)


class TestSelectionManager(unittest.TestCase):
    """SelectionManager测试"""
    
    def setUp(self):
        self.sm = SelectionManager()
    
    def test_dimension(self):
        """测试维度选择"""
        self.sm.dimension = 'gender'
        self.assertEqual(self.sm.dimension, 'gender')
    
    def test_salary_column(self):
        """测试薪资列选择"""
        self.sm.salary_column = 'pre_tax_salary'
        self.assertEqual(self.sm.salary_column, 'pre_tax_salary')
    
    def test_chart_type(self):
        """测试图表类型"""
        self.sm.chart_type = 'bar'
        self.assertEqual(self.sm.chart_type, 'bar')
    
    def test_filters(self):
        """测试筛选条件"""
        self.sm.set_filter('gender', '男')
        self.sm.set_filter('age', [25, 30, 35])
        
        filters = self.sm.get_filters()
        self.assertEqual(filters['gender'], '男')
        self.assertEqual(len(filters['age']), 3)
        
        self.sm.remove_filter('gender')
        self.assertNotIn('gender', self.sm.get_filters())
        
        self.sm.clear_filters()
        self.assertEqual(len(self.sm.get_filters()), 0)
    
    def test_reset(self):
        """测试重置"""
        self.sm.dimension = 'gender'
        self.sm.salary_column = 'post_tax_salary'
        self.sm.chart_type = 'pie'
        self.sm.set_filter('test', 'value')
        
        self.sm.reset()
        
        self.assertEqual(self.sm.dimension, '')
        self.assertEqual(self.sm.salary_column, 'pre_tax_salary')
        self.assertEqual(self.sm.chart_type, 'bar')
        self.assertEqual(len(self.sm.get_filters()), 0)


class TestEventBus(unittest.TestCase):
    """EventBus测试"""
    
    def setUp(self):
        self.eb = EventBus()
    
    def test_subscribe_and_publish(self):
        """测试订阅和发布"""
        received = []
        
        def handler(event):
            received.append(event)
        
        self.eb.subscribe('test_event', handler)
        self.eb.publish('test_event', {'data': 'test'})
        
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].data['data'], 'test')
    
    def test_unsubscribe(self):
        """测试取消订阅"""
        received = []
        
        def handler(event):
            received.append(event)
        
        self.eb.subscribe('test_event', handler)
        self.eb.publish('test_event', {})
        
        self.eb.unsubscribe('test_event', handler)
        self.eb.publish('test_event', {})
        
        self.assertEqual(len(received), 1)
    
    def test_multiple_handlers(self):
        """测试多个处理器"""
        results = []
        
        def handler1(event):
            results.append('handler1')
        
        def handler2(event):
            results.append('handler2')
        
        self.eb.subscribe('test_event', handler1)
        self.eb.subscribe('test_event', handler2)
        self.eb.publish('test_event', {})
        
        self.assertEqual(len(results), 2)
    
    def test_get_handlers(self):
        """测试获取处理器"""
        def handler(event):
            pass
        
        self.eb.subscribe('test_event', handler)
        
        handlers = self.eb.get_handlers('test_event')
        self.assertEqual(len(handlers), 1)
    
    def test_clear_handlers(self):
        """测试清除处理器"""
        def handler(event):
            pass
        
        self.eb.subscribe('test_event', handler)
        self.eb.clear_handlers('test_event')
        
        handlers = self.eb.get_handlers('test_event')
        self.assertEqual(len(handlers), 0)


if __name__ == '__main__':
    unittest.main()
