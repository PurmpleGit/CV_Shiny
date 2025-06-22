import executors.executor
from executors.controller import Button
import time

class SpamExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                self.keyDown(Button.B)
                time.sleep(0.050)
                self.keyUp(Button.B)
                time.sleep(0.050)
            else:
                return
    
            