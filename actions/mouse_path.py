from actions.mouse_action import MouseAction
import time

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