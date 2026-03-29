"""
应用异常定义模块
定义应用中使用的所有自定义异常类
"""

from typing import Optional, Any


class AppException(Exception):
    """应用基础异常类"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} - 详情: {self.details}"
        return self.message


class DataException(AppException):
    """数据相关异常基类"""
    pass


class DataLoadError(DataException):
    """数据加载异常"""
    pass


class DataValidationError(DataException):
    """数据验证异常"""
    pass


class AnalysisException(AppException):
    """分析相关异常"""
    pass


class ConfigurationException(AppException):
    """配置相关异常"""
    pass


class VisualizationException(AppException):
    """可视化相关异常"""
    pass
