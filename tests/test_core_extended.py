import unittest
import pandas as pd
import numpy as np
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.data_loader import DataLoader
from src.core.data_processor import DataProcessor
from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer
from src.exceptions import DataLoadError, DataValidationError


class TestDataLoaderExtended(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        self.test_data = pd.DataFrame({
            '姓名': ['张三', '李四', '王五'],
            '性别': ['男', '女', '男'],
            '年龄': [25, 30, 35],
            '税前薪资': [10000, 15000, 20000]
        })
        
        self.temp_dir = tempfile.mkdtemp()
        self.excel_path = os.path.join(self.temp_dir, 'test_data.xlsx')
        self.test_data.to_excel(self.excel_path, index=False)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_excel_file(self):
        result = self.loader.load_excel(self.excel_path)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
    
    def test_load_excel_with_sheet_name(self):
        result = self.loader.load_excel(self.excel_path, sheet_name=0)
        self.assertIsNotNone(result)
    
    def test_get_sheet_names(self):
        names = self.loader.get_sheet_names(self.excel_path)
        self.assertIsInstance(names, list)
        self.assertTrue(len(names) > 0)
    
    def test_load_multiple_files(self):
        excel_path2 = os.path.join(self.temp_dir, 'test_data2.xlsx')
        self.test_data.to_excel(excel_path2, index=False)
        
        result = self.loader.load_multiple_files([self.excel_path, excel_path2])
        self.assertEqual(len(result), 6)
    
    def test_load_folder(self):
        result = self.loader.load_folder(self.temp_dir)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
    
    def test_load_invalid_file(self):
        invalid_path = os.path.join(self.temp_dir, 'invalid.txt')
        with open(invalid_path, 'w') as f:
            f.write('invalid content')
        
        with self.assertRaises(DataLoadError):
            self.loader.load_excel(invalid_path)
    
    def test_load_nonexistent_folder(self):
        with self.assertRaises(DataLoadError):
            self.loader.load_folder('/nonexistent/folder/path')
    
    def test_load_empty_folder(self):
        empty_dir = os.path.join(self.temp_dir, 'empty')
        os.makedirs(empty_dir)
        
        with self.assertRaises(DataLoadError):
            self.loader.load_folder(empty_dir)
    
    def test_apply_field_mapping(self):
        self.loader.data = self.test_data.copy()
        custom_mapping = {'姓名': 'employee_name'}
        self.loader.apply_field_mapping(custom_mapping)
        self.assertIn('employee_name', self.loader.data.columns)
    
    def test_get_data_info_empty(self):
        info = self.loader.get_data_info()
        self.assertEqual(info, {})
    
    def test_get_preview_empty(self):
        preview = self.loader.get_preview()
        self.assertIsNone(preview)
    
    def test_get_preview_with_data(self):
        self.loader.data = self.test_data
        preview = self.loader.get_preview(2)
        self.assertEqual(len(preview), 2)
    
    def test_custom_field_mapping(self):
        custom_mapping = {'姓名': 'name', '年龄': 'age'}
        loader = DataLoader(field_mapping=custom_mapping)
        self.assertEqual(loader.field_mapping['姓名'], 'name')


class TestDataProcessorExtended(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'education': ['本科', '硕士', '博士', '本科', '硕士']
        })
        self.processor = DataProcessor(self.test_data)
    
    def test_handle_missing_values_fill_median(self):
        data_with_missing = self.test_data.copy()
        data_with_missing.loc[0, 'salary'] = np.nan
        self.processor.set_data(data_with_missing)
        result = self.processor.handle_missing_values('fill_median', ['salary'])
        self.assertIn('salary', result)
    
    def test_handle_missing_values_fill_mode(self):
        data_with_missing = self.test_data.copy()
        data_with_missing.loc[0, 'education'] = np.nan
        self.processor.set_data(data_with_missing)
        result = self.processor.handle_missing_values('fill_mode', ['education'])
        self.assertIn('education', result)
    
    def test_detect_outliers_iqr(self):
        data_with_outlier = self.test_data.copy()
        data_with_outlier.loc[0, 'salary'] = 100000
        self.processor.set_data(data_with_outlier)
        outliers = self.processor.detect_outliers('salary', method='iqr')
        self.assertTrue(outliers.sum() > 0)
    
    def test_detect_outliers_zscore(self):
        data_with_outlier = self.test_data.copy()
        data_with_outlier.loc[0, 'salary'] = 100000
        self.processor.set_data(data_with_outlier)
        outliers = self.processor.detect_outliers('salary', method='zscore')
        self.assertTrue(outliers.sum() > 0)
    
    def test_remove_outliers_iqr(self):
        data_with_outlier = self.test_data.copy()
        data_with_outlier.loc[0, 'salary'] = 100000
        self.processor.set_data(data_with_outlier)
        count = self.processor.remove_outliers('salary', method='iqr')
        self.assertTrue(count > 0)
    
    def test_convert_dtype(self):
        result = self.processor.convert_dtype('salary', 'float')
        self.assertTrue(result)
    
    def test_create_calculated_field(self):
        result = self.processor.create_calculated_field(
            'double_salary',
            lambda df: df['salary'] * 2
        )
        self.assertTrue(result)
        self.assertIn('double_salary', self.processor.get_current_data().columns)
    
    def test_calculate_age_from_year(self):
        data = pd.DataFrame({
            'birth_year': [1990, 1995, 2000],
            'name': ['A', 'B', 'C']
        })
        processor = DataProcessor(data)
        result = processor.calculate_age_from_year('birth_year', reference_year=2024)
        self.assertTrue(result)
        self.assertIn('age', processor.get_current_data().columns)
    
    def test_encode_categorical(self):
        result = self.processor.encode_categorical(columns=['gender'])
        self.assertTrue(result)
    
    def test_get_data_summary(self):
        summary = self.processor.get_data_summary()
        self.assertIn('total_rows', summary)
        self.assertIn('total_columns', summary)


