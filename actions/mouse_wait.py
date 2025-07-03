from actions.mouse_action import MouseAction
import time

class MouseWait(MouseAction): 
    def __init__(self, time):
        self.time = time

    def __str__(self): 
        return f"Wait: {self.time}s"

    def execute(self):
        time.sleep(self.time)