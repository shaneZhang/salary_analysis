from typing import Dict, List, Optional, Tuple
import pandas as pd
from matplotlib.figure import Figure

from ..core.visualizer import DataVisualizer
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import AppLogger
from ..exceptions import VisualizationError


class VisualizationService:
    def __init__(self, data_manager: DataManager, config: ConfigManager, logger: AppLogger = None):
        self._data_manager = data_manager
        self._config = config
        self._logger = logger or AppLogger.get_instance()
        self._visualizer = DataVisualizer()
        self._setup_visualizer_config()
    
    def _setup_visualizer_config(self):
        app_config = self._config.get_app_config()
        self._visualizer.set_config({
            'figure_size': app_config.figure_size,
            'dpi': app_config.dpi,
            'title_fontsize': app_config.title_fontsize,
            'label_fontsize': app_config.label_fontsize,
            'tick_fontsize': app_config.tick_fontsize,
            'legend_fontsize': app_config.legend_fontsize,
            'colors': app_config.chart_colors
        })
    
    def _sync_visualizer_data(self):
        data = self._data_manager.get_data()
        if data is not None:
            self._visualizer.set_data(data)
    
    def create_bar_chart(self, x_data: List, y_data: List, 
                        title: str = '', xlabel: str = '', ylabel: str = '',
                        horizontal: bool = False) -> Dict:
        try:
            self._logger.info(f"创建柱状图: {title}")
            figure = self._visualizer.create_bar_chart(
                x_data, y_data, title, xlabel, ylabel,
                horizontal=horizontal
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建柱状图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_line_chart(self, x_data: List, y_data_list: List[List],
                         title: str = '', xlabel: str = '', ylabel: str = '',
                         labels: Optional[List[str]] = None) -> Dict:
        try:
            self._logger.info(f"创建折线图: {title}")
            figure = self._visualizer.create_line_chart(
                x_data, y_data_list, title, xlabel, ylabel, labels
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建折线图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_pie_chart(self, data: List, labels: List[str],
                        title: str = '') -> Dict:
        try:
            self._logger.info(f"创建饼图: {title}")
            figure = self._visualizer.create_pie_chart(data, labels, title)
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建饼图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_scatter_chart(self, x_data: List, y_data: List,
                            title: str = '', xlabel: str = '', ylabel: str = '') -> Dict:
        try:
            self._logger.info(f"创建散点图: {title}")
            figure = self._visualizer.create_scatter_chart(
                x_data, y_data, title, xlabel, ylabel
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建散点图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_boxplot(self, data_dict: Dict[str, List],
                      title: str = '', xlabel: str = '', ylabel: str = '') -> Dict:
        try:
            self._logger.info(f"创建箱线图: {title}")
            figure = self._visualizer.create_boxplot(
                data_dict, title, xlabel, ylabel
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建箱线图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_histogram(self, data: List, bins: int = 30,
                        title: str = '', xlabel: str = '', ylabel: str = 'Frequency',
                        kde: bool = False) -> Dict:
        try:
            self._logger.info(f"创建直方图: {title}")
            figure = self._visualizer.create_histogram(
                data, bins, title, xlabel, ylabel, kde=kde
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建直方图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_heatmap(self, data: pd.DataFrame,
                       title: str = '') -> Dict:
        try:
            self._logger.info(f"创建热力图: {title}")
            figure = self._visualizer.create_heatmap(data, title)
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建热力图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_salary_distribution_chart(self, salary_col: str = 'pre_tax_salary',
                                        group_col: Optional[str] = None) -> Dict:
        try:
            self._sync_visualizer_data()
            data = self._data_manager.get_data()
            if data is None:
                return {'success': False, 'error': '没有数据'}
            
            self._logger.info(f"创建薪资分布图: {salary_col}")
            figure = self._visualizer.create_salary_distribution_chart(
                data, salary_col, group_col
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建薪资分布图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_comparison_chart(self, dimension_col: str,
                               salary_col: str = 'pre_tax_salary',
                               chart_type: str = 'bar') -> Dict:
        try:
            self._sync_visualizer_data()
            data = self._data_manager.get_data()
            if data is None:
                return {'success': False, 'error': '没有数据'}
            
            self._logger.info(f"创建对比图: {dimension_col}")
            figure = self._visualizer.create_comparison_chart(
                data, dimension_col, salary_col, chart_type
            )
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建对比图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_trend_chart(self, time_col: str,
                          salary_col: str = 'pre_tax_salary') -> Dict:
        try:
            self._sync_visualizer_data()
            data = self._data_manager.get_data()
            if data is None:
                return {'success': False, 'error': '没有数据'}
            
            self._logger.info(f"创建趋势图: {time_col}")
            figure = self._visualizer.create_trend_chart(data, time_col, salary_col)
            return {
                'success': True,
                'figure': figure
            }
        except Exception as e:
            self._logger.error(f"创建趋势图失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def save_chart(self, output_path: str, dpi: int = 300, 
                   format: str = 'png') -> Dict:
        try:
            self._logger.info(f"保存图表: {output_path}")
            self._visualizer.save_chart(output_path, dpi, format)
            return {
                'success': True,
                'output_path': output_path
            }
        except VisualizationError as e:
            self._logger.error(f"保存图表失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_current_figure(self) -> Optional[Figure]:
        return self._visualizer.get_current_figure()
    
    def set_figure_size(self, width: float, height: float):
        self._visualizer.set_figure_size(width, height)
    
    def set_dpi(self, dpi: int):
        self._visualizer.set_dpi(dpi)
    
    def set_color_scheme(self, colors: List[str]):
        self._visualizer.set_color_scheme(colors)
