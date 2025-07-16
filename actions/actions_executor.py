from PyQt5.QtCore import QThread, pyqtSignal

class ActionExecutor(QThread):
    """Thread-based executor for running a list of actions with optional looping and stop control.

    Attributes:
        update_action_index (pyqtSignal): Emitted with the index of the currently executing action.
        action_completed (pyqtSignal): Emitted when all actions have finished executing or were stopped.
        actions (list): List of actions to be executed.
        start_index (int): Index offset added to each emitted index.
        running (bool): Execution state flag to control stopping the thread.
        loop_count (int): Number of times to repeat the action sequence.
    """

    update_action_index = pyqtSignal(int)
    action_completed = pyqtSignal()

    def __init__(self, actions, start_index=0, loop_count=1):
        """Initialize executor with actions, optional start index, and loop count."""
        super().__init__()
        self.actions = actions
        self.start_index = start_index
        self.running = True
        self.loop_count = loop_count

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
                action.execute()
                current_action_index += 1
        self.action_completed.emit()

    def stop_execution(self):
        """Stop execution by setting the running flag to False."""
        self.running = False
