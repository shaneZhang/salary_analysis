from typing import Dict, List, Optional, Any
import pandas as pd

from ..core.data_processor import DataProcessor
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import AppLogger
from ..exceptions import DataProcessingError


class ProcessingService:
    def __init__(self, data_manager: DataManager, config: ConfigManager, logger: AppLogger = None):
        self._data_manager = data_manager
        self._config = config
        self._logger = logger or AppLogger.get_instance()
        self._processor = DataProcessor()
    
    def _sync_processor_data(self):
        data = self._data_manager.get_data()
        if data is not None:
            self._processor.set_data(data)
    
    def _sync_to_manager(self):
        processed_data = self._processor.get_current_data()
        if processed_data is not None:
            self._data_manager.set_data(processed_data)
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info("正在删除重复数据")
            count = self._processor.remove_duplicates(subset)
            self._sync_to_manager()
            
            self._logger.info(f"删除了 {count} 条重复记录")
            return {
                'success': True,
                'removed_count': count
            }
        except Exception as e:
            self._logger.error(f"删除重复数据失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def handle_missing_values(self, strategy: str = 'drop', 
                             columns: Optional[List[str]] = None,
                             fill_value: Any = None) -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info(f"正在处理缺失值，策略: {strategy}")
            result = self._processor.handle_missing_values(strategy, columns, fill_value)
            self._sync_to_manager()
            
            total_handled = sum(result.values())
            self._logger.info(f"处理了 {total_handled} 个缺失值")
            return {
                'success': True,
                'handled': result,
                'total_handled': total_handled
            }
        except Exception as e:
            self._logger.error(f"处理缺失值失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def detect_outliers(self, column: str, method: str = 'iqr', 
                       threshold: float = 1.5) -> Dict:
        try:
            self._sync_processor_data()
            outliers = self._processor.detect_outliers(column, method, threshold)
            return {
                'success': True,
                'outlier_count': int(outliers.sum()),
                'outlier_indices': outliers[outliers].index.tolist()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def remove_outliers(self, column: str, method: str = 'iqr', 
                       threshold: float = 1.5) -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info(f"正在移除异常值: {column}")
            count = self._processor.remove_outliers(column, method, threshold)
            self._sync_to_manager()
            
            self._logger.info(f"移除了 {count} 条异常值记录")
            return {
                'success': True,
                'removed_count': count
            }
        except Exception as e:
            self._logger.error(f"移除异常值失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_age_group(self, age_column: str = 'age') -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info("正在创建年龄分组")
            success = self._processor.create_age_group(
                age_column,
                self._config.get_age_bins(),
                self._config.get_age_labels()
            )
            if success:
                self._sync_to_manager()
                self._logger.info("年龄分组创建成功")
                return {'success': True}
            return {'success': False, 'error': '年龄字段不存在'}
        except DataProcessingError as e:
            self._logger.error(f"创建年龄分组失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_salary_group(self, salary_column: str = 'pre_tax_salary') -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info("正在创建薪资分组")
            success = self._processor.create_salary_group(
                salary_column,
                self._config.get_salary_bins(),
                self._config.get_salary_labels()
            )
            if success:
                self._sync_to_manager()
                self._logger.info("薪资分组创建成功")
                return {'success': True}
            return {'success': False, 'error': '薪资字段不存在'}
        except DataProcessingError as e:
            self._logger.error(f"创建薪资分组失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_experience_group(self, years_column: str = 'work_years') -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info("正在创建工作年限分组")
            success = self._processor.create_work_experience_group(
                years_column,
                self._config.get_experience_bins(),
                self._config.get_experience_labels()
            )
            if success:
                self._sync_to_manager()
                self._logger.info("工作年限分组创建成功")
                return {'success': True}
            return {'success': False, 'error': '工作年限字段不存在'}
        except DataProcessingError as e:
            self._logger.error(f"创建工作年限分组失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def filter_data(self, conditions: Dict[str, Any]) -> Dict:
        try:
            self._sync_processor_data()
            self._logger.info(f"正在筛选数据")
            before_count = len(self._processor.get_current_data()) if self._processor.get_current_data() is not None else 0
            removed = self._processor.apply_filter(conditions)
            self._sync_to_manager()
            
            self._logger.info(f"筛选完成，移除了 {removed} 条记录")
            return {
                'success': True,
                'removed_count': removed,
                'remaining_count': before_count - removed
            }
        except Exception as e:
            self._logger.error(f"数据筛选失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def convert_dtype(self, column: str, target_type: str) -> Dict:
        try:
            self._sync_processor_data()
            success = self._processor.convert_dtype(column, target_type)
            if success:
                self._sync_to_manager()
                return {'success': True}
            return {'success': False, 'error': '类型转换失败'}
        except DataProcessingError as e:
            return {'success': False, 'error': str(e)}
    
    def reset_data(self) -> Dict:
        try:
            self._data_manager.reset()
            self._logger.info("数据已重置")
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_data_summary(self) -> Dict:
        self._sync_processor_data()
        return self._processor.get_data_summary()
    
    def encode_categorical(self, columns: Optional[List[str]] = None, 
                          method: str = 'label') -> Dict:
        try:
            self._sync_processor_data()
            result = self._processor.encode_categorical(columns, method)
            self._sync_to_manager()
            return {'success': True, 'results': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
