# main.py
import tkinter as tk
from views import App

# -------------------------------
# Programa Principal
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()