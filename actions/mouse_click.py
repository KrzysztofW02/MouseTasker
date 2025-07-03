from actions.mouse_action import MouseAction
import pyautogui

class MouseClick(MouseAction): 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): 
        return f"Click: {self.x}, {self.y}"

    def execute(self):
        pyautogui.click(self.x, self.y)