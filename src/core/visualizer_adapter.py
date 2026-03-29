import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from typing import Optional, List, Dict

from .visualizer import DataVisualizer
from src.exceptions import VisualizationException


class DataVisualizerAdapter:
    """数据可视化适配器
    
    封装DataVisualizer，提供更方便的DataFrame接口。
    """
    
    def __init__(self, custom_style: Optional[Dict] = None):
        self._visualizer = DataVisualizer()
        if custom_style:
            self._visualizer.set_config(custom_style)
    
    def create_bar_chart(self, data: pd.DataFrame, group_by: str, value_col: str, 
                        title: str = '', xlabel: str = '', ylabel: str = '',
                        horizontal: bool = False) -> Figure:
        """创建柱状图"""
        if group_by not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {group_by} 或 {value_col}")
        
        grouped = data.groupby(group_by)[value_col].mean().sort_values(ascending=horizontal)
        
        if not title:
            title = f'{group_by} - 平均{value_col}对比'
        if not xlabel:
            xlabel = group_by if not horizontal else '平均薪资'
        if not ylabel:
            ylabel = '平均薪资' if not horizontal else group_by
        
        return self._visualizer.create_bar_chart(
            x_data=grouped.index.tolist(),
            y_data=grouped.values.tolist(),
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            horizontal=horizontal
        )
    
    def create_pie_chart(self, data: pd.DataFrame, group_by: str, value_col: str,
                        title: str = '') -> Figure:
        """创建饼图"""
        if group_by not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {group_by} 或 {value_col}")
        
        grouped = data.groupby(group_by)[value_col].sum()
        
        if not title:
            title = f'{group_by} - {value_col}占比'
        
        return self._visualizer.create_pie_chart(
            data=grouped.values.tolist(),
            labels=grouped.index.tolist(),
            title=title
        )
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                         title: str = '', xlabel: str = '', ylabel: str = '') -> Figure:
        """创建折线图"""
        if x_col not in data.columns or y_col not in data.columns:
            raise VisualizationException(f"列不存在: {x_col} 或 {y_col}")
        
        grouped = data.groupby(x_col)[y_col].mean().reset_index()
        
        if not title:
            title = f'{y_col}随{x_col}变化趋势'
        if not xlabel:
            xlabel = x_col
        if not ylabel:
            ylabel = y_col
        
        return self._visualizer.create_line_chart(
            x_data=grouped[x_col].tolist(),
            y_data_list=[grouped[y_col].tolist()],
            title=title,
            xlabel=xlabel,
            ylabel=ylabel
        )
    
    def create_scatter_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                            title: str = '', xlabel: str = '', ylabel: str = '') -> Figure:
        """创建散点图"""
        if x_col not in data.columns or y_col not in data.columns:
            raise VisualizationException(f"列不存在: {x_col} 或 {y_col}")
        
        valid_data = data[[x_col, y_col]].dropna()
        
        if not title:
            title = f'{x_col}与{y_col}关系'
        if not xlabel:
            xlabel = x_col
        if not ylabel:
            ylabel = y_col
        
        return self._visualizer.create_scatter_chart(
            x_data=valid_data[x_col].tolist(),
            y_data=valid_data[y_col].tolist(),
            title=title,
            xlabel=xlabel,
            ylabel=ylabel
        )
    
    def create_boxplot(self, data: pd.DataFrame, group_by: str, value_col: str,
                      title: str = '', xlabel: str = '', ylabel: str = '') -> Figure:
        """创建箱线图"""
        if group_by not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {group_by} 或 {value_col}")
        
        data_dict = {}
        for category in data[group_by].unique():
            subset = data[data[group_by] == category][value_col].dropna()
            if len(subset) > 0:
                data_dict[str(category)] = subset.tolist()
        
        if not title:
            title = f'{group_by} - {value_col}分布'
        if not xlabel:
            xlabel = group_by
        if not ylabel:
            ylabel = value_col
        
        return self._visualizer.create_boxplot(
            data_dict=data_dict,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel
        )
    
    def create_histogram(self, data: pd.DataFrame, column: str, bins: int = 30,
                        title: str = '', xlabel: str = '', ylabel: str = 'Frequency',
                        kde: bool = False) -> Figure:
        """创建直方图"""
        if column not in data.columns:
            raise VisualizationException(f"列不存在: {column}")
        
        valid_data = data[column].dropna().tolist()
        
        if not title:
            title = f'{column}分布'
        if not xlabel:
            xlabel = column
        
        return self._visualizer.create_histogram(
            data=valid_data,
            bins=bins,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            kde=kde
        )
    
    def create_heatmap(self, data: pd.DataFrame,
                       title: str = '',
                       cmap: str = 'YlOrRd',
                       annot: bool = True) -> Figure:
        """创建热力图"""
        if data.empty:
            raise VisualizationException("数据为空")
        
        # 只选择数值列
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.empty:
            raise VisualizationException("没有数值列用于创建热力图")
        
        corr_matrix = numeric_data.corr()
        
        if not title:
            title = '相关性热力图'
        
        return self._visualizer.create_heatmap(
            data=corr_matrix,
            title=title,
            cmap=cmap,
            annot=annot
        )
    
    def set_style(self, style_config: Dict) -> None:
        """设置样式配置"""
        self._visualizer.set_config(style_config)
    
    def get_current_figure(self) -> Optional[Figure]:
        """获取当前图表"""
        return self._visualizer.get_current_figure()
    
    def save_chart(self, output_path: str, dpi: int = 300, format: str = 'png') -> bool:
        """保存图表"""
        return self._visualizer.save_chart(output_path, dpi, format)
