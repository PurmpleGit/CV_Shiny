from executors.controller import Controller, Button
from executors.control_thread import ControlThread
class Executor():
    enabled:bool = False
    controller:Controller = Controller()
    control_thread:ControlThread = ControlThread()
    
    def enable(self) -> None:
        if not self.enabled:
            self.enabled = True
            self.control_thread.push(self.run)
    
    def disable(self) -> None:
        if self.enabled:
            self.enabled = False

    def run(self):
        raise NotImplementedError('Executor does not have an action overridden')
    
    def press(self, button:Button):
        if(self.enabled):
            self.controller.press(button)
            self.controller.print()
            
    def keyDown(self, button:Button):
        if(self.enabled):
            self.controller.hold(button)
            self.controller.print()
            
    def keyUp(self, button:Button):
        self.controller.release(button)
        if(self.enabled):
            self.controller.print()
