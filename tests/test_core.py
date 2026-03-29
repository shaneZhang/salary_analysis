"""
核心模块单元测试
"""

import unittest
import pandas as pd
import numpy as np
import tempfile
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.data_loader import DataLoader
from src.core.data_processor import DataProcessor
from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer
from src.exceptions import DataLoadError, DataValidationError


class TestDataLoader(unittest.TestCase):
    """DataLoader测试"""
    
    def setUp(self):
        self.loader = DataLoader()
        
        self.test_data = pd.DataFrame({
            '姓名': ['张三', '李四', '王五'],
            '性别': ['男', '女', '男'],
            '年龄': [25, 30, 35],
            '税前薪资': [10000, 15000, 20000]
        })
    
    def test_field_mapping(self):
        """测试字段映射"""
        mapping = self.loader.get_field_mapping()
        
        self.assertIn('姓名', mapping)
        self.assertEqual(mapping['姓名'], 'name')
    
    def test_load_excel(self):
        """测试加载Excel文件"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        try:
            self.test_data.to_excel(temp_path, index=False)
            
            result = self.loader.load_excel(temp_path)
            
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 3)
            self.assertIn('name', result.columns)
        finally:
            os.unlink(temp_path)
    
    def test_get_data_info(self):
        """测试获取数据信息"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        try:
            self.test_data.to_excel(temp_path, index=False)
            self.loader.load_excel(temp_path)
            
            info = self.loader.get_data_info()
            
            self.assertEqual(info['rows'], 3)
            self.assertEqual(info['columns'], 4)
        finally:
            os.unlink(temp_path)
    
    def test_validate_data(self):
        """测试数据验证"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        try:
            self.test_data.to_excel(temp_path, index=False)
            self.loader.load_excel(temp_path)
            
            is_valid, errors = self.loader.validate_data()
            
            self.assertTrue(is_valid)
            self.assertEqual(len(errors), 0)
        finally:
            os.unlink(temp_path)


class TestDataProcessor(unittest.TestCase):
    """DataProcessor测试"""
    
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Alice', 'Charlie'],
            'age': [25, 30, 25, 35],
            'salary': [10000, 15000, 10000, 20000],
            'score': [85.5, np.nan, 85.5, 90.0]
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_set_and_get_data(self):
        """测试设置和获取数据"""
        result = self.processor.get_current_data()
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)
    
    def test_remove_duplicates(self):
        """测试删除重复数据"""
        removed = self.processor.remove_duplicates()
        
        self.assertEqual(removed, 1)
        
        result = self.processor.get_current_data()
        self.assertEqual(len(result), 3)
    
    def test_handle_missing_values_drop(self):
        """测试删除缺失值"""
        result = self.processor.handle_missing_values('drop', ['score'])
        
        self.assertIn('score', result)
        
        data = self.processor.get_current_data()
        self.assertEqual(data['score'].isnull().sum(), 0)
    
    def test_handle_missing_values_fill_mean(self):
        """测试填充均值"""
        result = self.processor.handle_missing_values('fill_mean', ['score'])
        
        self.assertIn('score', result)
        
        data = self.processor.get_current_data()
        self.assertEqual(data['score'].isnull().sum(), 0)
    
    def test_detect_outliers(self):
        """测试检测异常值"""
        test_data = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 100]
        })
        self.processor.set_data(test_data)
        
        outliers = self.processor.detect_outliers('value', 'iqr', 1.5)
        
        self.assertEqual(outliers.sum(), 1)
    
    def test_remove_outliers(self):
        """测试移除异常值"""
        test_data = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 100]
        })
        self.processor.set_data(test_data)
        
        removed = self.processor.remove_outliers('value')
        
        self.assertGreater(removed, 0)
    
    def test_create_age_group(self):
        """测试创建年龄分组"""
        test_data = pd.DataFrame({
            'age': [20, 28, 35, 45, 55]
        })
        self.processor.set_data(test_data)
        
        success = self.processor.create_age_group('age')
        
        self.assertTrue(success)
        
        data = self.processor.get_current_data()
        self.assertIn('age_group', data.columns)
    
    def test_create_salary_group(self):
        """测试创建薪资分组"""
        test_data = pd.DataFrame({
            'salary': [3000, 8000, 15000, 25000, 40000]
        })
        self.processor.set_data(test_data)
        
        success = self.processor.create_salary_group('salary')
        
        self.assertTrue(success)
        
        data = self.processor.get_current_data()
        self.assertIn('salary_group', data.columns)
    
    def test_filter_data(self):
        """测试筛选数据"""
        result = self.processor.filter_data({'name': 'Alice'})
        
        self.assertEqual(len(result), 2)
    
    def test_reset_data(self):
        """测试重置数据"""
        self.processor.remove_duplicates()
        
        self.processor.reset_data()
        
        result = self.processor.get_current_data()
        self.assertEqual(len(result), 4)
    
    def test_get_data_summary(self):
        """测试获取数据摘要"""
        summary = self.processor.get_data_summary()
        
        self.assertEqual(summary['total_rows'], 4)
        self.assertEqual(summary['total_columns'], 4)
        self.assertIn('numeric_columns', summary)


class TestDataAnalyzer(unittest.TestCase):
    """DataAnalyzer测试"""
    
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David'],
            'gender': ['女', '男', '男', '女'],
            'age': [25, 30, 35, 28],
            'salary': [10000, 15000, 20000, 12000]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_descriptive_stats(self):
        """测试描述性统计"""
        stats = self.analyzer.get_descriptive_stats('salary')
        
        self.assertIn('mean', stats)
        self.assertIn('median', stats)
        self.assertIn('std', stats)
        self.assertEqual(stats['count'], 4)
    
    def test_get_frequency_analysis(self):
        """测试频率分析"""
        freq = self.analyzer.get_frequency_analysis('gender')
        
        self.assertEqual(len(freq), 2)
        self.assertIn('count', freq.columns)
        self.assertIn('percentage', freq.columns)
    
    def test_get_crosstab(self):
        """测试交叉分析"""
        crosstab = self.analyzer.get_crosstab('gender', 'name')
        
        self.assertEqual(crosstab.shape[0], 2)
    
    def test_compare_by_dimension(self):
        """测试维度对比"""
        result = self.analyzer.compare_by_dimension('gender', 'salary')
        
        self.assertEqual(len(result), 2)
        self.assertIn('人数', result.columns)
        self.assertIn('平均薪资', result.columns)
    
    def test_get_correlation_matrix(self):
        """测试相关系数矩阵"""
        corr = self.analyzer.get_correlation_matrix()
        
        self.assertIsNotNone(corr)
        self.assertIn('age', corr.columns)
        self.assertIn('salary', corr.columns)
    
    def test_get_correlation(self):
        """测试两列相关性"""
        corr = self.analyzer.get_correlation('age', 'salary')
        
        self.assertIn('pearson_r', corr)
        self.assertIn('spearman_r', corr)
    
    def test_get_summary_report(self):
        """测试摘要报告"""
        report = self.analyzer.get_summary_report('salary')
        
        self.assertIn('数据总量', report)
        self.assertIn('平均薪资', report)
        self.assertIn('中位薪资', report)
    
    def test_get_top_bottom(self):
        """测试获取最大/最小值"""
        top = self.analyzer.get_top_bottom('salary', n=2, top=True)
        
        self.assertEqual(len(top), 2)
        self.assertEqual(top['salary'].iloc[0], 20000)
        
        bottom = self.analyzer.get_top_bottom('salary', n=2, top=False)
        
        self.assertEqual(len(bottom), 2)
        self.assertEqual(bottom['salary'].iloc[0], 10000)


class TestDataVisualizer(unittest.TestCase):
    """DataVisualizer测试"""
    
    def setUp(self):
        self.visualizer = DataVisualizer()
        self.test_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D'],
            'value': [10, 20, 30, 40]
        })
    
    def test_create_figure(self):
        """测试创建图形"""
        fig = self.visualizer.create_figure()
        
        self.assertIsNotNone(fig)
    
    def test_create_bar_chart(self):
        """测试创建柱状图"""
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Bar Chart'
        )
        
        self.assertIsNotNone(fig)
    
    def test_create_line_chart(self):
        """测试创建折线图"""
        fig = self.visualizer.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30], [15, 25, 35]],
            title='Test Line Chart',
            labels=['Series1', 'Series2']
        )
        
        self.assertIsNotNone(fig)
    
    def test_create_pie_chart(self):
        """测试创建饼图"""
        fig = self.visualizer.create_pie_chart(
            data=[30, 40, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie Chart'
        )
        
        self.assertIsNotNone(fig)
    
    def test_create_histogram(self):
        """测试创建直方图"""
        fig = self.visualizer.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
            bins=5,
            title='Test Histogram'
        )
        
        self.assertIsNotNone(fig)
    
    def test_save_chart(self):
        """测试保存图表"""
        self.visualizer.create_bar_chart(
            x_data=['A', 'B'],
            y_data=[10, 20]
        )
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name
        
        try:
            result = self.visualizer.save_chart(temp_path)
            
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_path))
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
