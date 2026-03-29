import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Any, TYPE_CHECKING

from src.views.base import DialogView, FormView
from src.views.factory import UIComponentFactory, StyledWidget

if TYPE_CHECKING:
    from src.controllers import MainController


class CleanDialog(DialogView):
    """数据清洗对话框"""
    
    def __init__(self, parent, controller: 'MainController'):
        super().__init__(parent, controller, title="数据清洗")
        self.set_size(400, 300)
    
    def _create_content(self, parent) -> None:
        """创建对话框内容"""
        label = UIComponentFactory.create_label(
            parent, text="选择清洗操作:",
            font=StyledWidget.STYLES['heading_font']
        )
        label.pack(pady=10)
        
        # 清洗操作按钮
        operations = [
            ('删除重复数据', self._remove_duplicates),
            ('删除缺失值行', self._remove_missing),
            ('填充缺失值(均值)', self._fill_mean),
            ('移除异常值', self._remove_outliers),
        ]
        
        for text, command in operations:
            btn = UIComponentFactory.create_button(parent, text=text, command=command, width=30)
            btn.pack(fill=tk.X, padx=20, pady=5)
    
    def _create_buttons(self, parent) -> None:
        """创建对话框按钮"""
        self.add_button("关闭", command=lambda: self.close(None), side=tk.RIGHT)
    
    def _remove_duplicates(self) -> None:
        """删除重复数据"""
        count = self.controller.clean_duplicates()
        self.close(True)
        if count > 0:
            self.show_info(f"删除了 {count} 条重复记录", "完成")
        else:
            self.show_info("没有发现重复数据", "完成")
    
    def _remove_missing(self) -> None:
        """删除缺失值行"""
        result = self.controller.clean_missing_values('drop')
        self.close(True)
        total = sum(result.values())
        if total > 0:
            self.show_info(f"删除了 {total} 条含缺失值记录", "完成")
        else:
            self.show_info("没有发现缺失值", "完成")
    
    def _fill_mean(self) -> None:
        """用均值填充缺失值"""
        result = self.controller.clean_missing_values('fill_mean')
        self.close(True)
        total = sum(result.values())
        if total > 0:
            self.show_info(f"已填充 {total} 个缺失值", "完成")
        else:
            self.show_info("没有发现缺失值", "完成")
    
    def _remove_outliers(self) -> None:
        """移除异常值"""
        salary_cols = self.controller.get_salary_columns()
        salary_col = salary_cols[0] if salary_cols else None
        
        if salary_col:
            count = self.controller.clean_outliers(salary_col)
            self.close(True)
            if count > 0:
                self.show_info(f"移除了 {count} 条异常值记录", "完成")
            else:
                self.show_info("没有发现异常值", "完成")
        else:
            self.show_warning("没有找到合适的薪资列", "警告")


class GroupDialog(DialogView):
    """数据分组对话框"""
    
    def __init__(self, parent, controller: 'MainController'):
        super().__init__(parent, controller, title="数据分组")
        self.set_size(400, 250)
    
    def _create_content(self, parent) -> None:
        """创建对话框内容"""
        label = UIComponentFactory.create_label(
            parent, text="选择分组操作:",
            font=StyledWidget.STYLES['heading_font']
        )
        label.pack(pady=10)
        
        # 分组操作按钮
        operations = [
            ('年龄分组', self._create_age_group),
            ('薪资分组', self._create_salary_group),
            ('工作年限分组', self._create_experience_group),
        ]
        
        for text, command in operations:
            btn = UIComponentFactory.create_button(parent, text=text, command=command, width=30)
            btn.pack(fill=tk.X, padx=20, pady=5)
    
    def _create_buttons(self, parent) -> None:
        """创建对话框按钮"""
        self.add_button("关闭", command=lambda: self.close(None), side=tk.RIGHT)
    
    def _create_age_group(self) -> None:
        """创建年龄分组"""
        result = self.controller.create_age_group()
        self.close(True)
        if result:
            self.show_info("已创建年龄分组字段: age_group", "完成")
        else:
            self.show_warning("数据中没有年龄字段或分组失败", "警告")
    
    def _create_salary_group(self) -> None:
        """创建薪资分组"""
        salary_cols = self.controller.get_salary_columns()
        salary_col = salary_cols[0] if salary_cols else None
        
        if salary_col:
            result = self.controller.create_salary_group(salary_col)
            self.close(True)
            if result:
                self.show_info("已创建薪资分组字段: salary_group", "完成")
            else:
                self.show_warning("薪资分组失败", "警告")
        else:
            self.show_warning("没有找到合适的薪资列", "警告")
    
    def _create_experience_group(self) -> None:
        """创建工作年限分组"""
        result = self.controller.create_experience_group()
        self.close(True)
        if result:
            self.show_info("已创建工作年限分组字段: experience_group", "完成")
        else:
            self.show_warning("数据中没有工作年限字段或分组失败", "警告")


