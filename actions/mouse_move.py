from actions.mouse_action import MouseAction
import pyautogui

class MouseMove(MouseAction):
    """Move the mouse cursor to the specified screen coordinates over a duration.

    Attributes:
        x (int): Target x-coordinate.
        y (int): Target y-coordinate.
        duration (float): Time in seconds over which the move occurs.
    """

    def __init__(self, x: int, y: int, duration: float) -> None:
        self.x = x
        self.y = y
        self.duration = duration

    def __str__(self) -> str:
        return f"Move: ({self.x}, {self.y}, {self.duration}s)"

    def execute(self) -> None:
        """Perform the mouse move using pyautogui."""
        pyautogui.moveTo(self.x, self.y, self.duration)