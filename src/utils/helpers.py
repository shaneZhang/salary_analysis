"""
工具函数模块
"""

from typing import Union, Optional


def format_number(value: Union[int, float], decimal_places: int = 2) -> str:
    """
    格式化数字，添加千分位分隔符
    
    Args:
        value: 数值
        decimal_places: 小数位数
        
    Returns:
        格式化后的字符串
    """
    if value is None:
        return 'N/A'
    
    try:
        return f'{float(value):,.{decimal_places}f}'
    except (ValueError, TypeError):
        return str(value)


def format_percentage(value: Union[int, float], decimal_places: int = 2) -> str:
    """
    格式化百分比
    
    Args:
        value: 数值（0-100）
        decimal_places: 小数位数
        
    Returns:
        格式化后的字符串
    """
    if value is None:
        return 'N/A'
    
    try:
        return f'{float(value):.{decimal_places}f}%'
    except (ValueError, TypeError):
        return str(value)


def safe_divide(numerator: Union[int, float], 
                denominator: Union[int, float],
                default: float = 0.0) -> float:
    """
    安全除法，避免除零错误
    
    Args:
        numerator: 被除数
        denominator: 除数
        default: 除数为零时的默认返回值
        
    Returns:
        除法结果
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default


def truncate_string(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """
    截断字符串
    
    Args:
        text: 原始字符串
        max_length: 最大长度
        suffix: 截断后缀
        
    Returns:
        截断后的字符串
    """
    if not text:
        return ''
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def get_column_type_name(dtype) -> str:
    """
    获取数据类型的友好名称
    
    Args:
        dtype: pandas数据类型
        
    Returns:
        类型名称
    """
    dtype_str = str(dtype).lower()
    
    if 'int' in dtype_str:
        return '整数'
    elif 'float' in dtype_str:
        return '浮点数'
    elif 'datetime' in dtype_str:
        return '日期时间'
    elif 'category' in dtype_str:
        return '分类'
    elif 'object' in dtype_str or 'str' in dtype_str:
        return '文本'
    else:
        return '其他'
