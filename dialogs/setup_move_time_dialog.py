from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from dialogs.custom_double_validator import CustomDoubleValidator

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