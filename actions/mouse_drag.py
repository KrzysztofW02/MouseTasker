from actions.mouse_action import MouseAction
import pyautogui

class MouseDrag(MouseAction):
    """Drag the mouse cursor to the given (x, y) coordinates over a specified duration.

    Attributes:
        x (int): Target x-coordinate.
        y (int): Target y-coordinate.
        duration (float): Time in seconds over which the drag occurs.
    """

    def __init__(self, x: int, y: int, duration: float) -> None:
        self.x = x
        self.y = y
        self.duration = duration

    def __str__(self) -> str:
        return f"MouseDrag: {self.x}, {self.y}, {self.duration}s"
    
    def execute(self) -> None:
        """Perform the drag using pyautogui.dragTo."""
        pyautogui.dragTo(self.x, self.y, self.duration, button='left')
