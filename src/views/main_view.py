"""
主视图模块
定义应用的主界面
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Any, List, Dict, Callable
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from .base import BaseView, FrameView
from .factory import UIComponentFactory
from .dialogs import Dialogs, DataCleanDialog, DataGroupDialog, AboutDialog, HelpDialog


class MainView(BaseView):
    """主视图"""
    
    def __init__(self, root: tk.Tk, controller: Any = None):
        super().__init__(root, controller)
        self.root = root
        self._widget = root
        
        self.dimension_var = tk.StringVar()
        self.salary_var = tk.StringVar(value='pre_tax_salary')
        self.chart_type_var = tk.StringVar(value='bar')
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """设置UI"""
        self.root.configure(bg='#f5f5f5')
        
        self._create_menu()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._create_left_panel(left_panel)
        
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_right_panel(right_panel)
        
        self.status_bar = ttk.Label(self.root, text='就绪', relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _create_menu(self) -> None:
        """创建菜单"""
        menubar = UIComponentFactory.create_menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = UIComponentFactory.create_menu(menubar, tearoff=0)
        menubar.add_cascade(label='文件', menu=file_menu)
        file_menu.add_command(label='打开Excel文件', command=self._on_load_file)
        file_menu.add_command(label='打开文件夹', command=self._on_load_folder)
        file_menu.add_separator()
        file_menu.add_command(label='导出数据', command=self._on_export_data)
        file_menu.add_command(label='导出图表', command=self._on_export_chart)
        file_menu.add_separator()
        file_menu.add_command(label='退出', command=self.root.quit)
        
        data_menu = UIComponentFactory.create_menu(menubar, tearoff=0)
        menubar.add_cascade(label='数据处理', menu=data_menu)
        data_menu.add_command(label='数据清洗', command=self._on_clean_data)
        data_menu.add_command(label='数据分组', command=self._on_group_data)
        data_menu.add_command(label='重置数据', command=self._on_reset_data)
        
        analysis_menu = UIComponentFactory.create_menu(menubar, tearoff=0)
        menubar.add_cascade(label='分析', menu=analysis_menu)
        analysis_menu.add_command(label='描述性统计', command=self._on_descriptive_stats)
        analysis_menu.add_command(label='频率分析', command=self._on_frequency_analysis)
        analysis_menu.add_command(label='交叉分析', command=self._on_crosstab)
        analysis_menu.add_command(label='相关性分析', command=self._on_correlation)
        
        help_menu = UIComponentFactory.create_menu(menubar, tearoff=0)
        menubar.add_cascade(label='帮助', menu=help_menu)
        help_menu.add_command(label='使用说明', command=self._on_help)
        help_menu.add_command(label='关于', command=self._on_about)
    
    def _create_left_panel(self, parent: ttk.Frame) -> None:
        """创建左侧面板"""
        title_label = ttk.Label(parent, text='功能菜单', font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        buttons = [
            ('📂 数据导入', self._on_load_file),
            ('📊 数据概览', self._on_data_overview),
            ('🧹 数据清洗', self._on_clean_data),
            ('📈 统计分析', self._on_analysis),
            ('📉 可视化', self._on_visualization),
            ('📋 数据导出', self._on_export_data),
        ]
        
        for text, command in buttons:
            btn = UIComponentFactory.create_button(parent, text, command, width=20)
            btn.pack(pady=5, padx=10, fill=tk.X)
        
        info_frame = ttk.LabelFrame(parent, text='数据信息', padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=10)
        
        self.info_text = tk.Text(info_frame, height=15, width=25, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_right_panel(self, parent: ttk.Frame) -> None:
        """创建右侧面板"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.overview_frame = ttk.Frame(self.notebook)
        self.analysis_frame = ttk.Frame(self.notebook)
        self.visualization_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.overview_frame, text='数据概览')
        self.notebook.add(self.analysis_frame, text='统计分析')
        self.notebook.add(self.visualization_frame, text='可视化')
        
        self._create_overview_tab()
        self._create_analysis_tab()
        self._create_visualization_tab()
    
    def _create_overview_tab(self) -> None:
        """创建数据概览标签页"""
        control_frame = ttk.Frame(self.overview_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_button(
            control_frame, '刷新', self._on_data_overview
        ).pack(side=tk.LEFT, padx=5)
        
        self.overview_tree = UIComponentFactory.create_treeview(
            self.overview_frame, show='tree headings'
        )
        
        scrollbar_y = UIComponentFactory.create_scrollbar(
            self.overview_frame, orient='vertical', command=self.overview_tree.yview
        )
        scrollbar_x = UIComponentFactory.create_scrollbar(
            self.overview_frame, orient='horizontal', command=self.overview_tree.xview
        )
        
        self.overview_tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.overview_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_analysis_tab(self) -> None:
        """创建统计分析标签页"""
        control_frame = ttk.Frame(self.analysis_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text='分析维度:').pack(side=tk.LEFT, padx=5)
        self.dimension_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.dimension_var, width=15
        )
        self.dimension_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text='薪资字段:').pack(side=tk.LEFT, padx=5)
        self.salary_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.salary_var, width=15
        )
        self.salary_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_button(
            control_frame, '执行分析', self._on_execute_analysis
        ).pack(side=tk.LEFT, padx=10)
        
        self.analysis_result_text = UIComponentFactory.create_text(self.analysis_frame, height=30)
        self.analysis_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_visualization_tab(self) -> None:
        """创建可视化标签页"""
        control_frame = ttk.Frame(self.visualization_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text='图表类型:').pack(side=tk.LEFT, padx=5)
        chart_types = ['bar', 'line', 'pie', 'scatter', 'boxplot', 'histogram']
        self.chart_type_combo = UIComponentFactory.create_combobox(
            control_frame, values=chart_types,
            textvariable=self.chart_type_var, width=12
        )
        self.chart_type_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text='分组维度:').pack(side=tk.LEFT, padx=5)
        self.viz_dimension_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.dimension_var, width=12
        )
        self.viz_dimension_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_button(
            control_frame, '生成图表', self._on_generate_chart
        ).pack(side=tk.LEFT, padx=10)
        
        UIComponentFactory.create_button(
            control_frame, '保存图表', self._on_export_chart
        ).pack(side=tk.LEFT, padx=5)
        
        self.chart_frame = ttk.Frame(self.visualization_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_info_text(self, info: str) -> None:
        """更新数据信息文本"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', info)
        self.info_text.config(state=tk.DISABLED)
    
    def update_data_table(self, data: pd.DataFrame, max_rows: int = 100) -> None:
        """更新数据表格"""
        self.overview_tree.delete(*self.overview_tree.get_children())
        
        columns = ['#'] + list(data.columns)
        self.overview_tree['columns'] = columns
        self.overview_tree['show'] = 'tree headings'
        
        self.overview_tree.heading('#', text='#')
        self.overview_tree.column('#', width=50, minwidth=50)
        
        for col in data.columns:
            self.overview_tree.heading(col, text=col)
            self.overview_tree.column(col, width=120, minwidth=80)
        
        for idx, row in data.head(max_rows).iterrows():
            values = [str(idx)] + [str(v) for v in row.values]
            self.overview_tree.insert('', tk.END, values=values)
    
    def update_analysis_result(self, result: str) -> None:
        """更新分析结果"""
        self.analysis_result_text.delete('1.0', tk.END)
        self.analysis_result_text.insert('1.0', result)
    
    def update_comboboxes(self, categorical_cols: List[str], numeric_cols: List[str]) -> None:
        """更新下拉框选项"""
        self.dimension_combo['values'] = categorical_cols
        self.viz_dimension_combo['values'] = categorical_cols
        
        salary_candidates = ['pre_tax_salary', 'post_tax_salary', 'base_salary', 'total_salary']
        available_salary = [col for col in numeric_cols 
                          if col.lower() in [s.lower() for s in salary_candidates]]
        if not available_salary:
            available_salary = numeric_cols
        
        self.salary_combo['values'] = available_salary
        if available_salary:
            self.salary_var.set(available_salary[0])
    
    def embed_chart(self, figure) -> None:
        """嵌入图表"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
    
    def set_status(self, message: str) -> None:
        """设置状态栏"""
        self.status_bar.config(text=message)
    
    def select_analysis_tab(self) -> None:
        """选择分析标签页"""
        self.notebook.select(1)
    
    def select_visualization_tab(self) -> None:
        """选择可视化标签页"""
        self.notebook.select(2)
    
    def select_overview_tab(self) -> None:
        """选择概览标签页"""
        self.notebook.select(0)
    
    def _on_load_file(self) -> None:
        if self.controller:
            self.controller.load_file()
    
    def _on_load_folder(self) -> None:
        if self.controller:
            self.controller.load_folder()
    
    def _on_export_data(self) -> None:
        if self.controller:
            self.controller.export_data()
    
    def _on_export_chart(self) -> None:
        if self.controller:
            self.controller.export_chart()
    
    def _on_clean_data(self) -> None:
        if self.controller:
            self.controller.clean_data()
    
    def _on_group_data(self) -> None:
        if self.controller:
            self.controller.group_data()
    
    def _on_reset_data(self) -> None:
        if self.controller:
            self.controller.reset_data()
    
    def _on_descriptive_stats(self) -> None:
        if self.controller:
            self.controller.show_descriptive_stats()
    
    def _on_frequency_analysis(self) -> None:
        if self.controller:
            self.controller.show_frequency_analysis()
    
    def _on_crosstab(self) -> None:
        if self.controller:
            self.controller.show_crosstab()
    
    def _on_correlation(self) -> None:
        if self.controller:
            self.controller.show_correlation()
    
    def _on_help(self) -> None:
        HelpDialog(self.root).show()
    
    def _on_about(self) -> None:
        AboutDialog(self.root).show()
    
    def _on_data_overview(self) -> None:
        if self.controller:
            self.controller.show_data_overview()
    
    def _on_analysis(self) -> None:
        self.select_analysis_tab()
    
    def _on_visualization(self) -> None:
        self.select_visualization_tab()
    
    def _on_execute_analysis(self) -> None:
        if self.controller:
            self.controller.execute_analysis()
    
    def _on_generate_chart(self) -> None:
        if self.controller:
            self.controller.generate_chart()
    
    def render(self) -> None:
        pass
