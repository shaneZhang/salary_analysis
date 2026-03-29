"""
分析控制器模块
处理分析相关的用户操作
"""

from typing import Optional, Any
from ..services.analysis_service import AnalysisService
from ..services.visualization_service import VisualizationService
from ..models.data_manager import DataManager
from ..models.app_state import AppStatusManager
from ..views.dialogs import Dialogs
from ..models.logger import LoggerMixin


class AnalysisController(LoggerMixin):
    """分析控制器"""
    
    def __init__(self, analysis_service: AnalysisService,
                 visualization_service: VisualizationService,
                 data_manager: DataManager,
                 status_manager: AppStatusManager):
        self._analysis_service = analysis_service
        self._visualization_service = visualization_service
        self._data_manager = data_manager
        self._status_manager = status_manager
        self._view: Optional[Any] = None
    
    def set_view(self, view: Any) -> None:
        """设置视图"""
        self._view = view
    
    def show_descriptive_stats(self) -> None:
        """显示描述性统计"""
        if not self._data_manager.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        salary_col = self._get_salary_column()
        result = self._analysis_service.get_descriptive_stats(salary_col)
        
        if result.get('success'):
            stats = result['stats']
            output = f"薪资字段: {salary_col}\n{'='*40}\n\n"
            for key, value in stats.items():
                if value is not None:
                    if isinstance(value, float):
                        output += f"{key}: {value:,.2f}\n"
                    else:
                        output += f"{key}: {value}\n"
            
            if self._view:
                self._view.update_analysis_result(output)
                self._view.select_analysis_tab()
        else:
            Dialogs.show_error('错误', result.get('error', '分析失败'))
    
    def show_frequency_analysis(self) -> None:
        """显示频率分析"""
        if not self._data_manager.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        dimension = self._get_dimension()
        if not dimension:
            Dialogs.show_warning('警告', '请选择分析维度')
            return
        
        result = self._analysis_service.get_frequency_analysis(dimension)
        
        if result.get('success'):
            data = result['data']
            output = f"频率分析: {dimension}\n{'='*40}\n\n"
            output += f"{'值':<20} {'数量':>10} {'占比':>10}\n"
            output += '-' * 40 + '\n'
            for row in data:
                output += f"{str(row[dimension]):<20} {row['count']:>10} {row['percentage']:>9.2f}%\n"
            
            if self._view:
                self._view.update_analysis_result(output)
                self._view.select_analysis_tab()
        else:
            Dialogs.show_error('错误', result.get('error', '分析失败'))
    
    def show_crosstab(self) -> None:
        """显示交叉分析"""
        if not self._data_manager.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        dimension = self._get_dimension()
        if not dimension:
            Dialogs.show_warning('警告', '请选择分析维度')
            return
        
        data = self._data_manager.get_data()
        col_col = 'gender' if 'gender' in data.columns else data.columns[0]
        
        result = self._analysis_service.get_crosstab(dimension, col_col)
        
        if result.get('success'):
            crosstab_data = result['data']
            output = f"交叉分析: {dimension} vs {col_col}\n{'='*40}\n\n"
            
            headers = list(crosstab_data.keys())
            if headers:
                row_headers = list(crosstab_data[headers[0]].keys())
                output += f"{'':<15}"
                for h in headers:
                    output += f"{str(h):>12}"
                output += '\n'
                output += '-' * 60 + '\n'
                
                for row_h in row_headers:
                    output += f"{str(row_h):<15}"
                    for h in headers:
                        output += f"{crosstab_data[h][row_h]:>12}"
                    output += '\n'
            
            if self._view:
                self._view.update_analysis_result(output)
                self._view.select_analysis_tab()
        else:
            Dialogs.show_error('错误', result.get('error', '分析失败'))
    
    def show_correlation(self) -> None:
        """显示相关性分析"""
        if not self._data_manager.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        result = self._analysis_service.get_correlation_matrix()
        
        if result.get('success'):
            corr_data = result['data']
            output = f"相关性分析\n{'='*60}\n\n"
            
            cols = list(corr_data.keys())
            output += f"{'':<15}"
            for col in cols:
                output += f"{col[:10]:>12}"
            output += '\n'
            output += '-' * 80 + '\n'
            
            for row_col in cols:
                output += f"{row_col[:15]:<15}"
                for col in cols:
                    val = corr_data[row_col].get(col, 0)
                    output += f"{val:>12.3f}"
                output += '\n'
            
            if self._view:
                self._view.update_analysis_result(output)
                self._view.select_analysis_tab()
        else:
            Dialogs.show_error('错误', result.get('error', '分析失败'))
    
    def execute_analysis(self) -> None:
        """执行分析"""
        self.show_descriptive_stats()
    
    def generate_chart(self) -> None:
        """生成图表"""
        if not self._data_manager.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        chart_type = self._get_chart_type()
        dimension = self._get_dimension()
        salary_col = self._get_salary_column()
        
        result = self._visualization_service.generate_chart_by_type(
            chart_type, dimension, salary_col
        )
        
        if result.get('success'):
            figure = self._visualization_service.get_current_figure()
            if figure and self._view:
                self._view.embed_chart(figure)
                self._view.select_visualization_tab()
        else:
            Dialogs.show_error('错误', result.get('error', '生成图表失败'))
    
    def export_chart(self) -> None:
        """导出图表"""
        figure = self._visualization_service.get_current_figure()
        
        if figure is None:
            Dialogs.show_warning('警告', '请先生成图表')
            return
        
        output_path = Dialogs.save_file('保存图表', '.png', 
                                        [('PNG图片', '*.png'), ('所有文件', '*.*')])
        
        if not output_path:
            return
        
        result = self._visualization_service.save_chart(output_path)
        
        if result.get('success'):
            Dialogs.show_info('成功', f"图表已保存到: {output_path}")
        else:
            Dialogs.show_error('错误', result.get('error', '保存失败'))
    
    def show_data_overview(self) -> None:
        """显示数据概览"""
        if not self._data_manager.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        data = self._data_manager.get_data()
        if self._view and data is not None:
            self._view.update_data_table(data)
            self._view.select_overview_tab()
    
    def _get_dimension(self) -> str:
        """获取维度"""
        if self._view and hasattr(self._view, 'dimension_var'):
            return self._view.dimension_var.get()
        return ''
    
    def _get_salary_column(self) -> str:
        """获取薪资列名"""
        if self._view and hasattr(self._view, 'salary_var'):
            return self._view.salary_var.get()
        return 'pre_tax_salary'
    
    def _get_chart_type(self) -> str:
        """获取图表类型"""
        if self._view and hasattr(self._view, 'chart_type_var'):
            return self._view.chart_type_var.get()
        return 'bar'
