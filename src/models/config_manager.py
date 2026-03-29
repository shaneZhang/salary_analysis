"""
配置管理器模块
管理系统配置，支持配置文件读写
"""

import os
import yaml
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
from .logger import get_logger, LoggerMixin
from ..exceptions import ConfigurationException


@dataclass
class AppConfig:
    """应用配置数据类"""
    
    field_mapping: Dict[str, str] = field(default_factory=lambda: {
        '姓名': 'name',
        '性别': 'gender',
        '年龄': 'age',
        '学历': 'education',
        '工作年限': 'work_years',
        '所在行业': 'industry',
        '岗位类型': 'position_type',
        '职级': 'level',
        '基本工资': 'base_salary',
        '绩效奖金': 'performance_bonus',
        '补贴总和': 'allowance',
        '税前薪资': 'pre_tax_salary',
        '税后薪资': 'post_tax_salary',
        '所属企业规模': 'company_size',
        '入职年份': 'join_year'
    })
    
    salary_bins: List[float] = field(default_factory=lambda: [0, 5000, 10000, 15000, 20000, 30000, 50000, float('inf')])
    salary_labels: List[str] = field(default_factory=lambda: ['5千以下', '5千-1万', '1万-1.5万', '1.5万-2万', '2万-3万', '3万-5万', '5万以上'])
    
    age_bins: List[int] = field(default_factory=lambda: [0, 25, 30, 35, 40, 50, 60, 100])
    age_labels: List[str] = field(default_factory=lambda: ['25岁以下', '25-30岁', '30-35岁', '35-40岁', '40-50岁', '50-60岁', '60岁以上'])
    
    experience_bins: List[float] = field(default_factory=lambda: [0, 1, 3, 5, 10, 15, 20, float('inf')])
    experience_labels: List[str] = field(default_factory=lambda: ['1年以下', '1-3年', '3-5年', '5-10年', '10-15年', '15-20年', '20年以上'])
    
    chart_colors: List[str] = field(default_factory=lambda: [
        '#3498db', '#e74c3c', '#2ecc71', '#f39c12', 
        '#9b59b6', '#1abc9c', '#e67e22', '#34495e'
    ])
    
    figure_size: tuple = (10, 6)
    dpi: int = 100
    
    app_title: str = '园区白领薪资数据分析工具'
    window_size: tuple = (1400, 800)


class ConfigManager(LoggerMixin):
    """
    配置管理器
    支持从YAML文件加载配置
    """
    
    DEFAULT_CONFIG_FILE = 'config.yaml'
    
    def __init__(self, config_path: Optional[str] = None):
        self._config_path = config_path
        self._config = AppConfig()
        self._custom_settings: Dict[str, Any] = {}
        
        if config_path:
            self.load(config_path)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
        """
        keys = key.split('.')
        value = self._get_config_dict()
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        self._custom_settings[key] = value
    
    def _get_config_dict(self) -> Dict[str, Any]:
        """获取配置字典"""
        config_dict = {
            'field_mapping': self._config.field_mapping,
            'salary_bins': self._config.salary_bins,
            'salary_labels': self._config.salary_labels,
            'age_bins': self._config.age_bins,
            'age_labels': self._config.age_labels,
            'experience_bins': self._config.experience_bins,
            'experience_labels': self._config.experience_labels,
            'chart_colors': self._config.chart_colors,
            'figure_size': list(self._config.figure_size),
            'dpi': self._config.dpi,
            'app_title': self._config.app_title,
            'window_size': list(self._config.window_size),
        }
        config_dict.update(self._custom_settings)
        return config_dict
    
    def load(self, config_path: Optional[str] = None) -> None:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
        """
        path = config_path or self._config_path
        
        if not path:
            path = self._find_config_file()
        
        if not path or not os.path.exists(path):
            self.logger.info("No config file found, using defaults")
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            if config_data:
                self._apply_config(config_data)
                self._config_path = path
                self.logger.info(f"Config loaded from {path}")
                
        except Exception as e:
            raise ConfigurationException(f"Failed to load config: {e}")
    
    def _find_config_file(self) -> Optional[str]:
        """查找配置文件"""
        search_paths = [
            self.DEFAULT_CONFIG_FILE,
            os.path.join('config', self.DEFAULT_CONFIG_FILE),
            os.path.join(os.path.dirname(__file__), '..', '..', self.DEFAULT_CONFIG_FILE),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _apply_config(self, config_data: Dict[str, Any]) -> None:
        """应用配置数据"""
        if 'field_mapping' in config_data:
            self._config.field_mapping.update(config_data['field_mapping'])
        
        if 'salary_bins' in config_data:
            self._config.salary_bins = config_data['salary_bins']
        
        if 'salary_labels' in config_data:
            self._config.salary_labels = config_data['salary_labels']
        
        if 'age_bins' in config_data:
            self._config.age_bins = config_data['age_bins']
        
        if 'age_labels' in config_data:
            self._config.age_labels = config_data['age_labels']
        
        if 'experience_bins' in config_data:
            self._config.experience_bins = config_data['experience_bins']
        
        if 'experience_labels' in config_data:
            self._config.experience_labels = config_data['experience_labels']
        
        if 'chart_colors' in config_data:
            self._config.chart_colors = config_data['chart_colors']
        
        if 'figure_size' in config_data:
            self._config.figure_size = tuple(config_data['figure_size'])
        
        if 'dpi' in config_data:
            self._config.dpi = config_data['dpi']
        
        if 'app_title' in config_data:
            self._config.app_title = config_data['app_title']
        
        if 'window_size' in config_data:
            self._config.window_size = tuple(config_data['window_size'])
        
        for key, value in config_data.items():
            if key not in ['field_mapping', 'salary_bins', 'salary_labels', 
                          'age_bins', 'age_labels', 'experience_bins', 
                          'experience_labels', 'chart_colors', 'figure_size',
                          'dpi', 'app_title', 'window_size']:
                self._custom_settings[key] = value
    
    def save(self, config_path: Optional[str] = None) -> None:
        """保存配置到文件"""
        path = config_path or self._config_path or self.DEFAULT_CONFIG_FILE
        
        try:
            config_dict = self._get_config_dict()
            
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, allow_unicode=True, default_flow_style=False)
            
            self.logger.info(f"Config saved to {path}")
            
        except Exception as e:
            raise ConfigurationException(f"Failed to save config: {e}")
    
    def get_field_mapping(self) -> Dict[str, str]:
        """获取字段映射"""
        return self._config.field_mapping.copy()
    
    def get_salary_bins(self) -> List[float]:
        """获取薪资分组区间"""
        return self._config.salary_bins.copy()
    
    def get_salary_labels(self) -> List[str]:
        """获取薪资分组标签"""
        return self._config.salary_labels.copy()
    
    def get_age_bins(self) -> List[int]:
        """获取年龄分组区间"""
        return self._config.age_bins.copy()
    
    def get_age_labels(self) -> List[str]:
        """获取年龄分组标签"""
        return self._config.age_labels.copy()
    
    def get_experience_bins(self) -> List[float]:
        """获取工作年限分组区间"""
        return self._config.experience_bins.copy()
    
    def get_experience_labels(self) -> List[str]:
        """获取工作年限分组标签"""
        return self._config.experience_labels.copy()
    
    def get_chart_colors(self) -> List[str]:
        """获取图表颜色"""
        return self._config.chart_colors.copy()
    
    def get_app_config(self) -> AppConfig:
        """获取应用配置对象"""
        return self._config
