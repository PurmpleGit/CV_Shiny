import executors.executor
from executors.controller import Button
import time

class ThrowExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                self.keyDown(Button.A)
                time.sleep(0.050)
                self.keyUp(Button.A)
                time.sleep(0.050)
            else:
                return
    
            