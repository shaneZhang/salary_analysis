import pytest
import pandas as pd
import numpy as np
from typing import Generator

# 添加项目路径到Python路径
import sys
sys.path.insert(0, '/Users/zhangyuqing/Desktop/traecn-2026-03-29/salary_analysis')


@pytest.fixture(scope="session")
def sample_dataframe() -> pd.DataFrame:
    """创建样本DataFrame用于测试"""
    np.random.seed(42)
    n = 100
    
    data = {
        'name': [f'Person_{i}' for i in range(n)],
        'gender': np.random.choice(['男', '女'], size=n),
        'age': np.random.randint(22, 55, size=n),
        'department': np.random.choice(['技术部', '市场部', '销售部', 'HR', '财务部'], size=n),
        'position': np.random.choice(['工程师', '经理', '主管', '专员'], size=n),
        'work_years': np.random.randint(1, 25, size=n),
        'education': np.random.choice(['本科', '硕士', '博士', '大专'], size=n),
        'pre_tax_salary': np.random.randint(8000, 50000, size=n),
        'base_salary': np.random.randint(5000, 30000, size=n),
        'bonus': np.random.randint(0, 20000, size=n)
    }
    
    return pd.DataFrame(data)


@pytest.fixture(scope="session")
def sample_dataframe_with_missing(sample_dataframe) -> pd.DataFrame:
    """创建包含缺失值的DataFrame"""
    df = sample_dataframe.copy()
    df.loc[df.sample(frac=0.1).index, 'pre_tax_salary'] = np.nan
    df.loc[df.sample(frac=0.05).index, 'age'] = np.nan
    return df


@pytest.fixture(scope="session")
def sample_dataframe_with_duplicates(sample_dataframe) -> pd.DataFrame:
    """创建包含重复数据的DataFrame"""
    df = sample_dataframe.copy()
    duplicates = df.sample(n=10)
    df = pd.concat([df, duplicates], ignore_index=True)
    return df


@pytest.fixture(scope="session")
def temp_excel_file(tmp_path_factory, sample_dataframe) -> Generator[str, None, None]:
    """创建临时Excel文件"""
    tmp_path = tmp_path_factory.mktemp("data")
    file_path = tmp_path / "test_data.xlsx"
    sample_dataframe.to_excel(file_path, index=False)
    yield str(file_path)
