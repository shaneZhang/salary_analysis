import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from typing import Optional, Dict, Any, List

from src.views.base import BaseView, DataDrivenView, FigureView
from src.views.factory import UIComponentFactory, StyledWidget
from src.models import Logger


class MainView(BaseView):
    """主视图
    
    应用主界面视图。
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._status_bar: Optional[ttk.Label] = None
        self._notebook: Optional[ttk.Notebook] = None
        self._info_text: Optional[tk.Text] = None
        self._overview_tree: Optional[ttk.Treeview] = None
        self._analysis_result_text: Optional[tk.Text] = None
        self._chart_frame: Optional[ttk.Frame] = None
        self._figure_view: Optional[FigureView] = None
        
        # UI组件变量
        self._dimension_var = tk.StringVar()
        self._salary_var = tk.StringVar(value='pre_tax_salary')
        self._chart_type_var = tk.StringVar(value='bar')
        self._viz_dimension_var = tk.StringVar()
        
        # 下拉框组件
        self._dimension_combo: Optional[ttk.Combobox] = None
        self._salary_combo: Optional[ttk.Combobox] = None
        self._viz_dimension_combo: Optional[ttk.Combobox] = None
    
    def render(self) -> None:
        """渲染主界面"""
        self.parent.title('园区白领薪资数据分析工具')
        self.parent.geometry('1400x800')
        self.parent.configure(bg=StyledWidget.STYLES['colors']['bg'])
        
        self._create_menu()
        self._create_main_layout()
    
    def _create_menu(self) -> None:
        """创建菜单栏"""
        menubar = UIComponentFactory.create_menu(self.parent)
        self.parent.config(menu=menubar)
        
        # 文件菜单
        file_menu = UIComponentFactory.create_menu(menubar)
        menubar.add_cascade(label='文件', menu=file_menu)
        file_menu.add_command(label='打开Excel文件', command=self.controller.load_file)
        file_menu.add_command(label='打开文件夹', command=self.controller.load_folder)
        file_menu.add_separator()
        file_menu.add_command(label='导出数据', command=self.controller.export_data)
        file_menu.add_command(label='导出图表', command=self.controller.export_chart)
        file_menu.add_separator()
        file_menu.add_command(label='退出', command=self.parent.quit)
        
        # 数据处理菜单
        data_menu = UIComponentFactory.create_menu(menubar)
        menubar.add_cascade(label='数据处理', menu=data_menu)
        data_menu.add_command(label='数据清洗', command=self._show_clean_dialog)
        data_menu.add_command(label='数据筛选', command=self._show_filter_dialog)
        data_menu.add_command(label='数据分组', command=self._show_group_dialog)
        data_menu.add_command(label='重置数据', command=self.controller.reset_data)
        
        # 分析菜单
        analysis_menu = UIComponentFactory.create_menu(menubar)
        menubar.add_cascade(label='分析', menu=analysis_menu)
        analysis_menu.add_command(label='描述性统计', command=self._show_descriptive_stats)
        analysis_menu.add_command(label='频率分析', command=self._show_frequency_analysis)
        analysis_menu.add_command(label='交叉分析', command=self._show_crosstab)
        analysis_menu.add_command(label='相关性分析', command=self._show_correlation)
        
        # 帮助菜单
        help_menu = UIComponentFactory.create_menu(menubar)
        menubar.add_cascade(label='帮助', menu=help_menu)
        help_menu.add_command(label='使用说明', command=self._show_help)
        help_menu.add_command(label='关于', command=self._show_about)
    
    def _create_main_layout(self) -> None:
        """创建主布局"""
        main_frame = UIComponentFactory.create_frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧面板
        left_panel = UIComponentFactory.create_frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._create_left_panel(left_panel)
        
        # 右侧面板
        right_panel = UIComponentFactory.create_frame(main_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_right_panel(right_panel)
        
        # 状态栏
        self._status_bar = ttk.Label(self.parent, text='就绪', relief=tk.SUNKEN, anchor=tk.W)
        self._status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _create_left_panel(self, parent) -> None:
        """创建左侧面板"""
        title_label = UIComponentFactory.create_label(
            parent, text='功能菜单', 
            font=StyledWidget.STYLES['title_font']
        )
        title_label.pack(pady=(0, 20))
        
        buttons = [
            ('📂 数据导入', self.controller.load_file),
            ('📊 数据概览', self._show_data_overview),
            ('🧹 数据清洗', self._show_clean_dialog),
            ('📈 统计分析', self._show_analysis),
            ('📉 可视化', self._show_visualization),
            ('📋 数据导出', self.controller.export_data),
        ]
        
        for text, command in buttons:
            btn = UIComponentFactory.create_button(parent, text=text, command=command, width=20)
            btn.pack(pady=5, padx=10, fill=tk.X)
        
        info_frame = UIComponentFactory.create_labelframe(parent, text='数据信息')
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=10)
        
        self._info_text = UIComponentFactory.create_text(info_frame, height=15, width=25, state=tk.DISABLED)
        self._info_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_right_panel(self, parent) -> None:
        """创建右侧面板"""
        self._notebook = UIComponentFactory.create_notebook(parent)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        
        # 数据概览标签页
        overview_frame = UIComponentFactory.create_frame(self._notebook)
        self._notebook.add(overview_frame, text='数据概览')
        self._create_overview_tab(overview_frame)
        
        # 统计分析标签页
        analysis_frame = UIComponentFactory.create_frame(self._notebook)
        self._notebook.add(analysis_frame, text='统计分析')
        self._create_analysis_tab(analysis_frame)
        
        # 可视化标签页
        visualization_frame = UIComponentFactory.create_frame(self._notebook)
        self._notebook.add(visualization_frame, text='可视化')
        self._create_visualization_tab(visualization_frame)
    
    def _create_overview_tab(self, parent) -> None:
        """创建数据概览标签页"""
        control_frame = UIComponentFactory.create_frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_button(control_frame, text='刷新', command=self._show_data_overview, width=10).pack(side=tk.LEFT, padx=5)
        
        tree_frame = UIComponentFactory.create_frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._overview_tree = ttk.Treeview(tree_frame, show='tree headings')
        scrollbar_y = UIComponentFactory.create_scrollbar(tree_frame, orient=tk.VERTICAL, command=self._overview_tree.yview)
        scrollbar_x = UIComponentFactory.create_scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self._overview_tree.xview)
        
        self._overview_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._overview_tree.pack(fill=tk.BOTH, expand=True)
    
    def _create_analysis_tab(self, parent) -> None:
        """创建统计分析标签页"""
        control_frame = UIComponentFactory.create_frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_label(control_frame, text='分析维度:').pack(side=tk.LEFT, padx=5)
        
        self._dimension_combo = UIComponentFactory.create_combobox(control_frame, values=[], textvariable=self._dimension_var, width=15)
        self._dimension_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_label(control_frame, text='薪资字段:').pack(side=tk.LEFT, padx=5)
        
        self._salary_combo = UIComponentFactory.create_combobox(control_frame, values=[], textvariable=self._salary_var, width=15)
        self._salary_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_button(control_frame, text='执行分析', command=self._execute_analysis, width=10).pack(side=tk.LEFT, padx=10)
        
        result_frame = UIComponentFactory.create_frame(parent)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._analysis_result_text = UIComponentFactory.create_text(result_frame, height=30)
        scrollbar_y = UIComponentFactory.create_scrollbar(result_frame, orient=tk.VERTICAL, command=self._analysis_result_text.yview)
        self._analysis_result_text.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self._analysis_result_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    
    def _create_visualization_tab(self, parent) -> None:
        """创建可视化标签页"""
        control_frame = UIComponentFactory.create_frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_label(control_frame, text='图表类型:').pack(side=tk.LEFT, padx=5)
        
        chart_types = ['bar', 'horizontal', 'pie', 'line', 'scatter', 'boxplot', 'histogram', 'heatmap']
        chart_type_combo = UIComponentFactory.create_combobox(
            control_frame, values=chart_types, 
            textvariable=self._chart_type_var, width=12
        )
        chart_type_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_label(control_frame, text='分组维度:').pack(side=tk.LEFT, padx=5)
        
        self._viz_dimension_combo = UIComponentFactory.create_combobox(
            control_frame, values=[], 
            textvariable=self._viz_dimension_var, width=12
        )
        self._viz_dimension_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_button(
            control_frame, text='生成图表', 
            command=self._generate_chart, width=10
        ).pack(side=tk.LEFT, padx=10)
        
        UIComponentFactory.create_button(
            control_frame, text='保存图表', 
            command=self.controller.export_chart, width=10
        ).pack(side=tk.LEFT, padx=5)
        
        self._chart_frame = UIComponentFactory.create_frame(parent)
        self._chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._figure_view = FigureView(self._chart_frame)
    
    # === 对话框方法 ===
    
    def _show_clean_dialog(self) -> None:
        """显示数据清洗对话框"""
        if not self.controller.has_data():
            self.show_warning("请先加载数据")
            return
        
        from src.views.dialogs import CleanDialog
        dialog = CleanDialog(self.parent, self.controller)
        dialog.show()
    
    def _show_filter_dialog(self) -> None:
        """显示数据筛选对话框"""
        self.show_info("数据筛选功能开发中...")
    
    def _show_group_dialog(self) -> None:
        """显示数据分组对话框"""
        if not self.controller.has_data():
            self.show_warning("请先加载数据")
            return
        
        from src.views.dialogs import GroupDialog
        dialog = GroupDialog(self.parent, self.controller)
        dialog.show()
    
    # === 分析方法 ===
    
    def _show_descriptive_stats(self) -> None:
        """显示描述性统计"""
        salary_col = self._salary_var.get()
        if not salary_col:
            salary_cols = self.controller.get_salary_columns()
            if salary_cols:
                salary_col = salary_cols[0]
            else:
                self.show_warning("没有可用的薪资字段")
                return
        
        stats = self.controller.get_descriptive_stats(salary_col)
        if not stats:
            return
        
        result = f'薪资字段: {salary_col}\n{"="*40}\n\n'
        for key, value in stats.items():
            if value is not None:
                if isinstance(value, float):
                    result += f'{key}: {value:,.2f}\n'
                else:
                    result += f'{key}: {value}\n'
        
        self._analysis_result_text.delete('1.0', tk.END)
        self._analysis_result_text.insert('1.0', result)
        self._notebook.select(1)  # 切换到分析标签页
    
    def _show_frequency_analysis(self) -> None:
        """显示频率分析"""
        dimension = self._dimension_var.get()
        if not dimension:
            self.show_warning("请选择分析维度")
            return
        
        freq = self.controller.get_frequency_analysis(dimension)
        if freq.empty:
            return
        
        result = f'频率分析: {dimension}\n{"="*40}\n\n'
        result += freq.to_string(index=False)
        
        self._analysis_result_text.delete('1.0', tk.END)
        self._analysis_result_text.insert('1.0', result)
        self._notebook.select(1)
    
    def _show_crosstab(self) -> None:
        """显示交叉分析"""
        dimension = self._dimension_var.get()
        if not dimension:
            self.show_warning("请选择分析维度")
            return
        
        data = self.controller.get_current_data()
        if data is None:
            return
        
        col_col = 'gender' if 'gender' in data.columns else data.columns[0]
        crosstab = self.controller.get_crosstab(dimension, col_col)
        
        result = f'交叉分析: {dimension} x {col_col}\n{"="*40}\n\n'
        result += crosstab.to_string()
        
        self._analysis_result_text.delete('1.0', tk.END)
        self._analysis_result_text.insert('1.0', result)
        self._notebook.select(1)
    
    def _show_correlation(self) -> None:
        """显示相关性分析"""
        corr = self.controller.get_correlation_matrix()
        
        result = f'相关性矩阵\n{"="*40}\n\n'
        result += corr.to_string()
        
        self._analysis_result_text.delete('1.0', tk.END)
        self._analysis_result_text.insert('1.0', result)
        self._notebook.select(1)
    
    def _execute_analysis(self) -> None:
        """执行分析"""
        dimension = self._dimension_var.get()
        salary_col = self._salary_var.get()
        
        if not dimension:
            self.show_warning("请选择分析维度")
            return
        
        comparison = self.controller.compare_by_dimension(dimension, salary_col)
        
        result = f'维度分析: {dimension}\n薪资字段: {salary_col}\n{"="*50}\n\n'
        result += comparison.to_string(index=False)
        
        self._analysis_result_text.delete('1.0', tk.END)
        self._analysis_result_text.insert('1.0', result)
    
    def _show_analysis(self) -> None:
        """切换到分析标签页并显示默认分析"""
        self._notebook.select(1)
        self._show_descriptive_stats()
    
    # === 可视化方法 ===
    
    def _generate_chart(self) -> None:
        """生成图表"""
        chart_type = self._chart_type_var.get()
        dimension = self._viz_dimension_var.get()
        salary_col = self._salary_var.get()
        
        if not dimension and chart_type not in ['histogram', 'heatmap']:
            self.show_warning("请选择分组维度")
            return
        
        self.controller.generate_chart(chart_type, dimension, salary_col, self._chart_frame)
    
    def display_chart(self, figure: Figure, parent_widget=None) -> None:
        """显示图表"""
        if self._figure_view:
            self._figure_view.clear()
            self._figure_view.embed_figure(figure, toolbar=True)
    
    def _show_visualization(self) -> None:
        """切换到可视化标签页"""
        self._notebook.select(2)
    
    # === 数据概览方法 ===
    
    def _show_data_overview(self) -> None:
        """显示数据概览"""
        data = self.controller.get_current_data()
        if data is None:
            self.show_warning("请先加载数据")
            return
        
        self._overview_tree.delete(*self._overview_tree.get_children())
        
        columns = ['#'] + list(data.columns)
        self._overview_tree['columns'] = columns
        self._overview_tree['show'] = 'tree headings'
        
        self._overview_tree.heading('#', text='#')
        self._overview_tree.column('#', width=50, minwidth=50)
        
        for col in data.columns:
            self._overview_tree.heading(col, text=col)
            self._overview_tree.column(col, width=120, minwidth=80)
        
        for idx, row in data.head(100).iterrows():
            values = [str(idx)] + [str(v) for v in row.values]
            self._overview_tree.insert('', tk.END, values=values)
    
    # === 辅助方法 ===
    
    def update_data_info(self) -> None:
        """更新数据信息"""
        if self._info_text is None:
            return
        
        self._info_text.config(state=tk.NORMAL)
        self._info_text.delete('1.0', tk.END)
        
        info = self.controller.get_data_info()
        
        if info:
            info_text = f'记录数: {info.get("rows", 0)}\n'
            info_text += f'字段数: {info.get("columns", 0)}\n\n'
            info_text += '字段列表:\n'
            
            for col in info.get('column_names', []):
                info_text += f'  - {col}\n'
            
            missing = info.get('missing_values', {})
            if sum(missing.values()) > 0:
                info_text += '\n缺失值:\n'
                for col, count in missing.items():
                    if count > 0:
                        info_text += f'  - {col}: {count}\n'
            
            self._info_text.insert('1.0', info_text)
        
        self._info_text.config(state=tk.DISABLED)
        
        # 更新下拉框选项
        self._update_comboboxes()
    
    def _update_comboboxes(self) -> None:
        """更新下拉框选项"""
        dimensions = self.controller.get_available_dimensions()
        salary_cols = self.controller.get_salary_columns()
        
        if self._dimension_combo:
            self._dimension_combo['values'] = dimensions
        
        if self._viz_dimension_combo:
            self._viz_dimension_combo['values'] = dimensions
        
        if self._salary_combo:
            self._salary_combo['values'] = salary_cols
            if salary_cols:
                self._salary_var.set(salary_cols[0])
    
    def set_status(self, text: str) -> None:
        """设置状态栏文本"""
        if self._status_bar:
            self._status_bar.config(text=text)
    
    def _show_help(self) -> None:
        """显示帮助"""
        help_text = '''数据导入:
  - 支持打开单个Excel文件或整个文件夹
  - 自动识别常见字段名称并映射

数据处理:
  - 删除重复数据、缺失值处理
  - 数据分组（年龄、薪资、工作年限）
  - 异常值检测与处理

分析功能:
  - 描述性统计（均值、中位数、标准差等）
  - 频率分析、交叉分析
  - 相关性分析

可视化:
  - 柱状图、折线图、饼图
  - 散点图、箱线图、直方图
  - 支持图表导出'''
        self.show_info(help_text, "使用说明")
    
    def _show_about(self) -> None:
        """显示关于"""
        self.show_info("园区白领薪资数据分析工具\n\n版本: 2.0.0\n\n基于 Python + Pandas + Matplotlib 构建", "关于")
