import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import Optional, List, Dict, Any, Callable


class Dialogs:
    @staticmethod
    def show_info(title: str, message: str):
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(title: str, message: str):
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_error(title: str, message: str):
        messagebox.showerror(title, message)
    
    @staticmethod
    def ask_yes_no(title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def select_file(title: str = '选择文件', 
                   filetypes: List[tuple] = None) -> Optional[str]:
        if filetypes is None:
            filetypes = [('Excel文件', '*.xlsx *.xls'), ('所有文件', '*.*')]
        
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )
        
        return file_path if file_path else None
    
    @staticmethod
    def select_folder(title: str = '选择文件夹') -> Optional[str]:
        root = tk.Tk()
        root.withdraw()
        
        folder_path = filedialog.askdirectory(title=title)
        
        return folder_path if folder_path else None
    
    @staticmethod
    def save_file(title: str = '保存文件',
                 defaultextension: str = '.xlsx',
                 filetypes: List[tuple] = None) -> Optional[str]:
        if filetypes is None:
            filetypes = [('Excel文件', '*.xlsx'), ('CSV文件', '*.csv'), ('所有文件', '*.*')]
        
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        
        return file_path if file_path else None
    
    @staticmethod
    def show_clean_data_dialog(parent, on_clean_callback: Callable):
        dialog = tk.Toplevel(parent)
        dialog.title('数据清洗')
        dialog.geometry('400x300')
        dialog.transient(parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text='选择清洗操作:').pack(pady=10)
        
        operations = [
            ('删除重复数据', 'duplicates'),
            ('删除缺失值行', 'missing'),
            ('填充缺失值(均值)', 'fill_mean'),
            ('移除异常值', 'outliers')
        ]
        
        for text, operation in operations:
            ttk.Button(
                dialog, text=text,
                command=lambda op=operation: on_clean_data_action(dialog, on_clean_callback, op)
            ).pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(dialog, text='取消', command=dialog.destroy).pack(pady=10)
    
    @staticmethod
    def show_group_data_dialog(parent, on_group_callback: Callable):
        dialog = tk.Toplevel(parent)
        dialog.title('数据分组')
        dialog.geometry('400x250')
        dialog.transient(parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text='选择分组操作:').pack(pady=10)
        
        operations = [
            ('年龄分组', 'age'),
            ('薪资分组', 'salary'),
            ('工作年限分组', 'experience')
        ]
        
        for text, operation in operations:
            ttk.Button(
                dialog, text=text,
                command=lambda op=operation: on_group_action(dialog, on_group_callback, op)
            ).pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(dialog, text='取消', command=dialog.destroy).pack(pady=10)
    
    @staticmethod
    def show_input_dialog(parent, title: str, prompt: str, 
                         initial_value: str = '') -> Optional[str]:
        return simpledialog.askstring(title, prompt, initialvalue=initial_value, parent=parent)


def on_clean_data_action(dialog: tk.Toplevel, callback: Callable, operation: str):
    dialog.destroy()
    if callback:
        callback(operation)


def on_group_action(dialog: tk.Toplevel, callback: Callable, operation: str):
    dialog.destroy()
    if callback:
        callback(operation)
