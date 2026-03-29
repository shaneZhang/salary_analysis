import logging
import os
from typing import Optional


class Logger:
    """统一日志管理器
    
    提供应用日志记录功能，支持不同日志级别和输出目标。
    """
    
    _instance: Optional['Logger'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_level: str = 'INFO', log_file: Optional[str] = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._logger = logging.getLogger('salary_analysis')
        self._logger.setLevel(self._get_log_level(log_level))
        self._logger.propagate = False
        
        self._setup_handlers(log_file)
        self._initialized = True
    
    def _get_log_level(self, level: str) -> int:
        """转换日志级别字符串为logging模块常量"""
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(level.upper(), logging.INFO)
    
    def _setup_handlers(self, log_file: Optional[str] = None):
        """设置日志处理器"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """记录调试级别日志"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """记录信息级别日志"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """记录警告级别日志"""
        self._logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """记录错误级别日志"""
        self._logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """记录严重错误级别日志"""
        self._logger.critical(message, exc_info=exc_info)
    
    def set_level(self, level: str):
        """设置日志级别"""
        self._logger.setLevel(self._get_log_level(level))
    
    def get_logger(self) -> logging.Logger:
        """获取底层logging.Logger实例"""
        return self._logger
