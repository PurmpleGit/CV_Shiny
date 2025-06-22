import executors.executor
from executors.controller import Button

class SearchExecutor(executors.executor.Executor):
    def run(self):
        while True:
            if self.enabled:
                self.press(Button.RIGHT)
                self.press(Button.RIGHT)
                self.press(Button.RIGHT)
                self.press(Button.RIGHT)
                self.press(Button.LEFT)
                self.press(Button.LEFT)
                self.press(Button.LEFT)
            else:
                return
    
            