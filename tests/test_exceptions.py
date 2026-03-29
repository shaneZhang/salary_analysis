import pytest

from src.exceptions import (
    AppException,
    DataException,
    DataLoadError,
    DataProcessingError,
    DataValidationError,
    AnalysisException,
    VisualizationException,
    ConfigurationException,
    FileFormatError,
    InvalidColumnError
)


class TestAppException:
    """测试AppException基类"""
    
    def test_app_exception_creation(self):
        """测试创建AppException"""
        message = "Test exception message"
        exc = AppException(message)
        
        assert str(exc) == message
        assert exc.message == message
    
    def test_app_exception_with_details(self):
        """测试带详细信息的AppException"""
        message = "Test exception"
        details = {"key": "value", "code": 500}
        exc = AppException(message, details=details)
        
        assert exc.details == details
        assert "key" in exc.details
    
    def test_app_exception_to_dict(self):
        """测试to_dict方法"""
        message = "Test exception"
        exc = AppException(message)
        result = exc.to_dict()
        
        assert isinstance(result, dict)
        assert "error_type" in result
        assert "message" in result
        assert result["message"] == message


class TestDataException:
    """测试DataException类"""
    
    def test_data_exception_inheritance(self):
        """测试DataException继承自AppException"""
        exc = DataException("Data error")
        assert isinstance(exc, AppException)
    
    def test_data_exception_message(self):
        """测试DataException消息"""
        message = "Data processing failed"
        exc = DataException(message)
        assert str(exc) == message


class TestDataLoadError:
    """测试DataLoadError类"""
    
    def test_data_load_error_inheritance(self):
        """测试DataLoadError继承自DataException"""
        exc = DataLoadError("Load error")
        assert isinstance(exc, DataException)
        assert isinstance(exc, AppException)
    
    def test_data_load_error_with_filepath(self):
        """测试带文件路径的DataLoadError"""
        message = "Failed to load file"
        filepath = "/path/to/file.xlsx"
        exc = DataLoadError(message, file_path=filepath)
        
        assert exc.file_path == filepath
        assert filepath in str(exc)


class TestDataProcessingError:
    """测试DataProcessingError类"""
    
    def test_data_processing_error_inheritance(self):
        """测试DataProcessingError继承自DataException"""
        exc = DataProcessingError("Processing error")
        assert isinstance(exc, DataException)
    
    def test_data_processing_error_with_column(self):
        """测试带列名的DataProcessingError"""
        message = "Invalid column data"
        column = "salary"
        exc = DataProcessingError(message, column=column)
        
        assert exc.column == column


class TestAnalysisException:
    """测试AnalysisException类"""
    
    def test_analysis_exception_inheritance(self):
        """测试AnalysisException继承自AppException"""
        exc = AnalysisException("Analysis error")
        assert isinstance(exc, AppException)
    
    def test_analysis_exception_message(self):
        """测试AnalysisException消息"""
        message = "Statistical analysis failed"
        exc = AnalysisException(message)
        assert str(exc) == message


class TestVisualizationException:
    """测试VisualizationException类"""
    
    def test_visualization_exception_inheritance(self):
        """测试VisualizationException继承自AppException"""
        exc = VisualizationException("Visualization error")
        assert isinstance(exc, AppException)
    
    def test_visualization_exception_with_chart_type(self):
        """测试带图表类型的VisualizationException"""
        message = "Failed to create chart"
        chart_type = "bar"
        exc = VisualizationException(message, chart_type=chart_type)
        
        assert exc.chart_type == chart_type


class TestConfigurationException:
    """测试ConfigurationException类"""
    
    def test_config_exception_inheritance(self):
        """测试ConfigurationException继承自AppException"""
        exc = ConfigurationException("Config error")
        assert isinstance(exc, AppException)
    
    def test_config_exception_with_key(self):
        """测试带配置键的ConfigurationException"""
        message = "Missing configuration key"
        key = "database.host"
        exc = ConfigurationException(message, key=key)
        
        assert exc.key == key


class TestDataValidationError:
    """测试DataValidationError类"""
    
    def test_validation_exception_inheritance(self):
        """测试DataValidationError继承自DataException"""
        exc = DataValidationError("Validation error")
        assert isinstance(exc, DataException)
        assert isinstance(exc, AppException)


class TestFileFormatError:
    """测试FileFormatError类"""
    
    def test_file_format_error_inheritance(self):
        """测试FileFormatError继承自DataLoadError"""
        exc = FileFormatError("File format error")
        assert isinstance(exc, DataLoadError)
        assert isinstance(exc, DataException)


class TestInvalidColumnError:
    """测试InvalidColumnError类"""
    
    def test_invalid_column_error_inheritance(self):
        """测试InvalidColumnError继承自DataException"""
        exc = InvalidColumnError("Invalid column")
        assert isinstance(exc, DataException)
    
    def test_invalid_column_error_with_column_name(self):
        """测试带列名的InvalidColumnError"""
        message = "Column not found"
        column = "salary"
        exc = InvalidColumnError(message, column=column)
        
        assert exc.column == column
