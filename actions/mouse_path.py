from actions.mouse_action import MouseAction
import time
from pynput.mouse import Controller

class MousePath(MouseAction):
    """Record and replay a sequence of mouse movements with timing.

    Attributes:
        points (list[tuple[int, int, float]]): 
            List of (x, y, time_delta) tuples representing movement steps.
    """

    def __init__(self) -> None:
        """Initialize an empty path."""
        self.points: list[tuple[int, int, float]] = []

    def add_point(self, x: int, y: int, time_delta: float) -> None:
        """Append a new point with its time delta."""
        self.points.append((x, y, time_delta))

    def __str__(self) -> str:
        """Return a summary of the recorded path."""
        return f"Path with {len(self.points)} points"

    def execute(self) -> None:
        """Replay the recorded path using pynput."""
        mouse = Controller()
        for x, y, time_delta in self.points:
            mouse.position = (x, y)
            time.sleep(time_delta)
