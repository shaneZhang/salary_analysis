"""
服务层单元测试
"""

import unittest
import pandas as pd
import tempfile
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.data_manager import DataManager
from src.models.config_manager import ConfigManager
from src.events.event_bus import EventBus
from src.services.data_service import DataService
from src.services.processing_service import ProcessingService
from src.services.analysis_service import AnalysisService
from src.services.visualization_service import VisualizationService


class TestDataService(unittest.TestCase):
    """DataService测试"""
    
    def setUp(self):
        self.event_bus = EventBus()
        self.data_manager = DataManager(event_bus=self.event_bus)
        self.config = ConfigManager()
        self.service = DataService(self.data_manager, self.config, self.event_bus)
        
        self.test_data = pd.DataFrame({
            '姓名': ['张三', '李四'],
            '年龄': [25, 30],
            '税前薪资': [10000, 15000]
        })
    
    def test_load_file(self):
        """测试加载文件"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        try:
            self.test_data.to_excel(temp_path, index=False)
            
            result = self.service.load_file(temp_path)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['rows'], 2)
        finally:
            os.unlink(temp_path)
    
    def test_get_data_info(self):
        """测试获取数据信息"""
        self.data_manager.set_data(self.test_data)
        
        info = self.service.get_data_info()
        
        self.assertEqual(info['rows'], 2)
    
    def test_has_data(self):
        """测试数据存在检查"""
        self.assertFalse(self.service.has_data())
        
        self.data_manager.set_data(self.test_data)
        self.assertTrue(self.service.has_data())
    
    def test_get_column_names(self):
        """测试获取列名"""
        self.data_manager.set_data(self.test_data)
        
        all_cols = self.service.get_column_names()
        self.assertEqual(len(all_cols), 3)
    
    def test_export_data(self):
        """测试导出数据"""
        self.data_manager.set_data(self.test_data)
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        try:
            result = self.service.export_data(temp_path, 'excel')
            
            self.assertTrue(result['success'])
            self.assertTrue(os.path.exists(temp_path))
        finally:
            os.unlink(temp_path)


class TestProcessingService(unittest.TestCase):
    """ProcessingService测试"""
    
    def setUp(self):
        self.event_bus = EventBus()
        self.data_manager = DataManager(event_bus=self.event_bus)
        self.config = ConfigManager()
        self.service = ProcessingService(self.data_manager, self.config, self.event_bus)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Alice'],
            'age': [25, 30, 25],
            'salary': [10000, 15000, 10000],
            'work_years': [2, 5, 2]
        })
    
    def test_remove_duplicates(self):
        """测试删除重复数据"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.remove_duplicates()
        
        self.assertTrue(result['success'])
        self.assertEqual(result['removed_count'], 1)
    
    def test_handle_missing_values(self):
        """测试处理缺失值"""
        data_with_nan = self.test_data.copy()
        data_with_nan.loc[0, 'salary'] = None
        self.data_manager.set_data(data_with_nan)
        
        result = self.service.handle_missing_values('drop', ['salary'])
        
        self.assertTrue(result['success'])
    
    def test_create_age_group(self):
        """测试创建年龄分组"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.create_age_group('age')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['new_column'], 'age_group')
    
    def test_create_salary_group(self):
        """测试创建薪资分组"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.create_salary_group('salary')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['new_column'], 'salary_group')
    
    def test_create_experience_group(self):
        """测试创建工作年限分组"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.create_experience_group('work_years')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['new_column'], 'experience_group')
    
    def test_filter_data(self):
        """测试筛选数据"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.filter_data({'name': 'Alice'})
        
        self.assertTrue(result['success'])
    
    def test_get_data_summary(self):
        """测试获取数据摘要"""
        self.data_manager.set_data(self.test_data)
        
        summary = self.service.get_data_summary()
        
        self.assertEqual(summary['total_rows'], 3)


class TestAnalysisService(unittest.TestCase):
    """AnalysisService测试"""
    
    def setUp(self):
        self.event_bus = EventBus()
        self.data_manager = DataManager(event_bus=self.event_bus)
        self.config = ConfigManager()
        self.service = AnalysisService(self.data_manager, self.config, self.event_bus)
        
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'gender': ['女', '男', '男'],
            'age': [25, 30, 35],
            'salary': [10000, 15000, 20000]
        })
    
    def test_get_descriptive_stats(self):
        """测试描述性统计"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.get_descriptive_stats('salary')
        
        self.assertTrue(result['success'])
        self.assertIn('stats', result)
        self.assertIn('mean', result['stats'])
    
    def test_get_frequency_analysis(self):
        """测试频率分析"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.get_frequency_analysis('gender')
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 2)
    
    def test_get_crosstab(self):
        """测试交叉分析"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.get_crosstab('gender', 'name')
        
        self.assertTrue(result['success'])
        self.assertIn('data', result)
    
    def test_compare_by_dimension(self):
        """测试维度对比"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.compare_by_dimension('gender', 'salary')
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 2)
    
    def test_get_correlation_matrix(self):
        """测试相关系数矩阵"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.get_correlation_matrix()
        
        self.assertTrue(result['success'])
        self.assertIn('data', result)
    
    def test_get_summary_report(self):
        """测试摘要报告"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.get_summary_report('salary')
        
        self.assertTrue(result['success'])
        self.assertIn('report', result)
        self.assertIn('平均薪资', result['report'])
    
    def test_get_top_bottom(self):
        """测试获取最大/最小值"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.get_top_bottom('salary', n=2, top=True)
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 2)


class TestVisualizationService(unittest.TestCase):
    """VisualizationService测试"""
    
    def setUp(self):
        self.event_bus = EventBus()
        self.data_manager = DataManager(event_bus=self.event_bus)
        self.config = ConfigManager()
        self.service = VisualizationService(self.data_manager, self.config, self.event_bus)
        
        self.test_data = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [10, 20, 30]
        })
    
    def test_create_bar_chart(self):
        """测试创建柱状图"""
        result = self.service.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test'
        )
        
        self.assertTrue(result['success'])
    
    def test_create_line_chart(self):
        """测试创建折线图"""
        result = self.service.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30]],
            title='Test'
        )
        
        self.assertTrue(result['success'])
    
    def test_create_pie_chart(self):
        """测试创建饼图"""
        result = self.service.create_pie_chart(
            data=[30, 40, 30],
            labels=['A', 'B', 'C'],
            title='Test'
        )
        
        self.assertTrue(result['success'])
    
    def test_create_histogram(self):
        """测试创建直方图"""
        result = self.service.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4],
            bins=4,
            title='Test'
        )
        
        self.assertTrue(result['success'])
    
    def test_generate_chart_by_type(self):
        """测试根据类型生成图表"""
        self.data_manager.set_data(self.test_data)
        
        result = self.service.generate_chart_by_type('bar', 'category', 'value')
        
        self.assertTrue(result['success'])
    
    def test_save_chart(self):
        """测试保存图表"""
        self.service.create_bar_chart(['A'], [10])
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name
        
        try:
            result = self.service.save_chart(temp_path)
            
            self.assertTrue(result['success'])
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
