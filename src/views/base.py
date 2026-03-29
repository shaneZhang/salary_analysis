import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Any, Dict, List
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.models import Logger


class BaseView:
    """视图基类
    
    所有UI视图组件的基类，提供基本的UI组件管理功能。
    """
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self._widget: Optional[tk.Widget] = None
        self._children: Dict[str, 'BaseView'] = {}
        self._logger = Logger()
    
    def get_widget(self) -> Optional[tk.Widget]:
        """获取当前视图的根组件"""
        return self._widget
    
    def render(self) -> None:
        """渲染视图"""
        raise NotImplementedError("子类必须实现 render 方法")
    
    def destroy(self) -> None:
        """销毁视图"""
        if self._widget:
            self._widget.destroy()
            self._widget = None
    
    def show_message(self, message: str, title: str = "提示", msg_type: str = "info") -> None:
        """显示消息对话框"""
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "question":
            return messagebox.askquestion(title, message)
        elif msg_type == "yesno":
            return messagebox.askyesno(title, message)
    
    def show_error(self, message: str, title: str = "错误") -> None:
        """显示错误对话框"""
        self.show_message(message, title, "error")
    
    def show_warning(self, message: str, title: str = "警告") -> None:
        """显示警告对话框"""
        self.show_message(message, title, "warning")
    
    def show_info(self, message: str, title: str = "提示") -> None:
        """显示信息对话框"""
        self.show_message(message, title, "info")


class ObserverMixin:
    """观察者混入类
    
    提供数据变化观察功能。
    """
    
    def __init__(self):
        self._data_observer: Optional[Callable] = None
        self._observer_registered = False
    
    def set_data_observer(self, observer: Callable[[Any], None]) -> None:
        """设置数据变化观察者"""
        self._data_observer = observer
    
    def on_data_changed(self, data: Any) -> None:
        """数据变化回调"""
        if self._data_observer:
            self._data_observer(data)


class DataDrivenView(BaseView, ObserverMixin):
    """数据驱动视图基类
    
    支持数据变化自动更新的视图基类。
    """
    
    def __init__(self, parent, controller):
        BaseView.__init__(self, parent, controller)
        ObserverMixin.__init__(self)
        self._current_data = None
    
    def update_data(self, data: Any) -> None:
        """更新数据"""
        self._current_data = data
        self.on_data_changed(data)
    
    def get_current_data(self) -> Any:
        """获取当前数据"""
        return self._current_data


class FigureView:
    """Matplotlib图表视图
    
    提供Matplotlib图表嵌入Tkinter的功能。
    """
    
    def __init__(self, parent):
        self.parent = parent
        self._canvas: Optional[FigureCanvasTkAgg] = None
        self._toolbar: Optional[NavigationToolbar2Tk] = None
        self._frame: Optional[ttk.Frame] = None
    
    def embed_figure(self, figure: Figure, toolbar: bool = True) -> ttk.Frame:
        """将图表嵌入到Tkinter容器中"""
        if self._frame:
            self._frame.destroy()
        
        self._frame = ttk.Frame(self.parent)
        self._frame.pack(fill=tk.BOTH, expand=True)
        
        self._canvas = FigureCanvasTkAgg(figure, master=self._frame)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        if toolbar:
            self._toolbar = NavigationToolbar2Tk(self._canvas, self._frame)
            self._toolbar.update()
        
        return self._frame
    
    def clear(self) -> None:
        """清除当前图表"""
        if self._canvas:
            self._canvas.get_tk_widget().destroy()
            self._canvas = None
        if self._toolbar:
            self._toolbar.destroy()
            self._toolbar = None
        if self._frame:
            for widget in self._frame.winfo_children():
                widget.destroy()
    
    def refresh(self) -> None:
        """刷新图表"""
        if self._canvas:
            self._canvas.draw()


