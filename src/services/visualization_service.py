"""
可视化服务模块
封装图表生成功能
"""

from typing import Optional, Dict, Any, List
import pandas as pd
from matplotlib.figure import Figure
from ..core.visualizer import DataVisualizer
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import LoggerMixin
from ..exceptions import VisualizationException
from ..events.event_bus import EventBus, EVENT_TYPES


class VisualizationService(LoggerMixin):
    """
    可视化服务
    协调可视化器和数据管理器
    """
    
    def __init__(self, data_manager: DataManager, config: ConfigManager,
                 event_bus: Optional[EventBus] = None):
        self._data_manager = data_manager
        self._config = config
        self._event_bus = event_bus
        
        figure_size = config.get('figure_size', (10, 6))
        if isinstance(figure_size, list):
            figure_size = tuple(figure_size)
        
        chart_config = {
            'figure_size': figure_size,
            'dpi': config.get('dpi', 100),
            'colors': config.get_chart_colors()
        }
        self._visualizer = DataVisualizer(chart_config)
    
    def create_bar_chart(self, x_data: List, y_data: List,
                        title: str = '', xlabel: str = '', ylabel: str = '',
                        horizontal: bool = False) -> Dict[str, Any]:
        """
        创建柱状图
        
        Args:
            x_data: X轴数据
            y_data: Y轴数据
            title: 标题
            xlabel: X轴标签
            ylabel: Y轴标签
            horizontal: 是否水平
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_bar_chart(
                x_data, y_data, title, xlabel, ylabel,
                horizontal=horizontal
            )
            
            return {
                'success': True,
                'chart_type': 'bar'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_line_chart(self, x_data: List, y_data_list: List[List[float]],
                         title: str = '', xlabel: str = '', ylabel: str = '',
                         labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        创建折线图
        
        Args:
            x_data: X轴数据
            y_data_list: Y轴数据列表
            title: 标题
            xlabel: X轴标签
            ylabel: Y轴标签
            labels: 图例标签
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_line_chart(
                x_data, y_data_list, title, xlabel, ylabel, labels
            )
            
            return {
                'success': True,
                'chart_type': 'line'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_pie_chart(self, data: List, labels: List[str],
                        title: str = '') -> Dict[str, Any]:
        """
        创建饼图
        
        Args:
            data: 数据
            labels: 标签
            title: 标题
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_pie_chart(data, labels, title)
            
            return {
                'success': True,
                'chart_type': 'pie'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_scatter_chart(self, x_data: List, y_data: List,
                            title: str = '', xlabel: str = '', ylabel: str = '') -> Dict[str, Any]:
        """
        创建散点图
        
        Args:
            x_data: X轴数据
            y_data: Y轴数据
            title: 标题
            xlabel: X轴标签
            ylabel: Y轴标签
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_scatter_chart(
                x_data, y_data, title, xlabel, ylabel
            )
            
            return {
                'success': True,
                'chart_type': 'scatter'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_boxplot(self, data_dict: Dict[str, List],
                      title: str = '', xlabel: str = '', ylabel: str = '') -> Dict[str, Any]:
        """
        创建箱线图
        
        Args:
            data_dict: 数据字典
            title: 标题
            xlabel: X轴标签
            ylabel: Y轴标签
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_boxplot(
                data_dict, title, xlabel, ylabel
            )
            
            return {
                'success': True,
                'chart_type': 'boxplot'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_histogram(self, data: List, bins: int = 30,
                        title: str = '', xlabel: str = '',
                        kde: bool = False) -> Dict[str, Any]:
        """
        创建直方图
        
        Args:
            data: 数据
            bins: 分组数
            title: 标题
            xlabel: X轴标签
            kde: 是否显示核密度估计
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_histogram(
                data, bins, title, xlabel, kde=kde
            )
            
            return {
                'success': True,
                'chart_type': 'histogram'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_heatmap(self, data: pd.DataFrame,
                       title: str = '') -> Dict[str, Any]:
        """
        创建热力图
        
        Args:
            data: 数据框
            title: 标题
            
        Returns:
            结果
        """
        try:
            figure = self._visualizer.create_heatmap(data, title)
            
            return {
                'success': True,
                'chart_type': 'heatmap'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_salary_distribution_chart(self, salary_col: str = 'pre_tax_salary',
                                        group_col: Optional[str] = None) -> Dict[str, Any]:
        """
        创建薪资分布图
        
        Args:
            salary_col: 薪资列
            group_col: 分组列
            
        Returns:
            结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        try:
            figure = self._visualizer.create_salary_distribution_chart(
                data, salary_col, group_col
            )
            
            return {
                'success': True,
                'chart_type': 'salary_distribution'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_comparison_chart(self, dimension_col: str,
                               salary_col: str = 'pre_tax_salary',
                               chart_type: str = 'bar') -> Dict[str, Any]:
        """
        创建对比图
        
        Args:
            dimension_col: 维度列
            salary_col: 薪资列
            chart_type: 图表类型
            
        Returns:
            结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        try:
            figure = self._visualizer.create_comparison_chart(
                data, dimension_col, salary_col, chart_type
            )
            
            return {
                'success': True,
                'chart_type': 'comparison'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_trend_chart(self, time_col: str,
                          salary_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        创建趋势图
        
        Args:
            time_col: 时间列
            salary_col: 薪资列
            
        Returns:
            结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        try:
            figure = self._visualizer.create_trend_chart(data, time_col, salary_col)
            
            return {
                'success': True,
                'chart_type': 'trend'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_chart_by_type(self, chart_type: str,
                               dimension: Optional[str] = None,
                               value_col: str = 'pre_tax_salary') -> Dict[str, Any]:
        """
        根据类型生成图表
        
        Args:
            chart_type: 图表类型
            dimension: 维度列
            value_col: 数值列
            
        Returns:
            结果
        """
        data = self._data_manager.get_data()
        if data is None:
            return {'success': False, 'error': '没有数据'}
        
        try:
            if chart_type == 'bar' and dimension:
                return self.create_comparison_chart(dimension, value_col, 'bar')
            elif chart_type == 'pie' and dimension:
                freq = data[dimension].value_counts()
                return self.create_pie_chart(
                    freq.values.tolist(),
                    freq.index.tolist(),
                    f'{dimension}分布'
                )
            elif chart_type == 'histogram':
                return self.create_histogram(
                    data[value_col].dropna().tolist(),
                    bins=20,
                    title=f'{value_col}分布',
                    xlabel=value_col
                )
            elif chart_type == 'boxplot' and dimension:
                boxplot_data = {}
                for cat in data[dimension].unique():
                    boxplot_data[str(cat)] = data[data[dimension] == cat][value_col].dropna().tolist()
                return self.create_boxplot(
                    boxplot_data,
                    title=f'{dimension} - {value_col}分布',
                    xlabel=dimension,
                    ylabel=value_col
                )
            else:
                return {'success': False, 'error': f'不支持的图表类型: {chart_type}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_chart(self, output_path: str, dpi: int = 300,
                  format: str = 'png') -> Dict[str, Any]:
        """
        保存图表
        
        Args:
            output_path: 输出路径
            dpi: 分辨率
            format: 格式
            
        Returns:
            结果
        """
        try:
            self._visualizer.save_chart(output_path, dpi, format)
            
            if self._event_bus:
                self._event_bus.publish(EVENT_TYPES['CHART_GENERATED'], {
                    'output_path': output_path
                })
            
            return {
                'success': True,
                'output_path': output_path
            }
        except VisualizationException as e:
            return {'success': False, 'error': str(e)}
    
    def get_current_figure(self) -> Optional[Figure]:
        """获取当前图形"""
        return self._visualizer.get_current_figure()
