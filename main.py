import tkinter as tk
from ttkthemes import ThemedTk
from MouseTasker import App

if __name__ == "__main__":
    root = ThemedTk(theme="radiance")
    root.set_theme("radiance", themebg=True)
    app = App(root)
    root.mainloop()

