from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt5.QtCore import QLocale

class MoveDialog(QDialog):
    def __init__(self, parent=None, x=None, y=None, time=None):
        super().__init__(parent)
        self.setWindowTitle("Move Action")
        
        self.layout = QVBoxLayout()
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)
        self.time_input = QLineEdit(self)

        int_validator = QIntValidator(self)
        double_validator = CustomDoubleValidator()
        self.x_input.setValidator(int_validator)
        self.y_input.setValidator(int_validator)
        self.time_input.setValidator(double_validator)
        
        if x is not None:
            self.x_input.setText(str(x))
        if y is not None:
            self.y_input.setText(str(y))
        if time is not None:
            self.time_input.setText(str(time))
        
        self.layout.addWidget(QLabel("X:"))
        self.layout.addWidget(self.x_input)
        self.layout.addWidget(QLabel("Y:"))
        self.layout.addWidget(self.y_input)
        self.layout.addWidget(QLabel("Time:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None

    def accept(self):
        if not self.x_input.text() or not self.y_input.text() or not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            self.result = (int(self.x_input.text()), int(self.y_input.text()), float(self.time_input.text()))
        except ValueError:
            pass
        super().accept()

class ClickDialog(QDialog):
    def __init__(self, parent=None, x=None, y=None):
        super().__init__(parent)
        self.setWindowTitle("Click Action")
        
        self.layout = QVBoxLayout()
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)

        int_validator = QIntValidator(self)
        self.x_input.setValidator(int_validator)
        self.y_input.setValidator(int_validator)

        if x is not None:
            self.x_input.setText(str(x))
        if y is not None:
            self.y_input.setText(str(y))
        
        self.layout.addWidget(QLabel("X:"))
        self.layout.addWidget(self.x_input)
        self.layout.addWidget(QLabel("Y:"))
        self.layout.addWidget(self.y_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None

    def accept(self):
        if not self.x_input.text() or not self.y_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        self.result = (int(self.x_input.text()), int(self.y_input.text()))
        super().accept()


class WaitDialog(QDialog):
    def __init__(self, parent=None, time=None):
        super().__init__(parent)
        self.setWindowTitle("Wait Action")
        
        self.layout = QVBoxLayout()
        self.time_input = QLineEdit(self)

        double_validator = CustomDoubleValidator()
        self.time_input.setValidator(double_validator)

        if time is not None:
            self.time_input.setText(str(time))
        
        self.layout.addWidget(QLabel("Time:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None

    def accept(self):
        if not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        self.result = float(self.time_input.text())
        super().accept()
    

class MoveClickDialog(QDialog):
    def __init__(self, parent=None, x=None, y=None, time=None):
        super().__init__(parent)
        self.setWindowTitle("MoveClick Action")
        
        self.layout = QVBoxLayout()
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)
        self.time_input = QLineEdit(self)

        int_validator = QIntValidator(self)
        double_validator = CustomDoubleValidator()
        self.x_input.setValidator(int_validator)
        self.y_input.setValidator(int_validator)
        self.time_input.setValidator(double_validator)

        if x is not None:
            self.x_input.setText(str(x))
        if y is not None:
            self.y_input.setText(str(y))
        if time is not None:
            self.time_input.setText(str(time))
        
        self.layout.addWidget(QLabel("X:"))
        self.layout.addWidget(self.x_input)
        self.layout.addWidget(QLabel("Y:"))
        self.layout.addWidget(self.y_input)
        self.layout.addWidget(QLabel("Time:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None

    def accept(self):
        if not self.x_input.text() or not self.y_input.text() or not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        self.result = (int(self.x_input.text()), int(self.y_input.text()), float(self.time_input.text()))
        super().accept()

class MouseDragDialog(QDialog):
    def __init__(self, parent=None, x=None, y=None, time=None):
        super().__init__(parent)
        self.setWindowTitle("MouseDrag Action")
        
        self.layout = QVBoxLayout()
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)
        self.time_input = QLineEdit(self)

        int_validator = QIntValidator(self)
        double_validator = CustomDoubleValidator()
        self.x_input.setValidator(int_validator)
        self.y_input.setValidator(int_validator)
        self.time_input.setValidator(double_validator)

        if x is not None:
            self.x_input.setText(str(x))
        if y is not None:
            self.y_input.setText(str(y))
        if time is not None:
            self.time_input.setText(str(time))
        
        self.layout.addWidget(QLabel("X:"))
        self.layout.addWidget(self.x_input)
        self.layout.addWidget(QLabel("Y:"))
        self.layout.addWidget(self.y_input)
        self.layout.addWidget(QLabel("Time:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None

    def accept(self):
        if not self.x_input.text() or not self.y_input.text() or not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        self.result = (int(self.x_input.text()), int(self.y_input.text()), float(self.time_input.text()))
        super().accept()

class LoopDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Run in Loop")
        self.layout = QVBoxLayout()

        self.label = QLabel("Enter number of loops:")
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        self.button_box = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_box.addWidget(self.ok_button)
        self.button_box.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_box)
        self.setLayout(self.layout)

    def accept(self):
        try:
            self.loop_count = int(self.input_field.text())
            if self.loop_count <= 0:
                raise ValueError
            super().accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a positive integer.")

class AdvancedOptionsDialog(QDialog):
    def __init__(self, parent=None, main_application=None):
        super().__init__(parent)
        self.main_application = main_application
        self.setWindowTitle("Advanced Options")
        layout = QVBoxLayout()

        self.random_time_in_moves_movesclicks_button = QPushButton("Randomize Move/MoveClick Times")
        self.random_time_in_moves_movesclicks_button.clicked.connect(self.random_time_in_moves_movesclicks)
        layout.addWidget(self.random_time_in_moves_movesclicks_button)

        self.random_coord_in_moves_moveclicks_button = QPushButton("Randomize Move/MoveClick Coordinates")
        self.random_coord_in_moves_moveclicks_button.clicked.connect(self.random_coord_in_moves_moveclicks)
        layout.addWidget(self.random_coord_in_moves_moveclicks_button)

        self.random_coord_in_clicks_button = QPushButton("Randomize Click Coordinates")
        self.random_coord_in_clicks_button.clicked.connect(self.random_coord_in_clicks)
        layout.addWidget(self.random_coord_in_clicks_button)

        self.random_time_in_wait_button = QPushButton("Randomize Wait Times")
        self.random_time_in_wait_button.clicked.connect(self.random_time_in_wait)
        layout.addWidget(self.random_time_in_wait_button)

        self.random_coord_in_moves_moveclicks_button2 = QPushButton("Offset Move/MoveClick Coordinates")
        self.random_coord_in_moves_moveclicks_button2.clicked.connect(self.change_coord_in_moves_moveclicks)
        layout.addWidget(self.random_coord_in_moves_moveclicks_button2)

        self.random_time_in_moves_moveclicks_button2 = QPushButton("Offset Move/MoveClick Times")
        self.random_time_in_moves_moveclicks_button2.clicked.connect(self.change_time_in_moves_movesclicks)
        layout.addWidget(self.random_time_in_moves_moveclicks_button2)

        self.random_time_in_wait_button2 = QPushButton("Offset Wait Times")
        self.random_time_in_wait_button2.clicked.connect(self.change_random_time_in_wait)
        layout.addWidget(self.random_time_in_wait_button2)

        self.random_coord_in_clicks2 = QPushButton("Offset Click Coordinates")
        self.random_coord_in_clicks2.clicked.connect(self.change_coord_in_clicks)
        layout.addWidget(self.random_coord_in_clicks2)

        self.setLayout(layout)

    def random_time_in_moves_movesclicks(self):
        if self.main_application:
            self.main_application.open_setup_move_time_dialog()

    def random_coord_in_moves_moveclicks(self):
        if self.main_application:
            self.main_application.open_setup_move_coord_dialog()

    def random_coord_in_clicks(self):
        if self.main_application:
            self.main_application.open_setup_click_coord_dialog()

    def random_time_in_wait(self):
        if self.main_application:
            self.main_application.open_setup_wait_range_dialog()

    def change_coord_in_moves_moveclicks(self):
        if self.main_application:
            self.main_application.open_setup_coord_range_dialog()
    
    def change_time_in_moves_movesclicks(self):
        if self.main_application:
            self.main_application.open_setup_moveclick_time_range_dialog()

    def change_random_time_in_wait(self):
        if self.main_application:
            self.main_application.open_setup_time_range_dialog()

    def change_coord_in_clicks(self):
        if self.main_application:
            self.main_application.open_setup_click_coord_range_dialog()

class SetupWaitRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Range")
        self.layout = QVBoxLayout()
        
        self.min_time_input = QLineEdit(self)
        self.max_time_input = QLineEdit(self)
        
        double_validator = CustomDoubleValidator()
        self.min_time_input.setValidator(double_validator)
        self.max_time_input.setValidator(double_validator)
        
        self.layout.addWidget(QLabel("Min Time:"))
        self.layout.addWidget(self.min_time_input)
        self.layout.addWidget(QLabel("Max Time:"))
        self.layout.addWidget(self.max_time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.min_time_input.text() or not self.max_time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            min_time = float(self.min_time_input.text())
            max_time = float(self.max_time_input.text())
            if min_time > max_time:
                raise ValueError("Minimum time should not be greater than maximum time.")
            self.result = (min_time, max_time)
        except ValueError as e:
            QMessageBox.warning(self, "Warning", f"Invalid input: {e}")
            return
        super().accept()

class SetupMoveClickTimeRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup MoveClick Time Range")
        self.layout = QVBoxLayout()
        
        self.min_time_input = QLineEdit(self)
        self.max_time_input = QLineEdit(self)
        
        double_validator = CustomDoubleValidator()
        self.min_time_input.setValidator(double_validator)
        self.max_time_input.setValidator(double_validator)
        
        self.layout.addWidget(QLabel("Min Time:"))
        self.layout.addWidget(self.min_time_input)
        self.layout.addWidget(QLabel("Max Time:"))
        self.layout.addWidget(self.max_time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.min_time_input.text() or not self.max_time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            min_time = float(self.min_time_input.text())
            max_time = float(self.max_time_input.text())
            if min_time > max_time:
                raise ValueError("Minimum time should not be greater than maximum time.")
            self.result = (min_time, max_time)
        except ValueError as e:
            QMessageBox.warning(self, "Warning", f"Invalid input: {e}")
            return
        super().accept()

class SetupCoordRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Coordinate Range")
        self.layout = QVBoxLayout()
        
        self.min_x_input = QLineEdit(self)
        self.max_x_input = QLineEdit(self)
        self.min_y_input = QLineEdit(self)
        self.max_y_input = QLineEdit(self)
        
        int_validator = QIntValidator(self)
        self.min_x_input.setValidator(int_validator)
        self.max_x_input.setValidator(int_validator)
        self.min_y_input.setValidator(int_validator)
        self.max_y_input.setValidator(int_validator)
        
        self.layout.addWidget(QLabel("Min X:"))
        self.layout.addWidget(self.min_x_input)
        self.layout.addWidget(QLabel("Max X:"))
        self.layout.addWidget(self.max_x_input)
        self.layout.addWidget(QLabel("Min Y:"))
        self.layout.addWidget(self.min_y_input)
        self.layout.addWidget(QLabel("Max Y:"))
        self.layout.addWidget(self.max_y_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.min_x_input.text() or not self.max_x_input.text() or not self.min_y_input.text() or not self.max_y_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            min_x = int(self.min_x_input.text())
            max_x = int(self.max_x_input.text())
            min_y = int(self.min_y_input.text())
            max_y = int(self.max_y_input.text())
            if min_x > max_x or min_y > max_y:
                raise ValueError("Minimum values should not be greater than maximum values.")
            self.result = (min_x, max_x, min_y, max_y)
        except ValueError as e:
            QMessageBox.warning(self, "Warning", f"Invalid input: {e}")
            return
        super().accept()

class SetupClickCoordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Click Coordinate Range")
        self.layout = QVBoxLayout()
        
        self.min_x_input = QLineEdit(self)
        self.max_x_input = QLineEdit(self)
        self.min_y_input = QLineEdit(self)
        self.max_y_input = QLineEdit(self)
        
        int_validator = QIntValidator(self)
        self.min_x_input.setValidator(int_validator)
        self.max_x_input.setValidator(int_validator)
        self.min_y_input.setValidator(int_validator)
        self.max_y_input.setValidator(int_validator)
        
        self.layout.addWidget(QLabel("Min X:"))
        self.layout.addWidget(self.min_x_input)
        self.layout.addWidget(QLabel("Max X:"))
        self.layout.addWidget(self.max_x_input)
        self.layout.addWidget(QLabel("Min Y:"))
        self.layout.addWidget(self.min_y_input)
        self.layout.addWidget(QLabel("Max Y:"))
        self.layout.addWidget(self.max_y_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.min_x_input.text() or not self.max_x_input.text() or not self.min_y_input.text() or not self.max_y_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            min_x = int(self.min_x_input.text())
            max_x = int(self.max_x_input.text())
            min_y = int(self.min_y_input.text())
            max_y = int(self.max_y_input.text())
            if min_x > max_x or min_y > max_y:
                raise ValueError("Minimum values should not be greater than maximum values.")
            self.result = (min_x, max_x, min_y, max_y)
        except ValueError as e:
            QMessageBox.warning(self, "Warning", f"Invalid input: {e}")
            return
        super().accept()


class SetupMoveCoordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Move, MoveClicks Coordinates")
        self.layout = QVBoxLayout()
        
        self.x_input = QLineEdit(self)
        
        int_validator = QIntValidator(self)
        self.x_input.setValidator(int_validator)
        
        self.layout.addWidget(QLabel("Range:"))
        self.layout.addWidget(self.x_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.x_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            x = int(self.x_input.text())
            self.result = (x)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid input.")
            return
        super().accept()

class SetupMoveTimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Move, MoveClicks Time")
        self.layout = QVBoxLayout()
        
        self.time_input = QLineEdit(self)
        
        double_validator = CustomDoubleValidator()
        self.time_input.setValidator(double_validator)
        
        self.layout.addWidget(QLabel("Range:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            time = float(self.time_input.text())
            self.result = (time)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid input.")
            return
        super().accept()
    
class SetupTimeRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Time Range")
        self.layout = QVBoxLayout()
        
        self.time_input = QLineEdit(self)
        
        double_validator = CustomDoubleValidator()
        self.time_input.setValidator(double_validator)
        
        self.layout.addWidget(QLabel("Range:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            time = float(self.time_input.text())
            self.result = (time)
        except ValueError as e:
            QMessageBox.warning(self, "Warning", f"Invalid input: {e}")
            return
        super().accept()

class SetupClickCoordRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Setup Click Coordinates")
        self.layout = QVBoxLayout()
        
        self.x_input = QLineEdit(self)
        
        int_validator = QIntValidator(self)
        self.x_input.setValidator(int_validator)
        
        self.layout.addWidget(QLabel("Range:"))
        self.layout.addWidget(self.x_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        if not self.x_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        try:
            x = int(self.x_input.text())
            self.result = (x)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid input.")
            return
        super().accept()


class CustomDoubleValidator(QDoubleValidator):
    def __init__(self, *args):
        super().__init__(*args)
        self.setLocale(QLocale(QLocale.English))

    def validate(self, string, pos):
        if 'e' in string.lower() or ',' in string:
            return (QValidator.Invalid, string, pos)
        return super().validate(string, pos)