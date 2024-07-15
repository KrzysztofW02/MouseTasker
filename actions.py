import pyautogui
import time

class MouseAction:
    def execute(self):
        pass

class MouseMove(MouseAction):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def __str__(self): 
        return f"Move: {self.x}, {self.y}, {self.time}s"

    def execute(self):
        pyautogui.moveTo(self.x, self.y, self.time)

class MouseClick(MouseAction): 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): 
        return f"Click: {self.x}, {self.y}"

    def execute(self):
        pyautogui.click(self.x, self.y)

class Wait(MouseAction): 
    def __init__(self, time):
        self.time = time

    def __str__(self): 
        return f"Wait: {self.time}s"

    def execute(self):
        time.sleep(self.time)

class MouseMoveClick(MouseAction):
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def __str__(self):
       return f"MoveClick: {self.x}, {self.y}, {self.time}s"

    def execute(self):
        pyautogui.moveTo(self.x, self.y, self.time)
        pyautogui.click()

class MouseDrag(MouseAction):
    #pyautogui.dragTo(300, 400, 2, button='left')  # drag mouse to X of 300, Y of 400 over 2 seconds while holding down left mouse button
    def __init__(self, x, y, time):
        self.x = x 
        self.y = y
        self.time = time

    def __str__(self):
        return f"MouseDrag: {self.x}, {self.y}, {self.time}s"
    
    def execute(self):
        pyautogui.dragTo(self.x, self.y, self.time, button='left')