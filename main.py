import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.controllers import MainController
from src.views import MainView


def main():
    """应用主入口"""
    root = tk.Tk()
    
    try:
        root.tk.call('tk', 'scaling', 1.5)
    except:
        pass
    
    controller = MainController()
    view = MainView(root, controller)
    controller.set_view(view, root)
    controller.run()
    
    root.mainloop()


if __name__ == '__main__':
    main()
