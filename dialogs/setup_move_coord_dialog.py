from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator

class SetupMoveCoordDialog(QDialog):
    """Dialog for setting a random range value for move and move-click coordinates.

    The given range will be randomly added or subtracted to X and Y coordinates of 
    move and move-click actions to simulate variability.

    Attributes:
        result (tuple[int]): A one-element tuple containing the range as an integer.
    """

    def __init__(self, parent=None) -> None:
        """Initialize the dialog for coordinate randomization range."""
        super().__init__(parent)
        self.setWindowTitle("Setup Move, MoveClicks Coordinates")
        self.layout = QVBoxLayout()

        self.x_input = QLineEdit(self)

        # Input for the randomness range (will be added/subtracted from original coords)
        int_validator = QIntValidator(self)
        self.x_input.setValidator(int_validator)

        self.layout.addWidget(QLabel("Range:"))
        self.layout.addWidget(self.x_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
        self.result = None

    def accept(self) -> None:
        """Validate input and set the result as a tuple containing one integer."""
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