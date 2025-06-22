import executors.executor
from executors.controller import Button

class RunExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                self.press(Button.LEFT)
                self.press(Button.DOWN)
                self.press(Button.RIGHT)
                self.press(Button.A)
                self.press(Button.B)
                self.press(Button.B)
            else:
                return
    
            