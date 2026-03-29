"""
应用状态管理模块
管理应用的全局状态
"""

from typing import Any, Dict, Optional, Callable, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from .logger import LoggerMixin


class AppState(Enum):
    """应用状态枚举"""
    IDLE = 'idle'
    LOADING = 'loading'
    PROCESSING = 'processing'
    ANALYZING = 'analyzing'
    ERROR = 'error'


@dataclass
class StatusInfo:
    """状态信息"""
    state: AppState = AppState.IDLE
    message: str = ''
    progress: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class AppStatusManager(LoggerMixin):
    """
    应用状态管理器
    管理应用的全局状态和状态变更通知
    """
    
    def __init__(self):
        self._state: AppState = AppState.IDLE
        self._message: str = '就绪'
        self._progress: float = 0.0
        self._observers: List[Callable[[StatusInfo], None]] = []
        self._history: List[StatusInfo] = []
        self._max_history: int = 50
    
    @property
    def state(self) -> AppState:
        """获取当前状态"""
        return self._state
    
    @property
    def message(self) -> str:
        """获取当前消息"""
        return self._message
    
    @property
    def progress(self) -> float:
        """获取当前进度"""
        return self._progress
    
    def set_state(self, state: AppState, message: str = '', progress: float = 0.0) -> None:
        """
        设置状态
        
        Args:
            state: 新状态
            message: 状态消息
            progress: 进度 (0-100)
        """
        self._state = state
        self._message = message
        self._progress = max(0.0, min(100.0, progress))
        
        status_info = StatusInfo(
            state=self._state,
            message=self._message,
            progress=self._progress
        )
        
        self._add_to_history(status_info)
        self._notify_observers(status_info)
    
    def set_idle(self, message: str = '就绪') -> None:
        """设置为空闲状态"""
        self.set_state(AppState.IDLE, message, 0.0)
    
    def set_loading(self, message: str = '加载中...', progress: float = 0.0) -> None:
        """设置为加载状态"""
        self.set_state(AppState.LOADING, message, progress)
    
    def set_processing(self, message: str = '处理中...', progress: float = 0.0) -> None:
        """设置为处理状态"""
        self.set_state(AppState.PROCESSING, message, progress)
    
    def set_analyzing(self, message: str = '分析中...', progress: float = 0.0) -> None:
        """设置为分析状态"""
        self.set_state(AppState.ANALYZING, message, progress)
    
    def set_error(self, message: str = '发生错误') -> None:
        """设置为错误状态"""
        self.set_state(AppState.ERROR, message, 0.0)
    
    def subscribe(self, observer: Callable[[StatusInfo], None]) -> None:
        """订阅状态变更"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable[[StatusInfo], None]) -> bool:
        """取消订阅"""
        if observer in self._observers:
            self._observers.remove(observer)
            return True
        return False
    
    def get_status_info(self) -> StatusInfo:
        """获取当前状态信息"""
        return StatusInfo(
            state=self._state,
            message=self._message,
            progress=self._progress
        )
    
    def get_history(self, limit: int = 10) -> List[StatusInfo]:
        """获取状态历史"""
        return self._history[-limit:]
    
    def is_busy(self) -> bool:
        """检查是否处于忙碌状态"""
        return self._state in (AppState.LOADING, AppState.PROCESSING, AppState.ANALYZING)
    
    def _add_to_history(self, status_info: StatusInfo) -> None:
        """添加到历史记录"""
        self._history.append(status_info)
        if len(self._history) > self._max_history:
            self._history.pop(0)
    
    def _notify_observers(self, status_info: StatusInfo) -> None:
        """通知观察者"""
        for observer in self._observers:
            try:
                observer(status_info)
            except Exception as e:
                self.logger.error(f"Status observer error: {e}")


class SelectionManager:
    """选择状态管理器"""
    
    def __init__(self):
        self._dimension: str = ''
        self._salary_column: str = 'pre_tax_salary'
        self._chart_type: str = 'bar'
        self._filters: Dict[str, Any] = {}
    
    @property
    def dimension(self) -> str:
        return self._dimension
    
    @dimension.setter
    def dimension(self, value: str) -> None:
        self._dimension = value
    
    @property
    def salary_column(self) -> str:
        return self._salary_column
    
    @salary_column.setter
    def salary_column(self, value: str) -> None:
        self._salary_column = value
    
    @property
    def chart_type(self) -> str:
        return self._chart_type
    
    @chart_type.setter
    def chart_type(self, value: str) -> None:
        self._chart_type = value
    
    def set_filter(self, column: str, value: Any) -> None:
        """设置筛选条件"""
        self._filters[column] = value
    
    def remove_filter(self, column: str) -> None:
        """移除筛选条件"""
        self._filters.pop(column, None)
    
    def clear_filters(self) -> None:
        """清除所有筛选条件"""
        self._filters.clear()
    
    def get_filters(self) -> Dict[str, Any]:
        """获取所有筛选条件"""
        return self._filters.copy()
    
    def reset(self) -> None:
        """重置所有选择"""
        self._dimension = ''
        self._salary_column = 'pre_tax_salary'
        self._chart_type = 'bar'
        self._filters.clear()
