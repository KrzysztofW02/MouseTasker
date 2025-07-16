from actions.mouse_action import MouseAction
import time

class MouseWait(MouseAction):
    """Pause execution for a specified duration.

    Attributes:
        time (float): Duration in seconds to wait.
    """

    def __init__(self, time: float) -> None:
        self.time = time

    def __str__(self) -> str:
        return f"Wait: ({self.time}s)"

    def execute(self) -> None:
        """Sleep for the specified duration using time.sleep."""
        time.sleep(self.time)