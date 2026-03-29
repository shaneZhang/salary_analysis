"""视图层"""

from .base import BaseView, ObserverMixin
from .factory import UIComponentFactory
from .main_view import MainView
from .dialogs import Dialogs

__all__ = ['BaseView', 'ObserverMixin', 'UIComponentFactory', 'MainView', 'Dialogs']
