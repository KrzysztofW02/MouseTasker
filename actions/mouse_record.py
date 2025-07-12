from actions.mouse_click import MouseClick, MouseAction
import time
from actions.mouse_path import MousePath
from pynput.mouse import Listener, Button

class MouseRecord:
    """Capture mouse movements and clicks into a list of actions.

    Attributes:
        actions (list[MouseAction]): Recorded sequence of MousePath and MouseClick actions.
        listener (Listener | None): pynput listener for mouse events.
        start_time (float | None): Timestamp of the last recorded event.
        current_path (MousePath | None): Ongoing movement path before next click.
    """

    def __init__(self) -> None:
        """Initialize the recorder with no actions."""
        self.actions: list[MouseAction] = []
        self.listener: Listener | None = None
        self.start_time: float | None = None
        self.current_path: MousePath | None = None

    def start(self) -> None:
        """Begin recording mouse events."""
        self.actions = []
        self.start_time = time.time()
        self.current_path = MousePath()
        self.listener = Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()

    def stop(self) -> None:
        """Stop recording and flush any pending path."""
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.current_path and self.current_path.points:
            self.actions.append(self.current_path)

    def on_move(self, x: int, y: int) -> None:
        """Handle mouse move events, recording position and time delta."""
        current_time = time.time()
        elapsed = current_time - self.start_time  # type: ignore
        self.current_path.add_point(x, y, elapsed)  # type: ignore
        self.start_time = current_time

    def on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """Handle mouse click events, splitting paths and recording clicks."""
        if pressed and button == Button.left:
            if self.current_path and self.current_path.points:
                self.actions.append(self.current_path)
            self.actions.append(MouseClick(x, y))
            self.current_path = MousePath()

    def get_actions(self) -> list[MouseAction]:
        """Return the recorded sequence of actions."""
        return self.actions