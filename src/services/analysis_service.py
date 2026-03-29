from typing import Dict, List, Optional, Any
import pandas as pd

from ..core.data_analyzer import DataAnalyzer
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import AppLogger
from ..exceptions import AnalysisError


class AnalysisService:
    def __init__(self, data_manager: DataManager, config: ConfigManager, logger: AppLogger = None):
        self._data_manager = data_manager
        self._config = config
        self._logger = logger or AppLogger.get_instance()
        self._analyzer = DataAnalyzer()
    
    def _sync_analyzer_data(self):
        data = self._data_manager.get_data()
        if data is not None:
            self._analyzer.set_data(data)
    
    def get_descriptive_stats(self, column: str) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取描述性统计: {column}")
            stats = self._analyzer.get_descriptive_stats(column)
            return {
                'success': True,
                'stats': stats
            }
        except Exception as e:
            self._logger.error(f"获取描述性统计失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_grouped_stats(self, group_by: str, value_col: str) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取分组统计: {group_by} by {value_col}")
            result = self._analyzer.get_grouped_stats(group_by, value_col)
            return {
                'success': True,
                'data': result.to_dict('records')
            }
        except Exception as e:
            self._logger.error(f"获取分组统计失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_frequency_analysis(self, column: str) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取频率分析: {column}")
            freq = self._analyzer.get_frequency_analysis(column)
            return {
                'success': True,
                'data': freq.to_dict('records')
            }
        except Exception as e:
            self._logger.error(f"获取频率分析失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_crosstab(self, row_col: str, col_col: str, 
                     normalize: bool = False) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取交叉分析: {row_col} vs {col_col}")
            crosstab = self._analyzer.get_crosstab(row_col, col_col, normalize)
            return {
                'success': True,
                'data': crosstab.to_dict()
            }
        except Exception as e:
            self._logger.error(f"获取交叉分析失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def compare_by_dimension(self, dimension: str, 
                            value_col: str = 'pre_tax_salary') -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"按维度比较: {dimension}")
            comparison = self._analyzer.compare_by_dimension(dimension, value_col)
            return {
                'success': True,
                'data': comparison.to_dict('records')
            }
        except Exception as e:
            self._logger.error(f"按维度比较失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_correlation_matrix(self, columns: Optional[List[str]] = None) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info("获取相关性矩阵")
            corr = self._analyzer.get_correlation_matrix(columns)
            return {
                'success': True,
                'data': corr.to_dict()
            }
        except Exception as e:
            self._logger.error(f"获取相关性矩阵失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_correlation(self, col1: str, col2: str) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取相关性: {col1} vs {col2}")
            corr = self._analyzer.get_correlation(col1, col2)
            return {
                'success': True,
                'correlation': corr
            }
        except Exception as e:
            self._logger.error(f"获取相关性失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_trend_analysis(self, time_col: str, value_col: str) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取趋势分析: {time_col}")
            trend = self._analyzer.get_trend_analysis(time_col, value_col)
            return {
                'success': True,
                'data': trend.to_dict('records')
            }
        except Exception as e:
            self._logger.error(f"获取趋势分析失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_salary_distribution(self, salary_col: str = 'pre_tax_salary') -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取薪资分布: {salary_col}")
            dist = self._analyzer.get_salary_distribution(
                salary_col,
                self._config.get_salary_bins(),
                self._config.get_salary_labels()
            )
            return {
                'success': True,
                'data': dist.to_dict('records')
            }
        except Exception as e:
            self._logger.error(f"获取薪资分布失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_summary_report(self, salary_col: str = 'pre_tax_salary') -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info("获取汇总报告")
            report = self._analyzer.get_summary_report(salary_col)
            return {
                'success': True,
                'report': report
            }
        except Exception as e:
            self._logger.error(f"获取汇总报告失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_dimensions_analysis(self, dimensions: List[str], 
                               salary_col: str = 'pre_tax_salary') -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取多维度分析: {dimensions}")
            results = self._analyzer.get_dimensions_analysis(dimensions, salary_col)
            return {
                'success': True,
                'data': {k: v.to_dict('records') for k, v in results.items()}
            }
        except Exception as e:
            self._logger.error(f"获取多维度分析失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_boxplot_data(self, group_by: str, value_col: str) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取箱线图数据: {group_by}")
            data = self._analyzer.get_boxplot_data(group_by, value_col)
            return {
                'success': True,
                'data': data
            }
        except Exception as e:
            self._logger.error(f"获取箱线图数据失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_top_bottom(self, column: str, n: int = 10, top: bool = True) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取{'最高' if top else '最低'} {n} 条记录: {column}")
            result = self._analyzer.get_top_bottom(column, n, top)
            return {
                'success': True,
                'data': result.to_dict('records')
            }
        except Exception as e:
            self._logger.error(f"获取Top/Bottom失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_percentile_distribution(self, column: str, 
                                   percentiles: List[float] = None) -> Dict:
        try:
            self._sync_analyzer_data()
            self._logger.info(f"获取百分位分布: {column}")
            result = self._analyzer.get_percentile_distribution(column, percentiles)
            return {
                'success': True,
                'percentiles': result
            }
        except Exception as e:
            self._logger.error(f"获取百分位分布失败: {str(e)}")
            return {'success': False, 'error': str(e)}
