import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json

from ..exceptions import ConfigurationError


@dataclass
class AppConfig:
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
    chart_colors: List[str] = field(default_factory=lambda: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'])
    figure_size: tuple = (10, 6)
    dpi: int = 100
    title_fontsize: int = 14
    label_fontsize: int = 12
    tick_fontsize: int = 10
    legend_fontsize: int = 10


class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._app_config: AppConfig = AppConfig()
        
        if config_path and os.path.exists(config_path):
            self.load()
    
    def load(self) -> None:
        if not self.config_path:
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            self._apply_config()
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"配置文件格式错误: {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"加载配置文件失败: {str(e)}")
    
    def _apply_config(self) -> None:
        if 'field_mapping' in self._config:
            self._app_config.field_mapping = self._config['field_mapping']
        if 'salary_bins' in self._config:
            self._app_config.salary_bins = self._config['salary_bins']
        if 'salary_labels' in self._config:
            self._app_config.salary_labels = self._config['salary_labels']
        if 'age_bins' in self._config:
            self._app_config.age_bins = self._config['age_bins']
        if 'age_labels' in self._config:
            self._app_config.age_labels = self._config['age_labels']
        if 'experience_bins' in self._config:
            self._app_config.experience_bins = self._config['experience_bins']
        if 'experience_labels' in self._config:
            self._app_config.experience_labels = self._config['experience_labels']
        if 'chart_colors' in self._config:
            self._app_config.chart_colors = self._config['chart_colors']
        if 'figure_size' in self._config:
            self._app_config.figure_size = tuple(self._config['figure_size'])
        if 'dpi' in self._config:
            self._app_config.dpi = self._config['dpi']
    
    def save(self) -> None:
        if not self.config_path:
            return
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConfigurationError(f"保存配置文件失败: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
    
    def get_field_mapping(self) -> Dict[str, str]:
        return self._app_config.field_mapping.copy()
    
    def get_salary_bins(self) -> List[float]:
        return self._app_config.salary_bins.copy()
    
    def get_salary_labels(self) -> List[str]:
        return self._app_config.salary_labels.copy()
    
    def get_age_bins(self) -> List[int]:
        return self._app_config.age_bins.copy()
    
    def get_age_labels(self) -> List[str]:
        return self._app_config.age_labels.copy()
    
    def get_experience_bins(self) -> List[float]:
        return self._app_config.experience_bins.copy()
    
    def get_experience_labels(self) -> List[str]:
        return self._app_config.experience_labels.copy()
    
    def get_chart_colors(self) -> List[str]:
        return self._app_config.chart_colors.copy()
    
    def get_figure_size(self) -> tuple:
        return self._app_config.figure_size
    
    def get_dpi(self) -> int:
        return self._app_config.dpi
    
    def get_app_config(self) -> AppConfig:
        return self._app_config