class FormView(BaseView):
    """表单视图基类
    
    提供表单输入组件的管理功能。
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._fields: Dict[str, tk.Widget] = {}
        self._variables: Dict[str, tk.Variable] = {}
    
    def add_field(self, name: str, widget: tk.Widget, variable: Optional[tk.Variable] = None) -> None:
        """添加表单字段"""
        self._fields[name] = widget
        if variable:
            self._variables[name] = variable
    
    def get_field_value(self, name: str) -> Any:
        """获取字段值"""
        if name in self._variables:
            return self._variables[name].get()
        return None
    
    def set_field_value(self, name: str, value: Any) -> None:
        """设置字段值"""
        if name in self._variables:
            self._variables[name].set(value)
    
    def get_form_data(self) -> Dict[str, Any]:
        """获取所有表单数据"""
        return {name: var.get() for name, var in self._variables.items()}
    
    def set_form_data(self, data: Dict[str, Any]) -> None:
        """设置表单数据"""
        for name, value in data.items():
            self.set_field_value(name, value)
    
    def clear_form(self) -> None:
        """清空表单"""
        for var in self._variables.values():
            if isinstance(var, tk.StringVar):
                var.set("")
            elif isinstance(var, tk.IntVar):
                var.set(0)
            elif isinstance(var, tk.DoubleVar):
                var.set(0.0)
            elif isinstance(var, tk.BooleanVar):
                var.set(False)
    
    def validate_form(self) -> bool:
        """验证表单数据
        
        子类可以重写此方法实现具体的验证逻辑
        """
        return True


class DialogView(BaseView):
    """对话框基类
    
    模态对话框的基类。
    """
    
    def __init__(self, parent, controller, title: str = "对话框"):
        super().__init__(parent, controller)
        self._dialog = tk.Toplevel(parent)
        self._dialog.title(title)
        self._dialog.transient(parent)
        self._dialog.grab_set()
        self._result = None
        self._widget = self._dialog
    
    def set_modal(self, modal: bool = True) -> None:
        """设置是否为模态对话框"""
        if modal:
            self._dialog.grab_set()
        else:
            self._dialog.grab_release()
    
    def set_size(self, width: int, height: int) -> None:
        """设置对话框大小"""
        self._dialog.geometry(f"{width}x{height}")
    
    def center(self) -> None:
        """将对话框居中显示"""
        self._dialog.update_idletasks()
        x = (self._dialog.winfo_screenwidth() // 2) - (self._dialog.winfo_width() // 2)
        y = (self._dialog.winfo_screenheight() // 2) - (self._dialog.winfo_height() // 2)
        self._dialog.geometry(f"+{x}+{y}")
    
    def show(self) -> Any:
        """显示对话框并等待结果"""
        self.render()
        self.center()
        self._dialog.wait_window()
        return self._result
    
    def close(self, result: Any = None) -> None:
        """关闭对话框"""
        self._result = result
        self._dialog.destroy()
    
    def add_button(self, text: str, command: Callable, side: str = tk.RIGHT, padx: int = 5, pady: int = 5) -> ttk.Button:
        """添加按钮"""
        btn = ttk.Button(self._button_frame, text=text, command=command)
        btn.pack(side=side, padx=padx, pady=pady)
        return btn
    
    def render(self) -> None:
        """渲染对话框"""
        self._content_frame = ttk.Frame(self._dialog, padding="10")
        self._content_frame.pack(fill=tk.BOTH, expand=True)
        
        self._button_frame = ttk.Frame(self._dialog, padding="5")
        self._button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self._create_content(self._content_frame)
        self._create_buttons(self._button_frame)
    
    def _create_content(self, parent) -> None:
        """创建对话框内容
        
        子类应该重写此方法
        """
        pass
    
    def _create_buttons(self, parent) -> None:
        """创建对话框按钮
        
        子类可以重写此方法
        """
        self.add_button("确定", command=lambda: self.close(True))
        self.add_button("取消", command=lambda: self.close(False))
