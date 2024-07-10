import tkinter as tk
from tkinter import simpledialog, ttk
import pyautogui
import time

class MouseAction:
    def execute(self):
        pass

class MouseMove(MouseAction):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self):
        pyautogui.moveTo(self.x, self.y) 

class MouseClick(MouseAction):
    def execute(self):
        pyautogui.click()

class Wait(MouseAction):
    def __init__(self, time):
        self.time = time

    def execute(self):
        time.sleep(self.time)

class ActionDialog(simpledialog.Dialog):
    def body(self, master):
        pass

    def apply(self):
        pass

class MoveDialog(ActionDialog):
    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)

        self.x = tk.Entry(master)
        self.y = tk.Entry(master)

        self.x.grid(row=0, column=1)
        self.y.grid(row=1, column=1)

    def apply(self):
        x = int(self.x.get())
        y = int(self.y.get())
        self.result = MouseMove(x, y)  

class App:
    def __init__(self, root):
        self.root = root
        self.actions = []

        self.setup_ui()

    def setup_ui(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        ttk.Button(self.frame, text="Add Move", command=self.add_move).pack()
        ttk.Button(self.frame, text="Add Click", command=self.add_click).pack()
        ttk.Button(self.frame, text="Add Wait", command=self.add_wait).pack()
        ttk.Button(self.frame, text="Run", command=self.run_actions).pack()

        self.actions_listbox = tk.Listbox(self.frame)
        self.actions_listbox.pack()

    def add_move(self):
        dialog = MoveDialog(self.root)
        if dialog.result:
            self.actions.append(dialog.result)
            self.actions_listbox.insert(tk.END, f"Move: {dialog.result.x}, {dialog.result.y}")  

    def add_click(self):
        self.actions.append(MouseClick())
        self.actions_listbox.insert(tk.END, "Click")

    def add_wait(self):
        time = simpledialog.askfloat("Wait", "Time:")
        if time:
            self.actions.append(Wait(time))
            self.actions_listbox.insert(tk.END, f"Wait: {time}s")

    def run_actions(self):
        for action in self.actions:
            action.execute()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()