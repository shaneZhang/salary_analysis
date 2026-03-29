from typing import Any, Callable, Dict, Optional
from enum import Enum


class AppStateStatus(Enum):
    IDLE = "idle"
    LOADING = "loading"
    PROCESSING = "processing"
    ANALYZING = "analyzing"
    ERROR = "error"


class AppState:
    _instance: Optional['AppState'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._state: Dict[str, Any] = {
            'status': AppStateStatus.IDLE,
            'current_file': None,
            'last_operation': None,
            'error_message': None
        }
        self._observers: list = []
    
    def get_state(self) -> Dict[str, Any]:
        return self._state.copy()
    
    def set_state(self, key: str, value: Any) -> None:
        self._state[key] = value
        self._notify_observers()
    
    def subscribe(self, observer: Callable) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self) -> None:
        for observer in self._observers:
            try:
                observer(self._state)
            except Exception:
                pass
    
    def set_status(self, status: AppStateStatus) -> None:
        self.set_state('status', status)
    
    def get_status(self) -> AppStateStatus:
        return self._state.get('status', AppStateStatus.IDLE)
    
    def set_current_file(self, file_path: Optional[str]) -> None:
        self.set_state('current_file', file_path)
    
    def get_current_file(self) -> Optional[str]:
        return self._state.get('current_file')
    
    def set_last_operation(self, operation: str) -> None:
        self.set_state('last_operation', operation)
    
    def get_last_operation(self) -> Optional[str]:
        return self._state.get('last_operation')
    
    def set_error(self, message: str) -> None:
        self._state['error_message'] = message
        self.set_status(AppStateStatus.ERROR)
    
    def clear_error(self) -> None:
        self._state['error_message'] = None
        self.set_status(AppStateStatus.IDLE)
    
    def get_error(self) -> Optional[str]:
        return self._state.get('error_message')
    
    def reset(self) -> None:
        self._state = {
            'status': AppStateStatus.IDLE,
            'current_file': None,
            'last_operation': None,
            'error_message': None
        }
        self._notify_observers()
    
    @classmethod
    def get_instance(cls) -> 'AppState':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
