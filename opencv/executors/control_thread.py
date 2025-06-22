from queue import SimpleQueue
from threading import Thread

class ControlThread():
    execution_queue:SimpleQueue
    execution_thread:Thread

    def __init__(self) -> None:
        self.execution_queue = SimpleQueue()
        self.execution_thread = Thread(target = self.execute, daemon=True).start()
    
    def push(self, execution_thread:callable) -> None:
        self.execution_queue.put(execution_thread)

    def pop(self) -> callable:
        return self.execution_queue.get()

    def execute(self) -> None:
        while True:
            function_to_run = self.pop()
            function_to_run()