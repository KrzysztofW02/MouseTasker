from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class ShortcutsDialog(QDialog):
    """Dialog to display keyboard shortcuts in a grid layout."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        layout = QGridLayout(self)
        layout.setColumnStretch(0, 1)  
        layout.setColumnStretch(1, 1)  
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(8)

        header_action = QLabel("Action")
        header_action.setAlignment(Qt.AlignLeft)
        header_key = QLabel("Shortcut")
        header_key.setAlignment(Qt.AlignLeft)
        header_action.setStyleSheet("font-weight: bold;")
        header_key.setStyleSheet("font-weight: bold;")
        layout.addWidget(header_action, 0, 0)
        layout.addWidget(header_key,  0, 1)

        shortcuts = [
            ("Run / Stop", "F1"),
            ("Run in Loop / Stop", "F2"),
            ("Check Coordinates", "F3"),
            ("Advanced Options", "F4"),
            ("Show Shortcuts", "F5"),
            ("Start Recording", "F10"),
            ("Copy", "Ctrl+C"),
            ("Undo", "Ctrl+Z"),
            ("Save", "Ctrl+S"),
            ("Paste", "Ctrl+V"),
            ("Load", "Ctrl+L"),
            ("Delete", "Delete"),
        ]

        for row, (action, key) in enumerate(shortcuts, start=1):
            lbl_action = QLabel(action)
            lbl_key = QLabel(key)
            lbl_action.setAlignment(Qt.AlignLeft)
            lbl_key.setAlignment(Qt.AlignLeft)
            layout.addWidget(lbl_action, row, 0)
            layout.addWidget(lbl_key,    row, 1)

        btn = QPushButton("OK", self)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, len(shortcuts) + 1, 0, 1, 2)

        self.setLayout(layout)