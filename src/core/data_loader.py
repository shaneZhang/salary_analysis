import pandas as pd
import os
from typing import Optional, List, Dict, Tuple

from src.exceptions import (
    DataLoadError,
    DataValidationError,
    FileFormatError
)


class DataLoader:
    """数据加载器
    
    负责从各种数据源加载数据，不包含任何GUI依赖。
    """
    
    def __init__(self, field_mapping: Optional[Dict[str, str]] = None):
        self.data: Optional[pd.DataFrame] = None
        self.file_path: Optional[str] = None
        self.sheet_names: List[str] = []
        
        self.field_mapping = field_mapping or {
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
        }
    
    def get_sheet_names(self, file_path: str) -> List[str]:
        """获取Excel文件的工作表名称"""
        try:
            xl_file = pd.ExcelFile(file_path)
            self.sheet_names = xl_file.sheet_names
            return self.sheet_names
        except Exception as e:
            raise FileFormatError(f"读取工作表失败: {str(e)}") from e
    
    def load_excel(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """加载Excel文件
        
        Args:
            file_path: Excel文件路径
            sheet_name: 工作表名称，默认为第一个工作表
            
        Returns:
            加载的数据DataFrame
            
        Raises:
            DataLoadError: 加载失败时抛出
        """
        try:
            if sheet_name:
                self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                self.data = pd.read_excel(file_path)
            
            self.file_path = file_path
            self._auto_map_fields()
            return self.data
            
        except Exception as e:
            raise DataLoadError(f"读取Excel文件失败: {str(e)}") from e
    
    def load_multiple_files(self, file_paths: List[str]) -> pd.DataFrame:
        """批量加载多个Excel文件并合并"""
        try:
            dfs = []
            for file_path in file_paths:
                df = pd.read_excel(file_path)
                dfs.append(df)
            
            if dfs:
                self.data = pd.concat(dfs, ignore_index=True)
                self._auto_map_fields()
                return self.data
            
            raise DataLoadError("没有加载到任何数据")
            
        except Exception as e:
            raise DataLoadError(f"批量导入失败: {str(e)}") from e
    
    def load_folder(self, folder_path: str) -> pd.DataFrame:
        """加载文件夹中的所有Excel文件"""
        try:
            excel_files = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(('.xlsx', '.xls')):
                        excel_files.append(os.path.join(root, file))
            
            if not excel_files:
                raise DataLoadError("文件夹中没有找到Excel文件")
            
            return self.load_multiple_files(excel_files)
            
        except DataLoadError:
            raise
        except Exception as e:
            raise DataLoadError(f"读取文件夹失败: {str(e)}") from e
    
    def _auto_map_fields(self):
        """自动映射字段名称"""
        if self.data is None:
            return
        
        new_columns = {}
        for col in self.data.columns:
            col_lower = str(col).lower().strip()
            for chinese, english in self.field_mapping.items():
                if chinese == col or col_lower == chinese.lower():
                    new_columns[col] = english
                    break
        
        if new_columns:
            self.data.rename(columns=new_columns, inplace=True)
    
    def get_preview(self, n: int = 10) -> Optional[pd.DataFrame]:
        """获取数据预览"""
        if self.data is None:
            return None
        return self.data.head(n)
    
    def get_data_info(self) -> Dict:
        """获取数据信息"""
        if self.data is None:
            return {}
        
        return {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_names': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict()
        }
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """验证数据有效性"""
        if self.data is None:
            return False, ['没有加载数据']
        
        errors = []
        
        numeric_cols = ['age', 'work_years', 'base_salary', 'performance_bonus', 
                       'allowance', 'pre_tax_salary', 'post_tax_salary', 'join_year']
        
        for col in numeric_cols:
            if col in self.data.columns:
                non_numeric = pd.to_numeric(self.data[col], errors='coerce')
                null_count = non_numeric.isnull().sum()
                if null_count > 0:
                    errors.append(f"字段 '{col}' 存在 {null_count} 个无效数值")
        
        if errors:
            return False, errors
        return True, []
    
    def get_field_mapping(self) -> Dict[str, str]:
        """获取字段映射"""
        return self.field_mapping.copy()
    
    def apply_field_mapping(self, mapping: Dict[str, str]):
        """应用自定义字段映射"""
        if self.data is not None and mapping:
            self.data.rename(columns=mapping, inplace=True)
    
    def export_data(self, data: pd.DataFrame, output_path: str, format: str = 'excel') -> bool:
        """导出数据到文件"""
        try:
            if format == 'excel':
                data.to_excel(output_path, index=False)
            elif format == 'csv':
                data.to_csv(output_path, index=False, encoding='utf-8-sig')
            else:
                raise DataLoadError(f"不支持的格式: {format}")
            
            return True
            
        except Exception as e:
            raise DataLoadError(f"导出失败: {str(e)}") from e
    
    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """检查是否为支持的文件格式"""
        return file_path.lower().endswith(('.xlsx', '.xls', '.csv'))
