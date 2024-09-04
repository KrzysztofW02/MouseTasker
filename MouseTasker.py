from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QAction, QMenu, QMenuBar, QHBoxLayout, QFileDialog, QMessageBox, QDialog, QShortcut, QLabel, QAbstractItemView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtGui
from actions import MouseMove, MouseClick, Wait, MouseMoveClick, MouseDrag
from dialogs import MoveDialog, ClickDialog, WaitDialog, MoveClickDialog, MouseDragDialog, LoopDialog, AdvancedOptionsDialog, SetupWaitRangeDialog, SetupMoveClickTimeRangeDialog, SetupCoordRangeDialog, SetupClickCoordDialog, SetupMoveCoordDialog, SetupMoveTimeDialog, SetupTimeRangeDialog, SetupClickCoordRangeDialog
from chat import ChatDialog
import keyboard
import pyautogui
import copy
import random

class ActionExecutor(QThread):
    update_action_index = pyqtSignal(int)
    action_completed = pyqtSignal()

    def __init__(self, actions, start_index=0, loop_count=1):
        super().__init__()
        self.actions = actions
        self.start_index = start_index
        self.running = True
        self.loop_count = loop_count

    def run(self):
        for _ in range(self.loop_count):
            if not self.running:
                break
            current_action_index = 0
            while self.running and current_action_index < len(self.actions):
                adjusted_index = current_action_index + self.start_index
                self.update_action_index.emit(adjusted_index)
                action = self.actions[current_action_index]
                action.execute()
                current_action_index += 1
        self.action_completed.emit()

    def stop_execution(self):
        self.running = False

