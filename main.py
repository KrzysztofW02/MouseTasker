"""
Entry point for the Mouse Tasker application.

Attributes:
    custom_button_style (str): CSS rules to style all QPushButton widgets.
"""
import sys
from PyQt5.QtWidgets import QApplication
from mouse_tasker import MainWindow
import qtvscodestyle as qtvsc

# Custom CSS for QPushButton styling
custom_button_style = """
QPushButton {
    background-color: #323232;
    color: #FFF;
    border: 1px solid #555;
    border-radius: 10px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #444;
    color: #FFF;
    border: 1px solid #666;
}
QPushButton:pressed {
    background-color: #555;
    color: #FFF;
    border: 1px solid #777;
}
"""

def main() -> None:
    """Initialize QApplication, apply styles, and launch the main window."""
    app = QApplication(sys.argv)
    base_stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
    app.setStyleSheet(base_stylesheet + custom_button_style)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
