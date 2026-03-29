import tkinter as tk
from typing import Optional

from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.logger import AppLogger
from ..models.app_state import AppState, AppStateStatus
from ..services.data_service import DataService
from ..services.processing_service import ProcessingService
from ..services.analysis_service import AnalysisService
from ..services.visualization_service import VisualizationService
from ..views.main_view import MainView
from ..views.dialogs import Dialogs


class MainController:
    def __init__(self, root: tk.Tk, config_path: Optional[str] = None):
        self.root = root
        self.root.title('园区白领薪资数据分析工具')
        self.root.geometry('1400x800')
        
        self._init_models(config_path)
        self._init_services()
        self._init_view()
        self._setup_data_observer()
    
    def _init_models(self, config_path: Optional[str]):
        self.config = ConfigManager(config_path)
        self.data_manager = DataManager()
        self.logger = AppLogger.get_instance()
        self.app_state = AppState.get_instance()
    
    def _init_services(self):
        self.data_service = DataService(self.data_manager, self.config, self.logger)
        self.processing_service = ProcessingService(self.data_manager, self.config, self.logger)
        self.analysis_service = AnalysisService(self.data_manager, self.config, self.logger)
        self.viz_service = VisualizationService(self.data_manager, self.config, self.logger)
    
    def _init_view(self):
        self.view = MainView(self.root, self)
        self.view.render()
    
    def _setup_data_observer(self):
        self.data_manager.subscribe(self._on_data_change)
    
    def _on_data_change(self, data):
        if data is not None:
            self._update_info_text()
            self._update_comboboxes()
    
    def _update_info_text(self):
        info = self.data_manager.get_data_info()
        if info.get('has_data'):
            text = f"记录数: {info['rows']}\n"
            text += f"字段数: {info['columns']}\n\n"
            text += "字段列表:\n"
            for col in info['column_names']:
                text += f"  - {col}\n"
            
            missing = info.get('missing_values', {})
            if any(v > 0 for v in missing.values()):
                text += '\n缺失值:\n'
                for col, count in missing.items():
                    if count > 0:
                        text += f'  - {col}: {count}\n'
            
            self.view.update_info_text(text)
    
    def _update_comboboxes(self):
        info = self.data_manager.get_data_info()
        if info.get('has_data'):
            self.view.update_comboboxes(
                info.get('categorical_columns', []),
                info.get('numeric_columns', [])
            )
    
    def load_file(self):
        file_path = Dialogs.select_file('选择Excel文件')
        if file_path:
            self.view.update_status(f'正在加载: {file_path}')
            self.root.update()
            
            result = self.data_service.load_file(file_path)
            
            if result['success']:
                self.view.show_message('成功', f"数据加载成功！\n共 {result['rows']} 条记录")
                self.view.update_status('数据加载成功')
                self.show_data_overview()
            else:
                self.view.show_message('错误', f"加载失败: {result.get('error', '未知错误')}", 'error')
                self.view.update_status('数据加载失败')
    
    def load_folder(self):
        folder_path = Dialogs.select_folder('选择文件夹')
        if folder_path:
            self.view.update_status(f'正在加载文件夹: {folder_path}')
            self.root.update()
            
            result = self.data_service.load_folder(folder_path)
            
            if result['success']:
                self.view.show_message('成功', f"数据加载成功！\n共 {result['rows']} 条记录")
                self.view.update_status('数据加载成功')
                self.show_data_overview()
            else:
                self.view.show_message('错误', f"加载失败: {result.get('error', '未知错误')}", 'error')
                self.view.update_status('数据加载失败')
    
    def export_data(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        output_path = Dialogs.save_file('保存数据', '.xlsx')
        if output_path:
            result = self.data_service.export_data(output_path, 'excel' if output_path.endswith('.xlsx') else 'csv')
            if result['success']:
                self.view.show_message('成功', f"数据已导出到: {output_path}")
            else:
                self.view.show_message('错误', f"导出失败: {result.get('error', '未知错误')}", 'error')
    
    def export_chart(self):
        output_path = Dialogs.save_file('保存图表', '.png', [('PNG图片', '*.png'), ('所有文件', '*.*')])
        if output_path:
            result = self.viz_service.save_chart(output_path)
            if result['success']:
                self.view.show_message('成功', f"图表已保存到: {output_path}")
            else:
                self.view.show_message('错误', f"保存失败: {result.get('error', '未知错误')}", 'error')
    
    def clean_data(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        Dialogs.show_clean_data_dialog(self.root, self._do_clean)
    
    def _do_clean(self, operation: str):
        if operation == 'duplicates':
            result = self.processing_service.remove_duplicates()
            if result['success']:
                self.view.show_message('完成', f"删除了 {result['removed_count']} 条重复记录")
        
        elif operation == 'missing':
            result = self.processing_service.handle_missing_values('drop')
            if result['success']:
                self.view.show_message('完成', f"处理了 {result['total_handled']} 个缺失值")
        
        elif operation == 'fill_mean':
            result = self.processing_service.handle_missing_values('fill_mean')
            if result['success']:
                self.view.show_message('完成', '已用均值填充数值型缺失值')
        
        elif operation == 'outliers':
            salary_col = self.view.get_salary_column()
            result = self.processing_service.remove_outliers(salary_col)
            if result['success']:
                self.view.show_message('完成', f"移除了 {result['removed_count']} 条异常值记录")
        
        self._update_info_text()
    
    def filter_data(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        self.view.show_message('提示', '数据筛选功能开发中...\n可使用数据概览表格进行查看')
    
    def group_data(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        Dialogs.show_group_data_dialog(self.root, self._do_group)
    
    def _do_group(self, operation: str):
        if operation == 'age':
            result = self.processing_service.create_age_group()
            if result['success']:
                self.view.show_message('完成', '已创建年龄分组字段: age_group')
            else:
                self.view.show_message('警告', result.get('error', '年龄字段不存在'), 'warning')
        
        elif operation == 'salary':
            salary_col = self.view.get_salary_column()
            result = self.processing_service.create_salary_group(salary_col)
            if result['success']:
                self.view.show_message('完成', '已创建薪资分组字段: salary_group')
            else:
                self.view.show_message('警告', result.get('error', '薪资字段不存在'), 'warning')
        
        elif operation == 'experience':
            result = self.processing_service.create_experience_group()
            if result['success']:
                self.view.show_message('完成', '已创建工作年限分组字段: experience_group')
            else:
                self.view.show_message('警告', result.get('error', '工作年限字段不存在'), 'warning')
        
        self._update_info_text()
    
    def reset_data(self):
        if self.data_manager.has_data():
            result = self.processing_service.reset_data()
            if result['success']:
                self._update_info_text()
                self.view.show_message('完成', '数据已重置')
    
    def show_descriptive_stats(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        salary_col = self.view.get_salary_column()
        result = self.analysis_service.get_descriptive_stats(salary_col)
        
        if result['success']:
            stats = result['stats']
            text = f"薪资字段: {salary_col}\n{'='*40}\n\n"
            for key, value in stats.items():
                if value is not None:
                    if isinstance(value, float):
                        text += f"{key}: {value:,.2f}\n"
                    else:
                        text += f"{key}: {value}\n"
            
            self.view.update_analysis_result(text)
    
    def show_frequency_analysis(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        dimension = self.view.get_dimension()
        if not dimension:
            self.view.show_message('警告', '请选择分析维度', 'warning')
            return
        
        result = self.analysis_service.get_frequency_analysis(dimension)
        
        if result['success']:
            data = result['data']
            text = f"频率分析: {dimension}\n{'='*40}\n\n"
            for row in data:
                text += f"{row[dimension]}: {row['count']} ({row['percentage']}%)\n"
            
            self.view.update_analysis_result(text)
    
    def show_crosstab(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        dimension = self.view.get_dimension()
        if not dimension:
            self.view.show_message('警告', '请选择分析维度', 'warning')
            return
        
        info = self.data_manager.get_data_info()
        col_col = 'gender' if 'gender' in info.get('column_names', []) else info.get('column_names', [None])[0]
        
        result = self.analysis_service.get_crosstab(dimension, col_col)
        
        if result['success']:
            text = f"交叉分析: {dimension} vs {col_col}\n{'='*40}\n\n"
            for row_key, values in result['data'].items():
                text += f"{row_key}: {values}\n"
            
            self.view.update_analysis_result(text)
    
    def show_correlation(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        result = self.analysis_service.get_correlation_matrix()
        
        if result['success']:
            text = "相关性矩阵\n" + "="*40 + "\n\n"
            for row_key, values in result['data'].items():
                text += f"{row_key}: {values}\n"
            
            self.view.update_analysis_result(text)
    
    def show_help(self):
        help_text = """
园区白领薪资数据分析工具 - 使用说明

1. 数据导入
   - 点击"数据导入"或菜单"文件->打开Excel文件"
   - 支持单个Excel文件或整个文件夹导入

2. 数据处理
   - 数据清洗：删除重复、处理缺失值、移除异常值
   - 数据分组：按年龄、薪资、工作年限分组

3. 统计分析
   - 描述性统计：查看薪资的基本统计信息
   - 频率分析：查看各维度的分布情况
   - 相关性分析：查看数值字段间的相关性

4. 可视化
   - 支持柱状图、折线图、饼图、散点图等多种图表
   - 可导出图表为PNG格式
        """
        self.view.show_message('使用说明', help_text)
    
    def show_about(self):
        self.view.show_message('关于', '园区白领薪资数据分析工具 v2.0\n\n基于Python + Pandas + Matplotlib开发\n采用MVC架构设计')
    
    def show_data_overview(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        data = self.data_manager.get_data()
        self.view.update_overview_tree(data)
    
    def show_analysis(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        self.show_descriptive_stats()
    
    def show_visualization(self):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        self.generate_chart('bar', self.view.get_viz_dimension(), self.view.get_salary_column())
    
    def execute_analysis(self, dimension: str, salary_col: str):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        if dimension:
            result = self.analysis_service.compare_by_dimension(dimension, salary_col)
            
            if result['success']:
                text = f"按 {dimension} 分组分析\n{'='*40}\n\n"
                for row in result['data']:
                    text += f"{row[dimension]}:\n"
                    text += f"  人数: {row['人数']}\n"
                    text += f"  平均薪资: {row['平均薪资']:,.2f}\n"
                    text += f"  中位薪资: {row['中位薪资']:,.2f}\n\n"
                
                self.view.update_analysis_result(text)
        else:
            self.show_descriptive_stats()
    
    def generate_chart(self, chart_type: str, dimension: str, salary_col: str):
        if not self.data_manager.has_data():
            self.view.show_message('警告', '请先加载数据', 'warning')
            return
        
        result = None
        
        if chart_type == 'bar':
            if dimension:
                result = self.viz_service.create_comparison_chart(dimension, salary_col, 'bar')
            else:
                result = self.viz_service.create_salary_distribution_chart(salary_col)
        
        elif chart_type == 'line':
            result = self.viz_service.create_trend_chart(dimension or 'join_year', salary_col)
        
        elif chart_type == 'pie':
            if dimension:
                freq_result = self.analysis_service.get_frequency_analysis(dimension)
                if freq_result['success']:
                    data = [row['count'] for row in freq_result['data']]
                    labels = [row[dimension] for row in freq_result['data']]
                    result = self.viz_service.create_pie_chart(data, labels, f'{dimension}分布')
        
        elif chart_type == 'scatter':
            info = self.data_manager.get_data_info()
            numeric_cols = info.get('numeric_columns', [])
            if len(numeric_cols) >= 2:
                data = self.data_manager.get_data()
                x_data = data[numeric_cols[0]].dropna().tolist()
                y_data = data[numeric_cols[1]].dropna().tolist()
                min_len = min(len(x_data), len(y_data))
                result = self.viz_service.create_scatter_chart(
                    x_data[:min_len], y_data[:min_len],
                    f'{numeric_cols[0]} vs {numeric_cols[1]}',
                    numeric_cols[0], numeric_cols[1]
                )
        
        elif chart_type == 'boxplot':
            if dimension:
                boxplot_result = self.analysis_service.get_boxplot_data(dimension, salary_col)
                if boxplot_result['success']:
                    data_dict = {k: [v['min'], v['q1'], v['median'], v['q3'], v['max']] 
                                for k, v in boxplot_result['data'].items()}
                    result = self.viz_service.create_boxplot(
                        boxplot_result['data'], 
                        f'{dimension} - {salary_col}分布',
                        dimension, salary_col
                    )
        
        elif chart_type == 'histogram':
            result = self.viz_service.create_salary_distribution_chart(salary_col)
        
        if result and result.get('success'):
            self.view.embed_chart(result['figure'])
        elif result:
            self.view.show_message('错误', f"生成图表失败: {result.get('error', '未知错误')}", 'error')
