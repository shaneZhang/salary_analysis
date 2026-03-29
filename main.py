"""
园区白领薪资数据分析工具
主程序入口

基于MVC架构重构
"""

import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.config_manager import ConfigManager
from src.controllers.main_controller import MainController


def main():
    """主函数"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    
    if os.path.exists(config_path):
        config = ConfigManager(config_path)
    else:
        config = ConfigManager()
    
    root = tk.Tk()
    
    app = MainController(root, config)
    
    app.run()


if __name__ == '__main__':
    main()
