from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator

class ClickDialog(QDialog):
    """Dialog for entering X and Y coordinates for a click action.

    Attributes:
        x_input (QLineEdit): Input field for the X-coordinate.
        y_input (QLineEdit): Input field for the Y-coordinate.
        result (Optional[Tuple[int, int]]): Tuple of (x, y) after acceptance, or None.
    """
    def __init__(self, parent=None, x=None, y=None) -> None:
        """Initialize the dialog, pre-filling coordinates if provided."""
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
        """Validate inputs and set result before closing."""
        if not self.x_input.text() or not self.y_input.text():
            QMessageBox.warning(self, "Warning", "All fields must be filled out.")
            return
        self.result = (int(self.x_input.text()), int(self.y_input.text()))
        super().accept()