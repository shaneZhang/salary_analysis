import pandas as pd
from typing import Optional, List, Dict, Any, Callable

from src.models import DataManager, ConfigManager, Logger
from src.core import DataProcessor
from src.exceptions import DataProcessingError, InvalidColumnError


class ProcessingService:
    """数据处理服务层
    
    提供数据清洗、转换、分组等服务。
    """
    
    def __init__(self, data_manager: DataManager, config_manager: ConfigManager):
        self._data_manager = data_manager
        self._config_manager = config_manager
        self._logger = Logger()
        self._processor = DataProcessor()
    
    def _ensure_data(self) -> pd.DataFrame:
        """确保有数据可用"""
        data = self._data_manager.get_data()
        if data is None:
            raise DataProcessingError("没有可用的数据")
        self._processor.set_data(data)
        return data
    
    def _update_data(self):
        """更新数据到DataManager"""
        self._data_manager.set_data(self._processor.get_current_data())
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> int:
        """删除重复数据"""
        self._ensure_data()
        count = self._processor.remove_duplicates(subset)
        self._update_data()
        if count > 0:
            self._logger.info(f"删除了 {count} 条重复记录")
        return count
    
    def handle_missing_values(self, strategy: str = 'drop', 
                            columns: Optional[List[str]] = None,
                            fill_value: Any = None) -> Dict[str, int]:
        """处理缺失值"""
        self._ensure_data()
        result = self._processor.handle_missing_values(strategy, columns, fill_value)
        self._update_data()
        self._logger.info(f"处理缺失值完成: {result}")
        return result
    
    def remove_outliers(self, column: str, method: str = 'iqr', 
                       threshold: float = 1.5) -> int:
        """移除异常值"""
        self._ensure_data()
        count = self._processor.remove_outliers(column, method, threshold)
        self._update_data()
        if count > 0:
            self._logger.info(f"移除了 {count} 条异常值记录")
        return count
    
    def create_age_group(self, age_column: str = 'age') -> bool:
        """创建年龄分组"""
        self._ensure_data()
        bins = self._config_manager.get_age_bins()
        labels = self._config_manager.get_age_labels()
        result = self._processor.create_age_group(age_column, bins, labels)
        self._update_data()
        if result:
            self._logger.info("创建年龄分组完成")
        return result
    
    def create_salary_group(self, salary_column: str) -> bool:
        """创建薪资分组"""
        self._ensure_data()
        bins = self._config_manager.get_salary_bins()
        labels = self._config_manager.get_salary_labels()
        result = self._processor.create_salary_group(salary_column, bins, labels)
        self._update_data()
        if result:
            self._logger.info("创建薪资分组完成")
        return result
    
    def create_work_experience_group(self, years_column: str = 'work_years') -> bool:
        """创建工作年限分组"""
        self._ensure_data()
        bins = self._config_manager.get_experience_bins()
        labels = self._config_manager.get_experience_labels()
        result = self._processor.create_work_experience_group(years_column, bins, labels)
        self._update_data()
        if result:
            self._logger.info("创建工作年限分组完成")
        return result
    
    def filter_data(self, conditions: Dict[str, Any]) -> pd.DataFrame:
        """根据条件过滤数据（不修改原始数据）"""
        self._ensure_data()
        return self._processor.filter_data(conditions)
    
    def apply_filter(self, conditions: Dict[str, Any]) -> int:
        """应用过滤条件"""
        self._ensure_data()
        count = self._processor.apply_filter(conditions)
        self._update_data()
        if count > 0:
            self._logger.info(f"过滤了 {count} 条记录")
        return count
    
    def convert_column_type(self, column: str, target_type: str) -> bool:
        """转换列的数据类型"""
        self._ensure_data()
        result = self._processor.convert_dtype(column, target_type)
        self._update_data()
        return result
    
    def create_calculated_field(self, field_name: str, 
                               calculation: Callable[[pd.DataFrame], pd.Series]) -> bool:
        """创建计算字段"""
        self._ensure_data()
        result = self._processor.create_calculated_field(field_name, calculation)
        self._update_data()
        if result:
            self._logger.info(f"创建计算字段: {field_name}")
        return result
    
    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要信息"""
        data = self._data_manager.get_data()
        if data is None:
            return {}
        self._processor.set_data(data)
        return self._processor.get_data_summary()
    
    def get_processed_data(self) -> Optional[pd.DataFrame]:
        """获取处理后的数据"""
        return self._processor.get_current_data()
