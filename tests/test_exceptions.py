"""
异常处理测试
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.exceptions import (
    AppException, DataException, DataLoadError, DataValidationError,
    AnalysisException, VisualizationException, ConfigurationException
)


class TestExceptions(unittest.TestCase):
    """异常类测试"""
    
    def test_app_exception(self):
        """测试基础异常"""
        e = AppException("Test error")
        self.assertEqual(str(e), "Test error")
        self.assertEqual(e.message, "Test error")
    
    def test_data_load_error(self):
        """测试数据加载异常"""
        e = DataLoadError("File not found")
        self.assertEqual(str(e), "File not found")
        self.assertIsInstance(e, AppException)
    
    def test_data_validation_error(self):
        """测试数据验证异常"""
        e = DataValidationError("Invalid data")
        self.assertEqual(str(e), "Invalid data")
        self.assertIsInstance(e, AppException)
    
    def test_data_exception(self):
        """测试数据异常"""
        e = DataException("Data error")
        self.assertEqual(str(e), "Data error")
        self.assertIsInstance(e, AppException)
    
    def test_analysis_exception(self):
        """测试分析异常"""
        e = AnalysisException("Analysis failed")
        self.assertEqual(str(e), "Analysis failed")
        self.assertIsInstance(e, AppException)
    
    def test_visualization_exception(self):
        """测试可视化异常"""
        e = VisualizationException("Chart error")
        self.assertEqual(str(e), "Chart error")
        self.assertIsInstance(e, AppException)
    
    def test_configuration_exception(self):
        """测试配置异常"""
        e = ConfigurationException("Config error")
        self.assertEqual(str(e), "Config error")
        self.assertIsInstance(e, AppException)


if __name__ == '__main__':
    unittest.main()
