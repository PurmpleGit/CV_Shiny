import executors.executor
from executors.controller import Button
import time

class BallExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                self.press(Button.UP)
                time.sleep(0.05)
            else:
                return
    
            