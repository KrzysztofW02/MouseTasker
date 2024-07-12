import tkinter as tk
from tkinter import simpledialog, messagebox
from actions import MouseMove, MouseClick, Wait, MouseMoveClick, MouseDrag

class ActionDialog(simpledialog.Dialog):
    def body(self, master):
        pass

    def apply(self):
        pass

class MoveDialog(ActionDialog):
    def __init__(self, master, x=0, y=0, time=1):
        self.x_val = x
        self.y_val = y
        self.wait_val = time
        super().__init__(master)

    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)
        tk.Label(master, text="Czas (s):").grid(row=2)

        self.x = tk.Entry(master)
        self.x.insert(0, str(self.x_val))
        self.y = tk.Entry(master)
        self.y.insert(0, str(self.y_val))
        self.time = tk.Entry(master)
        self.time.insert(0, str(self.wait_val))

        self.x.grid(row=0, column=1)
        self.y.grid(row=1, column=1)
        self.time.grid(row=2, column=1)

    def apply(self):
        try:
            x = int(self.x.get())
            y = int(self.y.get())
            time = float(self.time.get())
            self.result = MouseMove(x, y, time)
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić poprawne wartości liczbowe.")

class ClickDialog(ActionDialog):
    def __init__(self, master, x=0, y=0):
        self.x_val = x
        self.y_val = y
        super().__init__(master)

    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)

        self.x = tk.Entry(master)
        self.x.insert(0, str(self.x_val))
        self.y = tk.Entry(master)
        self.y.insert(0, str(self.y_val))

        self.x.grid(row=0, column=1)
        self.y.grid(row=1, column=1)

    def apply(self):
        try:
            x = int(self.x.get())
            y = int(self.y.get())
            self.result = MouseClick(x, y)
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić poprawne wartości liczbowe.")

class WaitDialog(ActionDialog):
    def __init__(self, master, time_value=1):
        self.time_val = time_value
        super().__init__(master)

    def body(self, master):
        tk.Label(master, text="Czas (s):").grid(row=0)
        self.time_entry = tk.Entry(master)
        self.time_entry.insert(0, str(self.time_val))
        self.time_entry.grid(row=0, column=1)

    def apply(self):
        try:
            time_value = float(self.time_entry.get())
            self.result = Wait(time_value)
        except ValueError:
            messagebox.showerror("Błąd", "Proszę wprowadzić poprawny czas.")

class MoveClickDialog(ActionDialog):
    def __init__(self, master, x=0, y=0, time=1):
        self.x_val = x
        self.y_val = y
        self.wait_val = time
        super().__init__(master)

    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)
        tk.Label(master, text="Time (s):").grid(row=2)

        self.x = tk.Entry(master)
        self.x.insert(0, str(self.x_val))
        self.y = tk.Entry(master)
        self.y.insert(0, str(self.y_val))
        self.time = tk.Entry(master)
        self.time.insert(0, str(self.wait_val))

        self.x.grid(row=0, column=1)
        self.y.grid(row=1, column=1)
        self.time.grid(row=2, column=1)

    def apply(self):
        try:
            x = int(self.x.get())
            y = int(self.y.get())
            time = float(self.time.get())
            self.result = MouseMoveClick(x, y, time)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")

class MouseDragDialog(ActionDialog):
    def __init__(self, master, x=0, y=0, time=1):
        self.x_val = x
        self.y_val = y
        self.wait_val = time
        super().__init__(master)

    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)
        tk.Label(master, text="Time (s):").grid(row=2)

        self.x = tk.Entry(master)
        self.x.insert(0, str(self.x_val))
        self.y = tk.Entry(master)
        self.y.insert(0, str(self.y_val))
        self.time = tk.Entry(master)
        self.time.insert(0, str(self.wait_val))

        self.x.grid(row=0, column=1)
        self.y.grid(row=1, column=1)
        self.time.grid(row=2, column=1)

    def apply(self):
        try:
            x = int(self.x.get())
            y = int(self.y.get())
            time = float(self.time.get())
            self.result = MouseDrag(x, y, time)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")