import unittest
import pandas as pd
import numpy as np
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.data_loader import DataLoader
from src.core.data_processor import DataProcessor
from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer
from src.exceptions import DataLoadError, DataProcessingError


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        self.test_data = pd.DataFrame({
            '姓名': ['张三', '李四', '王五'],
            '性别': ['男', '女', '男'],
            '年龄': [25, 30, 35],
            '税前薪资': [10000, 15000, 20000]
        })
    
    def test_field_mapping(self):
        mapping = self.loader.get_field_mapping()
        self.assertIn('姓名', mapping)
        self.assertEqual(mapping['姓名'], 'name')
    
    def test_auto_map_fields(self):
        self.loader.data = self.test_data.copy()
        self.loader._auto_map_fields()
        self.assertIn('name', self.loader.data.columns)
        self.assertIn('gender', self.loader.data.columns)
    
    def test_get_preview(self):
        self.loader.data = self.test_data
        preview = self.loader.get_preview(2)
        self.assertEqual(len(preview), 2)
    
    def test_get_data_info(self):
        self.loader.data = self.test_data
        info = self.loader.get_data_info()
        self.assertEqual(info['rows'], 3)
        self.assertEqual(info['columns'], 4)
    
    def test_validate_data(self):
        self.loader.data = self.test_data
        is_valid, errors = self.loader.validate_data()
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_data_with_invalid(self):
        invalid_data = pd.DataFrame({
            '姓名': ['张三', '李四', '王五'],
            'age': [25, None, 35],
            '税前薪资': [10000, 15000, 20000]
        })
        invalid_data['age'] = ['25', 'not_a_number', '35']
        self.loader.data = invalid_data
        self.loader._auto_map_fields()
        is_valid, errors = self.loader.validate_data()
        self.assertFalse(is_valid)


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Alice'],
            'age': [25, 30, 35, 25],
            'salary': [10000, 15000, 20000, 10000],
            'work_years': [2, 5, 10, 2]
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_set_and_get_data(self):
        data = self.processor.get_current_data()
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 4)
    
    def test_remove_duplicates(self):
        count = self.processor.remove_duplicates()
        self.assertEqual(count, 1)
        self.assertEqual(len(self.processor.get_current_data()), 3)
    
    def test_handle_missing_values_drop(self):
        data_with_missing = self.test_data.copy()
        data_with_missing.loc[0, 'salary'] = np.nan
        self.processor.set_data(data_with_missing)
        result = self.processor.handle_missing_values('drop', ['salary'])
        self.assertIn('salary', result)
    
    def test_handle_missing_values_fill_mean(self):
        data_with_missing = self.test_data.copy()
        data_with_missing.loc[0, 'salary'] = np.nan
        self.processor.set_data(data_with_missing)
        result = self.processor.handle_missing_values('fill_mean', ['salary'])
        self.assertIn('salary', result)
    
    def test_detect_outliers(self):
        data_with_outlier = self.test_data.copy()
        data_with_outlier.loc[0, 'salary'] = 100000
        self.processor.set_data(data_with_outlier)
        outliers = self.processor.detect_outliers('salary')
        self.assertTrue(outliers.sum() > 0)
    
    def test_remove_outliers(self):
        data_with_outlier = self.test_data.copy()
        data_with_outlier.loc[0, 'salary'] = 100000
        self.processor.set_data(data_with_outlier)
        count = self.processor.remove_outliers('salary')
        self.assertTrue(count > 0)
    
    def test_create_age_group(self):
        success = self.processor.create_age_group('age')
        self.assertTrue(success)
        self.assertIn('age_group', self.processor.get_current_data().columns)
    
    def test_create_salary_group(self):
        success = self.processor.create_salary_group('salary')
        self.assertTrue(success)
        self.assertIn('salary_group', self.processor.get_current_data().columns)
    
    def test_create_experience_group(self):
        success = self.processor.create_work_experience_group('work_years')
        self.assertTrue(success)
        self.assertIn('experience_group', self.processor.get_current_data().columns)
    
    def test_filter_data(self):
        filtered = self.processor.filter_data({'name': 'Alice'})
        self.assertEqual(len(filtered), 2)
    
    def test_reset_data(self):
        self.processor.remove_duplicates()
        self.processor.reset_data()
        self.assertEqual(len(self.processor.get_current_data()), 4)
    
    def test_get_data_summary(self):
        summary = self.processor.get_data_summary()
        self.assertEqual(summary['total_rows'], 4)
        self.assertEqual(summary['total_columns'], 4)


