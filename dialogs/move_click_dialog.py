from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator
from dialogs.custom_double_validator import CustomDoubleValidator

class MoveClickDialog(QDialog):
    """Dialog for configuring MoveClick action parameters.

    Attributes:
        x_input (QLineEdit): Field for the target x-coordinate.
        y_input (QLineEdit): Field for the target y-coordinate.
        time_input (QLineEdit): Field for the move duration.
        result (tuple[int, int, float]): (x, y, time) set on accept.
    """

    def __init__(
        self,
        parent=None,
        x: int = None,
        y: int = None,
        time: float = None
    ) -> None:
        """Initialize the dialog, pre-filling fields if values are provided."""
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
        self.result: tuple[int, int, float] = (0, 0, 0.0)

    def accept(self) -> None:
        """Validate inputs and set result as (x, y, time), then close."""
        if (
            not self.x_input.text()
            or not self.y_input.text()
            or not self.time_input.text()
        ):
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return

        x_val = int(self.x_input.text())
        y_val = int(self.y_input.text())
        t_val = float(self.time_input.text())
        self.result = (x_val, y_val, t_val)
        super().accept()