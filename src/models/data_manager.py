from typing import Any, Callable, Dict, List, Optional
import pandas as pd


class DataManager:
    def __init__(self):
        self._data: Optional[pd.DataFrame] = None
        self._original_data: Optional[pd.DataFrame] = None
        self._observers: List[Callable[[pd.DataFrame], None]] = []
    
    def get_data(self) -> Optional[pd.DataFrame]:
        return self._data
    
    def set_data(self, data: pd.DataFrame) -> None:
        self._data = data.copy() if data is not None else None
        if self._original_data is None:
            self._original_data = data.copy() if data is not None else None
        self._notify_observers()
    
    def update_data(self, updater: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        if self._data is not None:
            self._data = updater(self._data)
            self._notify_observers()
    
    def subscribe(self, observer: Callable[[pd.DataFrame], None]) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self) -> None:
        for observer in self._observers:
            try:
                observer(self._data)
            except Exception:
                pass
    
    def reset(self) -> None:
        if self._original_data is not None:
            self._data = self._original_data.copy()
            self._notify_observers()
    
    def get_data_info(self) -> Dict[str, Any]:
        if self._data is None:
            return {
                'rows': 0,
                'columns': 0,
                'column_names': [],
                'has_data': False
            }
        
        return {
            'rows': len(self._data),
            'columns': len(self._data.columns),
            'column_names': list(self._data.columns),
            'has_data': True,
            'numeric_columns': list(self._data.select_dtypes(include=['number']).columns),
            'categorical_columns': list(self._data.select_dtypes(include=['object', 'category']).columns),
            'missing_values': self._data.isnull().sum().to_dict()
        }
    
    def has_data(self) -> bool:
        return self._data is not None and len(self._data) > 0
    
    def get_original_data(self) -> Optional[pd.DataFrame]:
        return self._original_data
    
    def clear(self) -> None:
        self._data = None
        self._original_data = None
        self._notify_observers()
