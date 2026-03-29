class AppException(Exception):
    """应用基础异常类"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        return self.message
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'details': self.details
        }


class DataException(AppException):
    """数据相关异常"""
    pass


class DataLoadError(DataException):
    """数据加载异常"""
    def __init__(self, message: str, file_path: str = None, details: dict = None):
        super().__init__(message, details)
        self.file_path = file_path
    
    def __str__(self):
        base_msg = super().__str__()
        if self.file_path:
            return f"{base_msg} (文件: {self.file_path})"
        return base_msg


class DataProcessingError(DataException):
    """数据处理异常"""
    def __init__(self, message: str, column: str = None, details: dict = None):
        super().__init__(message, details)
        self.column = column
    
    def __str__(self):
        base_msg = super().__str__()
        if self.column:
            return f"{base_msg} (列: {self.column})"
        return base_msg


class DataValidationError(DataException):
    """数据验证异常"""
    def __init__(self, message: str, field: str = None, details: dict = None):
        super().__init__(message, details)
        self.field = field


class AnalysisException(AppException):
    """分析相关异常"""
    def __init__(self, message: str, dimension: str = None, details: dict = None):
        super().__init__(message, details)
        self.dimension = dimension


class VisualizationException(AppException):
    """可视化相关异常"""
    def __init__(self, message: str, chart_type: str = None, details: dict = None):
        super().__init__(message, details)
        self.chart_type = chart_type
    
    def __str__(self):
        base_msg = super().__str__()
        if self.chart_type:
            return f"{base_msg} (图表类型: {self.chart_type})"
        return base_msg


class ConfigurationException(AppException):
    """配置相关异常"""
    def __init__(self, message: str, key: str = None, details: dict = None):
        super().__init__(message, details)
        self.key = key
    
    def __str__(self):
        base_msg = super().__str__()
        if self.key:
            return f"{base_msg} (配置键: {self.key})"
        return base_msg


class FileFormatError(DataLoadError):
    """文件格式错误"""
    pass


class InvalidColumnError(DataException):
    """无效列名错误"""
    def __init__(self, message: str, column: str = None, details: dict = None):
        super().__init__(message, details)
        self.column = column
