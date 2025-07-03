from actions.mouse_action import MouseAction
import pyautogui

class MouseMove(MouseAction):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def __str__(self): 
        return f"Move: {self.x}, {self.y}, {self.time}s"

    def execute(self):
        pyautogui.moveTo(self.x, self.y, self.time)