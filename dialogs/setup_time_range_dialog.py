from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from dialogs.custom_double_validator import CustomDoubleValidator

class SetupTimeRangeDialog(QDialog):
    """Dialog for setting a random time range adjustment for wait actions.

    The provided float value will be randomly added or subtracted from
    each 'wait' action time to introduce timing variability.

    Attributes:
        result (tuple[float]): A one-element tuple containing the range value as a float.
    """
    def __init__(self, parent=None):
        """Initialize the dialog for random wait time adjustment."""
        super().__init__(parent)
        self.setWindowTitle("Setup Time Range")
        self.layout = QVBoxLayout()
        
        self.time_input = QLineEdit(self)
        
        double_validator = CustomDoubleValidator()
        # Input for the randomness range (will be added/subtracted from original time)
        self.time_input.setValidator(double_validator)
        
        self.layout.addWidget(QLabel("Range:"))
        self.layout.addWidget(self.time_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.setLayout(self.layout)
        self.result = None
    
    def accept(self):
        """Validate input and set the result as a tuple containing one float."""
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