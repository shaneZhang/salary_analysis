"""
数据控制器模块
处理数据相关的用户操作
"""

from typing import Optional, Any, Dict
from ..services.data_service import DataService
from ..services.processing_service import ProcessingService
from ..models.data_manager import DataManager
from ..models.app_state import AppStatusManager, AppState
from ..views.dialogs import Dialogs
from ..models.logger import LoggerMixin


class DataController(LoggerMixin):
    """数据控制器"""
    
    def __init__(self, data_service: DataService, processing_service: ProcessingService,
                 data_manager: DataManager, status_manager: AppStatusManager):
        self._data_service = data_service
        self._processing_service = processing_service
        self._data_manager = data_manager
        self._status_manager = status_manager
        self._view: Optional[Any] = None
    
    def set_view(self, view: Any) -> None:
        """设置视图"""
        self._view = view
    
    def load_file(self) -> None:
        """加载文件"""
        file_path = Dialogs.select_file('选择Excel文件')
        
        if not file_path:
            return
        
        self._status_manager.set_loading(f'正在加载: {file_path}')
        
        result = self._data_service.load_file(file_path)
        
        if result.get('success'):
            self._update_view_after_load(result)
            Dialogs.show_info('成功', f"数据加载成功！\n共 {result['rows']} 条记录")
            self._status_manager.set_idle('数据加载成功')
        else:
            Dialogs.show_error('错误', f"加载失败: {result.get('error')}")
            self._status_manager.set_error('数据加载失败')
    
    def load_folder(self) -> None:
        """加载文件夹"""
        folder_path = Dialogs.select_folder('选择文件夹')
        
        if not folder_path:
            return
        
        self._status_manager.set_loading(f'正在加载文件夹: {folder_path}')
        
        result = self._data_service.load_folder(folder_path)
        
        if result.get('success'):
            self._update_view_after_load(result)
            Dialogs.show_info('成功', f"数据加载成功！\n共 {result['rows']} 条记录")
            self._status_manager.set_idle('数据加载成功')
        else:
            Dialogs.show_error('错误', f"加载失败: {result.get('error')}")
            self._status_manager.set_error('数据加载失败')
    
    def export_data(self) -> None:
        """导出数据"""
        if not self._data_service.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        output_path = Dialogs.save_file('保存数据', '.xlsx')
        
        if not output_path:
            return
        
        file_format = 'excel' if output_path.endswith('.xlsx') else 'csv'
        result = self._data_service.export_data(output_path, file_format)
        
        if result.get('success'):
            Dialogs.show_info('成功', f"数据已导出到: {output_path}")
        else:
            Dialogs.show_error('错误', f"导出失败: {result.get('error')}")
    
    def clean_data(self, operation: str = None) -> None:
        """数据清洗"""
        if not self._data_service.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        if operation:
            self._execute_clean(operation)
        else:
            from ..views.dialogs import DataCleanDialog
            dialog = DataCleanDialog(
                self._view.root if self._view else None,
                self._execute_clean
            )
            dialog.show()
    
    def _execute_clean(self, operation: str) -> None:
        """执行清洗操作"""
        result = None
        
        if operation == 'duplicates':
            result = self._processing_service.remove_duplicates()
            if result.get('success'):
                Dialogs.show_info('完成', f"删除了 {result['removed_count']} 条重复记录")
        
        elif operation == 'missing':
            result = self._processing_service.handle_missing_values('drop')
            if result.get('success'):
                Dialogs.show_info('完成', f"处理了 {result['total_processed']} 个缺失值")
        
        elif operation == 'fill_mean':
            result = self._processing_service.handle_missing_values('fill_mean')
            if result.get('success'):
                Dialogs.show_info('完成', '已用均值填充数值型缺失值')
        
        elif operation == 'outliers':
            salary_col = self._get_salary_column()
            result = self._processing_service.remove_outliers(salary_col)
            if result.get('success'):
                Dialogs.show_info('完成', f"移除了 {result['removed_count']} 条异常值记录")
        
        if result and result.get('success'):
            self._update_view_info()
    
    def group_data(self, group_type: str = None) -> None:
        """数据分组"""
        if not self._data_service.has_data():
            Dialogs.show_warning('警告', '请先加载数据')
            return
        
        if group_type:
            self._execute_group(group_type)
        else:
            from ..views.dialogs import DataGroupDialog
            dialog = DataGroupDialog(
                self._view.root if self._view else None,
                self._execute_group
            )
            dialog.show()
    
    def _execute_group(self, group_type: str) -> None:
        """执行分组操作"""
        result = None
        
        if group_type == 'age':
            result = self._processing_service.create_age_group()
            if result.get('success'):
                Dialogs.show_info('完成', '已创建年龄分组字段: age_group')
            else:
                Dialogs.show_warning('警告', '数据中没有年龄字段')
        
        elif group_type == 'salary':
            salary_col = self._get_salary_column()
            result = self._processing_service.create_salary_group(salary_col)
            if result.get('success'):
                Dialogs.show_info('完成', '已创建薪资分组字段: salary_group')
            else:
                Dialogs.show_warning('警告', '数据中没有薪资字段')
        
        elif group_type == 'experience':
            result = self._processing_service.create_experience_group()
            if result.get('success'):
                Dialogs.show_info('完成', '已创建工作年限分组字段: experience_group')
            else:
                Dialogs.show_warning('警告', '数据中没有工作年限字段')
        
        if result and result.get('success'):
            self._update_view_info()
    
    def reset_data(self) -> None:
        """重置数据"""
        if not self._data_service.has_data():
            return
        
        result = self._processing_service.reset_data()
        
        if result.get('success'):
            self._update_view_info()
            Dialogs.show_info('完成', '数据已重置')
    
    def _update_view_after_load(self, result: Dict) -> None:
        """加载数据后更新视图"""
        if not self._view:
            return
        
        info = self._data_service.get_data_info()
        
        info_text = f"记录数: {info.get('rows', 0)}\n"
        info_text += f"字段数: {info.get('columns', 0)}\n\n"
        info_text += '字段列表:\n'
        for col in info.get('column_names', []):
            info_text += f'  - {col}\n'
        
        missing = info.get('missing_values', {})
        if missing:
            info_text += '\n缺失值:\n'
            for col, count in missing.items():
                if count > 0:
                    info_text += f'  - {col}: {count}\n'
        
        self._view.update_info_text(info_text)
        
        categorical_cols = self._data_service.get_column_names('categorical')
        numeric_cols = self._data_service.get_column_names('numeric')
        self._view.update_comboboxes(categorical_cols, numeric_cols)
        
        data = self._data_manager.get_data()
        if data is not None:
            self._view.update_data_table(data)
    
    def _update_view_info(self) -> None:
        """更新视图信息"""
        if not self._view:
            return
        
        info = self._data_service.get_data_info()
        
        info_text = f"记录数: {info.get('rows', 0)}\n"
        info_text += f"字段数: {info.get('columns', 0)}\n\n"
        info_text += '字段列表:\n'
        for col in info.get('column_names', []):
            info_text += f'  - {col}\n'
        
        self._view.update_info_text(info_text)
        
        data = self._data_manager.get_data()
        if data is not None:
            self._view.update_data_table(data)
    
    def _get_salary_column(self) -> str:
        """获取薪资列名"""
        if self._view and hasattr(self._view, 'salary_var'):
            return self._view.salary_var.get()
        return 'pre_tax_salary'
