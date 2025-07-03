from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator

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