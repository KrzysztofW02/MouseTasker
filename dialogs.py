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

        self.random_time_in_moves_movesclicks_button = QPushButton("Random Time in Moves, MoveClicks")
        self.random_time_in_moves_movesclicks_button.clicked.connect(self.random_time_in_moves_movesclicks)
        layout.addWidget(self.random_time_in_moves_movesclicks_button)

        self.random_coord_in_moves_moveclicks_button = QPushButton("Random coordinates in Moves, MoveClicks")
        self.random_coord_in_moves_moveclicks_button.clicked.connect(self.random_coord_in_moves_moveclicks)
        layout.addWidget(self.random_coord_in_moves_moveclicks_button)

        self.random_coord_in_clicks_button = QPushButton("Random coordinates in Clicks")
        self.random_coord_in_clicks_button.clicked.connect(self.random_coord_in_clicks)
        layout.addWidget(self.random_coord_in_clicks_button)

        self.random_time_in_wait_button = QPushButton("Random time in Waits")
        self.random_time_in_wait_button.clicked.connect(self.random_time_in_wait)
        layout.addWidget(self.random_time_in_wait_button)

        self.setLayout(layout)

    def random_time_in_moves_movesclicks(self):
        if self.main_application:
            self.main_application.random_time_in_moves_movesclicks()

    def random_coord_in_moves_moveclicks(self):
        if self.main_application:
            self.main_application.random_coord_in_moves_moveclicks()

    def random_coord_in_clicks(self):
        if self.main_application:
            self.main_application.random_coord_in_clicks()

    def random_time_in_wait(self):
        if self.main_application:
            self.main_application.random_time_in_wait()


class CustomDoubleValidator(QDoubleValidator):
    def __init__(self, *args):
        super().__init__(*args)
        self.setLocale(QLocale(QLocale.English))

    def validate(self, string, pos):
        if 'e' in string.lower() or ',' in string:
            return (QValidator.Invalid, string, pos)
        return super().validate(string, pos)