class AppException(Exception):
    """应用基础异常"""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} - {self.details}"
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


class DataProcessingError(DataException):
    """数据处理异常"""
    pass


class AnalysisException(AppException):
    """分析相关异常基类"""
    pass


class AnalysisError(AnalysisException):
    """分析操作异常"""
    pass


class VisualizationException(AppException):
    """可视化相关异常基类"""
    pass


class VisualizationError(VisualizationException):
    """可视化操作异常"""
    pass


class ConfigurationException(AppException):
    """配置相关异常基类"""
    pass


class ConfigurationError(ConfigurationException):
    """配置操作异常"""
    pass
