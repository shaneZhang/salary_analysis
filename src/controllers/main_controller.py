"""
主控制器模块
协调所有子控制器，管理应用生命周期
"""

import tkinter as tk
from typing import Optional
from ..services.data_service import DataService
from ..services.processing_service import ProcessingService
from ..services.analysis_service import AnalysisService
from ..services.visualization_service import VisualizationService
from ..models.data_manager import DataManager
from ..models.config_manager import ConfigManager
from ..models.app_state import AppStatusManager, SelectionManager
from ..events.event_bus import EventBus
from ..views.main_view import MainView
from .data_controller import DataController
from .analysis_controller import AnalysisController
from ..models.logger import LoggerMixin


class MainController(LoggerMixin):
    """主控制器"""
    
    def __init__(self, root: tk.Tk, config: Optional[ConfigManager] = None):
        self.root = root
        self._config = config or ConfigManager()
        
        self._event_bus = EventBus()
        self._data_manager = DataManager(event_bus=self._event_bus)
        self._status_manager = AppStatusManager()
        self._selection_manager = SelectionManager()
        
        self._setup_services()
        self._setup_controllers()
        self._setup_view()
        self._setup_event_handlers()
    
    def _setup_services(self) -> None:
        """设置服务层"""
        self._data_service = DataService(
            self._data_manager, self._config, self._event_bus
        )
        self._processing_service = ProcessingService(
            self._data_manager, self._config, self._event_bus
        )
        self._analysis_service = AnalysisService(
            self._data_manager, self._config, self._event_bus
        )
        self._visualization_service = VisualizationService(
            self._data_manager, self._config, self._event_bus
        )
    
    def _setup_controllers(self) -> None:
        """设置控制器"""
        self._data_controller = DataController(
            self._data_service, self._processing_service,
            self._data_manager, self._status_manager
        )
        self._analysis_controller = AnalysisController(
            self._analysis_service, self._visualization_service,
            self._data_manager, self._status_manager
        )
    
    def _setup_view(self) -> None:
        """设置视图"""
        app_config = self._config.get_app_config()
        self.root.title(app_config.app_title)
        
        window_size = app_config.window_size
        self.root.geometry(f'{window_size[0]}x{window_size[1]}')
        
        self._view = MainView(self.root, self)
        
        self._data_controller.set_view(self._view)
        self._analysis_controller.set_view(self._view)
    
    def _setup_event_handlers(self) -> None:
        """设置事件处理"""
        self._status_manager.subscribe(self._on_status_change)
    
    def _on_status_change(self, status_info) -> None:
        """状态变更处理"""
        if self._view:
            self._view.set_status(status_info.message)
    
    def load_file(self) -> None:
        """加载文件"""
        self._data_controller.load_file()
    
    def load_folder(self) -> None:
        """加载文件夹"""
        self._data_controller.load_folder()
    
    def export_data(self) -> None:
        """导出数据"""
        self._data_controller.export_data()
    
    def export_chart(self) -> None:
        """导出图表"""
        self._analysis_controller.export_chart()
    
    def clean_data(self) -> None:
        """数据清洗"""
        self._data_controller.clean_data()
    
    def group_data(self) -> None:
        """数据分组"""
        self._data_controller.group_data()
    
    def reset_data(self) -> None:
        """重置数据"""
        self._data_controller.reset_data()
    
    def show_descriptive_stats(self) -> None:
        """显示描述性统计"""
        self._analysis_controller.show_descriptive_stats()
    
    def show_frequency_analysis(self) -> None:
        """显示频率分析"""
        self._analysis_controller.show_frequency_analysis()
    
    def show_crosstab(self) -> None:
        """显示交叉分析"""
        self._analysis_controller.show_crosstab()
    
    def show_correlation(self) -> None:
        """显示相关性分析"""
        self._analysis_controller.show_correlation()
    
    def show_data_overview(self) -> None:
        """显示数据概览"""
        self._analysis_controller.show_data_overview()
    
    def execute_analysis(self) -> None:
        """执行分析"""
        self._analysis_controller.execute_analysis()
    
    def generate_chart(self) -> None:
        """生成图表"""
        self._analysis_controller.generate_chart()
    
    def run(self) -> None:
        """运行应用"""
        self.logger.info("Application started")
        self.root.mainloop()
