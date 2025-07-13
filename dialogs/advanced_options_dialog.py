from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton

class AdvancedOptionsDialog(QDialog):
    """Dialog presenting advanced/randomization options and offsets.

    Attributes:
        main_application (Optional[MainApplication]):
            Reference to the main application used to open setup dialogs.
    """
    def __init__(self, parent=None, main_application=None) -> None:
        """Initialize the dialog with buttons for each advanced option."""
        super().__init__(parent)
        self.main_application = main_application
        self.setWindowTitle("Advanced Options")
        layout = QVBoxLayout()

        self.random_time_in_moves_movesclicks_button = QPushButton("Randomize Move/MoveClick Times")
        self.random_time_in_moves_movesclicks_button.clicked.connect(self.random_time_in_moves_movesclicks)
        layout.addWidget(self.random_time_in_moves_movesclicks_button)

        self.random_coord_in_moves_moveclicks_button = QPushButton("Randomize Move/MoveClick Coordinates")
        self.random_coord_in_moves_moveclicks_button.clicked.connect(self.random_coord_in_moves_moveclicks)
        layout.addWidget(self.random_coord_in_moves_moveclicks_button)

        self.random_coord_in_clicks_button = QPushButton("Randomize Click Coordinates")
        self.random_coord_in_clicks_button.clicked.connect(self.random_coord_in_clicks)
        layout.addWidget(self.random_coord_in_clicks_button)

        self.random_time_in_wait_button = QPushButton("Randomize Wait Times")
        self.random_time_in_wait_button.clicked.connect(self.random_time_in_wait)
        layout.addWidget(self.random_time_in_wait_button)

        self.random_coord_in_moves_moveclicks_button2 = QPushButton("Offset Move/MoveClick Coordinates")
        self.random_coord_in_moves_moveclicks_button2.clicked.connect(self.change_coord_in_moves_moveclicks)
        layout.addWidget(self.random_coord_in_moves_moveclicks_button2)

        self.random_time_in_moves_moveclicks_button2 = QPushButton("Offset Move/MoveClick Times")
        self.random_time_in_moves_moveclicks_button2.clicked.connect(self.change_time_in_moves_movesclicks)
        layout.addWidget(self.random_time_in_moves_moveclicks_button2)

        self.random_time_in_wait_button2 = QPushButton("Offset Wait Times")
        self.random_time_in_wait_button2.clicked.connect(self.change_random_time_in_wait)
        layout.addWidget(self.random_time_in_wait_button2)

        self.random_coord_in_clicks2 = QPushButton("Offset Click Coordinates")
        self.random_coord_in_clicks2.clicked.connect(self.change_coord_in_clicks)
        layout.addWidget(self.random_coord_in_clicks2)

        self.speed_button = QPushButton("Speed")
        self.speed_button.clicked.connect(self.open_speed_dialog)
        layout.addWidget(self.speed_button)


        self.setLayout(layout)

    def random_time_in_moves_movesclicks(self):
        if self.main_application:
            self.main_application.open_setup_move_time_dialog()

    def random_coord_in_moves_moveclicks(self):
        if self.main_application:
            self.main_application.open_setup_move_coord_dialog()

    def random_coord_in_clicks(self):
        if self.main_application:
            self.main_application.open_setup_click_coord_dialog()

    def random_time_in_wait(self):
        if self.main_application:
            self.main_application.open_setup_wait_range_dialog()

    def change_coord_in_moves_moveclicks(self):
        if self.main_application:
            self.main_application.open_setup_coord_range_dialog()
    
    def change_time_in_moves_movesclicks(self):
        if self.main_application:
            self.main_application.open_setup_moveclick_time_range_dialog()

    def change_random_time_in_wait(self):
        if self.main_application:
            self.main_application.open_setup_time_range_dialog()

    def change_coord_in_clicks(self):
        if self.main_application:
            self.main_application.open_setup_click_coord_range_dialog()

    def open_speed_dialog(self):
        if self.main_application:
            self.main_application.open_setup_speed_dialog()