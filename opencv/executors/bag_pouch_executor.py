import executors.executor
from executors.controller import Button
import time

class BagPouchExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                time.sleep(0.5)
                self.press(Button.LEFT)
            else:
                return
    
            