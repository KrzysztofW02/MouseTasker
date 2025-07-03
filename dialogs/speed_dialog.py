from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

class SpeedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Speed Multiplier")

        self.speed_options = ["x2", "x3", "x4", "x5", "x10"]
        self.selected_speed = None

        layout = QVBoxLayout(self)

        for speed_option in self.speed_options:
            button = QPushButton(speed_option, self)
            button.clicked.connect(lambda checked, opt=speed_option: self.select_speed(opt))
            layout.addWidget(button)

        custom_speed_layout = QHBoxLayout()
        self.custom_speed_input = QLineEdit(self)
        self.custom_speed_input.setPlaceholderText("x?")
        custom_speed_button = QPushButton("Set Custom Speed", self)
        custom_speed_button.clicked.connect(self.set_custom_speed)

        custom_speed_layout.addWidget(self.custom_speed_input)
        custom_speed_layout.addWidget(custom_speed_button)
        layout.addLayout(custom_speed_layout)
        self.custom_speed_input.returnPressed.connect(self.set_custom_speed)

    def select_speed(self, speed_option):
        self.selected_speed = float(speed_option[1:])  
        self.accept()

    def set_custom_speed(self):
        try:
            custom_speed = float(self.custom_speed_input.text())
            if custom_speed <= 0:
                raise ValueError("Multiplier must be greater than 0.")
            self.selected_speed = custom_speed
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", f"Please enter a valid positive number.\n\nError: {e}")