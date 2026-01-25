from PyQt5.QtCore import QThread, pyqtSignal
from pynput.mouse import Controller
from actions.mouse_transition import MouseTransition, calculate_transition_needed, get_action_end_position


class ActionExecutor(QThread):
    """Thread-based executor for running a list of actions with optional looping and stop control.

    Attributes:
        update_action_index (pyqtSignal): Emitted with the index of the currently executing action.
        action_completed (pyqtSignal): Emitted when all actions have finished executing or were stopped.
        actions (list): List of actions to be executed.
        start_index (int): Index offset added to each emitted index.
        running (bool): Execution state flag to control stopping the thread.
        loop_count (int): Number of times to repeat the action sequence.
        auto_transition (bool): Whether to auto-insert smooth transitions between actions.
        transition_threshold (int): Min pixel distance to trigger auto-transition.
    """

    update_action_index = pyqtSignal(int)
    action_completed = pyqtSignal()

    def __init__(self, actions, start_index=0, loop_count=1, auto_transition=True, transition_threshold=1):
        """Initialize executor with actions, optional start index, and loop count."""
        super().__init__()
        self.actions = actions
        self.start_index = start_index
        self.running = True
        self.loop_count = loop_count
        self.auto_transition = auto_transition
        self.transition_threshold = transition_threshold

    def _get_current_cursor_position(self) -> tuple:
        """Get current mouse cursor position."""
        mouse = Controller()
        return mouse.position

    def _maybe_insert_transition(self, next_action) -> None:
        """Insert a smooth transition if cursor is far from next action's target."""
        if not self.auto_transition:
            return
        
        current_pos = self._get_current_cursor_position()
        transition = calculate_transition_needed(
            current_pos, 
            next_action, 
            self.transition_threshold
        )
        
        if transition:
            transition.execute()

    def run(self):
        """Start executing actions in a loop until finished or stopped."""
        for _ in range(self.loop_count):
            if not self.running:
                break
            current_action_index = 0
            while self.running and current_action_index < len(self.actions):
                adjusted_index = current_action_index + self.start_index
                self.update_action_index.emit(adjusted_index)
                action = self.actions[current_action_index]
                
                self._maybe_insert_transition(action)
                
                action.execute()
                current_action_index += 1
        self.action_completed.emit()

    def stop_execution(self):
        """Stop execution by setting the running flag to False."""
        self.running = False
