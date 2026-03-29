import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
import yaml

from src.exceptions import ConfigurationException


@dataclass
class AppConfig:
    """应用配置数据类"""
    
    # 字段映射配置
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
    
    # 薪资分组区间
    salary_bins: List[float] = field(default_factory=lambda: [
        0, 5000, 8000, 10000, 15000, 20000, 30000, 50000, float('inf')
    ])
    
    salary_labels: List[str] = field(default_factory=lambda: [
        '5千以下', '5千-8千', '8千-1万', '1万-1.5万',
        '1.5万-2万', '2万-3万', '3万-5万', '5万以上'
    ])
    
    # 年龄分组区间
    age_bins: List[int] = field(default_factory=lambda: [0, 25, 30, 35, 40, 50, 60, 100])
    
    age_labels: List[str] = field(default_factory=lambda: [
        '25岁以下', '25-30岁', '30-35岁', '35-40岁',
        '40-50岁', '50-60岁', '60岁以上'
    ])
    
    # 工作年限分组区间
    experience_bins: List[float] = field(default_factory=lambda: [
        0, 1, 3, 5, 10, 15, 20, float('inf')
    ])
    
    experience_labels: List[str] = field(default_factory=lambda: [
        '1年以下', '1-3年', '3-5年', '5-10年',
        '10-15年', '15-20年', '20年以上'
    ])
    
    # 图表颜色配置
    chart_colors: List[str] = field(default_factory=lambda: [
        '#3498db', '#e74c3c', '#2ecc71', '#f39c12',
        '#9b59b6', '#1abc9c', '#e67e22', '#34495e'
    ])
    
    # 图表配置
    figure_size: tuple = (10, 6)
    dpi: int = 100
    title_fontsize: int = 14
    label_fontsize: int = 12
    tick_fontsize: int = 10
    
    # 薪资字段候选列表
    salary_candidates: List[str] = field(default_factory=lambda: [
        'pre_tax_salary', 'post_tax_salary', 'base_salary', 'total_salary'
    ])


class ConfigManager:
    """配置管理器
    
    负责加载、保存和管理应用配置。
    支持单例模式以确保全局配置一致性。
    """
    
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls, config_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_path: Optional[str] = None):
        if self._initialized:
            return
        self._config = AppConfig()
        self._config_path = config_path or self._get_default_config_path()
        self._initialized = True
    
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, 'config.yaml')
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        支持点号分隔的嵌套键，如 'chart_config.title_fontsize'
        """
        config_dict = asdict(self._config)
        keys = key.split('.')
        
        value = config_dict
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        if hasattr(self._config, key):
            setattr(self._config, key, value)
        else:
            # 尝试设置嵌套属性
            config_dict = asdict(self._config)
            keys = key.split('.')
            
            if len(keys) > 1:
                current = config_dict
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value
                self._update_config_from_dict(config_dict)
            else:
                raise ConfigurationException(f"未知配置项: {key}")
    
    def get_config(self) -> AppConfig:
        """获取配置对象"""
        return self._config
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self._config)
    
    def load(self) -> None:
        """从配置文件加载配置"""
        if not os.path.exists(self._config_path):
            return
        
        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
            
            if config_dict:
                self._update_config_from_dict(config_dict)
        except Exception as e:
            raise ConfigurationException(f"加载配置文件失败: {str(e)}") from e
    
    def save(self) -> None:
        """保存配置到文件"""
        try:
            config_dict = asdict(self._config)
            
            with open(self._config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True, indent=2)
        except Exception as e:
            raise ConfigurationException(f"保存配置文件失败: {str(e)}") from e
    
    def _update_config_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """从字典更新配置"""
        for key, value in config_dict.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
    
    def get_field_mapping(self) -> Dict[str, str]:
        """获取字段映射配置"""
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
        """获取图表颜色配置"""
        return self._config.chart_colors.copy()
    
    def get_salary_candidates(self) -> List[str]:
        """获取薪资字段候选列表"""
        return self._config.salary_candidates.copy()
    
    @property
    def config(self) -> AppConfig:
        """获取当前配置对象"""
        return self._config
