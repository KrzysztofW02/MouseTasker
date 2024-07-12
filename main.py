import sys
from PyQt5.QtWidgets import QApplication
from MouseTasker import MainWindow
import qtvscodestyle as qtvsc

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
    
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
    
    app.setStyleSheet(stylesheet + custom_button_style)
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())