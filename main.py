# main.py

import tkinter as tk
from gui_handler import GUIHandler

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIHandler(root)
    root.mainloop()
