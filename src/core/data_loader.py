"""
数据加载模块（重构版）
移除GUI依赖，改为纯业务逻辑
"""

import pandas as pd
import os
from typing import Optional, List, Dict, Tuple
from ..exceptions import DataLoadError, DataValidationError
from ..models.logger import LoggerMixin


class DataLoader(LoggerMixin):
    """
    数据加载器
    负责从各种来源加载数据
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
    
    def load_excel(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        加载Excel文件
        
        Args:
            file_path: 文件路径
            sheet_name: 工作表名称
            
        Returns:
            加载的数据框
            
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
            self.logger.info(f"Loaded Excel file: {file_path}, rows: {len(self.data)}")
            return self.data
            
        except Exception as e:
            raise DataLoadError(f"读取Excel文件失败: {str(e)}", details=file_path) from e
    
    def load_multiple_files(self, file_paths: List[str]) -> pd.DataFrame:
        """
        加载多个文件
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            合并后的数据框
        """
        try:
            dfs = []
            for file_path in file_paths:
                df = pd.read_excel(file_path)
                dfs.append(df)
            
            if dfs:
                self.data = pd.concat(dfs, ignore_index=True)
                self._auto_map_fields()
                self.logger.info(f"Loaded {len(file_paths)} files, total rows: {len(self.data)}")
                return self.data
            
            raise DataLoadError("没有可加载的文件")
            
        except DataLoadError:
            raise
        except Exception as e:
            raise DataLoadError(f"批量导入失败: {str(e)}") from e
    
    def load_folder(self, folder_path: str) -> pd.DataFrame:
        """
        加载文件夹中的所有Excel文件
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            合并后的数据框
        """
        try:
            excel_files = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(('.xlsx', '.xls')):
                        excel_files.append(os.path.join(root, file))
            
            if not excel_files:
                raise DataLoadError(f"文件夹中没有找到Excel文件: {folder_path}")
            
            self.logger.info(f"Found {len(excel_files)} Excel files in folder")
            return self.load_multiple_files(excel_files)
            
        except DataLoadError:
            raise
        except Exception as e:
            raise DataLoadError(f"读取文件夹失败: {str(e)}") from e
    
    def get_sheet_names(self, file_path: str) -> List[str]:
        """
        获取Excel文件的工作表名称
        
        Args:
            file_path: 文件路径
            
        Returns:
            工作表名称列表
        """
        try:
            xl_file = pd.ExcelFile(file_path)
            self.sheet_names = xl_file.sheet_names
            return self.sheet_names
        except Exception as e:
            raise DataLoadError(f"读取工作表失败: {str(e)}") from e
    
    def _auto_map_fields(self) -> None:
        """自动映射字段名"""
        if self.data is None:
            return
        
        new_columns = {}
        for col in self.data.columns:
            col_lower = col.lower().strip()
            for chinese, english in self.field_mapping.items():
                if chinese == col or col_lower == chinese.lower():
                    new_columns[col] = english
                    break
        
        if new_columns:
            self.data.rename(columns=new_columns, inplace=True)
            self.logger.debug(f"Auto-mapped fields: {new_columns}")
    
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
        """
        验证数据
        
        Returns:
            (是否有效, 错误列表)
        """
        if self.data is None:
            return False, ['没有加载数据']
        
        errors = []
        
        numeric_cols = ['age', 'work_years', 'base_salary', 'performance_bonus', 
                       'allowance', 'pre_tax_salary', 'post_tax_salary', 'join_year']
        
        for col in numeric_cols:
            if col in self.data.columns:
                non_numeric = pd.to_numeric(self.data[col], errors='coerce')
                null_count = non_numeric.isnull().sum()
                original_nulls = self.data[col].isnull().sum()
                if null_count > original_nulls:
                    errors.append(f"字段 '{col}' 存在 {null_count - original_nulls} 个无效数值")
        
        if errors:
            return False, errors
        return True, []
    
    def get_field_mapping(self) -> Dict[str, str]:
        """获取字段映射"""
        return self.field_mapping.copy()
    
    def set_field_mapping(self, mapping: Dict[str, str]) -> None:
        """设置字段映射"""
        self.field_mapping.update(mapping)
    
    def apply_field_mapping(self, mapping: Dict[str, str]) -> None:
        """应用字段映射到当前数据"""
        if self.data is not None and mapping:
            self.data.rename(columns=mapping, inplace=True)
    
    def export_data(self, output_path: str, format: str = 'excel') -> bool:
        """
        导出数据
        
        Args:
            output_path: 输出路径
            format: 格式 ('excel' 或 'csv')
            
        Returns:
            是否成功
        """
        if self.data is None:
            raise DataValidationError("没有可导出的数据")
        
        try:
            if format == 'excel':
                self.data.to_excel(output_path, index=False)
            elif format == 'csv':
                self.data.to_csv(output_path, index=False, encoding='utf-8-sig')
            else:
                raise DataValidationError(f"不支持的格式: {format}")
            
            self.logger.info(f"Data exported to: {output_path}")
            return True
            
        except Exception as e:
            raise DataLoadError(f"导出失败: {str(e)}") from e
