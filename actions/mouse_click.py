from actions.mouse_action import MouseAction
import pyautogui

class MouseClick(MouseAction):
    """Represents a single mouse click at given screen coordinates.

    Attributes:
        x (int): The x-coordinate where to click.
        y (int): The y-coordinate where to click.
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Click: ({self.x}, {self.y})"

    def execute(self) -> None:
        """Perform the click using pyautogui."""
        pyautogui.click(self.x, self.y)
