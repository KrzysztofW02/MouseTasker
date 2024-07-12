import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog
from threading import Thread
from actions import MouseMove, MouseClick, Wait, MouseMoveClick, MouseDrag
from dialogs import MoveDialog, ClickDialog, WaitDialog, MoveClickDialog, MouseDragDialog
import pyautogui
import copy
import threading


class App:
    def __init__(self, root):
        self.root = root
        self.root.set_theme("radiance")

        self.root.title("MouseTasker")
        self.actions = []

        self.running = False
        self.current_action_index = 0
        self.action_thread = None

        self.copied_action = None
        self.actions_history = []

        self.update_actions_history()

        screen_width = root.winfo_screenwidth()
        window_width = screen_width // 2
        self.root.geometry(f"{window_width}x500")

        self.setup_ui()
        self.create_menu()

    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def setup_ui(self):
        self.style = ttk.Style()
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #top buttons
        button_frame_top = ttk.Frame(self.frame)
        button_frame_top.pack(fill=tk.X, expand=False)

        top_buttons = ttk.Frame(button_frame_top)
        top_buttons.pack(side=tk.TOP, pady=10)

        ttk.Button(top_buttons, text="Add MoveClick", command=self.add_move_click, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Add Move", command=self.add_move, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Add Click", command=self.add_click, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Add Wait", command=self.add_wait, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Add Mouse Drag", command=self.add_mouse_drag, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="Run", command=self.run_actions, style="TButton").pack(side=tk.LEFT, padx=5)

        #Listbox
        self.actions_listbox = tk.Listbox(self.frame, height=15, width=50)
        self.actions_listbox.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.actions_listbox.config(bg="white", fg="black", borderwidth=0, highlightthickness=0, highlightbackground="#31363b", highlightcolor="#31363b")

        #bottom buttons
        button_frame_bottom = ttk.Frame(self.frame)
        button_frame_bottom.pack(fill=tk.X, expand=False)

        bottom_buttons = ttk.Frame(button_frame_bottom)
        bottom_buttons.pack(side=tk.TOP, pady=10)

        ttk.Button(bottom_buttons, text="Check Coordinations", command=self.check_coordinates, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_buttons, text="Save", command=self.save_actions, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_buttons, text="Load", command=self.load_actions, style="TButton").pack(side=tk.LEFT, padx=5)
        self.edit_button = ttk.Button(bottom_buttons, text="Edit", command=self.edit_action, style="TButton")
        self.edit_button.pack(side=tk.LEFT, padx=5)
        self.delete_button = ttk.Button(bottom_buttons, text="Delete", command=self.delete_action, style="TButton")
        self.delete_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_buttons, text="Help", command=self.show_shortcuts, style="TButton").pack(side=tk.LEFT, padx=5)


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

    #Menu bar
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_actions)
        file_menu.add_command(label="Load", command=self.load_actions)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo_action)
        edit_menu.add_command(label="Copy", command=self.copy_action)
        edit_menu.add_command(label="Paste", command=self.paste_action)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Shortcuts", command=self.show_shortcuts)
        menu_bar.add_cascade(label="Help", menu=help_menu)

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
    
    def add_move_click(self):
        dialog = MoveClickDialog(self.root)
        if dialog.result:
            selected_index = self.actions_listbox.curselection()
            if selected_index:
                insert_position = selected_index[0] + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, dialog.result)
            self.actions_listbox.insert(insert_position, f"MoveClick: {dialog.result.x}, {dialog.result.y}, {dialog.result.time}")
            self.update_actions_history()

    def add_mouse_drag(self):
        dialog = MouseDragDialog(self.root)
        if dialog.result:
            selected_index = self.actions_listbox.curselection()
            if selected_index:
                insert_position = selected_index[0] + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, dialog.result)
            self.actions_listbox.insert(insert_position, f"MouseDrag: {dialog.result.x}, {dialog.result.y}, {dialog.result.time}")
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
            elif isinstance(action, MouseMoveClick):
                dialog = MoveClickDialog(self.root, action.x, action.y, action.time)
                if dialog.result:
                    self.actions[selected_index[0]] = dialog.result
                    self.actions_listbox.delete(selected_index[0])
                    self.actions_listbox.insert(selected_index[0], f"MoveClick: {dialog.result.x}, {dialog.result.y}, {dialog.result.time}")
            elif isinstance(action, MouseDrag):
                dialog = MouseDragDialog(self.root, action.x, action.y, action.time)
                if dialog.result:
                    self.actions[selected_index[0]] = dialog.result
                    self.actions_listbox.delete(selected_index[0])
                    self.actions_listbox.insert(selected_index[0], f"MouseDrag: {dialog.result.x}, {dialog.result.y}, {dialog.result.time}")
            self.update_actions_history()

    def delete_action(self, event=None):
        selected_indices = self.actions_listbox.curselection()

        for index in reversed(selected_indices):
            self.actions.pop(index)
            self.actions_listbox.delete(index)
            self.update_actions_history()

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
        def action_runner():
            while self.running and self.current_action_index < len(self.actions):
                self.actions_listbox.select_clear(0, tk.END)
                self.actions_listbox.select_set(self.current_action_index)
                self.actions_listbox.see(self.current_action_index)

                action = self.actions[self.current_action_index]
                action.execute()
                self.current_action_index += 1

            self.running = False
            self.action_thread = None
            self.actions_listbox.select_clear(0, tk.END)

        self.action_thread = threading.Thread(target=action_runner)
        self.action_thread.start()

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
        # Warning before load new actions
        if messagebox.askyesno("Warning", "Loading a new file will remove your current actions list. Would you like to continue?"):
            filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if not filepath:  
                return
            temp_actions = [] 
            try:
                with open(filepath, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if parts[0] == "Move" and len(parts) == 4:
                            try:
                                action = MouseMove(int(parts[1]), int(parts[2]), float(parts[3]))
                            except ValueError:
                                messagebox.showerror("Error", "File is incorrect!")
                                return
                        elif parts[0] == "Click" and len(parts) == 3:
                            try:
                                action = MouseClick(int(parts[1]), int(parts[2]))
                            except ValueError:
                                messagebox.showerror("Error", "File is incorrect!")
                                return
                        elif parts[0] == "Wait" and len(parts) == 2:
                            try:
                                action = Wait(float(parts[1]))
                            except ValueError:
                                messagebox.showerror("Error", "File is incorrect!")
                                return
                        elif parts[0] == "MoveClick" and len(parts) == 4:
                            try:
                                action = MouseMoveClick(int(parts[1]), int(parts[2]), float(parts[3]))
                            except ValueError:
                                messagebox.showerror("Error", "File is incorrect!")
                                return
                        elif parts[0] == "MouseDrag" and len(parts) == 4:
                            try:
                                action = MouseDrag(int(parts[1]), int(parts[2]), float(parts[3]))
                            except ValueError:
                                messagebox.showerror("Error", "File is incorrect!")
                                return
                        else:
                            messagebox.showerror("Error", "File is incorrect!")
                            return
                        temp_actions.append(action)
            except FileNotFoundError:
                messagebox.showerror("Error", "File does not exist.")
                return

            self.actions.clear()
            self.actions_listbox.delete(0, tk.END)
            for action in temp_actions:
                self.actions.append(action)
                self.actions_listbox.insert(tk.END, str(action))

    def select_all_actions(self, event=None):
        self.actions_listbox.select_set(0, tk.END)

    def stop_actions(self, event=None):
        if not self.running:
            messagebox.showinfo("Info", "No actions currently running.")
            return
        
        self.running = False
       # if self.action_thread and self.action_thread.is_alive():
        # self.action_thread.join()  # Wait for thread to finish

        messagebox.showinfo("Info", "Actions stopped.")
        self.actions_listbox.select_clear(0, tk.END)  # Clear selection
    
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
            move_action = MouseMove(x, y, 1) ####### default time is 1 second instead of 0 @@@@@@@@@
            self.actions.append(move_action)
            self.actions_listbox.insert(tk.END, f"Move: {move_action.x}, {move_action.y}, {move_action.time}")
            coord_window.destroy()
            self.update_actions_history()
            

        def add_click_action():
            click_action = MouseClick(x, y)
            self.actions.append(click_action)
            self.actions_listbox.insert(tk.END, f"Click: {click_action.x}, {click_action.y}")
            coord_window.destroy()
            self.update_actions_history()

        def add_move_click():
            move_click_action = MouseMoveClick(x, y, 1)
            self.actions.append(move_click_action)
            self.actions_listbox.insert(tk.END, f"MoveClick: {move_click_action.x}, {move_click_action.y}, {move_click_action.time}")
            coord_window.destroy()
            self.update_actions_history()

        def add_mouse_drag():
            mouse_drag_action = MouseDrag(x, y, 1)
            self.actions.append(mouse_drag_action)
            self.actions_listbox.insert(tk.END, f"MouseDrag: {mouse_drag_action.x}, {mouse_drag_action.y}, {mouse_drag_action.time}")
            coord_window.destroy()
            self.update_actions_history()
        
        ttk.Button(button_frame, text="Add Move Click", command=add_move_click, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Move", command=add_move_action, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Click", command=add_click_action, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Mouse Drag", command=add_mouse_drag, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=coord_window.destroy, style="TButton").pack(side=tk.LEFT, padx=5)
