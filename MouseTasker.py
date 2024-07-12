from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QAction, QMenu, QMenuBar, QHBoxLayout, QFileDialog, QMessageBox, QDialog, QShortcut, QLabel
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from actions import MouseMove, MouseClick, Wait, MouseMoveClick, MouseDrag
from dialogs import MoveDialog, ClickDialog, WaitDialog, MoveClickDialog, MouseDragDialog
import pyautogui
import threading
import copy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MouseTasker")
        self.actions = []
        self.running = False
        self.current_action_index = 0
        self.action_thread = None
        self.copied_action = None
        self.actions_history = []

        self.setup_shortcuts()

        self.update_actions_history()
        
        screen_width = pyautogui.size().width
        window_width = screen_width // 2
        self.setGeometry(100, 100, window_width, 500)

        self.setup_ui()
        self.create_menu()
    def setup_shortcuts(self): #####################SHORTCUTS
        shortcut_check_coordinates = QShortcut(QKeySequence('C'), self)
        shortcut_check_coordinates.activated.connect(self.check_coordinates)

        shortcut_delete_action = QShortcut(QKeySequence.Delete, self)
        shortcut_delete_action.activated.connect(self.delete_action)

        shortcut_save_actions = QShortcut(QKeySequence('Ctrl+S'), self)
        shortcut_save_actions.activated.connect(self.save_actions)

        shortcut_run_actions = QShortcut(QKeySequence('F1'), self)
        shortcut_run_actions.activated.connect(self.run_actions)

        shortcut_stop_actions = QShortcut(QKeySequence('F2'), self)
        shortcut_stop_actions.activated.connect(self.stop_actions)

        shortcut_show_shortcuts = QShortcut(QKeySequence('F5'), self)
        shortcut_show_shortcuts.activated.connect(self.show_shortcuts)

        shortcut_copy_action = QShortcut(QKeySequence('Ctrl+C'), self)
        shortcut_copy_action.activated.connect(self.copy_action)

        shortcut_paste_action = QShortcut(QKeySequence('Ctrl+V'), self)
        shortcut_paste_action.activated.connect(self.paste_action)

        shortcut_undo_action = QShortcut(QKeySequence('Ctrl+Z'), self)
        shortcut_undo_action.activated.connect(self.undo_action)

        shortcut_select_all_actions = QShortcut(QKeySequence('Ctrl+A'), self)
        shortcut_select_all_actions.activated.connect(self.select_all_actions)

    def refresh_ui(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.top_buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.top_buttons_layout)

        self.add_move_click_button = QPushButton("Add MoveClick")
        self.add_move_click_button.clicked.connect(self.add_move_click)
        self.top_buttons_layout.addWidget(self.add_move_click_button)

        self.add_move_button = QPushButton("Add Move")
        self.add_move_button.clicked.connect(self.add_move)
        self.top_buttons_layout.addWidget(self.add_move_button)

        self.add_click_button = QPushButton("Add Click")
        self.add_click_button.clicked.connect(self.add_click)
        self.top_buttons_layout.addWidget(self.add_click_button)

        self.add_wait_button = QPushButton("Add Wait")
        self.add_wait_button.clicked.connect(self.add_wait)
        self.top_buttons_layout.addWidget(self.add_wait_button)

        self.add_mouse_drag_button = QPushButton("Add Mouse Drag")
        self.add_mouse_drag_button.clicked.connect(self.add_mouse_drag)
        self.top_buttons_layout.addWidget(self.add_mouse_drag_button)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_actions)
        self.top_buttons_layout.addWidget(self.run_button)

        self.actions_list_widget = QListWidget()
        self.actions_list_widget.itemDoubleClicked.connect(self.edit_action)
        self.actions_list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.layout.addWidget(self.actions_list_widget)

        self.bottom_buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_buttons_layout)

        self.check_coordinates_button = QPushButton("Check Coordinates")
        self.check_coordinates_button.clicked.connect(self.check_coordinates)
        self.bottom_buttons_layout.addWidget(self.check_coordinates_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_actions)
        self.bottom_buttons_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_actions)
        self.bottom_buttons_layout.addWidget(self.load_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_action)
        self.bottom_buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_action)
        self.bottom_buttons_layout.addWidget(self.delete_button)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_shortcuts)
        self.bottom_buttons_layout.addWidget(self.help_button)

    #Menu bar
    def create_menu(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_actions)
        file_menu.addAction(save_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_actions)
        file_menu.addAction(load_action)

        edit_menu = QMenu("Edit", self)
        menu_bar.addMenu(edit_menu)

        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste_action)
        edit_menu.addAction(paste_action)

        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

        shortcuts_action = QAction("Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def add_move(self):
        dialog = MoveDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y, time = dialog.result
            action = MouseMove(x, y, time)
            self.actions.append(action)
            self.actions_list_widget.addItem(str(action))
            self.update_actions_history()

    def add_click(self):
        dialog = ClickDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y = dialog.result
            action = MouseClick(x, y)
            self.actions.append(action)
            self.actions_list_widget.addItem(str(action))
            self.update_actions_history()

    def add_wait(self):
        dialog = WaitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            time = dialog.result
            action = Wait(time)
            self.actions.append(action)
            self.actions_list_widget.addItem(str(action))
            self.update_actions_history()
    
    def add_move_click(self):
        dialog = MoveClickDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y, time = dialog.result
            action = MouseMoveClick(x, y, time)
            self.actions.append(action)
            self.actions_list_widget.addItem(str(action))
            self.update_actions_history()

    def add_mouse_drag(self):
        dialog = MouseDragDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y, time = dialog.result
            action = MouseDrag(x, y, time)
            self.actions.append(action)
            self.actions_list_widget.addItem(str(action))
            self.update_actions_history()


    def edit_action(self):
        selected_items = self.actions_list_widget.selectedItems()
        if selected_items:
            selected_index = self.actions_list_widget.row(selected_items[0])
            action = self.actions[selected_index]
            if isinstance(action, MouseMove):
                dialog = MoveDialog(self, action.x, action.y, action.time)
                if dialog.exec_() == QDialog.Accepted:
                    x, y, time = dialog.result
                    self.actions[selected_index] = MouseMove(x, y, time)
                    self.actions_list_widget.item(selected_index).setText(str(self.actions[selected_index]))
            elif isinstance(action, MouseClick):
                dialog = ClickDialog(self, action.x, action.y)
                if dialog.exec_() == QDialog.Accepted:
                    x, y = dialog.result
                    self.actions[selected_index] = MouseClick(x, y)
                    self.actions_list_widget.item(selected_index).setText(str(self.actions[selected_index]))
            elif isinstance(action, Wait):
                dialog = WaitDialog(self, action.time)
                if dialog.exec_() == QDialog.Accepted:
                    time = dialog.result
                    self.actions[selected_index] = Wait(time)
                    self.actions_list_widget.item(selected_index).setText(str(self.actions[selected_index]))
            elif isinstance(action, MouseMoveClick):
                dialog = MoveClickDialog(self, action.x, action.y, action.time)
                if dialog.exec_() == QDialog.Accepted:
                    x, y, time = dialog.result
                    self.actions[selected_index] = MouseMoveClick(x, y, time)
                    self.actions_list_widget.item(selected_index).setText(str(self.actions[selected_index]))
            elif isinstance(action, MouseDrag):
                dialog = MouseDragDialog(self, action.x, action.y, action.time)
                if dialog.exec_() == QDialog.Accepted:
                    x, y, time = dialog.result
                    self.actions[selected_index] = MouseDrag(x, y, time)
                    self.actions_list_widget.item(selected_index).setText(str(self.actions[selected_index]))
            self.update_actions_history()

    def delete_action(self):
        selected_items = self.actions_list_widget.selectedItems()
        if selected_items:
            selected_index = self.actions_list_widget.row(selected_items[0])
            del self.actions[selected_index]
            self.actions_list_widget.takeItem(selected_index)
            self.update_actions_history()

    def run_actions(self):
        if self.running:
            return

        self.running = True
        selected_indices = self.actions_list_widget.selectedIndexes()
        if selected_indices:
            self.current_action_index = selected_indices[0].row()
        else:
            self.current_action_index = 0

        # Start actions in a separate thread to allow stopping actions
        self.action_thread = threading.Thread(target=self.execute_actions)
        self.action_thread.start()

    def execute_actions(self):
        while self.running and self.current_action_index < len(self.actions):
            print(f"Clearing selections, current_action_index: {self.current_action_index}")
            for i in range(self.actions_list_widget.count()):
                self.actions_list_widget.item(i).setSelected(False)

            print(f"Selecting item: {self.current_action_index}")
            self.actions_list_widget.item(self.current_action_index).setSelected(True)
            self.actions_list_widget.scrollToItem(self.actions_list_widget.item(self.current_action_index))

            action = self.actions[self.current_action_index]
            print(f"Executing action: {action}")
            action.execute()
            self.current_action_index += 1

        print("Actions completed or stopped")
        self.running = False
        self.action_thread = None
        self.actions_list_widget.clearSelection()




    def save_actions(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Actions", "", "Text Files (*.txt);;All Files (*)")
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
                elif isinstance(action, MouseMoveClick):
                    file.write(f"MoveClick,{action.x},{action.y},{action.time}\n")
                elif isinstance(action, MouseDrag):
                    file.write(f"MouseDrag,{action.x},{action.y},{action.time}\n")

    def load_actions(self):
        if QMessageBox.warning(self, "Warning", "Loading a new file will remove your current actions list. Would you like to continue?",
                               QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return

        filepath, _ = QFileDialog.getOpenFileName(self, "Load Actions", "", "Text Files (*.txt);;All Files (*)")
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
                            QMessageBox.critical(self, "Error", "File is incorrect!")
                            return
                    elif parts[0] == "Click" and len(parts) == 3:
                        try:
                            action = MouseClick(int(parts[1]), int(parts[2]))
                        except ValueError:
                            QMessageBox.critical(self, "Error", "File is incorrect!")
                            return
                    elif parts[0] == "Wait" and len(parts) == 2:
                        try:
                            action = Wait(float(parts[1]))
                        except ValueError:
                            QMessageBox.critical(self, "Error", "File is incorrect!")
                            return
                    elif parts[0] == "MoveClick" and len(parts) == 4:
                        try:
                            action = MouseMoveClick(int(parts[1]), int(parts[2]), float(parts[3]))
                        except ValueError:
                            QMessageBox.critical(self, "Error", "File is incorrect!")
                            return
                    elif parts[0] == "MouseDrag" and len(parts) == 4:
                        try:
                            action = MouseDrag(int(parts[1]), int(parts[2]), float(parts[3]))
                        except ValueError:
                            QMessageBox.critical(self, "Error", "File is incorrect!")
                            return
                    else:
                        QMessageBox.critical(self, "Error", "File is incorrect!")
                        return
                    temp_actions.append(action)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File does not exist.")
            return

        self.actions.clear()
        self.actions_list_widget.clear()
        for action in temp_actions:
            self.actions.append(action)
            if isinstance(action, MouseMove):
                self.actions_list_widget.addItem(f"Move: {action.x}, {action.y}, {action.time}")
            elif isinstance(action, MouseClick):
                self.actions_list_widget.addItem(f"Click: {action.x}, {action.y}")
            elif isinstance(action, Wait):
                self.actions_list_widget.addItem(f"Wait: {action.time}s")
            elif isinstance(action, MouseMoveClick):
                self.actions_list_widget.addItem(f"MoveClick: {action.x}, {action.y}, {action.time}")
            elif isinstance(action, MouseDrag):
                self.actions_list_widget.addItem(f"MouseDrag: {action.x}, {action.y}, {action.time}")


    #def select_all_actions(self, event=None):
        #self.actions_listbox.select_set(0, tk.END) #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2
    
    def select_all_actions(self):
        self.actions_list_widget.clearSelection()  # Wyczyść istniejące zaznaczenia

        for i in range(self.actions_list_widget.count()):
            item = self.actions_list_widget.item(i)
            item.setSelected(True)

    def stop_actions(self):
        if not self.running:
            return

        self.running = False
        QMessageBox.information(self, "Info", "Actions stopped.")
        self.actions_list_widget.clearSelection()
    
    def show_shortcuts(self):
        message = "Shortcuts:\n\n" \
                  "Add MoveClick: Ctrl+1\n" \
                  "Add Move: Ctrl+2\n" \
                  "Add Click: Ctrl+3\n" \
                  "Add Wait: Ctrl+4\n" \
                  "Add Mouse Drag: Ctrl+5\n" \
                  "Run: Ctrl+R\n" \
                  "Stop: Ctrl+S\n" \
                  "Check Coordinates: Ctrl+C\n" \
                  "Save: Ctrl+S\n" \
                  "Load: Ctrl+L\n" \
                  "Edit: Ctrl+E\n" \
                  "Delete: Ctrl+D\n" \
                  "Show Shortcuts: Ctrl+H"
        QMessageBox.information(self, "Shortcuts", message)

    def copy_action(self):
        selected_index = self.actions_list_widget.currentRow()
        if selected_index != -1:
            self.copied_action = copy.deepcopy(self.actions[selected_index])
        

    def paste_action(self):
        if self.copied_action is not None:
            selected_index = self.actions_list_widget.currentRow()
            if selected_index != -1:
                insert_position = selected_index + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, self.copied_action)
            if isinstance(self.copied_action, MouseMove):
                self.actions_list_widget.insertItem(insert_position, f"Move: {self.copied_action.x}, {self.copied_action.y}, {self.copied_action.time}")
            elif isinstance(self.copied_action, MouseClick):
                self.actions_list_widget.insertItem(insert_position, f"Click: {self.copied_action.x}, {self.copied_action.y}")
            elif isinstance(self.copied_action, Wait):
                self.actions_list_widget.insertItem(insert_position, f"Wait: {self.copied_action.time}s")
            elif isinstance(self.copied_action, MouseMoveClick):
                self.actions_list_widget.insertItem(insert_position, f"MoveClick: {self.copied_action.x}, {self.copied_action.y}, {self.copied_action.time}")
            elif isinstance(self.copied_action, MouseDrag):
                self.actions_list_widget.insertItem(insert_position, f"MouseDrag: {self.copied_action.x}, {self.copied_action.y}, {self.copied_action.time}")
            self.update_actions_history()

    def undo_action(self):
        if self.actions_history:
            self.actions = self.actions_history.pop()
            self.refresh_actions_listbox()
        else:
            QMessageBox.information(self, "Info", "Actions history is empty.")


    def update_actions_history(self):
        self.actions_history.append(copy.deepcopy(self.actions))

    def refresh_actions_listbox(self):
        self.actions_list_widget.clear()
        for action in self.actions:
            if isinstance(action, MouseMove):
                self.actions_list_widget.addItem(f"Move: {action.x}, {action.y}, {action.time}")
            elif isinstance(action, MouseClick):
                self.actions_list_widget.addItem(f"Click: {action.x}, {action.y}")
            elif isinstance(action, Wait):
                self.actions_list_widget.addItem(f"Wait: {action.time}s")
            elif isinstance(action, MouseMoveClick):
                self.actions_list_widget.addItem(f"MoveClick: {action.x}, {action.y}, {action.time}")
            elif isinstance(action, MouseDrag):
                self.actions_list_widget.addItem(f"MouseDrag: {action.x}, {action.y}, {action.time}")

    def check_coordinates(self):
        x, y = pyautogui.position()
        coord_window = QMessageBox(self)
        coord_window.setWindowTitle("Current Mouse Position")
        coord_label = QLabel(f"X: {x}, Y: {y}")
        coord_label.setAlignment(Qt.AlignCenter)  
        coord_window.layout().addWidget(coord_label, 0, Qt.AlignLeft) 
        coord_window.setStyleSheet("QLabel{min-width: 500px; font-size: 20pt;}")



        add_move_button = coord_window.addButton("Add Move", QMessageBox.ActionRole)
        add_click_button = coord_window.addButton("Add Click", QMessageBox.ActionRole)
        add_move_click_button = coord_window.addButton("Add MoveClick", QMessageBox.ActionRole)
        add_mouse_drag_button = coord_window.addButton("Add Mouse Drag", QMessageBox.ActionRole)
        close_button = coord_window.addButton("Close", QMessageBox.RejectRole)

        coord_window.exec()

        if coord_window.clickedButton() == add_move_button:
            move_action = MouseMove(x, y, 1)
            self.actions.append(move_action)
            self.actions_list_widget.addItem(f"Move: {move_action.x}, {move_action.y}, {move_action.time}")
            self.update_actions_history()
        elif coord_window.clickedButton() == add_click_button:
            click_action = MouseClick(x, y)
            self.actions.append(click_action)
            self.actions_list_widget.addItem(f"Click: {click_action.x}, {click_action.y}")
            self.update_actions_history()
        elif coord_window.clickedButton() == add_move_click_button:
            move_click_action = MouseMoveClick(x, y, 1)
            self.actions.append(move_click_action)
            self.actions_list_widget.addItem(f"MoveClick: {move_click_action.x}, {move_click_action.y}, {move_click_action.time}")
            self.update_actions_history()
        elif coord_window.clickedButton() == add_mouse_drag_button:
            mouse_drag_action = MouseDrag(x, y, 1)
            self.actions.append(mouse_drag_action)
            self.actions_list_widget.addItem(f"MouseDrag: {mouse_drag_action.x}, {mouse_drag_action.y}, {mouse_drag_action.time}")
            self.update_actions_history()

