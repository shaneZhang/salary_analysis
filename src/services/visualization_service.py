import pandas as pd
from matplotlib.figure import Figure
from typing import Optional, List, Dict, Tuple

from src.models import DataManager, ConfigManager, Logger
from src.core import DataVisualizer
from src.exceptions import VisualizationException


class VisualizationService:
    """可视化服务层
    
    提供图表生成服务。
    """
    
    def __init__(self, data_manager: DataManager, config_manager: ConfigManager):
        self._data_manager = data_manager
        self._config_manager = config_manager
        self._logger = Logger()
        self._visualizer = DataVisualizer()
        
        self._update_config()
    
    def _update_config(self):
        """更新可视化配置"""
        chart_config = {
            'figure_size': self._config_manager.config.figure_size,
            'dpi': self._config_manager.config.dpi,
            'title_fontsize': self._config_manager.config.title_fontsize,
            'label_fontsize': self._config_manager.config.label_fontsize,
            'tick_fontsize': self._config_manager.config.tick_fontsize,
            'colors': self._config_manager.get_chart_colors()
        }
        self._visualizer.set_config(chart_config)
    
    def _ensure_data(self) -> pd.DataFrame:
        """确保有数据可用"""
        data = self._data_manager.get_data()
        if data is None:
            raise VisualizationException("没有可用的数据")
        return data
    
    def create_bar_chart(self, dimension_col: str, value_col: Optional[str] = None,
                        horizontal: bool = False, title: Optional[str] = None) -> Figure:
        """创建柱状图"""
        data = self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        if dimension_col not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {dimension_col} 或 {value_col}")
        
        grouped = data.groupby(dimension_col)[value_col].mean().sort_values(ascending=False)
        
        if title is None:
            title = f'{dimension_col} - 平均薪资对比'
        
        self._logger.info(f"创建柱状图: {dimension_col} vs {value_col}")
        
        return self._visualizer.create_bar_chart(
            x_data=grouped.index.tolist(),
            y_data=grouped.values.tolist(),
            title=title,
            xlabel='平均薪资' if horizontal else dimension_col,
            ylabel=dimension_col if horizontal else '平均薪资',
            horizontal=horizontal
        )
    
    def create_pie_chart(self, dimension_col: str, value_col: Optional[str] = None,
                        title: Optional[str] = None, top_n: int = 8) -> Figure:
        """创建饼图"""
        data = self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        if dimension_col not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {dimension_col} 或 {value_col}")
        
        grouped = data.groupby(dimension_col)[value_col].sum().sort_values(ascending=False)
        
        if len(grouped) > top_n:
            grouped = grouped.head(top_n)
        
        if title is None:
            title = f'{dimension_col} - 薪资占比'
        
        self._logger.info(f"创建饼图: {dimension_col}")
        
        return self._visualizer.create_pie_chart(
            data=grouped.values.tolist(),
            labels=grouped.index.tolist(),
            title=title
        )
    
    def create_line_chart(self, time_col: str, value_col: Optional[str] = None,
                         title: Optional[str] = None) -> Figure:
        """创建折线图（趋势图）"""
        data = self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        if time_col not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {time_col} 或 {value_col}")
        
        trend = data.groupby(time_col)[value_col].agg(['mean', 'median']).reset_index()
        
        x_data = trend[time_col].tolist()
        y_mean = trend['mean'].tolist()
        y_median = trend['median'].tolist()
        
        if title is None:
            title = '薪资趋势变化'
        
        self._logger.info(f"创建趋势图: {time_col}")
        
        return self._visualizer.create_line_chart(
            x_data=x_data,
            y_data_list=[y_mean, y_median],
            title=title,
            xlabel=time_col,
            ylabel='薪资',
            labels=['平均薪资', '中位薪资']
        )
    
    def create_scatter_chart(self, x_col: str, y_col: str,
                            title: Optional[str] = None,
                            show_trendline: bool = True) -> Figure:
        """创建散点图"""
        data = self._ensure_data()
        
        if x_col not in data.columns or y_col not in data.columns:
            raise VisualizationException(f"列不存在: {x_col} 或 {y_col}")
        
        valid_data = data[[x_col, y_col]].dropna()
        
        if title is None:
            title = f'{x_col} 与 {y_col} 关系'
        
        self._logger.info(f"创建散点图: {x_col} vs {y_col}")
        
        return self._visualizer.create_scatter_chart(
            x_data=valid_data[x_col].tolist(),
            y_data=valid_data[y_col].tolist(),
            title=title,
            xlabel=x_col,
            ylabel=y_col,
            show_trendline=show_trendline
        )
    
    def create_boxplot(self, dimension_col: str, value_col: Optional[str] = None,
                      title: Optional[str] = None) -> Figure:
        """创建箱线图"""
        data = self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        if dimension_col not in data.columns or value_col not in data.columns:
            raise VisualizationException(f"列不存在: {dimension_col} 或 {value_col}")
        
        box_data = {}
        for category in data[dimension_col].unique():
            subset = data[data[dimension_col] == category][value_col].dropna()
            if len(subset) > 0:
                box_data[str(category)] = subset.tolist()
        
        if title is None:
            title = f'{dimension_col} - 薪资分布'
        
        self._logger.info(f"创建箱线图: {dimension_col}")
        
        return self._visualizer.create_boxplot(
            data_dict=box_data,
            title=title,
            xlabel=dimension_col,
            ylabel='薪资'
        )
    
    def create_histogram(self, column: str, bins: int = 20,
                        title: Optional[str] = None, kde: bool = False) -> Figure:
        """创建直方图"""
        data = self._ensure_data()
        
        if column not in data.columns:
            raise VisualizationException(f"列不存在: {column}")
        
        hist_data = data[column].dropna().tolist()
        
        if title is None:
            title = f'{column} 分布直方图'
        
        self._logger.info(f"创建直方图: {column}")
        
        return self._visualizer.create_histogram(
            data=hist_data,
            bins=bins,
            title=title,
            xlabel=column,
            kde=kde
        )
    
    def create_heatmap(self, columns: Optional[List[str]] = None,
                      title: Optional[str] = None) -> Figure:
        """创建相关性热力图"""
        data = self._ensure_data()
        
        if columns is None:
            columns = data.select_dtypes(include=['number']).columns.tolist()
        
        corr_matrix = data[columns].corr().round(3)
        
        if title is None:
            title = '相关性热力图'
        
        self._logger.info("创建相关性热力图")
        
        return self._visualizer.create_heatmap(
            data=corr_matrix,
            title=title
        )
    
    def create_comparison_chart(self, dimension_col: str, value_col: Optional[str] = None,
                               chart_type: str = 'bar') -> Figure:
        """创建比较图表"""
        data = self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        self._logger.info(f"创建比较图表: {dimension_col}")
        
        return self._visualizer.create_comparison_chart(
            df=data,
            dimension_col=dimension_col,
            salary_col=value_col,
            chart_type=chart_type
        )
    
    def create_trend_chart(self, time_col: str, value_col: Optional[str] = None) -> Figure:
        """创建趋势图表"""
        data = self._ensure_data()
        
        if value_col is None:
            value_col = self._get_default_salary_column()
        
        self._logger.info(f"创建趋势图表: {time_col}")
        
        return self._visualizer.create_trend_chart(
            df=data,
            time_col=time_col,
            salary_col=value_col
        )
    
    def save_current_chart(self, output_path: str, dpi: int = 300, format: str = 'png') -> bool:
        """保存当前图表到文件"""
        return self._visualizer.save_chart(output_path, dpi, format)
    
    def get_current_figure(self) -> Optional[Figure]:
        """获取当前Figure对象"""
        return self._visualizer.get_current_figure()
    
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
        
        raise VisualizationException("没有找到合适的薪资列")
    
    @property
    def visualizer(self) -> DataVisualizer:
        """获取底层可视化器"""
        return self._visualizer
