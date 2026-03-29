import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Any, Optional, Dict


class UIComponentFactory:
    """UI组件工厂
    
    提供统一的UI组件创建方法，确保UI风格的一致性。
    """
    
    @staticmethod
    def create_button(parent, text: str, command: Callable, **kwargs) -> ttk.Button:
        """创建按钮"""
        default_style = {'width': 20}
        default_style.update(kwargs)
        return ttk.Button(parent, text=text, command=command, **default_style)
    
    @staticmethod
    def create_label(parent, text: str, **kwargs) -> ttk.Label:
        """创建标签"""
        return ttk.Label(parent, text=text, **kwargs)
    
    @staticmethod
    def create_entry(parent, **kwargs) -> ttk.Entry:
        """创建输入框"""
        return ttk.Entry(parent, **kwargs)
    
    @staticmethod
    def create_combobox(parent, values: List[str], **kwargs) -> ttk.Combobox:
        """创建下拉选择框"""
        return ttk.Combobox(parent, values=values, **kwargs)
    
    @staticmethod
    def create_treeview(parent, columns: List[str], show: str = 'headings', **kwargs) -> ttk.Treeview:
        """创建树形表格"""
        tree = ttk.Treeview(parent, columns=columns, show=show, **kwargs)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, minwidth=80)
        
        return tree
    
    @staticmethod
    def create_text(parent, height: int = 10, width: int = 50, **kwargs) -> tk.Text:
        """创建文本框"""
        return tk.Text(parent, height=height, width=width, **kwargs)
    
    @staticmethod
    def create_scrollbar(parent, orient: str = tk.VERTICAL, **kwargs) -> ttk.Scrollbar:
        """创建滚动条"""
        return ttk.Scrollbar(parent, orient=orient, **kwargs)
    
    @staticmethod
    def create_labelframe(parent, text: str, padding: int = 10, **kwargs) -> ttk.LabelFrame:
        """创建带标签的框架"""
        return ttk.LabelFrame(parent, text=text, padding=padding, **kwargs)
    
    @staticmethod
    def create_notebook(parent, **kwargs) -> ttk.Notebook:
        """创建标签页"""
        return ttk.Notebook(parent, **kwargs)
    
    @staticmethod
    def create_frame(parent, **kwargs) -> ttk.Frame:
        """创建框架"""
        return ttk.Frame(parent, **kwargs)
    
    @staticmethod
    def create_separator(parent, orient: str = tk.HORIZONTAL, **kwargs) -> ttk.Separator:
        """创建分隔线"""
        return ttk.Separator(parent, orient=orient, **kwargs)
    
    @staticmethod
    def create_progressbar(parent, mode: str = 'determinate', **kwargs) -> ttk.Progressbar:
        """创建进度条"""
        return ttk.Progressbar(parent, mode=mode, **kwargs)
    
    @staticmethod
    def create_checkbutton(parent, text: str, variable: tk.Variable = None, **kwargs) -> ttk.Checkbutton:
        """创建复选框"""
        return ttk.Checkbutton(parent, text=text, variable=variable, **kwargs)
    
    @staticmethod
    def create_radiobutton(parent, text: str, variable: tk.Variable = None, value: Any = None, **kwargs) -> ttk.Radiobutton:
        """创建单选按钮"""
        return ttk.Radiobutton(parent, text=text, variable=variable, value=value, **kwargs)
    
    @staticmethod
    def create_spinbox(parent, from_: int = 0, to: int = 100, **kwargs) -> ttk.Spinbox:
        """创建数字选择框"""
        return ttk.Spinbox(parent, from_=from_, to=to, **kwargs)
    
    @staticmethod
    def create_menu(parent, tearoff: int = 0, **kwargs) -> tk.Menu:
        """创建菜单"""
        return tk.Menu(parent, tearoff=tearoff, **kwargs)
    
    @staticmethod
    def create_menubutton(parent, text: str, menu: tk.Menu = None, **kwargs) -> ttk.Menubutton:
        """创建菜单按钮"""
        btn = ttk.Menubutton(parent, text=text, **kwargs)
        if menu:
            btn.config(menu=menu)
        return btn
    
    @staticmethod
    def create_sizegrip(parent, **kwargs) -> ttk.Sizegrip:
        """创建大小调整手柄"""
        return ttk.Sizegrip(parent, **kwargs)


class StyledWidget:
    """样式化组件混合类
    
    提供统一的样式配置
    """
    
    STYLES = {
        'title_font': ('Arial', 14, 'bold'),
        'heading_font': ('Arial', 12, 'bold'),
        'normal_font': ('Arial', 10),
        'small_font': ('Arial', 9),
        'mono_font': ('Courier', 10),
        'colors': {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#1abc9c',
            'bg': '#f5f5f5',
            'fg': '#333333'
        }
    }
    
    @classmethod
    def get_style(cls, style_name: str) -> Any:
        """获取样式配置"""
        return cls.STYLES.get(style_name, {})
