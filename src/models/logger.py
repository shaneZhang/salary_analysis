import logging
import os
from datetime import datetime
from typing import Optional


class AppLogger:
    _instance: Optional['AppLogger'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_dir: str = None, log_level: int = logging.INFO):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._initialized = True
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
        self.log_level = log_level
        self.logger = logging.getLogger('SalaryAnalysis')
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        os.makedirs(self.log_dir, exist_ok=True)
        
        log_filename = datetime.now().strftime('%Y-%m-%d.log')
        log_path = os.path.join(self.log_dir, log_filename)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def critical(self, message: str):
        self.logger.critical(message)
    
    def set_level(self, level: int):
        self.log_level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    @classmethod
    def get_instance(cls) -> 'AppLogger':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
