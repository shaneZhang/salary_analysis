"""
UI组件工厂模块
统一创建UI组件
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional, Any, Dict


class UIComponentFactory:
    """UI组件工厂"""
    
    DEFAULT_BUTTON_WIDTH = 15
    DEFAULT_LABEL_WIDTH = 15
    DEFAULT_ENTRY_WIDTH = 20
    
    @staticmethod
    def create_button(parent: tk.Widget, text: str, command: Callable,
                     width: int = None, **kwargs) -> ttk.Button:
        """
        创建按钮
        
        Args:
            parent: 父组件
            text: 按钮文本
            command: 点击回调
            width: 宽度
            **kwargs: 其他参数
            
        Returns:
            按钮组件
        """
        if width is None:
            width = UIComponentFactory.DEFAULT_BUTTON_WIDTH
        
        return ttk.Button(parent, text=text, command=command, width=width, **kwargs)
    
    @staticmethod
    def create_label(parent: tk.Widget, text: str = '',
                    width: int = None, **kwargs) -> ttk.Label:
        """
        创建标签
        
        Args:
            parent: 父组件
            text: 标签文本
            width: 宽度
            **kwargs: 其他参数
            
        Returns:
            标签组件
        """
        if width is None:
            width = UIComponentFactory.DEFAULT_LABEL_WIDTH
        
        return ttk.Label(parent, text=text, width=width, **kwargs)
    
    @staticmethod
    def create_entry(parent: tk.Widget, width: int = None,
                    textvariable: tk.Variable = None, **kwargs) -> ttk.Entry:
        """
        创建输入框
        
        Args:
            parent: 父组件
            width: 宽度
            textvariable: 绑定变量
            **kwargs: 其他参数
            
        Returns:
            输入框组件
        """
        if width is None:
            width = UIComponentFactory.DEFAULT_ENTRY_WIDTH
        
        if textvariable:
            return ttk.Entry(parent, width=width, textvariable=textvariable, **kwargs)
        return ttk.Entry(parent, width=width, **kwargs)
    
    @staticmethod
    def create_combobox(parent: tk.Widget, values: List[str] = None,
                       width: int = None, textvariable: tk.Variable = None,
                       **kwargs) -> ttk.Combobox:
        """
        创建下拉框
        
        Args:
            parent: 父组件
            values: 选项列表
            width: 宽度
            textvariable: 绑定变量
            **kwargs: 其他参数
            
        Returns:
            下拉框组件
        """
        if width is None:
            width = UIComponentFactory.DEFAULT_ENTRY_WIDTH
        
        if values is None:
            values = []
        
        if textvariable:
            return ttk.Combobox(parent, values=values, width=width,
                               textvariable=textvariable, **kwargs)
        return ttk.Combobox(parent, values=values, width=width, **kwargs)
    
    @staticmethod
    def create_treeview(parent: tk.Widget, columns: List[str] = None,
                       show: str = 'headings', **kwargs) -> ttk.Treeview:
        """
        创建表格
        
        Args:
            parent: 父组件
            columns: 列名列表
            show: 显示模式
            **kwargs: 其他参数
            
        Returns:
            表格组件
        """
        if columns is None:
            columns = []
        
        return ttk.Treeview(parent, columns=columns, show=show, **kwargs)
    
    @staticmethod
    def create_text(parent: tk.Widget, width: int = None, height: int = None,
                   **kwargs) -> tk.Text:
        """
        创建文本框
        
        Args:
            parent: 父组件
            width: 宽度
            height: 高度
            **kwargs: 其他参数
            
        Returns:
            文本框组件
        """
        if width is None:
            width = 80
        if height is None:
            height = 25
        
        return tk.Text(parent, width=width, height=height, **kwargs)
    
    @staticmethod
    def create_frame(parent: tk.Widget, **kwargs) -> ttk.Frame:
        """
        创建框架
        
        Args:
            parent: 父组件
            **kwargs: 其他参数
            
        Returns:
            框架组件
        """
        return ttk.Frame(parent, **kwargs)
    
    @staticmethod
    def create_labelframe(parent: tk.Widget, text: str = '',
                         **kwargs) -> ttk.LabelFrame:
        """
        创建标签框架
        
        Args:
            parent: 父组件
            text: 标签文本
            **kwargs: 其他参数
            
        Returns:
            标签框架组件
        """
        return ttk.LabelFrame(parent, text=text, **kwargs)
    
    @staticmethod
    def create_scrollbar(parent: tk.Widget, orient: str = 'vertical',
                        command: Callable = None, **kwargs) -> ttk.Scrollbar:
        """
        创建滚动条
        
        Args:
            parent: 父组件
            orient: 方向 ('vertical' 或 'horizontal')
            command: 滚动命令
            **kwargs: 其他参数
            
        Returns:
            滚动条组件
        """
        orient_const = tk.VERTICAL if orient == 'vertical' else tk.HORIZONTAL
        return ttk.Scrollbar(parent, orient=orient_const, command=command, **kwargs)
    
    @staticmethod
    def create_menu(parent: tk.Widget, **kwargs) -> tk.Menu:
        """
        创建菜单
        
        Args:
            parent: 父组件
            **kwargs: 其他参数
            
        Returns:
            菜单组件
        """
        return tk.Menu(parent, **kwargs)
    
    @staticmethod
    def setup_treeview_columns(treeview: ttk.Treeview, 
                               columns: List[Dict[str, Any]]) -> None:
        """
        设置表格列
        
        Args:
            treeview: 表格组件
            columns: 列配置列表，每个元素包含 'name', 'text', 'width'
        """
        for col in columns:
            name = col.get('name', '')
            text = col.get('text', name)
            width = col.get('width', 100)
            
            treeview.heading(name, text=text)
            treeview.column(name, width=width, minwidth=50)
    
    @staticmethod
    def create_button_group(parent: tk.Widget, buttons: List[Dict[str, Any]],
                           orientation: str = 'vertical') -> ttk.Frame:
        """
        创建按钮组
        
        Args:
            parent: 父组件
            buttons: 按钮配置列表，每个元素包含 'text', 'command'
            orientation: 排列方向 ('vertical' 或 'horizontal')
            
        Returns:
            包含按钮的框架
        """
        frame = ttk.Frame(parent)
        
        for btn_config in buttons:
            text = btn_config.get('text', '')
            command = btn_config.get('command', None)
            width = btn_config.get('width', None)
            
            btn = UIComponentFactory.create_button(frame, text, command, width)
            
            if orientation == 'vertical':
                btn.pack(pady=5, padx=10, fill=tk.X)
            else:
                btn.pack(side=tk.LEFT, pady=5, padx=5)
        
        return frame
    
    @staticmethod
    def create_labeled_entry(parent: tk.Widget, label_text: str,
                            entry_width: int = None) -> Dict[str, tk.Widget]:
        """
        创建带标签的输入框
        
        Args:
            parent: 父组件
            label_text: 标签文本
            entry_width: 输入框宽度
            
        Returns:
            包含 'frame', 'label', 'entry' 的字典
        """
        frame = ttk.Frame(parent)
        label = UIComponentFactory.create_label(frame, label_text)
        entry = UIComponentFactory.create_entry(frame, entry_width)
        
        label.pack(side=tk.LEFT, padx=5)
        entry.pack(side=tk.LEFT, padx=5)
        
        return {'frame': frame, 'label': label, 'entry': entry}
    
    @staticmethod
    def create_labeled_combobox(parent: tk.Widget, label_text: str,
                               values: List[str] = None,
                               combo_width: int = None) -> Dict[str, tk.Widget]:
        """
        创建带标签的下拉框
        
        Args:
            parent: 父组件
            label_text: 标签文本
            values: 选项列表
            combo_width: 下拉框宽度
            
        Returns:
            包含 'frame', 'label', 'combobox' 的字典
        """
        frame = ttk.Frame(parent)
        label = UIComponentFactory.create_label(frame, label_text)
        combobox = UIComponentFactory.create_combobox(frame, values, combo_width)
        
        label.pack(side=tk.LEFT, padx=5)
        combobox.pack(side=tk.LEFT, padx=5)
        
        return {'frame': frame, 'label': label, 'combobox': combobox}
