from actions.mouse_click import MouseClick
import time
from actions.mouse_path import MousePath
from pynput.mouse import Listener, Button

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