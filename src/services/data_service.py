import pandas as pd
from typing import Optional, List, Dict, Any

from src.models import DataManager, ConfigManager, Logger
from src.core import DataLoader, DataProcessor
from src.exceptions import DataLoadError, DataProcessingError


class DataService:
    """数据服务层
    
    协调数据加载、处理和存储，提供统一的数据访问接口。
    """
    
    def __init__(self, data_manager: DataManager, config_manager: ConfigManager):
        self._data_manager = data_manager
        self._config_manager = config_manager
        self._logger = Logger()
        
        self._loader = DataLoader(field_mapping=config_manager.get_field_mapping())
        self._processor = DataProcessor()
    
    def load_file(self, file_path: str, sheet_name: Optional[str] = None) -> bool:
        """加载单个Excel文件"""
        try:
            self._logger.info(f"正在加载文件: {file_path}")
            data = self._loader.load_excel(file_path, sheet_name)
            self._data_manager.set_data(data)
            self._logger.info(f"文件加载成功，共 {len(data)} 条记录")
            return True
        except DataLoadError as e:
            self._logger.error(f"文件加载失败: {e}")
            raise
    
    def load_folder(self, folder_path: str) -> bool:
        """加载文件夹中的所有Excel文件"""
        try:
            self._logger.info(f"正在加载文件夹: {folder_path}")
            data = self._loader.load_folder(folder_path)
            self._data_manager.set_data(data)
            self._logger.info(f"文件夹加载成功，共 {len(data)} 条记录")
            return True
        except DataLoadError as e:
            self._logger.error(f"文件夹加载失败: {e}")
            raise
    
    def load_multiple_files(self, file_paths: List[str]) -> bool:
        """批量加载多个文件"""
        try:
            self._logger.info(f"正在批量加载 {len(file_paths)} 个文件")
            data = self._loader.load_multiple_files(file_paths)
            self._data_manager.set_data(data)
            self._logger.info(f"批量加载成功，共 {len(data)} 条记录")
            return True
        except DataLoadError as e:
            self._logger.error(f"批量加载失败: {e}")
            raise
    
    def get_current_data(self) -> Optional[pd.DataFrame]:
        """获取当前数据"""
        return self._data_manager.get_data()
    
    def get_data_info(self) -> Dict[str, Any]:
        """获取数据信息"""
        return self._data_manager.get_data_info()
    
    def has_data(self) -> bool:
        """检查是否有数据"""
        return self._data_manager.has_data()
    
    def reset_data(self) -> None:
        """重置数据到原始状态"""
        self._data_manager.clear()
        self._logger.info("数据已重置")
    
    def export_data(self, output_path: str, format_type: str = 'excel') -> bool:
        """导出数据到文件"""
        data = self._data_manager.get_data()
        if data is None:
            raise DataLoadError("没有可导出的数据")
        
        try:
            return self._loader.export_data(data, output_path, format_type)
        except DataLoadError as e:
            self._logger.error(f"数据导出失败: {e}")
            raise
    
    def validate_data(self) -> tuple[bool, List[str]]:
        """验证数据有效性"""
        data = self._data_manager.get_data()
        if data is None:
            return False, ['没有加载数据']
        
        self._loader.data = data
        return self._loader.validate_data()
    
    def subscribe_to_data_changes(self, callback):
        """订阅数据变化"""
        self._data_manager.subscribe(callback)
    
    def unsubscribe_from_data_changes(self, callback):
        """取消订阅数据变化"""
        self._data_manager.unsubscribe(callback)
    
    @property
    def processor(self) -> DataProcessor:
        """获取数据处理器"""
        return self._processor
    
    @property
    def loader(self) -> DataLoader:
        """获取数据加载器"""
        return self._loader
