"""
数据处理模块（重构版）
移除GUI依赖，改为纯业务逻辑
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Callable
from ..exceptions import DataValidationError
from ..models.logger import LoggerMixin


class DataProcessor(LoggerMixin):
    """
    数据处理器
    负责数据清洗、转换和处理
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        self.data = data.copy() if data is not None else None
        self.original_data = data.copy() if data is not None else None
    
    def set_data(self, data: pd.DataFrame) -> None:
        """设置数据"""
        self.data = data.copy()
        self.original_data = data.copy()
    
    def reset_data(self) -> None:
        """重置数据到原始状态"""
        if self.original_data is not None:
            self.data = self.original_data.copy()
            self.logger.info("Data reset to original state")
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> int:
        """
        删除重复数据
        
        Args:
            subset: 用于判断重复的列名列表
            
        Returns:
            删除的记录数
        """
        if self.data is None:
            return 0
        
        before_count = len(self.data)
        self.data.drop_duplicates(subset=subset, inplace=True)
        after_count = len(self.data)
        
        removed = before_count - after_count
        self.logger.info(f"Removed {removed} duplicate records")
        return removed
    
    def handle_missing_values(self, strategy: str = 'drop', 
                            columns: Optional[List[str]] = None,
                            fill_value: Any = None) -> Dict[str, int]:
        """
        处理缺失值
        
        Args:
            strategy: 处理策略 ('drop', 'fill_mean', 'fill_median', 'fill_mode', 'fill_value', 'fill_forward', 'fill_backward')
            columns: 要处理的列
            fill_value: 填充值
            
        Returns:
            各列处理的缺失值数量
        """
        if self.data is None:
            return {}
        
        result = {}
        
        if columns is None:
            columns = self.data.columns.tolist()
        
        for col in columns:
            if col not in self.data.columns:
                continue
            
            null_count = self.data[col].isnull().sum()
            
            if null_count == 0:
                continue
            
            if strategy == 'drop':
                self.data.dropna(subset=[col], inplace=True)
                result[col] = null_count
            
            elif strategy == 'fill_mean' and pd.api.types.is_numeric_dtype(self.data[col]):
                self.data[col].fillna(self.data[col].mean(), inplace=True)
                result[col] = null_count
            
            elif strategy == 'fill_median' and pd.api.types.is_numeric_dtype(self.data[col]):
                self.data[col].fillna(self.data[col].median(), inplace=True)
                result[col] = null_count
            
            elif strategy == 'fill_mode':
                mode_value = self.data[col].mode()
                if len(mode_value) > 0:
                    self.data[col].fillna(mode_value[0], inplace=True)
                    result[col] = null_count
            
            elif strategy == 'fill_value':
                self.data[col].fillna(fill_value, inplace=True)
                result[col] = null_count
            
            elif strategy == 'fill_forward':
                self.data[col].fillna(method='ffill', inplace=True)
                result[col] = null_count
            
            elif strategy == 'fill_backward':
                self.data[col].fillna(method='bfill', inplace=True)
                result[col] = null_count
        
        self.logger.info(f"Handled missing values with strategy '{strategy}': {result}")
        return result
    
    def detect_outliers(self, column: str, method: str = 'iqr', 
                       threshold: float = 1.5) -> pd.Series:
        """
        检测异常值
        
        Args:
            column: 列名
            method: 检测方法 ('iqr' 或 'zscore')
            threshold: 阈值
            
        Returns:
            布尔序列，True表示异常值
        """
        if self.data is None or column not in self.data.columns:
            return pd.Series()
        
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            return pd.Series()
        
        if method == 'iqr':
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            return (self.data[column] < lower_bound) | (self.data[column] > upper_bound)
        
        elif method == 'zscore':
            mean = self.data[column].mean()
            std = self.data[column].std()
            z_scores = np.abs((self.data[column] - mean) / std)
            return z_scores > threshold
        
        return pd.Series()
    
    def remove_outliers(self, column: str, method: str = 'iqr', 
                       threshold: float = 1.5) -> int:
        """
        移除异常值
        
        Args:
            column: 列名
            method: 检测方法
            threshold: 阈值
            
        Returns:
            移除的记录数
        """
        if self.data is None:
            return 0
        
        outliers = self.detect_outliers(column, method, threshold)
        before_count = len(self.data)
        self.data = self.data[~outliers]
        
        removed = before_count - len(self.data)
        self.logger.info(f"Removed {removed} outliers from column '{column}'")
        return removed
    
    def convert_dtype(self, column: str, target_type: str) -> bool:
        """
        转换数据类型
        
        Args:
            column: 列名
            target_type: 目标类型 ('numeric', 'string', 'datetime', 'category')
            
        Returns:
            是否成功
        """
        if self.data is None or column not in self.data.columns:
            return False
        
        try:
            if target_type == 'numeric':
                self.data[column] = pd.to_numeric(self.data[column], errors='coerce')
            elif target_type == 'string':
                self.data[column] = self.data[column].astype(str)
            elif target_type == 'datetime':
                self.data[column] = pd.to_datetime(self.data[column], errors='coerce')
            elif target_type == 'category':
                self.data[column] = self.data[column].astype('category')
            
            self.logger.info(f"Converted column '{column}' to {target_type}")
            return True
        except Exception as e:
            raise DataValidationError(f"类型转换失败: {str(e)}")
    
    def create_calculated_field(self, field_name: str, 
                               calculation: Callable[[pd.DataFrame], pd.Series]) -> bool:
        """
        创建计算字段
        
        Args:
            field_name: 字段名
            calculation: 计算函数
            
        Returns:
            是否成功
        """
        if self.data is None:
            return False
        
        try:
            self.data[field_name] = calculation(self.data)
            self.logger.info(f"Created calculated field: {field_name}")
            return True
        except Exception as e:
            raise DataValidationError(f"计算字段创建失败: {str(e)}")
    
    def create_age_group(self, age_column: str = 'age', 
                        bins: Optional[List[int]] = None,
                        labels: Optional[List[str]] = None) -> bool:
        """
        创建年龄分组
        
        Args:
            age_column: 年龄列名
            bins: 分组区间
            labels: 分组标签
            
        Returns:
            是否成功
        """
        if self.data is None or age_column not in self.data.columns:
            return False
        
        if bins is None:
            bins = [0, 25, 30, 35, 40, 50, 60, 100]
        
        if labels is None:
            labels = ['25岁以下', '25-30岁', '30-35岁', '35-40岁', 
                     '40-50岁', '50-60岁', '60岁以上']
        
        try:
            self.data['age_group'] = pd.cut(self.data[age_column], 
                                           bins=bins, 
                                           labels=labels,
                                           right=False)
            self.logger.info("Created age group column")
            return True
        except Exception as e:
            raise DataValidationError(f"年龄分组失败: {str(e)}")
    
    def create_salary_group(self, salary_column: str = 'pre_tax_salary',
                          bins: Optional[List[float]] = None,
                          labels: Optional[List[str]] = None) -> bool:
        """
        创建薪资分组
        
        Args:
            salary_column: 薪资列名
            bins: 分组区间
            labels: 分组标签
            
        Returns:
            是否成功
        """
        if self.data is None or salary_column not in self.data.columns:
            return False
        
        if bins is None:
            bins = [0, 5000, 10000, 15000, 20000, 30000, 50000, float('inf')]
        
        if labels is None:
            labels = ['5千以下', '5千-1万', '1万-1.5万', '1.5万-2万', 
                     '2万-3万', '3万-5万', '5万以上']
        
        try:
            self.data['salary_group'] = pd.cut(self.data[salary_column],
                                               bins=bins,
                                               labels=labels,
                                               right=False)
            self.logger.info("Created salary group column")
            return True
        except Exception as e:
            raise DataValidationError(f"薪资分组失败: {str(e)}")
    
    def create_work_experience_group(self, years_column: str = 'work_years',
                                    bins: Optional[List[float]] = None,
                                    labels: Optional[List[str]] = None) -> bool:
        """
        创建工作年限分组
        
        Args:
            years_column: 工作年限列名
            bins: 分组区间
            labels: 分组标签
            
        Returns:
            是否成功
        """
        if self.data is None or years_column not in self.data.columns:
            return False
        
        if bins is None:
            bins = [0, 1, 3, 5, 10, 15, 20, float('inf')]
        
        if labels is None:
            labels = ['1年以下', '1-3年', '3-5年', '5-10年', 
                     '10-15年', '15-20年', '20年以上']
        
        try:
            self.data['experience_group'] = pd.cut(
                pd.to_numeric(self.data[years_column], errors='coerce'),
                bins=bins,
                labels=labels,
                right=False
            )
            self.logger.info("Created work experience group column")
            return True
        except Exception as e:
            raise DataValidationError(f"工作年限分组失败: {str(e)}")
    
    def filter_data(self, conditions: Dict[str, Any]) -> pd.DataFrame:
        """
        筛选数据
        
        Args:
            conditions: 筛选条件字典
            
        Returns:
            筛选后的数据框
        """
        if self.data is None:
            return pd.DataFrame()
        
        filtered = self.data.copy()
        
        for column, value in conditions.items():
            if column not in filtered.columns:
                continue
            
            if isinstance(value, list):
                filtered = filtered[filtered[column].isin(value)]
            else:
                filtered = filtered[filtered[column] == value]
        
        return filtered
    
    def apply_filter(self, conditions: Dict[str, Any]) -> int:
        """
        应用筛选条件
        
        Args:
            conditions: 筛选条件
            
        Returns:
            筛选掉的记录数
        """
        if self.data is None:
            return 0
        
        before_count = len(self.data)
        self.data = self.filter_data(conditions)
        
        return before_count - len(self.data)
    
    def encode_categorical(self, columns: Optional[List[str]] = None,
                          method: str = 'label') -> Dict[str, bool]:
        """
        编码分类变量
        
        Args:
            columns: 要编码的列
            method: 编码方法 ('label' 或 'onehot')
            
        Returns:
            各列编码结果
        """
        if self.data is None:
            return {}
        
        result = {}
        
        if columns is None:
            columns = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        for col in columns:
            if col not in self.data.columns:
                continue
            
            try:
                if method == 'label':
                    categories = self.data[col].unique()
                    mapping = {cat: i for i, cat in enumerate(categories)}
                    self.data[f'{col}_encoded'] = self.data[col].map(mapping)
                    result[col] = True
                elif method == 'onehot':
                    dummies = pd.get_dummies(self.data[col], prefix=col)
                    self.data = pd.concat([self.data, dummies], axis=1)
                    result[col] = True
            except Exception:
                result[col] = False
        
        self.logger.info(f"Encoded categorical columns with method '{method}': {result}")
        return result
    
    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要"""
        if self.data is None:
            return {}
        
        summary = {
            'total_rows': len(self.data),
            'total_columns': len(self.data.columns),
            'numeric_columns': [],
            'categorical_columns': [],
            'missing_values': {},
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
        
        for col in self.data.columns:
            if pd.api.types.is_numeric_dtype(self.data[col]):
                summary['numeric_columns'].append(col)
            else:
                summary['categorical_columns'].append(col)
            
            null_count = self.data[col].isnull().sum()
            if null_count > 0:
                summary['missing_values'][col] = int(null_count)
        
        return summary
    
    def get_current_data(self) -> Optional[pd.DataFrame]:
        """获取当前数据"""
        return self.data
