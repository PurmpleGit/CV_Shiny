import executors.executor
from executors.controller import Button
import time

class OpenBagExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                self.press(Button.B)
                self.press(Button.B)
                self.press(Button.UP)
                self.press(Button.RIGHT)
                self.press(Button.A)
                time.sleep(2)
            else:
                return
    
            