class MainWindow(QMainWindow):
    run_stop_signal = pyqtSignal()
    run_stop_loop_signal = pyqtSignal()
    check_coordinates_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MouseTasker")
        self.actions = []
        self.running = False
        self.executor_thread = None
        self.copied_action = None
        self.actions_history = []
        self.chat_dialog = None
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.setup_shortcuts()

        self.update_actions_history()
        
        screen_width = pyautogui.size().width
        window_width = screen_width // 2
        self.setGeometry(100, 100, window_width, 500)

        self.setup_ui()
        self.create_menu()

        self.actions_running = False

        self.run_stop_signal.connect(self.toggle_run_stop_actions)
        self.run_stop_loop_signal.connect(self.toogle_run_stop_loop_actions)
        self.check_coordinates_signal.connect(self.check_coordinates)

    def setup_shortcuts(self):
        keyboard.add_hotkey('f1', self.run_stop_signal.emit)
        keyboard.add_hotkey('f2', self.run_stop_loop_signal.emit)
        keyboard.add_hotkey('f3', self.check_coordinates_signal.emit)

        shortcut_delete_action = QShortcut(QKeySequence.Delete, self)
        shortcut_delete_action.activated.connect(self.delete_action)

        shortcut_save_actions = QShortcut(QKeySequence('Ctrl+S'), self)
        shortcut_save_actions.activated.connect(self.save_actions)

        shortcut_advanced_options = QShortcut(QKeySequence('F4'), self)
        shortcut_advanced_options.activated.connect(self.open_advanced_options_dialog)

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

        shortcut_select_all_actions = QShortcut(QKeySequence('Ctrl+L'), self)
        shortcut_select_all_actions.activated.connect(self.load_actions)

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

        self.chat_button = QPushButton("Open Chat")
        self.chat_button.clicked.connect(self.open_chat_dialog)
        self.top_buttons_layout.addWidget(self.chat_button)

        self.run_button = QPushButton("Run")
        self.run_menu = QMenu()
        self.run_action = QAction("Run", self)
        self.run_loop_action = QAction("Run in Loop", self)

        self.run_menu.addAction(self.run_action)
        self.run_menu.addAction(self.run_loop_action)

        self.run_action.triggered.connect(self.run_actions)
        self.run_loop_action.triggered.connect(self.run_actions_in_loop)
        
        self.run_button.setMenu(self.run_menu)
        
        self.top_buttons_layout.addWidget(self.run_button)

        self.actions_list_widget = QListWidget()
        self.actions_list_widget.itemDoubleClicked.connect(self.edit_action)
        self.actions_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.actions_list_widget.setStyleSheet("QListWidget { font-size: 11pt; }")
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

        self.Advanced_Options_button = QPushButton("Advanced Options")
        self.Advanced_Options_button.clicked.connect(self.open_advanced_options_dialog)
        self.bottom_buttons_layout.addWidget(self.Advanced_Options_button)

    #Menu bar
    def create_menu(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        save_action = QAction("Save\tCtrl+S", self)
        save_action.triggered.connect(self.save_actions)
        file_menu.addAction(save_action)

        load_action = QAction("Load\tCtrl+L", self)
        load_action.triggered.connect(self.load_actions)
        file_menu.addAction(load_action)

        edit_menu = QMenu("Edit", self)
        menu_bar.addMenu(edit_menu)

        undo_action = QAction("Undo\tCtrl+Z", self)
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)

        copy_action = QAction("Copy\tCtrl+C", self)
        copy_action.triggered.connect(self.copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste\tCtrl+V", self)
        paste_action.triggered.connect(self.paste_action)
        edit_menu.addAction(paste_action)

        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)
        about_me_action = QAction("About Me", self)
        help_menu.addAction(about_me_action)
        about_me_action.triggered.connect(self.show_about_dialog)

        shortcuts_action = QAction("Shortcuts\tF5", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def show_about_dialog(self):
        QMessageBox.about(self, "About Me", "Author: Krzysztof Wąsik\n" \
                                "GitHub: github.com/KrzysztofW02\n" \
                                "Contact: Krzysztof.Wasik2002@gmail.com\n")

    def add_move(self):
        dialog = MoveDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y, time = dialog.result
            action = MouseMove(x, y, time)
            selected_index = self.actions_list_widget.currentRow()
            if selected_index != -1:
                insert_position = selected_index + 1
            else:
                insert_position = len(self.actions)
            self.actions.append(action)
            self.actions_list_widget.insertItem(insert_position, str(action))
            self.update_actions_history()
        

    def add_click(self):
        dialog = ClickDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y = dialog.result
            action = MouseClick(x, y)
            selected_index = self.actions_list_widget.currentRow()
            if selected_index != -1:
                insert_position = selected_index + 1
            else:
                insert_position = len(self.actions)
            self.actions.append(action)
            self.actions_list_widget.insertItem(insert_position, str(action))
            self.update_actions_history()

    def add_wait(self):
        dialog = WaitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            time = dialog.result
            action = Wait(time)
            selected_index = self.actions_list_widget.currentRow()
            if selected_index != -1:
                insert_position = selected_index + 1
            else:
                insert_position = len(self.actions)
            self.actions.append(action)
            self.actions_list_widget.insertItem(insert_position, str(action))
            self.update_actions_history()
    
    def add_move_click(self):
        dialog = MoveClickDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y, time = dialog.result
            action = MouseMoveClick(x, y, time)
            selected_index = self.actions_list_widget.currentRow()
            if selected_index != -1:
                insert_position = selected_index + 1
            else:
                insert_position = len(self.actions)
            self.actions.append(action)
            self.actions_list_widget.insertItem(insert_position, str(action))
            self.update_actions_history()

    def add_mouse_drag(self):
        dialog = MouseDragDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x, y, time = dialog.result
            action = MouseDrag(x, y, time)
            selected_index = self.actions_list_widget.currentRow()
            if selected_index != -1:
                insert_position = selected_index + 1
            else:
                insert_position = len(self.actions)
            self.actions.insert(insert_position, action)
            self.actions_list_widget.insertItem(insert_position, str(action))
            self.update_actions_history()

    def open_chat_dialog(self):
        if self.chat_dialog is None:
            self.chat_dialog = ChatDialog(self)
        self.chat_dialog.show()
        self.chat_dialog.raise_()
        self.chat_dialog.activateWindow()


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
            selected_indices = sorted([self.actions_list_widget.row(item) for item in selected_items], reverse=True)
            for index in selected_indices:
                del self.actions[index]
                self.actions_list_widget.takeItem(index)
            
            self.update_actions_history()

    def toggle_run_stop_actions(self):
        if not self.actions_running:
            self.run_actions()
        else:
            self.stop_actions()

    def toogle_run_stop_loop_actions(self):
        if not self.actions_running:
            self.run_actions_in_loop()
        else:
            self.stop_actions()

    def run_actions(self):
        if self.actions_running:
            QMessageBox.warning(self, "Already Running", "Actions are already running.")
            return

        selected_items = self.actions_list_widget.selectedItems()
        if selected_items:
            selected_index = self.actions_list_widget.row(selected_items[0])
        else:
            selected_index = 0 

        actions_to_execute = self.actions[selected_index:]
        if not actions_to_execute:
            QMessageBox.warning(self, "No Actions", "There are no actions to execute.")
            return

        self.executor_thread = ActionExecutor(actions_to_execute, selected_index)
        self.executor_thread.update_action_index.connect(self.highlight_action)
        self.executor_thread.action_completed.connect(self.on_actions_completed)
        self.executor_thread.start()
        self.actions_running = True

    def run_actions_in_loop(self):
        if self.actions_running:
            QMessageBox.warning(self, "Already Running", "Actions are already running.")
            return

        actions_to_execute = self.actions
        if not actions_to_execute:
            QMessageBox.warning(self, "No Actions", "There are no actions to execute.")
            return
        
        dialog = LoopDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            loop_count = dialog.loop_count

            self.executor_thread = ActionExecutor(actions_to_execute, loop_count=loop_count)
            self.executor_thread.update_action_index.connect(self.highlight_action)
            self.executor_thread.action_completed.connect(self.on_actions_completed)
            self.executor_thread.start()
            self.actions_running = True


    def stop_actions(self):
        if self.executor_thread and self.executor_thread.isRunning():
            self.executor_thread.stop_execution()
            self.executor_thread.wait()
            self.actions_running = False
            QMessageBox.information(self, "Info", "Actions have been stopped.")

    def highlight_action(self, index):
        self.actions_list_widget.setCurrentRow(index)

    def on_actions_completed(self):
        self.actions_running = False

    def save_actions(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Actions", "", "Text Files (*.txt);;All Files (*)")
        if not filepath:
            return
        if not filepath.endswith('.txt'):
            filepath += '.txt'
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
        
    
    def select_all_actions(self):
        self.actions_list_widget.clearSelection() 

        for i in range(self.actions_list_widget.count()):
            item = self.actions_list_widget.item(i)
            item.setSelected(True)
    
    def show_shortcuts(self):
        message = "Copy: Ctrl+C      " \
                  "Undo: Ctrl+Z\n\n" \
                  "Save: Ctrl+S      " \
                  "Paste: Ctrl+V\n\n" \
                  "RUN / STOP: F1      " \
                  "RUN LOOP / STOP: F2\n\n" \
                  "Check Coordinates: F3      " \
                  "Advanced Options: F4\n\n" \
                  "Load: Ctrl+L      " \
                  "Delete: Delete\n\n" \
                  "Show Shortcuts: F5"
        QMessageBox.information(self, "Shortcuts", message)

    def copy_action(self):
        selected_items = self.actions_list_widget.selectedItems()
        if selected_items:
            self.copied_actions = [copy.deepcopy(self.actions[self.actions_list_widget.row(item)]) for item in selected_items]

    def paste_action(self):
        if hasattr(self, 'copied_actions') and self.copied_actions:
            selected_index = self.actions_list_widget.currentRow()
            insert_position = selected_index + 1 if selected_index != -1 else len(self.actions)

            for action in self.copied_actions:
                self.actions.insert(insert_position, action)
                if isinstance(action, MouseMove):
                    self.actions_list_widget.insertItem(insert_position, f"Move: {action.x}, {action.y}, {action.time}")
                elif isinstance(action, MouseClick):
                    self.actions_list_widget.insertItem(insert_position, f"Click: {action.x}, {action.y}")
                elif isinstance(action, Wait):
                    self.actions_list_widget.insertItem(insert_position, f"Wait: {action.time}s")
                elif isinstance(action, MouseMoveClick):
                    self.actions_list_widget.insertItem(insert_position, f"MoveClick: {action.x}, {action.y}, {action.time}")
                elif isinstance(action, MouseDrag):
                    self.actions_list_widget.insertItem(insert_position, f"MouseDrag: {action.x}, {action.y}, {action.time}")
                insert_position += 1

            self.update_actions_history()
    
    def undo_action(self):
        if len(self.actions_history) > 1: 
            self.actions_history.pop()  
            self.actions = self.actions_history[-1]  
            self.refresh_actions_listbox()
        elif len(self.actions_history) == 1:
            self.actions = []  
            self.actions_history = []  
            self.refresh_actions_listbox()


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


    def open_advanced_options_dialog(self):
        dialog = AdvancedOptionsDialog(self, self)
        dialog.exec_()

    def open_setup_wait_range_dialog(self):
        dialog = SetupWaitRangeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            min_time, max_time = dialog.result
            self.random_time_in_wait(min_time, max_time)

    def open_setup_move_time_dialog(self):
        dialog = SetupMoveClickTimeRangeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            min_time, max_time = dialog.result
            self.random_time_in_moves_movesclicks(min_time, max_time)

    def open_setup_move_coord_dialog(self):
        dialog = SetupCoordRangeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x_min, x_max, y_min, y_max = dialog.result
            self.random_coord_in_moves_moveclicks(x_min, x_max, y_min, y_max)

    def open_setup_click_coord_dialog(self):
        dialog = SetupClickCoordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x_min, x_max, y_min, y_max = dialog.result
            self.random_coord_in_clicks(x_min, x_max, y_min, y_max)

    def open_setup_coord_range_dialog(self):
        dialog = SetupMoveCoordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x = dialog.result
            self.change_coord_in_moves_moveclicks(x)
    
    def open_setup_moveclick_time_range_dialog(self):
        dialog = SetupMoveTimeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            time = dialog.result
            self.change_time_in_moves_movesclicks(time)
    
    def open_setup_time_range_dialog(self):
        dialog = SetupTimeRangeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            time = dialog.result
            self.change_random_time_in_wait(time)

    def open_setup_click_coord_range_dialog(self):
        dialog = SetupClickCoordRangeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            x = dialog.result
            self.change_random_coord_in_clicks(x)
            


    def random_time_in_moves_movesclicks(self, min_time, max_time):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to randomize time for.")
            return

        for action in self.actions:
            if isinstance(action, (MouseMove, MouseMoveClick)):
                action.time = random.uniform(min_time, max_time)
        self.update_actions_history()        
        self.refresh_actions_listbox()


    def random_coord_in_moves_moveclicks(self, x_min, x_max, y_min, y_max):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to randomize coordinates for.")
            return

        screen_width, screen_height = pyautogui.size()
        x_max = x_max if x_max is not None else screen_width
        y_max = y_max if y_max is not None else screen_height

        for action in self.actions:
            if isinstance(action, (MouseMove, MouseMoveClick)):
                action.x = random.randint(x_min, x_max)
                action.y = random.randint(y_min, y_max)
        self.update_actions_history()   
        self.refresh_actions_listbox()

    def random_coord_in_clicks(self, x_min=0, x_max=None, y_min=0, y_max=None):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to randomize coordinates for.")
            return
        
        screen_width, screen_height = pyautogui.size()
        x_max = x_max if x_max is not None else screen_width
        y_max = y_max if y_max is not None else screen_height

        for action in self.actions:
            if isinstance(action, MouseClick):
                action.x = random.randint(x_min, x_max)
                action.y = random.randint(y_min, y_max)
        self.update_actions_history()   
        self.refresh_actions_listbox()

    def random_time_in_wait(self, min_time, max_time):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to randomize time for.")
            return

        for action in self.actions:
            if isinstance(action, Wait):
                action.time = random.uniform(min_time, max_time)
        self.update_actions_history()   
        self.refresh_actions_listbox()

    def change_coord_in_moves_moveclicks(self, x):
        if not self.actions: 
            QMessageBox.warning(self, "Warning", "No actions to change coordinates for.")
            return
        
        for action in self.actions:
            if isinstance(action, (MouseMove, MouseMoveClick)):
                action.x = action.x + random.randint(-x, x)
                action.y = action.y + random.randint(-x, x)
        self.update_actions_history()
        self.refresh_actions_listbox()

    def change_time_in_moves_movesclicks(self, time):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to change time for.")
            return

        for action in self.actions:
            if isinstance(action, (MouseMove, MouseMoveClick)):
                action.time = max(0.01, action.time + random.uniform(-time, time))
        self.update_actions_history()
        self.refresh_actions_listbox()

    def change_random_time_in_wait(self, time):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to change time for.")
            return

        for action in self.actions:
            if isinstance(action, Wait):
                action.time = max(0.01, action.time + random.uniform(-time, time))
        self.update_actions_history()
        self.refresh_actions_listbox()
    
    def change_random_coord_in_clicks(self, x):
        if not self.actions:
            QMessageBox.warning(self, "Warning", "No actions to change coordinates for.")
            return

        for action in self.actions:
            if isinstance(action, MouseClick):
                action.x = action.x + random.randint(-x, x)
                action.y = action.y + random.randint(-x, x)
        self.update_actions_history()
        self.refresh_actions_listbox()

    def refresh_actions_listbox(self):
        self.actions_list_widget.clear()
        for action in self.actions:
            if isinstance(action, MouseMove):
                self.actions_list_widget.addItem(f"Move: {action.x}, {action.y}, {action.time:.2f}s")
            elif isinstance(action, MouseClick):
                self.actions_list_widget.addItem(f"Click: {action.x}, {action.y}")
            elif isinstance(action, Wait):
                self.actions_list_widget.addItem(f"Wait: {action.time:.2f}s")
            elif isinstance(action, MouseMoveClick):
                self.actions_list_widget.addItem(f"MoveClick: {action.x}, {action.y}, {action.time:.2f}s")
            elif isinstance(action, MouseDrag):
                self.actions_list_widget.addItem(f"MouseDrag: {action.x}, {action.y}, {action.time:.2f}s")


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

        selected_index = self.actions_list_widget.currentRow()
        insert_position = selected_index + 1 if selected_index != -1 else len(self.actions)

        if coord_window.clickedButton() == add_move_button:
            move_action = MouseMove(x, y, 1)
            self.actions.insert(insert_position, move_action)
            self.actions_list_widget.insertItem(insert_position, f"Move: {move_action.x}, {move_action.y}, {move_action.time}s")
        elif coord_window.clickedButton() == add_click_button:
            click_action = MouseClick(x, y)
            self.actions.insert(insert_position, click_action)
            self.actions_list_widget.insertItem(insert_position, f"Click: {click_action.x}, {click_action.y}")
        elif coord_window.clickedButton() == add_move_click_button:
            move_click_action = MouseMoveClick(x, y, 1)
            self.actions.insert(insert_position, move_click_action)
            self.actions_list_widget.insertItem(insert_position, f"MoveClick: {move_click_action.x}, {move_click_action.y}, {move_click_action.time}s")
        elif coord_window.clickedButton() == add_mouse_drag_button:
            mouse_drag_action = MouseDrag(x, y, 1)
            self.actions.insert(insert_position, mouse_drag_action)
            self.actions_list_widget.insertItem(insert_position, f"MouseDrag: {mouse_drag_action.x}, {mouse_drag_action.y}, {mouse_drag_action.time}s")

        self.update_actions_history()
