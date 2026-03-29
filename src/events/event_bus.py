"""
事件总线模块
实现发布-订阅模式，用于模块间解耦通信
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """事件对象"""
    event_type: str
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None


class EventBus:
    """
    事件总线
    实现发布-订阅模式，支持事件的订阅、取消订阅和发布
    """
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._history: List[Event] = []
        self._max_history: int = 100
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> bool:
        """
        取消订阅事件
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
            
        Returns:
            是否成功取消订阅
        """
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            return True
        return False
    
    def publish(self, event_type: str, data: Any = None, source: Optional[str] = None) -> None:
        """
        发布事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            source: 事件来源
        """
        event = Event(
            event_type=event_type,
            data=data,
            source=source
        )
        
        self._add_to_history(event)
        
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    self._handle_handler_error(handler, event, e)
    
    def _add_to_history(self, event: Event) -> None:
        """添加事件到历史记录"""
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)
    
    def _handle_handler_error(self, handler: Callable, event: Event, error: Exception) -> None:
        """处理事件处理器错误"""
        print(f"Event handler error: {handler.__name__} for event {event.event_type}: {error}")
    
    def get_handlers(self, event_type: str) -> List[Callable]:
        """获取指定事件类型的所有处理器"""
        return self._handlers.get(event_type, []).copy()
    
    def clear_handlers(self, event_type: Optional[str] = None) -> None:
        """清除处理器"""
        if event_type:
            self._handlers.pop(event_type, None)
        else:
            self._handlers.clear()
    
    def get_history(self, event_type: Optional[str] = None) -> List[Event]:
        """获取事件历史"""
        if event_type:
            return [e for e in self._history if e.event_type == event_type]
        return self._history.copy()


EVENT_TYPES = {
    'DATA_LOADED': 'data_loaded',
    'DATA_UPDATED': 'data_updated',
    'DATA_CLEARED': 'data_cleared',
    'ANALYSIS_COMPLETED': 'analysis_completed',
    'CHART_GENERATED': 'chart_generated',
    'ERROR_OCCURRED': 'error_occurred',
    'STATUS_CHANGED': 'status_changed',
}
