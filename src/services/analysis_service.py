"""
数据分析服务模块
封装数据分析功能
"""

from typing import Optional, Dict, Any, List
import pandas as pd
from ..core.data_analyzer import DataAnalyzer
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import LoggerMixin
from ..events.event_bus import EventBus, EVENT_TYPES


class AnalysisService(LoggerMixin):
    """
    数据分析服务
    协调数据分析器和数据管理器
    """
    
    def __init__(self, data_manager: DataManager, config: ConfigManager,
                 event_bus: Optional[EventBus] = None):
        self._data_manager = data_manager
        self._config = config
        self._event_bus = event_bus
        self._analyzer = DataAnalyzer()
    
    def get_descriptive_stats(self, column: str) -> Dict[str, Any]:
        """
        获取描述性统计
        
        Args:
            column: 列名
            
        Returns:
            统计结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        stats = self._analyzer.get_descriptive_stats(column)
        
        return {
            'success': True,
            'column': column,
            'stats': stats
        }
    
    def get_frequency_analysis(self, column: str) -> Dict[str, Any]:
        """
        频率分析
        
        Args:
            column: 列名
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        freq = self._analyzer.get_frequency_analysis(column)
        
        return {
            'success': True,
            'column': column,
            'data': freq.to_dict('records')
        }
    
    def get_crosstab(self, row_col: str, col_col: str,
                    normalize: bool = False) -> Dict[str, Any]:
        """
        交叉分析
        
        Args:
            row_col: 行列
            col_col: 列列
            normalize: 是否标准化
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        crosstab = self._analyzer.get_crosstab(row_col, col_col, normalize)
        
        return {
            'success': True,
            'row_column': row_col,
            'col_column': col_col,
            'data': crosstab.to_dict()
        }
    
    def compare_by_dimension(self, dimension: str, 
                            value_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        按维度对比分析
        
        Args:
            dimension: 维度列
            value_col: 数值列
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        comparison = self._analyzer.compare_by_dimension(dimension, value_col)
        
        return {
            'success': True,
            'dimension': dimension,
            'value_column': value_col,
            'data': comparison.to_dict('records')
        }
    
    def get_correlation_matrix(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        获取相关系数矩阵
        
        Args:
            columns: 列名列表
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        corr_matrix = self._analyzer.get_correlation_matrix(columns)
        
        return {
            'success': True,
            'data': corr_matrix.to_dict()
        }
    
    def get_correlation(self, col1: str, col2: str) -> Dict[str, Any]:
        """
        获取两列的相关性
        
        Args:
            col1: 第一列
            col2: 第二列
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        corr = self._analyzer.get_correlation(col1, col2)
        
        return {
            'success': True,
            'column1': col1,
            'column2': col2,
            'correlation': corr
        }
    
    def get_trend_analysis(self, time_col: str, 
                          value_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        趋势分析
        
        Args:
            time_col: 时间列
            value_col: 数值列
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        trend = self._analyzer.get_trend_analysis(time_col, value_col)
        
        return {
            'success': True,
            'time_column': time_col,
            'value_column': value_col,
            'data': trend.to_dict('records')
        }
    
    def get_salary_distribution(self, salary_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        薪资分布分析
        
        Args:
            salary_col: 薪资列
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        distribution = self._analyzer.get_salary_distribution(salary_col)
        
        return {
            'success': True,
            'salary_column': salary_col,
            'data': distribution.to_dict('records')
        }
    
    def get_summary_report(self, salary_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        获取摘要报告
        
        Args:
            salary_col: 薪资列
            
        Returns:
            报告结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        report = self._analyzer.get_summary_report(salary_col)
        
        return {
            'success': True,
            'report': report
        }
    
    def get_dimensions_analysis(self, dimensions: List[str],
                               salary_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        多维度分析
        
        Args:
            dimensions: 维度列表
            salary_col: 薪资列
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        results = self._analyzer.get_dimensions_analysis(dimensions, salary_col)
        
        serialized_results = {}
        for dim, df in results.items():
            serialized_results[dim] = df.to_dict('records')
        
        return {
            'success': True,
            'dimensions': dimensions,
            'results': serialized_results
        }
    
    def get_boxplot_data(self, group_by: str, value_col: str) -> Dict[str, Any]:
        """
        获取箱线图数据
        
        Args:
            group_by: 分组列
            value_col: 数值列
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        boxplot_data = self._analyzer.get_boxplot_data(group_by, value_col)
        
        return {
            'success': True,
            'group_by': group_by,
            'value_column': value_col,
            'data': boxplot_data
        }
    
    def get_top_bottom(self, column: str, n: int = 10, 
                      top: bool = True) -> Dict[str, Any]:
        """
        获取最大/最小的N条记录
        
        Args:
            column: 列名
            n: 数量
            top: True获取最大，False获取最小
            
        Returns:
            分析结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        self._analyzer.set_data(data)
        result = self._analyzer.get_top_bottom(column, n, top)
        
        return {
            'success': True,
            'column': column,
            'top': top,
            'data': result.to_dict('records')
        }
