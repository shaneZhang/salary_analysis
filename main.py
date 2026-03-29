import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.controllers.main_controller import MainController


def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    root = tk.Tk()
    
    app = MainController(root, config_path)
    
    root.mainloop()


if __name__ == '__main__':
    main()
