import tkinter as tk
from tkinter import simpledialog, ttk, messagebox, Toplevel, filedialog
import pyautogui
import time
import copy
from threading import Thread

class MouseAction:
    def execute(self):
        pass

class MouseMove(MouseAction): # normal move without click
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def __str__(self): # to copy or insert in correct form
        return f"Move: {self.x}, {self.y}, {self.time}"

    def execute(self):
        pyautogui.moveTo(self.x, self.y, self.time)

class MouseClick(MouseAction): # click on specific position
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): # to copy or insert in correct form
        return f"Click: {self.x}, {self.y}"

    def execute(self):
        pyautogui.click(self.x, self.y)

class Wait(MouseAction): # wait for specific seconds
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
    def __init__(self, master, x=0, y=0, time=0):
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
    def __init__(self, master, time_value=0):
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

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MouseTasker")
        self.actions = []

        self.running = False
        self.current_action_index = 0
        self.action_thread = None

        self.copied_action = None
        self.actions_history = []

        self.update_actions_history()

        screen_width = root.winfo_screenwidth()
        window_width = screen_width // 3
        self.root.geometry(f"{window_width}x500")

        self.setup_ui()

    def setup_ui(self):
        self.style = ttk.Style()
        self.style.configure("TButton",
                            font=("Helvetica", 12),
                            padding=10,
                            background="#323232",
                            foreground="white")
        self.style.map("TButton",
                    background=[('active', '#323232')],
                    foreground=[('active', 'white')])

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        button_frame_top = ttk.Frame(self.frame)
        button_frame_top.pack(fill=tk.X, expand=False)

        top_buttons = ttk.Frame(button_frame_top)
        top_buttons.pack(side=tk.TOP, pady=10)

        ttk.Button(top_buttons, text="Add Move", command=self.add_move, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Add Click", command=self.add_click, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Add Wait", command=self.add_wait, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Run", command=self.run_actions, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Check Coordinates", command=self.check_coordinates, style="TButton").pack(side=tk.LEFT, padx=5)
        

        button_frame_bottom = ttk.Frame(self.frame)
        button_frame_bottom.pack(fill=tk.X, expand=False)

        bottom_buttons = ttk.Frame(button_frame_bottom)
        bottom_buttons.pack(side=tk.TOP, pady=10)

        ttk.Button(bottom_buttons, text="Save", command=self.save_actions, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_buttons, text="Load", command=self.load_actions, style="TButton").pack(side=tk.LEFT, padx=5)
        self.edit_button = ttk.Button(bottom_buttons, text="Edit", command=self.edit_action, style="TButton")
        self.edit_button.pack(side=tk.LEFT, padx=5)
        self.delete_button = ttk.Button(bottom_buttons, text="Delete", command=self.delete_action, style="TButton")
        self.delete_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_buttons, text="Help", command=self.show_shortcuts, style="TButton").pack(side=tk.LEFT, padx=5)


        self.actions_listbox = tk.Listbox(self.frame, height=15, width=50)
        self.actions_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #Bindings keys
        self.actions_listbox.bind('<Double-1>', self.edit_action)
        self.root.bind('<c>', self.check_coordinates)
        self.root.bind('<Delete>', self.delete_action)
        self.root.bind('<Control-s>', lambda event: self.save_actions())
        self.root.bind('<Control-a>', self.select_all_actions)

        self.root.bind('<F1>', self.run_actions)
        self.root.bind('<F2>', self.stop_actions)
        self.root.bind('<F5>', self.show_shortcuts)
        self.root.bind('<Control-c>', self.copy_action)
        self.root.bind('<Control-v>', self.paste_action)
        self.root.bind('<Control-z>', self.undo_action)

    def add_move(self):
        dialog = MoveDialog(self.root)
        if dialog.result:
            selected_index = self.actions_listbox.curselection()
            if selected_index:
                insert_position = selected_index[0] + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, dialog.result)
            self.actions_listbox.insert(insert_position, f"Move: {dialog.result.x}, {dialog.result.y}, {dialog.result.time}")
            self.update_actions_history()

    def add_click(self):
        dialog = ClickDialog(self.root)
        if dialog.result:
            selected_index = self.actions_listbox.curselection()
            if selected_index:
                insert_position = selected_index[0] + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, dialog.result)
            self.actions_listbox.insert(insert_position, f"Click: {dialog.result.x}, {dialog.result.y}")
            self.update_actions_history()

    def add_wait(self):
        dialog = WaitDialog(self.root)
        if dialog.result:
            selected_index = self.actions_listbox.curselection()
            if selected_index:
                insert_position = selected_index[0] + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, dialog.result)
            self.actions_listbox.insert(insert_position, f"Wait: {dialog.result.time}s")
            self.update_actions_history()

    def edit_action(self, event=None):
        selected_index = self.actions_listbox.curselection()
        if selected_index:
            action = self.actions[selected_index[0]]
            if isinstance(action, MouseMove):
                dialog = MoveDialog(self.root, action.x, action.y, action.time)
                if dialog.result:
                    self.actions[selected_index[0]] = dialog.result
                    self.actions_listbox.delete(selected_index[0])
                    self.actions_listbox.insert(selected_index[0], f"Move: {dialog.result.x}, {dialog.result.y}, {dialog.result.time}")
            elif isinstance(action, MouseClick):
                dialog = ClickDialog(self.root, action.x, action.y)
                if dialog.result:
                    self.actions[selected_index[0]] = dialog.result
                    self.actions_listbox.delete(selected_index[0])
                    self.actions_listbox.insert(selected_index[0], f"Click: {dialog.result.x}, {dialog.result.y}")
            elif isinstance(action, Wait):
                dialog = WaitDialog(self.root, action.time)
                if dialog.result:
                    self.actions[selected_index[0]] = dialog.result
                    self.actions_listbox.delete(selected_index[0])
                    self.actions_listbox.insert(selected_index[0], f"Wait: {dialog.result.time}s")

    def delete_action(self, event=None):
        selected_indices = self.actions_listbox.curselection()


        for index in reversed(selected_indices):
            self.actions.pop(index)
            self.actions_listbox.delete(index)

    def run_actions(self, event=None):
        if self.running:
            messagebox.showinfo("Info", "Already running actions.")
            return
        
        self.running = True
        self.current_action_index = 0
        
        # Start actions in a separate thread to allow to stop actions
        self.action_thread = Thread(target=self.execute_actions)
        self.action_thread.start()

    def execute_actions(self):
        while self.running and self.current_action_index < len(self.actions):
            action = self.actions[self.current_action_index]
            action.execute()
            self.current_action_index += 1

        # Reset after actions are finished
        self.running = False
        self.action_thread = None

    def save_actions(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath: 
            return
        with open(filepath, 'w') as file:
            for action in self.actions:
                if isinstance(action, MouseMove):
                    file.write(f"Move,{action.x},{action.y},{action.time}\n")
                elif isinstance(action, MouseClick):
                    file.write(f"Click,{action.x},{action.y}\n")
                elif isinstance(action, Wait):
                    file.write(f"Wait,{action.time}\n")

    def load_actions(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath:  
            return
        self.actions.clear()
        self.actions_listbox.delete(0, tk.END)
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if parts[0] == "Move":
                        action = MouseMove(int(parts[1]), int(parts[2]), float(parts[3]))
                    elif parts[0] == "Click":
                        action = MouseClick(int(parts[1]), int(parts[2]))
                    elif parts[0] == "Wait":
                        action = Wait(float(parts[1]))
                    self.actions.append(action)
                    self.actions_listbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            messagebox.showerror("Error", "File does not exist.")

    def select_all_actions(self, event=None):
        self.actions_listbox.select_set(0, tk.END)

    def stop_actions(self, event=None):
        if not self.running:
            messagebox.showinfo("Info", "No actions currently running.")
            return
        
        self.running = False
        if self.action_thread and self.action_thread.is_alive():
            self.action_thread.join()  # Wait for thread to finish

        messagebox.showinfo("Info", "Actions stopped.")
    
    def show_shortcuts(self, event=None):
        messagebox.showinfo("Shortcuts", "Shortcuts:\n- Copy: Ctrl+C\n- Paste: Ctrl+V\n- Undo: Ctrl+Z\n- Save: Ctrl+S\n- Select All: Ctrl+A\n- Delete: Delete\n- Check Coordinates: C\n- Run: F1\n- Stop: F2\n- Show Shortcuts: F5")

    def copy_action(self, event=None):
        selected_index = self.actions_listbox.curselection()
        if selected_index:
            self.copied_action = self.actions[selected_index[0]]
        

    def paste_action(self, event=None):
        if hasattr(self, 'copied_action') and self.copied_action:
            selected_index = self.actions_listbox.curselection()
            if selected_index:
                insert_position = selected_index[0] + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, self.copied_action)
            self.actions_listbox.insert(insert_position, str(self.copied_action))
            self.update_actions_history()

    def undo_action(self, event=None):
        print("Undo action triggered")  
        if self.actions_history:
            print(f"Before undo: {self.actions_history}")  
            self.actions = self.actions_history.pop()
            self.refresh_actions_listbox()
        else:
            print("Actions history is empty")  

    def update_actions_history(self, event=None):
        print(f"Updating actions history: {self.actions}")  
        self.actions_history.append(copy.deepcopy(self.actions))

    def refresh_actions_listbox(self, event=None):
        self.actions_listbox.delete(0, tk.END)
        for action in self.actions:
            self.actions_listbox.insert(tk.END, str(action))

    def check_coordinates(self, event=None):
        x, y = pyautogui.position()
        coord_window = Toplevel(self.root)
        coord_window.title("Current Mouse Position")
        
        tk.Label(coord_window, text=f"X: {x}, Y: {y}").pack(pady=10)
        
        button_frame = tk.Frame(coord_window)
        button_frame.pack(pady=10)

        def add_move_action():
            move_action = MouseMove(x, y, 0)
            self.actions.append(move_action)
            self.actions_listbox.insert(tk.END, f"Move: {move_action.x}, {move_action.y}, {move_action.time}")
            coord_window.destroy()

        def add_click_action():
            click_action = MouseClick(x, y)
            self.actions.append(click_action)
            self.actions_listbox.insert(tk.END, f"Click: {click_action.x}, {click_action.y}")
            coord_window.destroy()
        
        ttk.Button(button_frame, text="Add Move", command=add_move_action, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Click", command=add_click_action, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=coord_window.destroy, style="TButton").pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
