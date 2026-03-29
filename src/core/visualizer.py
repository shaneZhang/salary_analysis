"""
数据可视化模块（重构版）
移除GUI依赖，改为纯业务逻辑
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple, Any
import platform
from ..exceptions import VisualizationException
from ..models.logger import LoggerMixin


if platform.system() == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
elif platform.system() == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial', 'sans-serif']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'sans-serif']

plt.rcParams['axes.unicode_minus'] = False


class DataVisualizer(LoggerMixin):
    """
    数据可视化器
    负责生成各种图表
    """
    
    def __init__(self, chart_config: Optional[Dict[str, Any]] = None):
        self.figure: Optional[Figure] = None
        self.current_chart_type: Optional[str] = None
        self.data: Optional[pd.DataFrame] = None
        
        default_config = {
            'figure_size': (10, 6),
            'dpi': 100,
            'title_fontsize': 14,
            'label_fontsize': 12,
            'tick_fontsize': 10,
            'legend_fontsize': 10,
            'colors': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', 
                      '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
        }
        
        self.chart_config = default_config
        if chart_config:
            if 'figure_size' in chart_config and isinstance(chart_config['figure_size'], list):
                chart_config['figure_size'] = tuple(chart_config['figure_size'])
            self.chart_config.update(chart_config)
    
    def set_data(self, data: pd.DataFrame) -> None:
        """设置数据"""
        self.data = data
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """设置图表配置"""
        self.chart_config.update(config)
    
    def create_figure(self, figsize: Tuple[float, float] = None, dpi: int = None) -> Figure:
        """创建图形"""
        if figsize is None:
            figsize = self.chart_config['figure_size']
        if dpi is None:
            dpi = self.chart_config['dpi']
        
        self.figure = Figure(figsize=figsize, dpi=dpi)
        return self.figure
    
    def clear_figure(self) -> None:
        """清除图形"""
        if self.figure is None:
            self.create_figure()
        else:
            self.figure.clf()
    
    def create_bar_chart(self, x_data: List, y_data: List, 
                        title: str = '', xlabel: str = '', ylabel: str = '',
                        labels: Optional[List[str]] = None,
                        color: Optional[str] = None,
                        horizontal: bool = False) -> Figure:
        """创建柱状图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        if color is None:
            color = self.chart_config['colors'][0]
        
        if horizontal:
            bars = ax.barh(x_data, y_data, color=color, edgecolor='white')
        else:
            bars = ax.bar(x_data, y_data, color=color, edgecolor='white')
        
        if labels:
            for bar, label in zip(bars, labels):
                if horizontal:
                    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                           f'{label}', va='center', fontsize=self.chart_config['tick_fontsize'])
                else:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, height,
                           f'{label}', ha='center', va='bottom', fontsize=self.chart_config['tick_fontsize'])
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        ax.set_xlabel(xlabel, fontsize=self.chart_config['label_fontsize'])
        ax.set_ylabel(ylabel, fontsize=self.chart_config['label_fontsize'])
        
        ax.tick_params(axis='both', labelsize=self.chart_config['tick_fontsize'])
        
        if horizontal:
            ax.invert_yaxis()
        
        self.figure.tight_layout()
        self.current_chart_type = 'bar'
        return self.figure
    
    def create_line_chart(self, x_data: List, y_data_list: List[List[float]],
                         title: str = '', xlabel: str = '', ylabel: str = '',
                         labels: Optional[List[str]] = None,
                         colors: Optional[List[str]] = None,
                         marker: str = 'o') -> Figure:
        """创建折线图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        if colors is None:
            colors = self.chart_config['colors']
        
        for i, y_data in enumerate(y_data_list):
            label = labels[i] if labels and i < len(labels) else None
            color = colors[i % len(colors)]
            ax.plot(x_data, y_data, marker=marker, label=label, color=color, linewidth=2, markersize=6)
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        ax.set_xlabel(xlabel, fontsize=self.chart_config['label_fontsize'])
        ax.set_ylabel(ylabel, fontsize=self.chart_config['label_fontsize'])
        
        ax.tick_params(axis='both', labelsize=self.chart_config['tick_fontsize'])
        
        if labels:
            ax.legend(fontsize=self.chart_config['legend_fontsize'], loc='best')
        
        ax.grid(True, linestyle='--', alpha=0.7)
        
        self.figure.tight_layout()
        self.current_chart_type = 'line'
        return self.figure
    
    def create_pie_chart(self, data: List, labels: List[str],
                        title: str = '',
                        colors: Optional[List[str]] = None,
                        explode: Optional[List[float]] = None,
                        autopct: str = '%1.1f%%') -> Figure:
        """创建饼图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        if colors is None:
            colors = self.chart_config['colors'][:len(data)]
        
        wedges, texts, autotexts = ax.pie(data, labels=labels, colors=colors,
                                          explode=explode, autopct=autopct,
                                          startangle=90, pctdistance=0.75)
        
        for autotext in autotexts:
            autotext.set_fontsize(self.chart_config['tick_fontsize'])
            autotext.set_color('white')
            autotext.set_weight('bold')
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        
        self.figure.tight_layout()
        self.current_chart_type = 'pie'
        return self.figure
    
    def create_scatter_chart(self, x_data: List, y_data: List,
                            title: str = '', xlabel: str = '', ylabel: str = '',
                            color: Optional[str] = None,
                            size: float = 50,
                            alpha: float = 0.6) -> Figure:
        """创建散点图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        if color is None:
            color = self.chart_config['colors'][0]
        
        ax.scatter(x_data, y_data, c=color, s=size, alpha=alpha, edgecolors='white')
        
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        ax.plot(sorted(x_data), p(sorted(x_data)), "r--", alpha=0.8, linewidth=2, label='Trend Line')
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        ax.set_xlabel(xlabel, fontsize=self.chart_config['label_fontsize'])
        ax.set_ylabel(ylabel, fontsize=self.chart_config['label_fontsize'])
        
        ax.tick_params(axis='both', labelsize=self.chart_config['tick_fontsize'])
        ax.legend(fontsize=self.chart_config['legend_fontsize'])
        ax.grid(True, linestyle='--', alpha=0.7)
        
        self.figure.tight_layout()
        self.current_chart_type = 'scatter'
        return self.figure
    
    def create_boxplot(self, data_dict: Dict[str, List],
                      title: str = '', xlabel: str = '', ylabel: str = '') -> Figure:
        """创建箱线图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        labels = list(data_dict.keys())
        data = list(data_dict.values())
        
        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        
        for patch, color in zip(bp['boxes'], self.chart_config['colors'][:len(labels)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        for median in bp['medians']:
            median.set_color('red')
            median.set_linewidth(2)
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        ax.set_xlabel(xlabel, fontsize=self.chart_config['label_fontsize'])
        ax.set_ylabel(ylabel, fontsize=self.chart_config['label_fontsize'])
        
        ax.tick_params(axis='both', labelsize=self.chart_config['tick_fontsize'])
        ax.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        self.figure.tight_layout()
        self.current_chart_type = 'boxplot'
        return self.figure
    
    def create_histogram(self, data: List, bins: int = 30,
                        title: str = '', xlabel: str = '', ylabel: str = 'Frequency',
                        color: Optional[str] = None,
                        kde: bool = False) -> Figure:
        """创建直方图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        if color is None:
            color = self.chart_config['colors'][0]
        
        n, bins_edges, patches = ax.hist(data, bins=bins, color=color, 
                                         edgecolor='white', alpha=0.7)
        
        if kde:
            from scipy import stats
            kde_x = np.linspace(min(data), max(data), 100)
            kde_y = stats.gaussian_kde(data)(kde_x)
            ax2 = ax.twinx()
            ax2.plot(kde_x, kde_y, 'r-', linewidth=2, label='KDE')
            ax2.set_ylabel('Density', fontsize=self.chart_config['label_fontsize'])
            ax2.legend(fontsize=self.chart_config['legend_fontsize'])
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        ax.set_xlabel(xlabel, fontsize=self.chart_config['label_fontsize'])
        ax.set_ylabel(ylabel, fontsize=self.chart_config['label_fontsize'])
        
        ax.tick_params(axis='both', labelsize=self.chart_config['tick_fontsize'])
        
        self.figure.tight_layout()
        self.current_chart_type = 'histogram'
        return self.figure
    
    def create_heatmap(self, data: pd.DataFrame,
                       title: str = '',
                       cmap: str = 'YlOrRd',
                       annot: bool = True) -> Figure:
        """创建热力图"""
        self.clear_figure()
        ax = self.figure.add_subplot(111)
        
        im = ax.imshow(data.values, cmap=cmap, aspect='auto')
        
        ax.set_xticks(np.arange(len(data.columns)))
        ax.set_yticks(np.arange(len(data.index)))
        ax.set_xticklabels(data.columns, rotation=45, ha='right')
        ax.set_yticklabels(data.index)
        
        if annot:
            for i in range(len(data.index)):
                for j in range(len(data.columns)):
                    text = ax.text(j, i, f'{data.values[i, j]:.2f}',
                                  ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title(title, fontsize=self.chart_config['title_fontsize'], pad=10)
        
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.ax.tick_params(labelsize=self.chart_config['tick_fontsize'])
        
        self.figure.tight_layout()
        self.current_chart_type = 'heatmap'
        return self.figure
    
    def create_salary_distribution_chart(self, df: pd.DataFrame, 
                                         salary_col: str = 'pre_tax_salary',
                                         group_col: Optional[str] = None) -> Figure:
        """创建薪资分布图"""
        self.clear_figure()
        
        if group_col and group_col in df.columns:
            ax = self.figure.add_subplot(111)
            groups = df[group_col].unique()
            
            data_to_plot = []
            for group in groups:
                data_to_plot.append(df[df[group_col] == group][salary_col].dropna().values)
            
            bp = ax.boxplot(data_to_plot, labels=groups, patch_artist=True)
            
            for patch, color in zip(bp['boxes'], self.chart_config['colors'][:len(groups)]):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_title(f'{group_col} - 薪资分布箱线图', fontsize=self.chart_config['title_fontsize'])
            ax.set_ylabel('薪资', fontsize=self.chart_config['label_fontsize'])
            ax.grid(True, linestyle='--', alpha=0.7, axis='y')
        else:
            salary_data = df[salary_col].dropna().values
            return self.create_histogram(salary_data, bins=20, 
                                        title='薪资分布直方图', xlabel='薪资')
        
        self.figure.tight_layout()
        self.current_chart_type = 'salary_distribution'
        return self.figure
    
    def create_comparison_chart(self, df: pd.DataFrame, 
                               dimension_col: str,
                               salary_col: str = 'pre_tax_salary',
                               chart_type: str = 'bar') -> Figure:
        """创建对比图"""
        grouped = df.groupby(dimension_col)[salary_col].mean().sort_values(ascending=False)
        
        if chart_type == 'bar':
            return self.create_bar_chart(
                x_data=grouped.index.tolist(),
                y_data=grouped.values.tolist(),
                title=f'{dimension_col} - 平均薪资对比',
                xlabel=dimension_col,
                ylabel='平均薪资',
                color=self.chart_config['colors'][0]
            )
        elif chart_type == 'horizontal':
            return self.create_bar_chart(
                x_data=grouped.index.tolist(),
                y_data=grouped.values.tolist(),
                title=f'{dimension_col} - 平均薪资对比',
                xlabel='平均薪资',
                ylabel=dimension_col,
                horizontal=True,
                color=self.chart_config['colors'][0]
            )
        
        return self.figure
    
    def create_trend_chart(self, df: pd.DataFrame,
                          time_col: str,
                          salary_col: str = 'pre_tax_salary') -> Figure:
        """创建趋势图"""
        trend = df.groupby(time_col)[salary_col].agg(['mean', 'median', 'count']).reset_index()
        
        x_data = trend[time_col].tolist()
        y_mean = trend['mean'].tolist()
        y_median = trend['median'].tolist()
        
        return self.create_line_chart(
            x_data=x_data,
            y_data_list=[y_mean, y_median],
            title='薪资趋势变化',
            xlabel=time_col,
            ylabel='薪资',
            labels=['平均薪资', '中位薪资']
        )
    
    def save_chart(self, output_path: str, dpi: int = 300, format: str = 'png') -> bool:
        """
        保存图表
        
        Args:
            output_path: 输出路径
            dpi: 分辨率
            format: 格式
            
        Returns:
            是否成功
        """
        if self.figure is None:
            raise VisualizationException("没有可保存的图表")
        
        try:
            self.figure.savefig(output_path, dpi=dpi, format=format, 
                             bbox_inches='tight', facecolor='white')
            self.logger.info(f"Chart saved to: {output_path}")
            return True
        except Exception as e:
            raise VisualizationException(f"保存图表失败: {str(e)}")
    
    def get_current_figure(self) -> Optional[Figure]:
        """获取当前图形"""
        return self.figure
    
    def set_figure_size(self, width: float, height: float) -> None:
        """设置图形大小"""
        self.chart_config['figure_size'] = (width, height)
    
    def set_dpi(self, dpi: int) -> None:
        """设置DPI"""
        self.chart_config['dpi'] = dpi
    
    def set_color_scheme(self, colors: List[str]) -> None:
        """设置颜色方案"""
        self.chart_config['colors'] = colors
