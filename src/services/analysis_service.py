import pandas as pd
from typing import Optional, List, Dict, Any

from src.models import DataManager, ConfigManager, Logger
from src.core import DataAnalyzer
from src.exceptions import AnalysisException, InvalidColumnError


class AnalysisService:
    """数据分析服务层
    
    提供统计分析功能。
    """
    
    def __init__(self, data_manager: DataManager, config_manager: ConfigManager):
        self._data_manager = data_manager
        self._config_manager = config_manager
        self._logger = Logger()
        self._analyzer = DataAnalyzer()
    
    def _ensure_data(self) -> pd.DataFrame:
        """确保有数据可用"""
        data = self._data_manager.get_data()
        if data is None:
            raise AnalysisException("没有可用的数据")
        self._analyzer.set_data(data)
        return data
    
    def get_descriptive_stats(self, column: str) -> Dict[str, float]:
        """获取描述性统计信息"""
        self._ensure_data()
        self._logger.info(f"获取列 '{column}' 的描述性统计信息")
        return self._analyzer.get_descriptive_stats(column)
    
    def get_grouped_stats(self, group_by: str, value_col: str) -> pd.DataFrame:
        """获取分组统计信息"""
        self._ensure_data()
        self._logger.info(f"按 {group_by} 分组，统计 {value_col}")
        return self._analyzer.get_grouped_stats(group_by, value_col)
    
    def get_frequency_analysis(self, column: str) -> pd.DataFrame:
        """获取频率分析结果"""
        self._ensure_data()
        self._logger.info(f"获取列 '{column}' 的频率分析")
        return self._analyzer.get_frequency_analysis(column)
    
    def get_crosstab(self, row_col: str, col_col: str, normalize: bool = False) -> pd.DataFrame:
        """获取交叉分析表"""
        self._ensure_data()
        self._logger.info(f"交叉分析: {row_col} vs {col_col}")
        return self._analyzer.get_crosstab(row_col, col_col, normalize)
    
    def compare_by_dimension(self, dimension: str, value_col: Optional[str] = None) -> pd.DataFrame:
        """按维度比较分析"""
        self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        self._logger.info(f"按维度 '{dimension}' 比较薪资分布")
        return self._analyzer.compare_by_dimension(dimension, value_col)
    
    def get_correlation_matrix(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """获取相关性矩阵"""
        self._ensure_data()
        self._logger.info("计算相关性矩阵")
        return self._analyzer.get_correlation_matrix(columns)
    
    def get_correlation(self, col1: str, col2: str) -> Dict[str, float]:
        """获取两列之间的相关性"""
        self._ensure_data()
        self._logger.info(f"计算 {col1} 和 {col2} 的相关性")
        return self._analyzer.get_correlation(col1, col2)
    
    def get_trend_analysis(self, time_col: str, value_col: Optional[str] = None) -> pd.DataFrame:
        """获取趋势分析结果"""
        self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        self._logger.info(f"趋势分析: {time_col} - {value_col}")
        return self._analyzer.get_trend_analysis(time_col, value_col)
    
    def get_percentile_distribution(self, column: str, percentiles: List[float] = None) -> Dict[str, float]:
        """获取百分位分布"""
        self._ensure_data()
        self._logger.info(f"获取列 '{column}' 的百分位分布")
        return self._analyzer.get_percentile_distribution(column, percentiles)
    
    def get_salary_distribution(self, salary_col: Optional[str] = None) -> pd.DataFrame:
        """获取薪资分布"""
        self._ensure_data()
        
        if salary_col is None:
            salary_col = self._get_default_salary_column()
        
        bins = self._config_manager.get_salary_bins()
        labels = self._config_manager.get_salary_labels()
        
        self._logger.info(f"获取薪资分布: {salary_col}")
        return self._analyzer.get_salary_distribution(salary_col, bins, labels)
    
    def get_summary_report(self, salary_col: Optional[str] = None) -> Dict[str, Any]:
        """获取汇总报告"""
        self._ensure_data()
        
        if salary_col is None:
            salary_col = self._get_default_salary_column()
        
        self._logger.info(f"生成汇总报告: {salary_col}")
        return self._analyzer.get_summary_report(salary_col)
    
    def get_dimensions_analysis(self, dimensions: List[str], salary_col: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """多维度分析"""
        self._ensure_data()
        
        if salary_col is None:
            salary_col = self._get_default_salary_column()
        
        self._logger.info(f"多维度分析: {dimensions}")
        return self._analyzer.get_dimensions_analysis(dimensions, salary_col)
    
    def get_boxplot_data(self, group_by: str, value_col: Optional[str] = None) -> Dict[str, Dict]:
        """获取箱线图数据"""
        self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        self._logger.info(f"获取箱线图数据: {group_by} - {value_col}")
        return self._analyzer.get_boxplot_data(group_by, value_col)
    
    def get_top_records(self, column: str, n: int = 10) -> pd.DataFrame:
        """获取Top N记录"""
        self._ensure_data()
        self._logger.info(f"获取按 '{column}' 排序的前 {n} 条记录")
        return self._analyzer.get_top_bottom(column, n, top=True)
    
    def get_bottom_records(self, column: str, n: int = 10) -> pd.DataFrame:
        """获取Bottom N记录"""
        self._ensure_data()
        self._logger.info(f"获取按 '{column}' 排序的后 {n} 条记录")
        return self._analyzer.get_top_bottom(column, n, top=False)
    
    def get_available_dimensions(self) -> List[str]:
        """获取可用的维度列"""
        data = self._data_manager.get_data()
        if data is None:
            return []
        return data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def get_numeric_columns(self) -> List[str]:
        """获取数值类型的列"""
        data = self._data_manager.get_data()
        if data is None:
            return []
        return data.select_dtypes(include=['number']).columns.tolist()
    
    def get_salary_columns(self) -> List[str]:
        """获取薪资相关的列"""
        numeric_cols = self.get_numeric_columns()
        salary_candidates = self._config_manager.get_salary_candidates()
        
        salary_cols = [col for col in numeric_cols if col.lower() in [s.lower() for s in salary_candidates]]
        
        if not salary_cols:
            return numeric_cols
        
        return salary_cols
    
    def _get_default_salary_column(self) -> str:
        """获取默认的薪资列"""
        salary_cols = self.get_salary_columns()
        if salary_cols:
            return salary_cols[0]
        
        numeric_cols = self.get_numeric_columns()
        if numeric_cols:
            return numeric_cols[0]
        
        raise AnalysisException("没有找到合适的薪资列")
