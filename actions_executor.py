from PyQt5.QtCore import QThread, pyqtSignal

class ActionExecutor(QThread):
    update_action_index = pyqtSignal(int)
    action_completed = pyqtSignal()

    def __init__(self, actions, start_index=0, loop_count=1):
        super().__init__()
        self.actions = actions
        self.start_index = start_index
        self.running = True
        self.loop_count = loop_count

    def run(self):
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
        self.running = False