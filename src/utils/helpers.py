from typing import Any, Optional
import pandas as pd


def format_number(value: Any, decimal_places: int = 2) -> str:
    if value is None:
        return ''
    
    if isinstance(value, (int, float)):
        if isinstance(value, float):
            return f'{value:,.{decimal_places}f}'
        return f'{value:,}'
    
    return str(value)


def get_column_type(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series):
        return 'numeric'
    elif pd.api.types.is_datetime64_any_dtype(series):
        return 'datetime'
    elif pd.api.types.is_categorical_dtype(series):
        return 'categorical'
    else:
        return 'text'


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def truncate_string(text: str, max_length: int = 50, suffix: str = '...') -> str:
    if text is None:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
