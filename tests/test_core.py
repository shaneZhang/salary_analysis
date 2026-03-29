import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from matplotlib.figure import Figure

from src.core import DataLoader, DataProcessor, DataAnalyzer, DataVisualizer, DataVisualizerAdapter
from src.exceptions import DataLoadError, DataProcessingError, AnalysisException, VisualizationException


class TestDataLoader:
    """测试DataLoader类"""
    
    def test_load_excel_file(self, temp_excel_file):
        """测试加载Excel文件"""
        loader = DataLoader()
        df = loader.load_excel(temp_excel_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100  # 样本数据有100行
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        loader = DataLoader()
        
        with pytest.raises(DataLoadError):
            loader.load_excel("/nonexistent/file.xlsx")
    
    def test_load_unsupported_format(self):
        """测试加载不支持的文件格式"""
        loader = DataLoader()
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"test content")
        
        with pytest.raises(DataLoadError):
            loader.load_excel(f.name)
        
        os.unlink(f.name)
    
    def test_load_folder(self, tmp_path, sample_dataframe):
        """测试加载文件夹"""
        # 创建多个Excel文件
        for i in range(3):
            file_path = tmp_path / f"data_{i}.xlsx"
            sample_dataframe.to_excel(file_path, index=False)
        
        loader = DataLoader()
        df = loader.load_folder(str(tmp_path))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 300  # 3个文件，每个100行


class TestDataProcessor:
    """测试DataProcessor类"""
    
    def test_remove_duplicates(self, sample_dataframe_with_duplicates):
        """测试删除重复数据"""
        processor = DataProcessor(sample_dataframe_with_duplicates)
        original_count = len(sample_dataframe_with_duplicates)
        
        removed = processor.remove_duplicates()
        
        assert removed == 10  # 删除了10条重复
        assert len(processor.data) == 100  # 原始数据100行，10条重复
        assert original_count - len(processor.data) == 10
    
    def test_handle_missing_values_drop(self, sample_dataframe_with_missing):
        """测试删除缺失值"""
        processor = DataProcessor(sample_dataframe_with_missing)
        result = processor.handle_missing_values(strategy='drop')
        
        assert isinstance(result, dict)
        assert processor.data['pre_tax_salary'].isna().sum() == 0
    
    def test_handle_missing_values_fill_mean(self, sample_dataframe_with_missing):
        """测试用均值填充缺失值"""
        processor = DataProcessor(sample_dataframe_with_missing)
        result = processor.handle_missing_values(strategy='fill_mean')
        
        assert isinstance(result, dict)
        assert processor.data['pre_tax_salary'].isna().sum() == 0
    
    def test_detect_outliers(self, sample_dataframe):
        """测试异常值检测"""
        processor = DataProcessor(sample_dataframe)
        outliers = processor.detect_outliers('pre_tax_salary')
        
        assert isinstance(outliers, pd.Series)
        assert len(outliers) == len(sample_dataframe)
    
    def test_remove_outliers(self, sample_dataframe):
        """测试移除异常值"""
        processor = DataProcessor(sample_dataframe.copy())
        count = processor.remove_outliers('pre_tax_salary')
        
        assert isinstance(count, int)
        assert len(processor.data) == len(sample_dataframe) - count
    
    def test_create_age_group(self, sample_dataframe):
        """测试创建年龄分组"""
        processor = DataProcessor(sample_dataframe)
        processor.create_age_group('age')
        
        assert 'age_group' in processor.data.columns
    
    def test_create_salary_group(self, sample_dataframe):
        """测试创建薪资分组"""
        processor = DataProcessor(sample_dataframe)
        processor.create_salary_group('pre_tax_salary')
        
        assert 'salary_group' in processor.data.columns
    
    def test_create_work_experience_group(self, sample_dataframe):
        """测试创建工作年限分组"""
        processor = DataProcessor(sample_dataframe)
        processor.create_work_experience_group('work_years')
        
        assert 'experience_group' in processor.data.columns


class TestDataAnalyzer:
    """测试DataAnalyzer类"""
    
    def test_get_descriptive_stats(self, sample_dataframe):
        """测试获取描述性统计"""
        analyzer = DataAnalyzer(sample_dataframe)
        stats = analyzer.get_descriptive_stats('pre_tax_salary')
        
        assert isinstance(stats, dict)
        assert len(stats) > 0
    
    def test_get_grouped_stats(self, sample_dataframe):
        """测试分组统计"""
        analyzer = DataAnalyzer(sample_dataframe)
        result = analyzer.get_grouped_stats('department', 'pre_tax_salary')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_frequency_analysis(self, sample_dataframe):
        """测试频率分析"""
        analyzer = DataAnalyzer(sample_dataframe)
        result = analyzer.get_frequency_analysis('department')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_crosstab(self, sample_dataframe):
        """测试交叉分析"""
        analyzer = DataAnalyzer(sample_dataframe)
        result = analyzer.get_crosstab('department', 'gender')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_correlation_matrix(self, sample_dataframe):
        """测试相关性矩阵"""
        analyzer = DataAnalyzer(sample_dataframe)
        result = analyzer.get_correlation_matrix()
        
        assert isinstance(result, pd.DataFrame)
        # 相关性矩阵应该是方阵
        assert result.shape[0] == result.shape[1]
    
    def test_get_summary_report(self, sample_dataframe):
        """测试汇总报告"""
        analyzer = DataAnalyzer(sample_dataframe)
        report = analyzer.get_summary_report('pre_tax_salary')
        
        assert isinstance(report, dict)
        assert 'total_records' in report
    
    def test_compare_by_dimension(self, sample_dataframe):
        """测试按维度比较"""
        analyzer = DataAnalyzer(sample_dataframe)
        result = analyzer.compare_by_dimension('department', 'pre_tax_salary')
        
        assert isinstance(result, pd.DataFrame)


class TestDataVisualizer:
    """测试DataVisualizer类"""
    
    def test_create_bar_chart(self, sample_dataframe):
        """测试创建柱状图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_bar_chart(sample_dataframe, 'department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_bar_chart_horizontal(self, sample_dataframe):
        """测试创建水平柱状图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_bar_chart(sample_dataframe, 'department', 'pre_tax_salary', horizontal=True)
        
        assert isinstance(fig, Figure)
    
    def test_create_pie_chart(self, sample_dataframe):
        """测试创建饼图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_pie_chart(sample_dataframe, 'department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_line_chart(self, sample_dataframe):
        """测试创建折线图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_line_chart(sample_dataframe, 'work_years', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_scatter_chart(self, sample_dataframe):
        """测试创建散点图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_scatter_chart(sample_dataframe, 'work_years', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_boxplot(self, sample_dataframe):
        """测试创建箱线图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_boxplot(sample_dataframe, 'department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_histogram(self, sample_dataframe):
        """测试创建直方图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_histogram(sample_dataframe, 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_heatmap(self, sample_dataframe):
        """测试创建热力图"""
        visualizer = DataVisualizerAdapter()
        fig = visualizer.create_heatmap(sample_dataframe)
        
        assert isinstance(fig, Figure)
    
    def test_set_custom_style(self, sample_dataframe):
        """测试设置自定义样式"""
        custom_style = {
            'figure_size': (10, 6),
            'dpi': 100
        }
        
        visualizer = DataVisualizerAdapter(custom_style)
        fig = visualizer.create_bar_chart(sample_dataframe, 'department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
