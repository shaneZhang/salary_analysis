"""
数据管理器模块
统一管理应用数据，提供数据变更通知机制
"""

import pandas as pd
from typing import Optional, Callable, List, Dict, Any
from .logger import get_logger, LoggerMixin
from ..events.event_bus import EventBus, EVENT_TYPES


class DataManager(LoggerMixin):
    """
    数据管理器
    统一管理应用数据，实现观察者模式
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        self._data: Optional[pd.DataFrame] = None
        self._original_data: Optional[pd.DataFrame] = None
        self._observers: List[Callable[[pd.DataFrame], None]] = []
        self._event_bus = event_bus
        self._metadata: Dict[str, Any] = {}
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """获取当前数据"""
        return self._data
    
    def set_data(self, data: pd.DataFrame, notify: bool = True) -> None:
        """
        设置数据
        
        Args:
            data: 数据框
            notify: 是否通知观察者
        """
        self._data = data.copy() if data is not None else None
        
        if self._original_data is None:
            self._original_data = data.copy() if data is not None else None
        
        if notify:
            self._notify_observers()
            self._publish_event(EVENT_TYPES['DATA_LOADED'], {'rows': len(data) if data is not None else 0})
    
    def update_data(self, updater: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        """
        更新数据
        
        Args:
            updater: 更新函数，接收数据框返回更新后的数据框
        """
        if self._data is not None:
            self._data = updater(self._data)
            self._notify_observers()
            self._publish_event(EVENT_TYPES['DATA_UPDATED'])
    
    def subscribe(self, observer: Callable[[pd.DataFrame], None]) -> None:
        """订阅数据变更"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable[[pd.DataFrame], None]) -> bool:
        """取消订阅"""
        if observer in self._observers:
            self._observers.remove(observer)
            return True
        return False
    
    def reset(self) -> None:
        """重置数据到原始状态"""
        if self._original_data is not None:
            self._data = self._original_data.copy()
            self._notify_observers()
            self._publish_event(EVENT_TYPES['DATA_UPDATED'])
    
    def clear(self) -> None:
        """清除数据"""
        self._data = None
        self._original_data = None
        self._metadata.clear()
        self._notify_observers()
        self._publish_event(EVENT_TYPES['DATA_CLEARED'])
    
    def get_data_info(self) -> Dict[str, Any]:
        """获取数据信息"""
        if self._data is None:
            return {'status': 'empty'}
        
        info = {
            'status': 'loaded',
            'rows': len(self._data),
            'columns': len(self._data.columns),
            'column_names': list(self._data.columns),
            'memory_usage': self._data.memory_usage(deep=True).sum(),
            'missing_values': self._data.isnull().sum().to_dict(),
            'dtypes': {col: str(dtype) for col, dtype in self._data.dtypes.items()}
        }
        
        return info
    
    def get_column_names(self, dtype_filter: Optional[str] = None) -> List[str]:
        """
        获取列名列表
        
        Args:
            dtype_filter: 数据类型过滤 ('numeric', 'categorical', None)
        """
        if self._data is None:
            return []
        
        if dtype_filter == 'numeric':
            return self._data.select_dtypes(include=['number']).columns.tolist()
        elif dtype_filter == 'categorical':
            return self._data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        return self._data.columns.tolist()
    
    def set_metadata(self, key: str, value: Any) -> None:
        """设置元数据"""
        self._metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """获取元数据"""
        return self._metadata.get(key, default)
    
    def has_data(self) -> bool:
        """检查是否有数据"""
        return self._data is not None and len(self._data) > 0
    
    def _notify_observers(self) -> None:
        """通知所有观察者"""
        for observer in self._observers:
            try:
                observer(self._data)
            except Exception as e:
                self.logger.error(f"Observer notification error: {e}")
    
    def _publish_event(self, event_type: str, data: Any = None) -> None:
        """发布事件"""
        if self._event_bus:
            self._event_bus.publish(event_type, data, source='DataManager')
