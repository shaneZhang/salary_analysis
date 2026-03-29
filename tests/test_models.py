import pytest
import pandas as pd
import os
import tempfile
from typing import Dict, Any

from src.models import DataManager, ConfigManager, Logger
from src.models.config_manager import AppConfig


class TestDataManager:
    """测试DataManager类"""
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        dm1 = DataManager()
        dm2 = DataManager()
        assert dm1 is dm2
    
    def test_set_and_get_data(self, sample_dataframe):
        """测试设置和获取数据"""
        dm = DataManager()
        dm.set_data(sample_dataframe, "test_data")
        
        result = dm.get_data("test_data")
        assert result is not None
        assert len(result) == len(sample_dataframe)
    
    def test_get_nonexistent_data(self):
        """测试获取不存在的数据"""
        dm = DataManager()
        result = dm.get_data("nonexistent")
        assert result is None
    
    def test_has_data(self, sample_dataframe):
        """测试has_data方法"""
        dm = DataManager()
        assert not dm.has_data()
        
        dm.set_data(sample_dataframe)
        assert dm.has_data()
    
    def test_update_data(self, sample_dataframe):
        """测试更新数据"""
        dm = DataManager()
        dm.set_data(sample_dataframe)
        
        new_df = sample_dataframe.head(50)
        dm.update_data(new_df)
        
        result = dm.get_data()
        assert len(result) == 50
    
    def test_data_change_notification(self, sample_dataframe):
        """测试数据变化通知"""
        dm = DataManager()
        notifications = []
        
        def callback(data):
            notifications.append(data)
        
        dm.subscribe(callback)
        
        dm.set_data(sample_dataframe)
        assert len(notifications) == 1
        assert notifications[0] is not None
        
        dm.update_data(sample_dataframe.head(10))
        assert len(notifications) == 2
    
    def test_get_data_info(self, sample_dataframe):
        """测试获取数据信息"""
        dm = DataManager()
        dm.set_data(sample_dataframe)
        
        info = dm.get_data_info()
        assert isinstance(info, dict)
        assert 'rows' in info
        assert 'columns' in info
        assert 'column_names' in info
        assert info['rows'] == len(sample_dataframe)
        assert info['columns'] == len(sample_dataframe.columns)
    
    def test_reset_data(self, sample_dataframe):
        """测试重置数据到原始状态"""
        dm = DataManager()
        dm.set_data(sample_dataframe)
        assert dm.has_data()
        
        # 修改数据
        modified = sample_dataframe.head(50)
        dm.update_data(modified)
        assert len(dm.get_data()) == 50
        
        # 重置到原始状态
        dm.reset()
        assert len(dm.get_data()) == 100  # 应该恢复到原始大小


class TestConfigManager:
    """测试ConfigManager类"""
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        ConfigManager._instance = None  # 重置单例
        cm1 = ConfigManager()
        cm2 = ConfigManager()
        assert cm1 is cm2
    
    def test_load_default_config(self):
        """测试加载默认配置"""
        ConfigManager._instance = None  # 重置单例
        cm = ConfigManager()
        config = cm.get_config()
        assert isinstance(config, AppConfig)
        assert config.field_mapping is not None
    
    def test_get_specific_config(self):
        """测试获取特定配置项"""
        ConfigManager._instance = None  # 重置单例
        cm = ConfigManager()
        
        figure_size = cm.get('figure_size')
        assert isinstance(figure_size, tuple)
        assert len(figure_size) == 2
        
        dpi = cm.get('dpi')
        assert isinstance(dpi, int)
    
    def test_get_nested_config(self):
        """测试获取嵌套配置"""
        ConfigManager._instance = None  # 重置单例
        cm = ConfigManager()
        
        field_mapping = cm.get('field_mapping')
        assert isinstance(field_mapping, dict)
        assert '姓名' in field_mapping  # 字段映射应该有姓名映射
    
    def test_set_and_save_config(self):
        """测试设置和保存配置"""
        ConfigManager._instance = None  # 重置单例
        cm = ConfigManager()
        
        # 设置顶层配置
        cm.set('dpi', 150)
        assert cm.get('dpi') == 150
        
        # 恢复默认
        cm.set('dpi', 100)
        assert cm.get('dpi') == 100
    
    def test_config_to_dict(self):
        """测试配置转换为字典"""
        ConfigManager._instance = None  # 重置单例
        cm = ConfigManager()
        config_dict = cm.to_dict()
        assert isinstance(config_dict, dict)
        assert 'field_mapping' in config_dict
        assert 'salary_bins' in config_dict


class TestLogger:
    """测试Logger类"""
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        Logger._instance = None  # 重置单例
        logger1 = Logger()
        logger2 = Logger()
        assert logger1 is logger2
    
    def test_get_logger(self):
        """测试获取logger实例"""
        Logger._instance = None  # 重置单例
        logger = Logger()
        import logging
        assert isinstance(logger.get_logger(), logging.Logger)
    
    def test_log_info(self, caplog):
        """测试INFO级别日志"""
        Logger._instance = None  # 重置单例
        # 允许日志传播到caplog
        logger = Logger()
        logger.get_logger().propagate = True
        test_message = "Test info message"
        
        logger.info(test_message)
        
        assert test_message in caplog.text
    
    def test_log_error(self, caplog):
        """测试ERROR级别日志"""
        Logger._instance = None  # 重置单例
        logger = Logger()
        logger.get_logger().propagate = True
        test_message = "Test error message"
        
        logger.error(test_message)
        
        assert test_message in caplog.text
    
    def test_log_warning(self, caplog):
        """测试WARNING级别日志"""
        Logger._instance = None  # 重置单例
        logger = Logger()
        logger.get_logger().propagate = True
        test_message = "Test warning message"
        
        logger.warning(test_message)
        
        assert test_message in caplog.text
    
    def test_log_debug(self, caplog):
        """测试DEBUG级别日志"""
        logger = Logger()
        test_message = "Test debug message"
        
        logger.debug(test_message)
