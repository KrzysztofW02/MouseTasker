from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from dialogs.custom_double_validator import CustomDoubleValidator

class SetupMoveClickTimeRangeDialog(QDialog):
    """Dialog for setting a time range (min/max) for randomizing delay in move or move-click actions.

    Attributes:
        result (tuple[float, float]): A tuple containing (min_time, max_time)
    """

    def __init__(self, parent=None) -> None:
        """Initialize the dialog with input fields for minimum and maximum time range."""
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

    def accept(self) -> None:
        """Validate inputs and set result as a tuple of floats (min_time, max_time)."""
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