class FilterDialog(FormView):
    """数据筛选对话框"""
    
    def __init__(self, parent, controller: 'MainController'):
        super().__init__(parent, controller)
        self._dialog = tk.Toplevel(parent)
        self._dialog.title("数据筛选")
        self._dialog.geometry("500x400")
        self._dialog.transient(parent)
        self._dialog.grab_set()
    
    def render(self) -> None:
        """渲染对话框"""
        # 筛选条件框架
        filter_frame = UIComponentFactory.create_labelframe(self._dialog, text="筛选条件", padding=10)
        filter_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 动态添加筛选条件行
        self._add_filter_row(filter_frame, 0)
        
        # 按钮框架
        button_frame = UIComponentFactory.create_frame(self._dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        UIComponentFactory.create_button(button_frame, text="添加条件", command=self._add_condition, width=10).pack(side=tk.LEFT, padx=5)
        UIComponentFactory.create_button(button_frame, text="应用筛选", command=self._apply_filter, width=10).pack(side=tk.RIGHT, padx=5)
        UIComponentFactory.create_button(button_frame, text="取消", command=self._dialog.destroy, width=10).pack(side=tk.RIGHT, padx=5)
    
    def _add_filter_row(self, parent, row: int) -> None:
        """添加筛选条件行"""
        columns = self.controller.get_current_data().columns.tolist() if self.controller.has_data() else []
        
        column_var = tk.StringVar()
        operator_var = tk.StringVar(value="=")
        value_var = tk.StringVar()
        
        UIComponentFactory.create_combobox(parent, values=columns, textvariable=column_var, width=15).grid(row=row, column=0, padx=5, pady=5)
        UIComponentFactory.create_combobox(parent, values=['=', '!=', '>', '<', '>=', '<=', 'contains'], textvariable=operator_var, width=10).grid(row=row, column=1, padx=5, pady=5)
        UIComponentFactory.create_entry(parent, textvariable=value_var, width=20).grid(row=row, column=2, padx=5, pady=5)
        
        # 保存变量
        if not hasattr(self, '_filter_vars'):
            self._filter_vars = []
        self._filter_vars.append((column_var, operator_var, value_var))
    
    def _add_condition(self) -> None:
        """添加筛选条件"""
        if hasattr(self, '_filter_vars'):
            self._add_filter_row(self._dialog.winfo_children()[0], len(self._filter_vars))
    
    def _apply_filter(self) -> None:
        """应用筛选"""
        # TODO: 实现筛选逻辑
        self.show_info("数据筛选功能开发中...")
        self._dialog.destroy()


class AnalysisDialog(DialogView):
    """高级分析对话框"""
    
    def __init__(self, parent, controller: 'MainController'):
        super().__init__(parent, controller, title="高级分析")
        self.set_size(600, 500)
        self._result_text: Optional[tk.Text] = None
    
    def _create_content(self, parent) -> None:
        """创建对话框内容"""
        # 分析类型选择
        type_frame = UIComponentFactory.create_labelframe(parent, text="分析类型", padding=10)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self._analysis_type = tk.StringVar(value="descriptive")
        
        analysis_types = [
            ("描述性统计", "descriptive"),
            ("频率分析", "frequency"),
            ("交叉分析", "crosstab"),
            ("相关性分析", "correlation"),
        ]
        
        for text, value in analysis_types:
            UIComponentFactory.create_radiobutton(
                type_frame, text=text, variable=self._analysis_type, value=value
            ).pack(anchor=tk.W, padx=5, pady=2)
        
        # 列选择
        column_frame = UIComponentFactory.create_labelframe(parent, text="选择列", padding=10)
        column_frame.pack(fill=tk.X, padx=10, pady=5)
        
        UIComponentFactory.create_label(column_frame, text="维度列:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        dimensions = self.controller.get_available_dimensions()
        self._dimension_var = tk.StringVar()
        UIComponentFactory.create_combobox(
            column_frame, values=dimensions, textvariable=self._dimension_var, width=20
        ).grid(row=0, column=1, padx=5, pady=5)
        
        UIComponentFactory.create_label(column_frame, text="值列:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        salary_cols = self.controller.get_salary_columns()
        self._value_var = tk.StringVar(value=salary_cols[0] if salary_cols else "")
        UIComponentFactory.create_combobox(
            column_frame, values=salary_cols, textvariable=self._value_var, width=20
        ).grid(row=1, column=1, padx=5, pady=5)
        
        # 结果显示
        result_frame = UIComponentFactory.create_labelframe(parent, text="分析结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self._result_text = UIComponentFactory.create_text(result_frame, height=15)
        scrollbar = UIComponentFactory.create_scrollbar(result_frame, orient=tk.VERTICAL, command=self._result_text.yview)
        self._result_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._result_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    
    def _create_buttons(self, parent) -> None:
        """创建对话框按钮"""
        self.add_button("执行分析", command=self._execute_analysis, side=tk.LEFT)
        self.add_button("关闭", command=lambda: self.close(None), side=tk.RIGHT)
    
    def _execute_analysis(self) -> None:
        """执行分析"""
        analysis_type = self._analysis_type.get()
        dimension = self._dimension_var.get()
        value_col = self._value_var.get()
        
        result = ""
        
        if analysis_type == "descriptive":
            stats = self.controller.get_descriptive_stats(value_col)
            result = f'描述性统计: {value_col}\n{"="*40}\n\n'
            for key, value in stats.items():
                if value is not None:
                    if isinstance(value, float):
                        result += f'{key}: {value:,.2f}\n'
                    else:
                        result += f'{key}: {value}\n'
        
        elif analysis_type == "frequency":
            freq = self.controller.get_frequency_analysis(dimension)
            result = f'频率分析: {dimension}\n{"="*40}\n\n'
            result += freq.to_string(index=False)
        
        elif analysis_type == "crosstab":
            crosstab = self.controller.get_crosstab(dimension, value_col)
            result = f'交叉分析: {dimension} x {value_col}\n{"="*40}\n\n'
            result += crosstab.to_string()
        
        elif analysis_type == "correlation":
            corr = self.controller.get_correlation_matrix()
            result = f'相关性矩阵\n{"="*40}\n\n'
            result += corr.to_string()
        
        if self._result_text:
            self._result_text.delete('1.0', tk.END)
            self._result_text.insert('1.0', result)
