from typing import Dict, List, Optional, Tuple
import pandas as pd

from ..core.data_loader import DataLoader
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import AppLogger
from ..exceptions import DataLoadError, DataValidationError


class DataService:
    def __init__(self, data_manager: DataManager, config: ConfigManager, logger: AppLogger = None):
        self._data_manager = data_manager
        self._config = config
        self._logger = logger or AppLogger.get_instance()
        self._loader = DataLoader(field_mapping=config.get_field_mapping())
    
    def load_file(self, file_path: str, sheet_name: Optional[str] = None) -> Dict:
        try:
            self._logger.info(f"正在加载文件: {file_path}")
            data = self._loader.load_excel(file_path, sheet_name)
            self._data_manager.set_data(data)
            
            is_valid, errors = self._loader.validate_data()
            
            result = {
                'success': True,
                'rows': len(data),
                'columns': len(data.columns),
                'is_valid': is_valid,
                'validation_errors': errors,
                'file_path': file_path
            }
            
            self._logger.info(f"文件加载成功: {len(data)} 行数据")
            return result
            
        except DataLoadError as e:
            self._logger.error(f"文件加载失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    def load_folder(self, folder_path: str) -> Dict:
        try:
            self._logger.info(f"正在加载文件夹: {folder_path}")
            data = self._loader.load_folder(folder_path)
            self._data_manager.set_data(data)
            
            is_valid, errors = self._loader.validate_data()
            
            result = {
                'success': True,
                'rows': len(data),
                'columns': len(data.columns),
                'is_valid': is_valid,
                'validation_errors': errors,
                'folder_path': folder_path
            }
            
            self._logger.info(f"文件夹加载成功: {len(data)} 行数据")
            return result
            
        except DataLoadError as e:
            self._logger.error(f"文件夹加载失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'folder_path': folder_path
            }
    
    def load_multiple_files(self, file_paths: List[str]) -> Dict:
        try:
            self._logger.info(f"正在加载 {len(file_paths)} 个文件")
            data = self._loader.load_multiple_files(file_paths)
            self._data_manager.set_data(data)
            
            is_valid, errors = self._loader.validate_data()
            
            result = {
                'success': True,
                'rows': len(data),
                'columns': len(data.columns),
                'is_valid': is_valid,
                'validation_errors': errors,
                'file_count': len(file_paths)
            }
            
            self._logger.info(f"多文件加载成功: {len(data)} 行数据")
            return result
            
        except DataLoadError as e:
            self._logger.error(f"多文件加载失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_sheet_names(self, file_path: str) -> List[str]:
        try:
            return self._loader.get_sheet_names(file_path)
        except DataLoadError:
            return []
    
    def get_data_info(self) -> Dict:
        return self._data_manager.get_data_info()
    
    def get_preview(self, n: int = 10) -> Optional[pd.DataFrame]:
        return self._loader.get_preview(n)
    
    def export_data(self, output_path: str, format: str = 'excel') -> Dict:
        try:
            self._logger.info(f"正在导出数据到: {output_path}")
            self._loader.data = self._data_manager.get_data()
            self._loader.export_data(output_path, format)
            
            self._logger.info(f"数据导出成功")
            return {
                'success': True,
                'output_path': output_path,
                'format': format
            }
            
        except DataValidationError as e:
            self._logger.error(f"数据导出失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_current_data(self) -> Tuple[bool, List[str]]:
        return self._loader.validate_data()
    
    def apply_field_mapping(self, mapping: Dict[str, str]) -> Dict:
        try:
            self._loader.apply_field_mapping(mapping)
            self._data_manager.set_data(self._loader.get_data())
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_field_mapping(self) -> Dict[str, str]:
        return self._config.get_field_mapping()
