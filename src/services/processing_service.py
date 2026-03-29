"""
数据处理服务模块
封装数据处理功能
"""

from typing import Optional, Dict, Any, List
import pandas as pd
from ..core.data_processor import DataProcessor
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import LoggerMixin
from ..events.event_bus import EventBus, EVENT_TYPES


class ProcessingService(LoggerMixin):
    """
    数据处理服务
    协调数据处理器和数据管理器
    """
    
    def __init__(self, data_manager: DataManager, config: ConfigManager,
                 event_bus: Optional[EventBus] = None):
        self._data_manager = data_manager
        self._config = config
        self._event_bus = event_bus
        self._processor = DataProcessor()
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        删除重复数据
        
        Args:
            subset: 用于判断重复的列名列表
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        removed = self._processor.remove_duplicates(subset)
        
        self._data_manager.set_data(self._processor.get_current_data())
        
        return {
            'success': True,
            'removed_count': removed,
            'remaining_count': len(self._processor.get_current_data())
        }
    
    def handle_missing_values(self, strategy: str = 'drop',
                             columns: Optional[List[str]] = None,
                             fill_value: Any = None) -> Dict[str, Any]:
        """
        处理缺失值
        
        Args:
            strategy: 处理策略
            columns: 要处理的列
            fill_value: 填充值
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        result = self._processor.handle_missing_values(strategy, columns, fill_value)
        
        self._data_manager.set_data(self._processor.get_current_data())
        
        return {
            'success': True,
            'processed_columns': result,
            'total_processed': sum(result.values())
        }
    
    def remove_outliers(self, column: str, method: str = 'iqr',
                       threshold: float = 1.5) -> Dict[str, Any]:
        """
        移除异常值
        
        Args:
            column: 列名
            method: 检测方法
            threshold: 阈值
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        removed = self._processor.remove_outliers(column, method, threshold)
        
        self._data_manager.set_data(self._processor.get_current_data())
        
        return {
            'success': True,
            'removed_count': removed,
            'column': column
        }
    
    def create_age_group(self, age_column: str = 'age') -> Dict[str, Any]:
        """
        创建年龄分组
        
        Args:
            age_column: 年龄列名
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        
        bins = self._config.get_age_bins()
        labels = self._config.get_age_labels()
        
        success = self._processor.create_age_group(age_column, bins, labels)
        
        if success:
            self._data_manager.set_data(self._processor.get_current_data())
            return {'success': True, 'new_column': 'age_group'}
        
        return {'success': False, 'error': '创建年龄分组失败'}
    
    def create_salary_group(self, salary_column: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        创建薪资分组
        
        Args:
            salary_column: 薪资列名
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        
        bins = self._config.get_salary_bins()
        labels = self._config.get_salary_labels()
        
        success = self._processor.create_salary_group(salary_column, bins, labels)
        
        if success:
            self._data_manager.set_data(self._processor.get_current_data())
            return {'success': True, 'new_column': 'salary_group'}
        
        return {'success': False, 'error': '创建薪资分组失败'}
    
    def create_experience_group(self, years_column: str = 'work_years') -> Dict[str, Any]:
        """
        创建工作年限分组
        
        Args:
            years_column: 工作年限列名
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        
        bins = self._config.get_experience_bins()
        labels = self._config.get_experience_labels()
        
        success = self._processor.create_work_experience_group(years_column, bins, labels)
        
        if success:
            self._data_manager.set_data(self._processor.get_current_data())
            return {'success': True, 'new_column': 'experience_group'}
        
        return {'success': False, 'error': '创建工作年限分组失败'}
    
    def filter_data(self, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        筛选数据
        
        Args:
            conditions: 筛选条件
            
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        removed = self._processor.apply_filter(conditions)
        
        self._data_manager.set_data(self._processor.get_current_data())
        
        return {
            'success': True,
            'removed_count': removed,
            'remaining_count': len(self._processor.get_current_data())
        }
    
    def reset_data(self) -> Dict[str, Any]:
        """
        重置数据
        
        Returns:
            处理结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._processor.set_data(data)
        self._processor.reset_data()
        self._data_manager.set_data(self._processor.get_current_data())
        
        return {'success': True}
    
    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要"""
        data = self._data_manager.get_data()
        if data is None:
            return {}
        
        self._processor.set_data(data)
        return self._processor.get_data_summary()
