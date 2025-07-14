from actions.mouse_action import MouseAction
import pyautogui

class MouseMoveClick(MouseAction):
    """Move the mouse to the given (x, y) coordinates over a specified duration, then click.

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
        return f"MoveClick: ({self.x}, {self.y}, {self.time}s)"

    def execute(self) -> None:
        """Perform the move and click using pyautogui."""
        pyautogui.moveTo(self.x, self.y, self.time)
        pyautogui.click()
