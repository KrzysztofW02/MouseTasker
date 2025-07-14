from actions.mouse_action import MouseAction
import pyautogui

class MouseMove(MouseAction):
    """Move the mouse cursor to the specified screen coordinates over a duration.

    Attributes:
        x (int): Target x-coordinate.
        y (int): Target y-coordinate.
        duration (float): Time in seconds over which the move occurs.
    """

    def __init__(self, x: int, y: int, time: float) -> None:
        self.x = x
        self.y = y
        self.time = time

    def __str__(self) -> str:
        return f"Move: ({self.x}, {self.y}, {self.time}s)"

    def execute(self) -> None:
        """Perform the mouse move using pyautogui."""
        pyautogui.moveTo(self.x, self.y, self.time)