import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Any


class BaseView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self._widget = None
        self._components = {}
    
    def get_widget(self) -> tk.Widget:
        return self._widget
    
    def render(self) -> None:
        raise NotImplementedError("Subclasses must implement render()")
    
    def destroy(self) -> None:
        if self._widget:
            self._widget.destroy()
    
    def add_component(self, name: str, component: Any) -> None:
        self._components[name] = component
    
    def get_component(self, name: str) -> Optional[Any]:
        return self._components.get(name)
    
    def clear_components(self) -> None:
        self._components.clear()


class ObserverMixin:
    def __init__(self):
        self._data_observer = None
        self._state_observer = None
    
    def set_data_observer(self, observer: Callable):
        self._data_observer = observer
    
    def set_state_observer(self, observer: Callable):
        self._state_observer = observer
    
    def notify_data_change(self, data):
        if self._data_observer:
            self._data_observer(data)
    
    def notify_state_change(self, state):
        if self._state_observer:
            self._state_observer(state)
