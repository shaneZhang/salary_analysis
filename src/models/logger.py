"""
日志管理模块
提供统一的日志记录功能
"""

import logging
import os
from typing import Optional
from datetime import datetime


_logger_instance: Optional[logging.Logger] = None


def get_logger(name: str = 'salary_analysis', 
               level: int = logging.INFO,
               log_file: Optional[str] = None) -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
        
    Returns:
        配置好的日志记录器
    """
    global _logger_instance
    
    if _logger_instance is not None:
        return _logger_instance
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    _logger_instance = logger
    return logger


def set_log_level(level: int) -> None:
    """设置日志级别"""
    global _logger_instance
    if _logger_instance:
        _logger_instance.setLevel(level)
        for handler in _logger_instance.handlers:
            handler.setLevel(level)


class LoggerMixin:
    """日志混入类，为类提供日志功能"""
    
    _logger: Optional[logging.Logger] = None
    
    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
