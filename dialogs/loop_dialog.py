from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

class LoopDialog(QDialog):
    """Dialog for specifying how many times to repeat an action.

    Attributes:
        loop_count (int): Number of loops entered by the user (set on accept).
    """

    def __init__(self, parent=None) -> None:
        """Initialize the loop-count dialog with OK/Cancel buttons."""
        super().__init__(parent)
        self.setWindowTitle("Run in Loop")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Enter number of loops:"))

        self.input_field = QLineEdit(self)
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

        # Initialize as zero will be set to a positive integer on accept
        self.loop_count = 0

    def accept(self) -> None:
        """Validate input as a positive integer and close dialog."""
        try:
            value = int(self.input_field.text())
            if value <= 0:
                raise ValueError
            self.loop_count = value
            super().accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a positive integer.")