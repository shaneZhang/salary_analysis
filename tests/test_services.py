import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from matplotlib.figure import Figure

from src.models import DataManager, ConfigManager
from src.services import DataService, ProcessingService, AnalysisService, VisualizationService


class TestDataService:
    """测试DataService类"""
    
    def setup_method(self):
        """每个测试前重置DataManager"""
        dm = DataManager()
        dm.reset()
    
    def test_load_file(self, temp_excel_file):
        """测试加载文件"""
        dm = DataManager()
        cm = ConfigManager()
        service = DataService(dm, cm)
        
        service.load_file(temp_excel_file)
        
        assert service.has_data()
        assert len(service.get_current_data()) == 100
    
    def test_load_folder(self, tmp_path, sample_dataframe):
        """测试加载文件夹"""
        for i in range(3):
            file_path = tmp_path / f"data_{i}.xlsx"
            sample_dataframe.to_excel(file_path, index=False)
        
        dm = DataManager()
        cm = ConfigManager()
        service = DataService(dm, cm)
        
        service.load_folder(str(tmp_path))
        
        assert service.has_data()
        assert len(service.get_current_data()) == 300
    
    def test_export_data_excel(self, sample_dataframe, tmp_path):
        """测试导出Excel"""
        dm = DataManager()
        cm = ConfigManager()
        service = DataService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        export_path = tmp_path / "exported_data.xlsx"
        service.export_data(str(export_path), format_type='excel')
        
        assert os.path.exists(export_path)
    
    def test_export_data_csv(self, sample_dataframe, tmp_path):
        """测试导出CSV"""
        dm = DataManager()
        cm = ConfigManager()
        service = DataService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        export_path = tmp_path / "exported_data.csv"
        service.export_data(str(export_path), format_type='csv')
        
        assert os.path.exists(export_path)
    
    def test_get_data_info(self, sample_dataframe):
        """测试获取数据信息"""
        dm = DataManager()
        cm = ConfigManager()
        service = DataService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        info = service.get_data_info()
        assert isinstance(info, dict)
        assert info['rows'] == 100
        assert info['columns'] == len(sample_dataframe.columns)
    
    def test_reset_data(self, sample_dataframe):
        """测试重置数据"""
        dm = DataManager()
        cm = ConfigManager()
        service = DataService(dm, cm)
        
        dm.set_data(sample_dataframe)
        assert service.has_data()
        
        service.reset_data()
        assert not service.has_data()


class TestProcessingService:
    """测试ProcessingService类"""
    
    def setup_method(self):
        """每个测试前重置DataManager"""
        dm = DataManager()
        dm.reset()
    
    def test_remove_duplicates(self, sample_dataframe_with_duplicates):
        """测试删除重复数据"""
        dm = DataManager()
        cm = ConfigManager()
        service = ProcessingService(dm, cm)
        
        dm.set_data(sample_dataframe_with_duplicates)
        original_count = len(sample_dataframe_with_duplicates)
        
        count = service.remove_duplicates()
        
        assert count == 10  # 重复了10条
        assert len(dm.get_data()) == original_count - 10
    
    def test_handle_missing_values(self, sample_dataframe_with_missing):
        """测试处理缺失值"""
        dm = DataManager()
        cm = ConfigManager()
        service = ProcessingService(dm, cm)
        
        dm.set_data(sample_dataframe_with_missing)
        
        result = service.handle_missing_values('drop')
        
        assert isinstance(result, dict)
        assert sum(result.values()) > 0
    
    def test_remove_outliers(self, sample_dataframe):
        """测试移除异常值"""
        dm = DataManager()
        cm = ConfigManager()
        service = ProcessingService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        count = service.remove_outliers('pre_tax_salary')
        
        assert isinstance(count, int)
    
    def test_create_age_group(self, sample_dataframe):
        """测试创建年龄分组"""
        dm = DataManager()
        cm = ConfigManager()
        service = ProcessingService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.create_age_group()
        
        assert result == True
        assert 'age_group' in dm.get_data().columns
    
    def test_create_salary_group(self, sample_dataframe):
        """测试创建薪资分组"""
        dm = DataManager()
        cm = ConfigManager()
        service = ProcessingService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.create_salary_group('pre_tax_salary')
        
        assert result == True
        assert 'salary_group' in dm.get_data().columns
    
    def test_create_work_experience_group(self, sample_dataframe):
        """测试创建工作年限分组"""
        dm = DataManager()
        cm = ConfigManager()
        service = ProcessingService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.create_work_experience_group()
        
        assert result == True
        assert 'experience_group' in dm.get_data().columns