class TestDataAnalyzerExtended(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'gender': ['F', 'M', 'M', 'M', 'F'],
            'age': [25, 30, 35, 40, 45],
            'salary': [10000, 15000, 20000, 25000, 30000],
            'work_years': [2, 5, 10, 15, 20],
            'department': ['IT', 'HR', 'IT', 'Finance', 'HR']
        })
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_salary_distribution(self):
        dist = self.analyzer.get_salary_distribution('salary')
        self.assertIn('薪资区间', dist.columns)
        self.assertIn('人数', dist.columns)
    
    def test_get_dimensions_analysis(self):
        results = self.analyzer.get_dimensions_analysis(['gender', 'department'], 'salary')
        self.assertIn('gender', results)
        self.assertIn('department', results)
    
    def test_calculate_growth_rate(self):
        growth = self.analyzer.calculate_growth_rate('work_years', 'salary')
        self.assertIsNotNone(growth)
    
    def test_get_crosstab_with_values(self):
        crosstab = self.analyzer.get_crosstab('gender', 'department')
        self.assertIsNotNone(crosstab)
    
    def test_set_data(self):
        new_data = pd.DataFrame({'a': [1, 2, 3]})
        self.analyzer.set_data(new_data)
        self.assertEqual(len(self.analyzer.data), 3)
    
    def test_get_current_data(self):
        data = self.analyzer.get_current_data()
        self.assertEqual(len(data), 5)


class TestDataVisualizerExtended(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()
        self.test_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D', 'E'],
            'value1': [10, 20, 30, 40, 50],
            'value2': [5, 15, 25, 35, 45]
        })
    
    def test_create_scatter_chart(self):
        fig = self.visualizer.create_scatter_chart(
            x_data=[1, 2, 3, 4, 5],
            y_data=[10, 20, 30, 40, 50],
            title='Test Scatter Chart'
        )
        self.assertIsNotNone(fig)
    
    def test_create_boxplot(self):
        fig = self.visualizer.create_boxplot(
            data_dict={'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]},
            title='Test Boxplot'
        )
        self.assertIsNotNone(fig)
    
    def test_create_heatmap(self):
        fig = self.visualizer.create_heatmap(
            data=pd.DataFrame([[1, 2], [3, 4]]),
            title='Test Heatmap'
        )
        self.assertIsNotNone(fig)
    
    def test_create_stacked_bar(self):
        fig = self.visualizer.create_stacked_bar(
            x_data=['A', 'B', 'C'],
            data_dict={'Series1': [10, 20, 30], 'Series2': [5, 10, 15]},
            title='Test Stacked Bar Chart'
        )
        self.assertIsNotNone(fig)
    
    def test_create_radar_chart(self):
        fig = self.visualizer.create_radar_chart(
            categories=['A', 'B', 'C', 'D'],
            values=[10, 20, 30, 40],
            title='Test Radar Chart'
        )
        self.assertIsNotNone(fig)
    
    def test_create_horizontal_bar(self):
        fig = self.visualizer.create_bar_chart(
            x_data=['A', 'B', 'C'],
            y_data=[10, 20, 30],
            title='Test Horizontal Bar',
            horizontal=True
        )
        self.assertIsNotNone(fig)
    
    def test_set_config(self):
        self.visualizer.set_config({'title_fontsize': 16})
        self.assertEqual(self.visualizer.chart_config['title_fontsize'], 16)
    
    def test_set_data(self):
        self.visualizer.set_data(self.test_data)
        self.assertIsNotNone(self.visualizer.data)
    
    def test_clear_figure(self):
        self.visualizer.create_figure()
        self.visualizer.clear_figure()
        self.assertIsNotNone(self.visualizer.figure)
    
    def test_save_chart(self):
        self.visualizer.create_bar_chart(['A', 'B'], [1, 2], 'Test')
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.close()
        result = self.visualizer.save_chart(temp_file.name)
        self.assertTrue(result)
        os.unlink(temp_file.name)
    
    def test_set_figure_size(self):
        self.visualizer.set_figure_size(12, 8)
        self.assertEqual(self.visualizer.chart_config['figure_size'], (12, 8))
    
    def test_set_dpi(self):
        self.visualizer.set_dpi(150)
        self.assertEqual(self.visualizer.chart_config['dpi'], 150)


if __name__ == '__main__':
    unittest.main()
