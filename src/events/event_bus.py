from typing import Any, Callable, Dict, List, Optional


class EventBus:
    _instance: Optional['EventBus'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
    
    def publish(self, event_type: str, data: Any = None) -> None:
        if event_type not in self._handlers:
            return
        
        for handler in self._handlers[event_type]:
            try:
                handler(data)
            except Exception:
                pass
    
    def clear(self) -> None:
        self._handlers.clear()
    
    def has_handlers(self, event_type: str) -> bool:
        return event_type in self._handlers and len(self._handlers[event_type]) > 0
    
    @classmethod
    def get_instance(cls) -> 'EventBus':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
