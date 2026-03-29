"""
视图基类模块
定义视图的基类和混入
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Any
from ..models.logger import LoggerMixin


class ObserverMixin:
    """观察者混入"""
    
    def __init__(self):
        self._data_observer: Optional[Callable] = None
    
    def set_data_observer(self, observer: Callable[[Any], None]) -> None:
        """设置数据观察者"""
        self._data_observer = observer
    
    def notify_data_change(self, data: Any) -> None:
        """通知数据变更"""
        if self._data_observer:
            self._data_observer(data)


class BaseView(LoggerMixin):
    """视图基类"""
    
    def __init__(self, parent: tk.Widget, controller: Any = None):
        self.parent = parent
        self.controller = controller
        self._widget: Optional[tk.Widget] = None
    
    def get_widget(self) -> tk.Widget:
        """获取主组件"""
        return self._widget
    
    def render(self) -> None:
        """渲染视图"""
        raise NotImplementedError("Subclasses must implement render()")
    
    def destroy(self) -> None:
        """销毁视图"""
        if self._widget:
            self._widget.destroy()
    
    def show(self) -> None:
        """显示视图"""
        if self._widget:
            self._widget.pack(fill=tk.BOTH, expand=True)
    
    def hide(self) -> None:
        """隐藏视图"""
        if self._widget:
            self._widget.pack_forget()


class FrameView(BaseView):
    """Frame视图基类"""
    
    def __init__(self, parent: tk.Widget, controller: Any = None):
        super().__init__(parent, controller)
        self._widget = ttk.Frame(parent)
    
    def render(self) -> None:
        pass


class NotebookView(BaseView):
    """Notebook视图基类"""
    
    def __init__(self, parent: tk.Widget, controller: Any = None):
        super().__init__(parent, controller)
        self._widget = ttk.Notebook(parent)
        self._tabs: dict = {}
    
    def add_tab(self, tab_view: BaseView, title: str) -> None:
        """添加标签页"""
        tab_view.render()
        self._widget.add(tab_view.get_widget(), text=title)
        self._tabs[title] = tab_view
    
    def get_tab(self, title: str) -> Optional[BaseView]:
        """获取标签页"""
        return self._tabs.get(title)
    
    def select_tab(self, index: int) -> None:
        """选择标签页"""
        self._widget.select(index)
