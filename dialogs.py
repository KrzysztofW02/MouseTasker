from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class MoveDialog(QDialog):
    def __init__(self, parent=None, x=None, y=None, time=None):
        super().__init__(parent)
        self.setWindowTitle("Move Action")
        
        self.layout = QVBoxLayout()
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)
        self.time_input = QLineEdit(self)
        
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