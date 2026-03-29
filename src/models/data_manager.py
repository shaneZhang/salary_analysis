import pandas as pd
from typing import Optional, List, Callable, Dict, Any


class DataManager:
    """统一数据管理器
    
    负责管理应用数据状态，提供数据变更通知机制。
    支持单例模式以确保全局数据一致性。
    """
    
    _instance: Optional['DataManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._data_store: Dict[str, pd.DataFrame] = {}
        self._original_data: Dict[str, pd.DataFrame] = {}
        self._default_key: str = 'main'
        self._observers: List[Callable[[Optional[pd.DataFrame]], None]] = []
        self._initialized = True
    
    def get_data(self, key: Optional[str] = None) -> Optional[pd.DataFrame]:
        """获取当前数据
        
        Args:
            key: 数据键名，默认使用主数据键
        """
        key = key or self._default_key
        return self._data_store.get(key)
    
    def set_data(self, data: pd.DataFrame, key: Optional[str] = None) -> None:
        """设置数据并通知观察者
        
        Args:
            data: 数据DataFrame
            key: 数据键名，默认使用主数据键
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("数据必须是 pandas.DataFrame 类型")
        
        key = key or self._default_key
        self._data_store[key] = data.copy()
        
        if key not in self._original_data:
            self._original_data[key] = data.copy()
        
        if key == self._default_key:
            self._notify_observers()
    
    def update_data(self, data: pd.DataFrame, key: Optional[str] = None) -> None:
        """更新数据
        
        Args:
            data: 新的数据DataFrame
            key: 数据键名，默认使用主数据键
        """
        key = key or self._default_key
        self.set_data(data, key)
    
    def subscribe(self, observer: Callable[[Optional[pd.DataFrame]], None]) -> None:
        """订阅主数据变化"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable) -> None:
        """取消订阅"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def reset(self, key: Optional[str] = None) -> None:
        """重置数据到原始状态
        
        Args:
            key: 数据键名，默认重置所有数据
        """
        if key is None:
            for k in self._original_data:
                if k in self._data_store:
                    self._data_store[k] = self._original_data[k].copy()
            self._notify_observers()
        else:
            if key in self._original_data:
                self._data_store[key] = self._original_data[key].copy()
                if key == self._default_key:
                    self._notify_observers()
    
    def get_data_info(self, key: Optional[str] = None) -> Dict[str, Any]:
        """获取数据信息
        
        Args:
            key: 数据键名，默认使用主数据键
        """
        key = key or self._default_key
        data = self._data_store.get(key)
        
        if data is None:
            return {}
        
        return {
            'rows': len(data),
            'columns': len(data.columns),
            'column_names': list(data.columns),
            'numeric_columns': data.select_dtypes(include=['number']).columns.tolist(),
            'categorical_columns': data.select_dtypes(include=['object', 'category']).columns.tolist(),
            'missing_values': data.isnull().sum().to_dict(),
            'memory_usage': data.memory_usage(deep=True).sum()
        }
    
    def has_data(self, key: Optional[str] = None) -> bool:
        """检查是否有数据
        
        Args:
            key: 数据键名，默认检查主数据
        """
        key = key or self._default_key
        data = self._data_store.get(key)
        return data is not None and len(data) > 0
    
    def clear(self, key: Optional[str] = None) -> None:
        """清除数据
        
        Args:
            key: 数据键名，默认清除所有数据
        """
        if key is None:
            self._data_store.clear()
        else:
            if key in self._data_store:
                del self._data_store[key]
        self._notify_observers()
    
    def _notify_observers(self) -> None:
        """通知所有观察者主数据已变更"""
        main_data = self._data_store.get(self._default_key)
        for observer in self._observers:
            observer(main_data)