class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David'],
            'gender': ['F', 'M', 'M', 'M'],
            'age': [25, 30, 35, 40],
            'salary': [10000, 15000, 20000, 25000],
            'join_year': [2020, 2019, 2018, 2017]
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_descriptive_stats(self):
        stats = self.analyzer.get_descriptive_stats('salary')
        self.assertEqual(stats['count'], 4)
        self.assertAlmostEqual(stats['mean'], 17500, places=0)
        self.assertEqual(stats['min'], 10000)
        self.assertEqual(stats['max'], 25000)
    
    def test_get_grouped_stats(self):
        grouped = self.analyzer.get_grouped_stats('gender', 'salary')
        self.assertEqual(len(grouped), 2)
    
    def test_get_frequency_analysis(self):
        freq = self.analyzer.get_frequency_analysis('gender')
        self.assertEqual(len(freq), 2)
        self.assertIn('count', freq.columns)
        self.assertIn('percentage', freq.columns)
    
    def test_get_crosstab(self):
        crosstab = self.analyzer.get_crosstab('gender', 'gender')
        self.assertIsNotNone(crosstab)
    
    def test_compare_by_dimension(self):
        comparison = self.analyzer.compare_by_dimension('gender', 'salary')
        self.assertEqual(len(comparison), 2)
        self.assertIn('平均薪资', comparison.columns)
    
    def test_get_correlation_matrix(self):
        corr = self.analyzer.get_correlation_matrix(['age', 'salary'])
        self.assertEqual(corr.shape, (2, 2))
    
    def test_get_correlation(self):
        corr = self.analyzer.get_correlation('age', 'salary')
        self.assertIn('pearson_r', corr)
        self.assertIn('spearman_r', corr)
    
    def test_get_summary_report(self):
        report = self.analyzer.get_summary_report('salary')
        self.assertEqual(report['数据总量'], 4)
        self.assertIn('平均薪资', report)
    
    def test_get_top_bottom(self):
        top = self.analyzer.get_top_bottom('salary', n=2, top=True)
        self.assertEqual(len(top), 2)
        self.assertEqual(top['salary'].iloc[0], 25000)
        
        bottom = self.analyzer.get_top_bottom('salary', n=2, top=False)
        self.assertEqual(len(bottom), 2)
        self.assertEqual(bottom['salary'].iloc[0], 10000)
    
    def test_get_percentile_distribution(self):
        percentiles = self.analyzer.get_percentile_distribution('salary')
        self.assertIn('p25', percentiles)
        self.assertIn('p50', percentiles)
        self.assertIn('p75', percentiles)
    
    def test_get_boxplot_data(self):
        boxplot_data = self.analyzer.get_boxplot_data('gender', 'salary')
        self.assertEqual(len(boxplot_data), 2)
        for key, values in boxplot_data.items():
            self.assertIn('min', values)
            self.assertIn('median', values)
            self.assertIn('max', values)


class TestDataVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
        self.test_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D'],
            'value': [10, 20, 30, 40]
        })
    
    def test_create_figure(self):
        fig = self.visualizer.create_figure()
        self.assertIsNotNone(fig)
    
    def test_create_bar_chart(self):
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Bar Chart'
        )
        self.assertIsNotNone(fig)
    
    def test_create_line_chart(self):
        fig = self.visualizer.create_line_chart(
            x_data=[1, 2, 3],
            y_data_list=[[10, 20, 30]],
            title='Test Line Chart'
        )
        self.assertIsNotNone(fig)
    
    def test_create_pie_chart(self):
        fig = self.visualizer.create_pie_chart(
            data=[10, 20, 30],
            labels=['A', 'B', 'C'],
            title='Test Pie Chart'
        )
        self.assertIsNotNone(fig)
    
    def test_create_histogram(self):
        fig = self.visualizer.create_histogram(
            data=[1, 2, 2, 3, 3, 3, 4, 4, 5],
            bins=5,
            title='Test Histogram'
        )
        self.assertIsNotNone(fig)
    
    def test_set_color_scheme(self):
        colors = ['#FF0000', '#00FF00', '#0000FF']
        self.visualizer.set_color_scheme(colors)
        self.assertEqual(self.visualizer.chart_config['colors'], colors)
    
    def test_set_figure_size(self):
        self.visualizer.set_figure_size(12, 8)
        self.assertEqual(self.visualizer.chart_config['figure_size'], (12, 8))


if __name__ == '__main__':
    unittest.main()
