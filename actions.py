import pyautogui
import time
from pynput.mouse import Listener
from pynput.mouse import Button

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

class MousePath(MouseAction):
    def __init__(self):
        self.points = []  

    def add_point(self, x, y, time_delta):
        self.points.append((x, y, time_delta))

    def __str__(self):
        return f"Path with {len(self.points)} points"

    def execute(self):
        from pynput.mouse import Controller
        mouse = Controller()
        for x, y, time_delta in self.points:
            mouse.position = (x, y)
            time.sleep(time_delta)
class MouseRecord:
    def __init__(self):
        self.actions = []
        self.listener = None
        self.start_time = None
        self.current_path = None

    def start(self):
        self.actions = []
        self.start_time = time.time()
        self.current_path = MousePath()
        self.listener = Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.current_path and self.current_path.points:
            self.actions.append(self.current_path)

    def on_move(self, x, y):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        self.current_path.add_point(x, y, elapsed_time)
        self.start_time = current_time

    def on_click(self, x, y, button, pressed):
        if pressed and button == Button.left:
            if self.current_path and self.current_path.points:
                self.actions.append(self.current_path)
            self.actions.append(MouseClick(x, y))
            self.current_path = MousePath()

    def get_actions(self):
        return self.actions

