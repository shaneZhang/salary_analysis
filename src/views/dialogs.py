"""
对话框模块
定义各种对话框
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable, List, Dict, Any


class Dialogs:
    """对话框工具类"""
    
    @staticmethod
    def show_info(title: str, message: str) -> None:
        """显示信息对话框"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(title: str, message: str) -> None:
        """显示警告对话框"""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_error(title: str, message: str) -> None:
        """显示错误对话框"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def ask_yes_no(title: str, message: str) -> bool:
        """显示是/否对话框"""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def ask_ok_cancel(title: str, message: str) -> bool:
        """显示确定/取消对话框"""
        return messagebox.askokcancel(title, message)
    
    @staticmethod
    def select_file(title: str = '选择文件',
                   filetypes: List[tuple] = None) -> Optional[str]:
        """
        选择文件
        
        Args:
            title: 对话框标题
            filetypes: 文件类型过滤器
            
        Returns:
            选择的文件路径
        """
        if filetypes is None:
            filetypes = [('Excel文件', '*.xlsx *.xls'), ('所有文件', '*.*')]
        
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )
        
        return file_path if file_path else None
    
    @staticmethod
    def select_folder(title: str = '选择文件夹') -> Optional[str]:
        """
        选择文件夹
        
        Args:
            title: 对话框标题
            
        Returns:
            选择的文件夹路径
        """
        root = tk.Tk()
        root.withdraw()
        
        folder_path = filedialog.askdirectory(title=title)
        
        return folder_path if folder_path else None
    
    @staticmethod
    def save_file(title: str = '保存文件',
                 defaultextension: str = '.xlsx',
                 filetypes: List[tuple] = None) -> Optional[str]:
        """
        保存文件对话框
        
        Args:
            title: 对话框标题
            defaultextension: 默认扩展名
            filetypes: 文件类型过滤器
            
        Returns:
            保存路径
        """
        if filetypes is None:
            filetypes = [('Excel文件', '*.xlsx'), ('CSV文件', '*.csv'), ('所有文件', '*.*')]
        
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        
        return file_path if file_path else None


class DataCleanDialog:
    """数据清洗对话框"""
    
    def __init__(self, parent: tk.Widget, on_clean: Callable[[str], None]):
        self.parent = parent
        self.on_clean = on_clean
        self.dialog: Optional[tk.Toplevel] = None
    
    def show(self) -> None:
        """显示对话框"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title('数据清洗')
        self.dialog.geometry('400x300')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text='选择清洗操作:', font=('Arial', 12)).pack(pady=10)
        
        operations = [
            ('删除重复数据', 'duplicates'),
            ('删除缺失值行', 'missing'),
            ('填充缺失值(均值)', 'fill_mean'),
            ('移除异常值', 'outliers')
        ]
        
        for text, operation in operations:
            btn = ttk.Button(
                self.dialog,
                text=text,
                command=lambda op=operation: self._execute(op)
            )
            btn.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(self.dialog, text='取消', command=self._close).pack(pady=20)
    
    def _execute(self, operation: str) -> None:
        """执行清洗操作"""
        self._close()
        if self.on_clean:
            self.on_clean(operation)
    
    def _close(self) -> None:
        """关闭对话框"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None


class DataGroupDialog:
    """数据分组对话框"""
    
    def __init__(self, parent: tk.Widget, on_group: Callable[[str], None],
                 available_columns: List[str] = None):
        self.parent = parent
        self.on_group = on_group
        self.available_columns = available_columns or []
        self.dialog: Optional[tk.Toplevel] = None
    
    def show(self) -> None:
        """显示对话框"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title('数据分组')
        self.dialog.geometry('400x250')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text='选择分组操作:', font=('Arial', 12)).pack(pady=10)
        
        operations = [
            ('年龄分组', 'age'),
            ('薪资分组', 'salary'),
            ('工作年限分组', 'experience')
        ]
        
        for text, operation in operations:
            btn = ttk.Button(
                self.dialog,
                text=text,
                command=lambda op=operation: self._execute(op)
            )
            btn.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(self.dialog, text='取消', command=self._close).pack(pady=20)
    
    def _execute(self, operation: str) -> None:
        """执行分组操作"""
        self._close()
        if self.on_group:
            self.on_group(operation)
    
    def _close(self) -> None:
        """关闭对话框"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None


class AboutDialog:
    """关于对话框"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
    
    def show(self) -> None:
        """显示对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title('关于')
        dialog.geometry('400x300')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        info_text = """
园区白领薪资数据分析工具
版本: 2.0.0

功能特点:
• 数据导入与导出
• 数据清洗与处理
• 统计分析
• 数据可视化

技术栈:
Python + Pandas + Matplotlib + Tkinter

架构模式:
MVC + 服务层架构
        """
        
        text = tk.Text(dialog, wrap=tk.WORD, padx=20, pady=20)
        text.insert('1.0', info_text)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(dialog, text='确定', command=dialog.destroy).pack(pady=10)


class HelpDialog:
    """帮助对话框"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
    
    def show(self) -> None:
        """显示对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title('使用说明')
        dialog.geometry('500x400')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        help_text = """
使用说明

1. 数据导入
   • 点击"数据导入"按钮或菜单"文件 > 打开Excel文件"
   • 支持单个文件、多个文件或整个文件夹导入

2. 数据概览
   • 导入数据后自动显示数据概览
   • 可查看数据的基本信息和字段列表

3. 数据清洗
   • 删除重复数据
   • 处理缺失值（删除或填充）
   • 移除异常值

4. 数据分组
   • 年龄分组：将年龄划分为不同区间
   • 薪资分组：将薪资划分为不同区间
   • 工作年限分组：将工作年限划分为不同区间

5. 统计分析
   • 描述性统计：查看数值字段的基本统计信息
   • 频率分析：查看分类字段的频率分布
   • 交叉分析：查看两个字段的交叉分布
   • 相关性分析：查看数值字段之间的相关性

6. 数据可视化
   • 柱状图：对比不同类别的数值
   • 折线图：展示趋势变化
   • 饼图：展示比例分布
   • 散点图：展示两个变量的关系
   • 箱线图：展示数据分布
   • 直方图：展示数值分布

7. 数据导出
   • 支持导出为Excel或CSV格式
   • 图表可保存为PNG格式
        """
        
        text_frame = ttk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.insert('1.0', help_text)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text.yview)
        
        ttk.Button(dialog, text='确定', command=dialog.destroy).pack(pady=10)
