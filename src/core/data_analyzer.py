import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple, Any
from scipy import stats

from src.exceptions import AnalysisException, InvalidColumnError


class DataAnalyzer:
    """数据分析器
    
    提供统计分析功能，不包含任何GUI依赖。
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None):
        self.data = data
    
    def set_data(self, data: pd.DataFrame):
        """设置分析数据"""
        self.data = data
    
    def get_descriptive_stats(self, column: str) -> Dict[str, float]:
        """获取描述性统计信息"""
        if self.data is None or column not in self.data.columns:
            raise InvalidColumnError(f"数据为空或列不存在: {column}")
        
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            raise AnalysisException(f"列 '{column}' 不是数值类型")
        
        col_data = self.data[column].dropna()
        
        if len(col_data) == 0:
            return {}
        
        stats_dict = {
            'count': int(len(col_data)),
            'mean': float(col_data.mean()),
            'median': float(col_data.median()),
            'std': float(col_data.std()),
            'min': float(col_data.min()),
            'max': float(col_data.max()),
            'q25': float(col_data.quantile(0.25)),
            'q50': float(col_data.quantile(0.50)),
            'q75': float(col_data.quantile(0.75)),
            'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25)),
            'skewness': float(col_data.skew()),
            'kurtosis': float(col_data.kurtosis()),
            'variance': float(col_data.var())
        }
        
        if len(col_data.mode()) > 0:
            stats_dict['mode'] = float(col_data.mode()[0])
        
        return stats_dict
    
    def get_grouped_stats(self, group_by: str, value_col: str) -> pd.DataFrame:
        """获取分组统计信息"""
        if self.data is None or group_by not in self.data.columns or value_col not in self.data.columns:
            raise InvalidColumnError(f"数据为空或列不存在: {group_by}, {value_col}")
        
        grouped = self.data.groupby(group_by)[value_col].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
            ('std', 'std'),
            ('min', 'min'),
            ('max', 'max'),
            ('sum', 'sum')
        ]).reset_index()
        
        return grouped
    
    def get_frequency_analysis(self, column: str) -> pd.DataFrame:
        """获取频率分析结果"""
        if self.data is None or column not in self.data.columns:
            raise InvalidColumnError(f"数据为空或列不存在: {column}")
        
        freq = self.data[column].value_counts().reset_index()
        freq.columns = [column, 'count']
        freq['percentage'] = (freq['count'] / freq['count'].sum() * 100).round(2)
        freq = freq.reset_index(drop=True)
        
        return freq
    
    def get_crosstab(self, row_col: str, col_col: str, 
                     normalize: bool = False) -> pd.DataFrame:
        """获取交叉分析表"""
        if self.data is None:
            raise AnalysisException("数据为空")
        
        if row_col not in self.data.columns or col_col not in self.data.columns:
            raise InvalidColumnError(f"列不存在: {row_col} 或 {col_col}")
        
        crosstab = pd.crosstab(self.data[row_col], self.data[col_col])
        
        if normalize:
            crosstab = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
        
        return crosstab
    
    def compare_by_dimension(self, dimension: str, value_col: str = 'pre_tax_salary') -> pd.DataFrame:
        """按维度比较分析"""
        if self.data is None or dimension not in self.data.columns:
            raise InvalidColumnError(f"数据为空或维度列不存在: {dimension}")
        
        if value_col not in self.data.columns:
            raise InvalidColumnError(f"值列不存在: {value_col}")
        
        comparison = self.data.groupby(dimension)[value_col].agg([
            ('人数', 'count'),
            ('平均薪资', 'mean'),
            ('中位薪资', 'median'),
            ('最高薪资', 'max'),
            ('最低薪资', 'min'),
            ('标准差', 'std')
        ]).reset_index()
        
        comparison['平均薪资'] = comparison['平均薪资'].round(2)
        comparison['中位薪资'] = comparison['中位薪资'].round(2)
        comparison['标准差'] = comparison['标准差'].round(2)
        
        return comparison
    
    def get_correlation_matrix(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """获取相关性矩阵"""
        if self.data is None:
            raise AnalysisException("数据为空")
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        if not columns:
            return pd.DataFrame()
        
        corr_matrix = self.data[columns].corr().round(3)
        return corr_matrix
    
    def get_correlation(self, col1: str, col2: str) -> Dict[str, float]:
        """获取两列之间的相关性"""
        if self.data is None:
            raise AnalysisException("数据为空")
        
        if col1 not in self.data.columns or col2 not in self.data.columns:
            raise InvalidColumnError(f"列不存在: {col1} 或 {col2}")
        
        if not (pd.api.types.is_numeric_dtype(self.data[col1]) and 
                pd.api.types.is_numeric_dtype(self.data[col2])):
            raise AnalysisException("两列必须都是数值类型")
        
        valid_data = self.data[[col1, col2]].dropna()
        
        if len(valid_data) < 3:
            return {}
        
        pearson_corr, pearson_p = stats.pearsonr(valid_data[col1], valid_data[col2])
        spearman_corr, spearman_p = stats.spearmanr(valid_data[col1], valid_data[col2])
        
        return {
            'pearson_r': round(pearson_corr, 4),
            'pearson_p': round(pearson_p, 4),
            'spearman_r': round(spearman_corr, 4),
            'spearman_p': round(spearman_p, 4)
        }
    
    def get_trend_analysis(self, time_col: str, value_col: str) -> pd.DataFrame:
        """获取趋势分析结果"""
        if self.data is None or time_col not in self.data.columns:
            raise InvalidColumnError(f"数据为空或时间列不存在: {time_col}")
        
        if value_col not in self.data.columns:
            raise InvalidColumnError(f"值列不存在: {value_col}")
        
        if not pd.api.types.is_numeric_dtype(self.data[value_col]):
            raise AnalysisException(f"值列 '{value_col}' 必须是数值类型")
        
        trend = self.data.groupby(time_col)[value_col].agg([
            ('人数', 'count'),
            ('平均薪资', 'mean'),
            ('中位薪资', 'median'),
            ('总薪资', 'sum')
        ]).reset_index()
        
        trend['平均薪资'] = trend['平均薪资'].round(2)
        trend['中位薪资'] = trend['中位薪资'].round(2)
        
        if len(trend) > 1:
            trend['薪资增长率'] = trend['平均薪资'].pct_change() * 100
            trend['薪资增长率'] = trend['薪资增长率'].round(2)
        
        return trend
    
    def get_percentile_distribution(self, column: str, 
                                   percentiles: List[float] = None) -> Dict[str, float]:
        """获取百分位分布"""
        if self.data is None or column not in self.data.columns:
            raise InvalidColumnError(f"数据为空或列不存在: {column}")
        
        if percentiles is None:
            percentiles = [10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 95, 99]
        
        result = {}
        col_data = self.data[column].dropna()
        
        for p in percentiles:
            result[f'p{int(p)}'] = float(col_data.quantile(p / 100))
        
        return result
    
    def get_salary_distribution(self, salary_col: str = 'pre_tax_salary',
                               bins: List[float] = None,
                               labels: List[str] = None) -> pd.DataFrame:
        """获取薪资分布"""
        if self.data is None or salary_col not in self.data.columns:
            raise InvalidColumnError(f"数据为空或薪资列不存在: {salary_col}")
        
        if bins is None:
            bins = [0, 5000, 8000, 10000, 15000, 20000, 30000, 50000, 100000, float('inf')]
        
        if labels is None:
            labels = ['5千以下', '5千-8千', '8千-1万', '1万-1.5万', 
                     '1.5万-2万', '2万-3万', '3万-5万', '5万-10万', '10万以上']
        
        distribution = pd.cut(self.data[salary_col], bins=bins, labels=labels)
        result = distribution.value_counts().sort_index().reset_index()
        result.columns = ['薪资区间', '人数']
        result['占比'] = (result['人数'] / result['人数'].sum() * 100).round(2)
        return result
    
    def get_top_bottom(self, column: str, n: int = 10, 
                      top: bool = True) -> pd.DataFrame:
        """获取Top/Nottom N记录"""
        if self.data is None or column not in self.data.columns:
            raise InvalidColumnError(f"数据为空或列不存在: {column}")
        
        if top:
            result = self.data.nlargest(n, column)
        else:
            result = self.data.nsmallest(n, column)
        
        return result
    
    def get_summary_report(self, salary_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """获取汇总报告"""
        if self.data is None or salary_col not in self.data.columns:
            raise InvalidColumnError(f"数据为空或薪资列不存在: {salary_col}")
        
        salary_data = self.data[salary_col].dropna()
        
        if len(salary_data) == 0:
            return {}
        
        report = {
            'total_records': int(len(self.data)),
            'valid_records': int(len(salary_data)),
            'mean_salary': round(float(salary_data.mean()), 2),
            'median_salary': round(float(salary_data.median()), 2),
            'max_salary': round(float(salary_data.max()), 2),
            'min_salary': round(float(salary_data.min()), 2),
            'std_dev': round(float(salary_data.std()), 2),
            'p25_salary': round(float(salary_data.quantile(0.25)), 2),
            'p75_salary': round(float(salary_data.quantile(0.75)), 2),
            'iqr': round(float(salary_data.quantile(0.75) - salary_data.quantile(0.25)), 2)
        }
        
        return report
    
    def get_dimensions_analysis(self, dimensions: List[str], 
                               salary_col: str = 'pre_tax_salary') -> Dict[str, pd.DataFrame]:
        """多维度分析"""
        if self.data is None:
            raise AnalysisException("数据为空")
        
        results = {}
        
        for dim in dimensions:
            if dim in self.data.columns:
                results[dim] = self.compare_by_dimension(dim, salary_col)
        
        return results
    
    def get_boxplot_data(self, group_by: str, value_col: str) -> Dict[str, Dict]:
        """获取箱线图数据"""
        if self.data is None or group_by not in self.data.columns:
            raise InvalidColumnError(f"数据为空或分组列不存在: {group_by}")
        
        if value_col not in self.data.columns:
            raise InvalidColumnError(f"值列不存在: {value_col}")
        
        result = {}
        
        for category in self.data[group_by].unique():
            subset = self.data[self.data[group_by] == category][value_col].dropna()
            
            if len(subset) > 0:
                result[str(category)] = {
                    'min': float(subset.min()),
                    'q1': float(subset.quantile(0.25)),
                    'median': float(subset.median()),
                    'q3': float(subset.quantile(0.75)),
                    'max': float(subset.max()),
                    'mean': float(subset.mean()),
                    'count': int(len(subset))
                }
        
        return result
    
    def get_current_data(self) -> Optional[pd.DataFrame]:
        """获取当前数据"""
        return self.data