class TestAnalysisService:
    """测试AnalysisService类"""
    
    def setup_method(self):
        """每个测试前重置DataManager"""
        dm = DataManager()
        dm.reset()
    
    def test_get_descriptive_stats(self, sample_dataframe):
        """测试获取描述性统计"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        stats = service.get_descriptive_stats('pre_tax_salary')
        
        assert isinstance(stats, dict)
        assert 'mean' in stats
        assert 'std' in stats
    
    def test_get_grouped_stats(self, sample_dataframe):
        """测试分组统计"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.get_grouped_stats('department', 'pre_tax_salary')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_frequency_analysis(self, sample_dataframe):
        """测试频率分析"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.get_frequency_analysis('department')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_crosstab(self, sample_dataframe):
        """测试交叉分析"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.get_crosstab('department', 'gender')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_correlation_matrix(self, sample_dataframe):
        """测试相关性矩阵"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.get_correlation_matrix()
        
        assert isinstance(result, pd.DataFrame)
    
    def test_compare_by_dimension(self, sample_dataframe):
        """测试按维度比较"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        result = service.compare_by_dimension('department', 'pre_tax_salary')
        
        assert isinstance(result, pd.DataFrame)
    
    def test_get_available_dimensions(self, sample_dataframe):
        """测试获取可用维度"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        dimensions = service.get_available_dimensions()
        
        assert isinstance(dimensions, list)
        assert len(dimensions) > 0
    
    def test_get_numeric_columns(self, sample_dataframe):
        """测试获取数值列"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        columns = service.get_numeric_columns()
        
        assert isinstance(columns, list)
        assert 'pre_tax_salary' in columns
    
    def test_get_salary_columns(self, sample_dataframe):
        """测试获取薪资列"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        columns = service.get_salary_columns()
        
        assert isinstance(columns, list)
    
    def test_get_summary_report(self, sample_dataframe):
        """测试获取汇总报告"""
        dm = DataManager()
        cm = ConfigManager()
        service = AnalysisService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        report = service.get_summary_report('pre_tax_salary')
        
        assert isinstance(report, dict)
        assert 'total_records' in report
        assert report['total_records'] == 100


class TestVisualizationService:
    """测试VisualizationService类"""
    
    def setup_method(self):
        """每个测试前重置DataManager"""
        dm = DataManager()
        dm.reset()
    
    def test_create_bar_chart(self, sample_dataframe):
        """测试创建柱状图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_bar_chart('department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_pie_chart(self, sample_dataframe):
        """测试创建饼图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_pie_chart('department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_line_chart(self, sample_dataframe):
        """测试创建折线图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_line_chart('work_years', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_scatter_chart(self, sample_dataframe):
        """测试创建散点图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_scatter_chart('work_years', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_boxplot(self, sample_dataframe):
        """测试创建箱线图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_boxplot('department', 'pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_histogram(self, sample_dataframe):
        """测试创建直方图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_histogram('pre_tax_salary')
        
        assert isinstance(fig, Figure)
    
    def test_create_heatmap(self, sample_dataframe):
        """测试创建热力图"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        fig = service.create_heatmap()
        
        assert isinstance(fig, Figure)
    
    def test_get_current_figure(self, sample_dataframe):
        """测试获取当前图表"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        assert service.get_current_figure() is None
        
        fig = service.create_bar_chart('department', 'pre_tax_salary')
        
        current_fig = service.get_current_figure()
        assert current_fig is not None
        assert isinstance(current_fig, Figure)
    
    def test_save_current_chart(self, sample_dataframe, tmp_path):
        """测试保存当前图表"""
        dm = DataManager()
        cm = ConfigManager()
        service = VisualizationService(dm, cm)
        
        dm.set_data(sample_dataframe)
        
        service.create_bar_chart('department', 'pre_tax_salary')
        
        save_path = tmp_path / "chart.png"
        service.save_current_chart(str(save_path))
        
        assert os.path.exists(save_path)
