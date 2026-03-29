import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict, Any, Callable

from .factory import UIComponentFactory
from .base import BaseView, ObserverMixin
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MainView(BaseView, ObserverMixin):
    def __init__(self, parent, controller=None):
        BaseView.__init__(self, parent, controller)
        ObserverMixin.__init__(self)
        self._setup_styles()
    
    def _setup_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
    
    def render(self):
        self._widget = ttk.Frame(self.parent)
        self._widget.pack(fill=tk.BOTH, expand=True)
        
        self._create_menu()
        self._create_main_layout()
        self._create_status_bar()
    
    def _create_menu(self):
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='文件', menu=file_menu)
        file_menu.add_command(label='打开Excel文件', command=self._on_load_file)
        file_menu.add_command(label='打开文件夹', command=self._on_load_folder)
        file_menu.add_separator()
        file_menu.add_command(label='导出数据', command=self._on_export_data)
        file_menu.add_command(label='导出图表', command=self._on_export_chart)
        file_menu.add_separator()
        file_menu.add_command(label='退出', command=self.parent.quit)
        
        data_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='数据处理', menu=data_menu)
        data_menu.add_command(label='数据清洗', command=self._on_clean_data)
        data_menu.add_command(label='数据筛选', command=self._on_filter_data)
        data_menu.add_command(label='数据分组', command=self._on_group_data)
        data_menu.add_command(label='重置数据', command=self._on_reset_data)
        
        analysis_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='分析', menu=analysis_menu)
        analysis_menu.add_command(label='描述性统计', command=self._on_descriptive_stats)
        analysis_menu.add_command(label='频率分析', command=self._on_frequency_analysis)
        analysis_menu.add_command(label='交叉分析', command=self._on_crosstab)
        analysis_menu.add_command(label='相关性分析', command=self._on_correlation)
        
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='帮助', menu=help_menu)
        help_menu.add_command(label='使用说明', command=self._on_help)
        help_menu.add_command(label='关于', command=self._on_about)
    
    def _create_main_layout(self):
        main_frame = UIComponentFactory.create_frame(self._widget, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_panel = UIComponentFactory.create_frame(main_frame, padding=5)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.configure(width=250)
        left_panel.pack_propagate(False)
        
        self._create_left_panel(left_panel)
        
        right_panel = UIComponentFactory.create_frame(main_frame, padding=5)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_right_panel(right_panel)
    
    def _create_left_panel(self, parent):
        title_label = UIComponentFactory.create_label(
            parent, text='功能菜单', style='Title.TLabel'
        )
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
            btn = UIComponentFactory.create_button(parent, text=text, command=command, width=20)
            btn.pack(pady=5, padx=10, fill=tk.X)
        
        info_frame = UIComponentFactory.create_labelframe(parent, text='数据信息', padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=10)
        
        self.info_text = UIComponentFactory.create_text(
            info_frame, height=15, width=25, state=tk.DISABLED
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_right_panel(self, parent):
        self.notebook = UIComponentFactory.create_notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.overview_frame = UIComponentFactory.create_frame(self.notebook)
        self.analysis_frame = UIComponentFactory.create_frame(self.notebook)
        self.visualization_frame = UIComponentFactory.create_frame(self.notebook)
        
        self.notebook.add(self.overview_frame, text='数据概览')
        self.notebook.add(self.analysis_frame, text='统计分析')
        self.notebook.add(self.visualization_frame, text='可视化')
        
        self._create_overview_tab()
        self._create_analysis_tab()
        self._create_visualization_tab()
    
    def _create_overview_tab(self):
        control_frame = UIComponentFactory.create_frame(self.overview_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_button(
            control_frame, text='刷新', command=self._on_data_overview
        ).pack(side=tk.LEFT, padx=5)
        
        self.overview_tree_frame, self.overview_tree = UIComponentFactory.setup_scrollable_treeview(
            self.overview_frame, columns=[], show='tree headings'
        )
        self.overview_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_analysis_tab(self):
        control_frame = UIComponentFactory.create_frame(self.analysis_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_label(control_frame, text='分析维度:').pack(side=tk.LEFT, padx=5)
        
        self.dimension_var = tk.StringVar()
        self.dimension_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.dimension_var, width=15
        )
        self.dimension_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_label(control_frame, text='薪资字段:').pack(side=tk.LEFT, padx=5)
        
        self.salary_var = tk.StringVar(value='pre_tax_salary')
        self.salary_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.salary_var, width=15
        )
        self.salary_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_button(
            control_frame, text='执行分析', command=self._on_execute_analysis
        ).pack(side=tk.LEFT, padx=10)
        
        self.analysis_result_text = UIComponentFactory.create_text(
            self.analysis_frame, height=30
        )
        self.analysis_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_visualization_tab(self):
        control_frame = UIComponentFactory.create_frame(self.visualization_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_label(control_frame, text='图表类型:').pack(side=tk.LEFT, padx=5)
        
        self.chart_type_var = tk.StringVar(value='bar')
        chart_types = ['bar', 'line', 'pie', 'scatter', 'boxplot', 'histogram']
        self.chart_type_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.chart_type_var, 
            values=chart_types, width=12
        )
        self.chart_type_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_label(control_frame, text='分组维度:').pack(side=tk.LEFT, padx=5)
        
        self.viz_dimension_var = tk.StringVar()
        self.viz_dimension_combo = UIComponentFactory.create_combobox(
            control_frame, textvariable=self.viz_dimension_var, width=12
        )
        self.viz_dimension_combo.pack(side=tk.LEFT, padx=5)
        
        UIComponentFactory.create_button(
            control_frame, text='生成图表', command=self._on_generate_chart
        ).pack(side=tk.LEFT, padx=10)
        
        UIComponentFactory.create_button(
            control_frame, text='保存图表', command=self._on_export_chart
        ).pack(side=tk.LEFT, padx=5)
        
        self.chart_frame = UIComponentFactory.create_frame(self.visualization_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_status_bar(self):
        self.status_bar = ttk.Label(
            self._widget, text='就绪', relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_info_text(self, info: str):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', info)
        self.info_text.config(state=tk.DISABLED)
    
    def update_status(self, text: str):
        self.status_bar.config(text=text)
    
    def update_comboboxes(self, categorical_cols: List[str], numeric_cols: List[str]):
        self.dimension_combo['values'] = categorical_cols
        self.viz_dimension_combo['values'] = categorical_cols
        
        salary_candidates = ['pre_tax_salary', 'post_tax_salary', 'base_salary', 'total_salary']
        available_salary = [col for col in numeric_cols if col.lower() in [s.lower() for s in salary_candidates]]
        if not available_salary:
            available_salary = numeric_cols
        
        self.salary_combo['values'] = available_salary
        if available_salary:
            self.salary_var.set(available_salary[0])
    
    def update_overview_tree(self, data, max_rows: int = 100):
        self.overview_tree.delete(*self.overview_tree.get_children())
        
        columns = ['#'] + list(data.columns)
        self.overview_tree['columns'] = columns
        
        self.overview_tree.heading('#', text='#')
        self.overview_tree.column('#', width=50, minwidth=50)
        
        for col in data.columns:
            self.overview_tree.heading(col, text=col)
            self.overview_tree.column(col, width=120, minwidth=80)
        
        for idx, row in data.head(max_rows).iterrows():
            values = [str(idx)] + [str(v) for v in row.values]
            self.overview_tree.insert('', tk.END, values=values)
    
    def update_analysis_result(self, text: str):
        self.analysis_result_text.delete('1.0', tk.END)
        self.analysis_result_text.insert('1.0', text)
    
    def embed_chart(self, figure):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
    
    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        if msg_type == 'info':
            messagebox.showinfo(title, message)
        elif msg_type == 'warning':
            messagebox.showwarning(title, message)
        elif msg_type == 'error':
            messagebox.showerror(title, message)
    
    def _on_load_file(self):
        if self.controller:
            self.controller.load_file()
    
    def _on_load_folder(self):
        if self.controller:
            self.controller.load_folder()
    
    def _on_export_data(self):
        if self.controller:
            self.controller.export_data()
    
    def _on_export_chart(self):
        if self.controller:
            self.controller.export_chart()
    
    def _on_clean_data(self):
        if self.controller:
            self.controller.clean_data()
    
    def _on_filter_data(self):
        if self.controller:
            self.controller.filter_data()
    
    def _on_group_data(self):
        if self.controller:
            self.controller.group_data()
    
    def _on_reset_data(self):
        if self.controller:
            self.controller.reset_data()
    
    def _on_descriptive_stats(self):
        if self.controller:
            self.controller.show_descriptive_stats()
    
    def _on_frequency_analysis(self):
        if self.controller:
            self.controller.show_frequency_analysis()
    
    def _on_crosstab(self):
        if self.controller:
            self.controller.show_crosstab()
    
    def _on_correlation(self):
        if self.controller:
            self.controller.show_correlation()
    
    def _on_help(self):
        if self.controller:
            self.controller.show_help()
    
    def _on_about(self):
        if self.controller:
            self.controller.show_about()
    
    def _on_data_overview(self):
        if self.controller:
            self.controller.show_data_overview()
    
    def _on_analysis(self):
        if self.controller:
            self.controller.show_analysis()
    
    def _on_visualization(self):
        if self.controller:
            self.controller.show_visualization()
    
    def _on_execute_analysis(self):
        if self.controller:
            dimension = self.dimension_var.get()
            salary_col = self.salary_var.get()
            self.controller.execute_analysis(dimension, salary_col)
    
    def _on_generate_chart(self):
        if self.controller:
            chart_type = self.chart_type_var.get()
            dimension = self.viz_dimension_var.get()
            salary_col = self.salary_var.get()
            self.controller.generate_chart(chart_type, dimension, salary_col)
    
    def get_dimension(self) -> str:
        return self.dimension_var.get()
    
    def get_salary_column(self) -> str:
        return self.salary_var.get()
    
    def get_chart_type(self) -> str:
        return self.chart_type_var.get()
    
    def get_viz_dimension(self) -> str:
        return self.viz_dimension_var.get()
