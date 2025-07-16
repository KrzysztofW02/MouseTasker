from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from dialogs.custom_double_validator import CustomDoubleValidator

class WaitDialog(QDialog):
    """Dialog for specifying a wait time in seconds.

    Attributes:
        time_input (QLineEdit): Input field for the wait time.
        result (float): Parsed time value entered by the user.
    """

    def __init__(self, parent=None, time=None) -> None:
        """Initialize the wait time dialog and set up input field."""
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

    def accept(self) -> None:
        """Validate the input and store the result as a float."""
        if not self.time_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        self.result = float(self.time_input.text())
        super().accept()