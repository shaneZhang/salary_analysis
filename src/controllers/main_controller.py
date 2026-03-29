import tkinter as tk
from tkinter import filedialog
from typing import Optional, Dict, Any, List, TYPE_CHECKING
import pandas as pd

from src.models import DataManager, ConfigManager, Logger
from src.services import DataService, ProcessingService, AnalysisService, VisualizationService
from src.exceptions import AppException, DataLoadError, DataProcessingError, AnalysisException, VisualizationException

if TYPE_CHECKING:
    from src.views import MainView


class MainController:
    """主控制器
    
    协调视图和服务层之间的交互，处理用户操作。
    """
    
    def __init__(self):        
        # 初始化模型层
        self._data_manager = DataManager()
        self._config_manager = ConfigManager()
        
        # 加载配置
        try:
            self._config_manager.load()
        except Exception as e:
            print(f"配置加载失败，使用默认配置: {e}")
        
        # 初始化日志
        self._logger = Logger()
        
        # 初始化服务层
        self._data_service = DataService(self._data_manager, self._config_manager)
        self._processing_service = ProcessingService(self._data_manager, self._config_manager)
        self._analysis_service = AnalysisService(self._data_manager, self._config_manager)
        self._visualization_service = VisualizationService(self._data_manager, self._config_manager)
        
        # 视图 - 后期设置以避免循环依赖
        self._view: Optional['MainView'] = None
        self._root: Optional[tk.Tk] = None
        
        # 订阅数据变化
        self._data_service.subscribe_to_data_changes(self._on_data_changed)
        
        self._logger.info("应用初始化完成")
    
    def set_view(self, view: 'MainView', root: tk.Tk) -> None:
        """设置视图对象"""
        self._view = view
        self._root = root
    
    def run(self) -> None:
        """运行应用"""
        if self._view:
            self._view.render()
    
    def _on_data_changed(self, data: Optional[pd.DataFrame]) -> None:
        """数据变化回调"""
        self._view.update_data_info()
    
    # === 文件操作 ===
    
    def load_file(self) -> None:
        """加载Excel文件"""
        file_path = filedialog.askopenfilename(
            title='选择Excel文件',
            filetypes=[('Excel文件', '*.xlsx *.xls'), ('所有文件', '*.*')]
        )
        
        if not file_path:
            return
        
        try:
            self._view.set_status(f"正在加载: {file_path}")
            if self._root:
                self._root.update()
            
            self._data_service.load_file(file_path)
            
            self._view.show_info(f"数据加载成功！\n共 {len(self._data_service.get_current_data())} 条记录")
            self._view.set_status("数据加载成功")
            
        except DataLoadError as e:
            self._view.show_error(str(e))
            self._view.set_status("数据加载失败")
            self._logger.error(f"文件加载失败: {e}")
        except Exception as e:
            self._view.show_error(f"发生未知错误: {str(e)}")
            self._view.set_status("错误")
            self._logger.error(f"未知错误: {e}", exc_info=True)
    
    def load_folder(self) -> None:
        """加载文件夹"""
        folder_path = filedialog.askdirectory(title='选择文件夹')
        
        if not folder_path:
            return
        
        try:
            self._view.set_status(f"正在加载文件夹: {folder_path}")
            if self._root:
                self._root.update()
            
            self._data_service.load_folder(folder_path)
            
            self._view.show_info(f"数据加载成功！\n共 {len(self._data_service.get_current_data())} 条记录")
            self._view.set_status("数据加载成功")
            
        except DataLoadError as e:
            self._view.show_error(str(e))
            self._view.set_status("数据加载失败")
            self._logger.error(f"文件夹加载失败: {e}")
        except Exception as e:
            self._view.show_error(f"发生未知错误: {str(e)}")
            self._view.set_status("错误")
            self._logger.error(f"未知错误: {e}", exc_info=True)
    
    def export_data(self) -> None:
        """导出数据"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel文件', '*.xlsx'), ('CSV文件', '*.csv')]
        )
        
        if not file_path:
            return
        
        try:
            format_type = 'excel' if file_path.endswith('.xlsx') else 'csv'
            self._data_service.export_data(file_path, format_type)
            self._view.show_info(f"数据已导出到:\n{file_path}")
        except DataLoadError as e:
            self._view.show_error(str(e))
            self._logger.error(f"数据导出失败: {e}")
    
    def export_chart(self) -> None:
        """导出图表"""
        figure = self._visualization_service.get_current_figure()
        if figure is None:
            self._view.show_warning("没有可导出的图表")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[('PNG图片', '*.png'), ('JPG图片', '*.jpg'), ('PDF文档', '*.pdf')]
        )
        
        if not file_path:
            return
        
        try:
            fmt = file_path.split('.')[-1]
            self._visualization_service.save_current_chart(file_path, format=fmt)
            self._view.show_info(f"图表已保存到:\n{file_path}")
        except Exception as e:
            self._view.show_error(f"保存失败: {str(e)}")
            self._logger.error(f"图表导出失败: {e}", exc_info=True)
    
    # === 数据处理 ===
    
    def clean_duplicates(self) -> int:
        """删除重复数据"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return 0
        
        try:
            count = self._processing_service.remove_duplicates()
            return count
        except DataProcessingError as e:
            self._view.show_error(str(e))
            return 0
    
    def clean_missing_values(self, strategy: str = 'drop') -> Dict[str, int]:
        """处理缺失值"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return {}
        
        try:
            result = self._processing_service.handle_missing_values(strategy)
            return result
        except DataProcessingError as e:
            self._view.show_error(str(e))
            return {}
    
    def clean_outliers(self, column: str) -> int:
        """移除异常值"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return 0
        
        try:
            count = self._processing_service.remove_outliers(column)
            return count
        except (DataProcessingError, AnalysisException) as e:
            self._view.show_error(str(e))
            return 0
    
    def create_age_group(self) -> bool:
        """创建年龄分组"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return False
        
        try:
            return self._processing_service.create_age_group()
        except DataProcessingError as e:
            self._view.show_error(str(e))
            return False
    
    def create_salary_group(self, salary_col: str) -> bool:
        """创建薪资分组"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return False
        
        try:
            return self._processing_service.create_salary_group(salary_col)
        except DataProcessingError as e:
            self._view.show_error(str(e))
            return False
    
    def create_experience_group(self) -> bool:
        """创建工作年限分组"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return False
        
        try:
            return self._processing_service.create_work_experience_group()
        except DataProcessingError as e:
            self._view.show_error(str(e))
            return False
    
    def reset_data(self) -> None:
        """重置数据"""
        self._data_service.reset_data()
        self._view.show_info("数据已重置")
    
    # === 数据分析 ===
    
    def get_descriptive_stats(self, column: str) -> Dict[str, float]:
        """获取描述性统计"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return {}
        
        try:
            return self._analysis_service.get_descriptive_stats(column)
        except AnalysisException as e:
            self._view.show_error(str(e))
            return {}
    
    def get_frequency_analysis(self, column: str) -> pd.DataFrame:
        """获取频率分析"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return pd.DataFrame()
        
        try:
            return self._analysis_service.get_frequency_analysis(column)
        except AnalysisException as e:
            self._view.show_error(str(e))
            return pd.DataFrame()
    
    def get_crosstab(self, row_col: str, col_col: str) -> pd.DataFrame:
        """获取交叉分析"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return pd.DataFrame()
        
        try:
            return self._analysis_service.get_crosstab(row_col, col_col)
        except AnalysisException as e:
            self._view.show_error(str(e))
            return pd.DataFrame()
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """获取相关性矩阵"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return pd.DataFrame()
        
        try:
            return self._analysis_service.get_correlation_matrix()
        except AnalysisException as e:
            self._view.show_error(str(e))
            return pd.DataFrame()
    
    def compare_by_dimension(self, dimension: str, salary_col: str) -> pd.DataFrame:
        """按维度比较"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return pd.DataFrame()
        
        try:
            return self._analysis_service.compare_by_dimension(dimension, salary_col)
        except AnalysisException as e:
            self._view.show_error(str(e))
            return pd.DataFrame()
    
    # === 数据可视化 ===
    
    def generate_chart(self, chart_type: str, dimension: str, salary_col: str, parent_widget):
        """生成图表"""
        if not self._data_service.has_data():
            self._view.show_warning("请先加载数据")
            return
        
        try:
            figure = None
            
            if chart_type == 'bar':
                figure = self._visualization_service.create_bar_chart(dimension, salary_col)
            elif chart_type == 'horizontal':
                figure = self._visualization_service.create_bar_chart(dimension, salary_col, horizontal=True)
            elif chart_type == 'pie':
                figure = self._visualization_service.create_pie_chart(dimension, salary_col)
            elif chart_type == 'line':
                if 'join_year' in self.get_numeric_columns():
                    figure = self._visualization_service.create_line_chart('join_year', salary_col)
                else:
                    self._view.show_warning("数据中没有时间字段")
                    return
            elif chart_type == 'scatter':
                if 'work_years' in self.get_numeric_columns():
                    figure = self._visualization_service.create_scatter_chart('work_years', salary_col)
                else:
                    self._view.show_warning("数据中没有工作年限字段")
                    return
            elif chart_type == 'boxplot':
                figure = self._visualization_service.create_boxplot(dimension, salary_col)
            elif chart_type == 'histogram':
                figure = self._visualization_service.create_histogram(salary_col, bins=20)
            elif chart_type == 'heatmap':
                figure = self._visualization_service.create_heatmap()
            
            if figure:
                self._view.display_chart(figure, parent_widget)
        
        except VisualizationException as e:
            self._view.show_error(str(e))
            self._logger.error(f"图表生成失败: {e}")
        except Exception as e:
            self._view.show_error(f"图表生成失败: {str(e)}")
            self._logger.error(f"图表生成失败: {e}", exc_info=True)
    
    # === 辅助方法 ===
    
    def get_current_data(self) -> Optional[pd.DataFrame]:
        """获取当前数据"""
        return self._data_service.get_current_data()
    
    def get_data_info(self) -> Dict[str, Any]:
        """获取数据信息"""
        return self._data_service.get_data_info()
    
    def has_data(self) -> bool:
        """检查是否有数据"""
        return self._data_service.has_data()
    
    def get_available_dimensions(self) -> List[str]:
        """获取可用维度"""
        return self._analysis_service.get_available_dimensions()
    
    def get_numeric_columns(self) -> List[str]:
        """获取数值列"""
        return self._analysis_service.get_numeric_columns()
    
    def get_salary_columns(self) -> List[str]:
        """获取薪资列"""
        return self._analysis_service.get_salary_columns()
    
    def get_summary_report(self, salary_col: str) -> Dict[str, Any]:
        """获取汇总报告"""
        if not self._data_service.has_data():
            return {}
        return self._analysis_service.get_summary_report(salary_col)
    
    @property
    def view(self) -> 'MainView':
        """获取视图对象"""
        return self._view
