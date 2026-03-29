"""
数据服务模块
封装数据加载和导出功能
"""

import os
from typing import Optional, Dict, Any, List, Tuple
import pandas as pd
from ..core.data_loader import DataLoader
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import LoggerMixin
from ..exceptions import DataLoadError, DataValidationError
from ..events.event_bus import EventBus, EVENT_TYPES


class DataService(LoggerMixin):
    """
    数据服务
    协调数据加载器和数据管理器
    """
    
    def __init__(self, data_manager: DataManager, config: ConfigManager, 
                 event_bus: Optional[EventBus] = None):
        self._data_manager = data_manager
        self._config = config
        self._event_bus = event_bus
        self._loader = DataLoader(field_mapping=config.get_field_mapping())
    
    def load_file(self, file_path: str) -> Dict[str, Any]:
        """
        加载单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            加载结果信息
        """
        try:
            data = self._loader.load_excel(file_path)
            self._data_manager.set_data(data)
            
            info = {
                'success': True,
                'file_path': file_path,
                'rows': len(data),
                'columns': len(data.columns)
            }
            
            if self._event_bus:
                self._event_bus.publish(EVENT_TYPES['DATA_LOADED'], info)
            
            return info
            
        except DataLoadError as e:
            self.logger.error(f"Failed to load file: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        加载文件夹
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            加载结果信息
        """
        try:
            data = self._loader.load_folder(folder_path)
            self._data_manager.set_data(data)
            
            info = {
                'success': True,
                'folder_path': folder_path,
                'rows': len(data),
                'columns': len(data.columns)
            }
            
            if self._event_bus:
                self._event_bus.publish(EVENT_TYPES['DATA_LOADED'], info)
            
            return info
            
        except DataLoadError as e:
            self.logger.error(f"Failed to load folder: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        加载多个文件
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            加载结果信息
        """
        try:
            data = self._loader.load_multiple_files(file_paths)
            self._data_manager.set_data(data)
            
            info = {
                'success': True,
                'file_count': len(file_paths),
                'rows': len(data),
                'columns': len(data.columns)
            }
            
            if self._event_bus:
                self._event_bus.publish(EVENT_TYPES['DATA_LOADED'], info)
            
            return info
            
        except DataLoadError as e:
            self.logger.error(f"Failed to load files: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_sheet_names(self, file_path: str) -> List[str]:
        """获取工作表名称"""
        return self._loader.get_sheet_names(file_path)
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """验证数据"""
        return self._loader.validate_data()
    
    def export_data(self, output_path: str, format: str = 'excel') -> Dict[str, Any]:
        """
        导出数据
        
        Args:
            output_path: 输出路径
            format: 格式 ('excel' 或 'csv')
            
        Returns:
            导出结果
        """
        data = self._data_manager.get_data()
        
        if data is None:
            return {'success': False, 'error': '没有可导出的数据'}
        
        try:
            self._loader.data = data
            self._loader.export_data(output_path, format)
            
            return {
                'success': True,
                'output_path': output_path,
                'rows': len(data)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_data_info(self) -> Dict[str, Any]:
        """获取数据信息"""
        return self._data_manager.get_data_info()
    
    def get_column_names(self, dtype_filter: Optional[str] = None) -> List[str]:
        """获取列名"""
        return self._data_manager.get_column_names(dtype_filter)
    
    def has_data(self) -> bool:
        """检查是否有数据"""
        return self._data_manager.has_data()
    
    def clear_data(self) -> None:
        """清除数据"""
        self._data_manager.clear()
        if self._event_bus:
            self._event_bus.publish(EVENT_TYPES['DATA_CLEARED'])
