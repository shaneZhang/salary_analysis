import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional, Any


class UIComponentFactory:
    @staticmethod
    def create_button(parent, text: str, command: Callable = None, 
                     width: int = None, **kwargs) -> ttk.Button:
        btn = ttk.Button(parent, text=text, command=command, **kwargs)
        if width:
            btn.configure(width=width)
        return btn
    
    @staticmethod
    def create_label(parent, text: str, font: tuple = None, **kwargs) -> ttk.Label:
        if font:
            return ttk.Label(parent, text=text, font=font, **kwargs)
        return ttk.Label(parent, text=text, **kwargs)
    
    @staticmethod
    def create_entry(parent, width: int = None, **kwargs) -> ttk.Entry:
        entry = ttk.Entry(parent, **kwargs)
        if width:
            entry.configure(width=width)
        return entry
    
    @staticmethod
    def create_combobox(parent, values: List[str] = None, 
                       width: int = None, **kwargs) -> ttk.Combobox:
        combo = ttk.Combobox(parent, **kwargs)
        if values:
            combo['values'] = values
        if width:
            combo.configure(width=width)
        return combo
    
    @staticmethod
    def create_treeview(parent, columns: List[str] = None, 
                       show: str = 'headings', **kwargs) -> ttk.Treeview:
        tree = ttk.Treeview(parent, show=show, **kwargs)
        if columns:
            tree['columns'] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=50)
        return tree
    
    @staticmethod
    def create_frame(parent, padding: int = 0, **kwargs) -> ttk.Frame:
        return ttk.Frame(parent, padding=padding, **kwargs)
    
    @staticmethod
    def create_labelframe(parent, text: str, padding: int = 0, **kwargs) -> ttk.LabelFrame:
        return ttk.LabelFrame(parent, text=text, padding=padding, **kwargs)
    
    @staticmethod
    def create_notebook(parent, **kwargs) -> ttk.Notebook:
        return ttk.Notebook(parent, **kwargs)
    
    @staticmethod
    def create_scrollbar(parent, orient: str = 'vertical', 
                        command: Callable = None) -> ttk.Scrollbar:
        scrollbar = ttk.Scrollbar(parent, orient=orient)
        if command:
            scrollbar.configure(command=command)
        return scrollbar
    
    @staticmethod
    def create_text(parent, height: int = 10, width: int = 50, 
                   state: str = 'normal', **kwargs) -> tk.Text:
        text = tk.Text(parent, height=height, width=width, **kwargs)
        if state != 'normal':
            text.configure(state=state)
        return text
    
    @staticmethod
    def create_menu(parent, tearoff: int = 0) -> tk.Menu:
        return tk.Menu(parent, tearoff=tearoff)
    
    @staticmethod
    def create_progressbar(parent, mode: str = 'determinate', 
                          length: int = None, **kwargs) -> ttk.Progressbar:
        pb = ttk.Progressbar(parent, mode=mode, **kwargs)
        if length:
            pb.configure(length=length)
        return pb
    
    @staticmethod
    def setup_scrollable_treeview(parent, columns: List[str], 
                                  show: str = 'headings') -> tuple:
        frame = UIComponentFactory.create_frame(parent)
        
        tree = UIComponentFactory.create_treeview(frame, columns=columns, show=show)
        
        scrollbar_y = UIComponentFactory.create_scrollbar(
            frame, orient='vertical', command=tree.yview
        )
        scrollbar_x = UIComponentFactory.create_scrollbar(
            frame, orient='horizontal', command=tree.xview
        )
        
        tree.configure(yscrollcommand=scrollbar_y.set, 
                      xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)
        
        return frame, tree
