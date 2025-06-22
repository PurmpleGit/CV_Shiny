
from enum import Enum
from serial import Serial
import time

class Button(bytes, Enum):
    A = bytes('A', 'utf-8')
    B = bytes('B', 'utf-8')
    SELECT = bytes('X', 'utf-8')

    LEFT = bytes('L', 'utf-8')
    RIGHT = bytes('R', 'utf-8')
    UP = bytes('U', 'utf-8')
    DOWN = bytes('D', 'utf-8')

class State(bytes, Enum):
    PRESSED = bytes('+', 'utf-8')
    RELEASED = bytes('-', 'utf-8')

class Controller():
    serial_port:Serial = Serial('COM7', 19200, timeout=2, write_timeout=2) 

    def press(self, button:Button, delay:int = 0.1):
        self.serial_port.write(State.PRESSED.value)
        self.serial_port.write(button.value)
        self.serial_port.flush()
        time.sleep(delay)
        self.serial_port.write(State.RELEASED.value)
        self.serial_port.write(button.value)
        self.serial_port.flush()
    
    def hold(self, button:Button):
        self.serial_port.write(State.PRESSED.value)
        self.serial_port.write(button.value)
        self.serial_port.flush()
    
    def release(self, button:Button):
        self.serial_port.write(State.RELEASED.value)
        self.serial_port.write(button.value)
        self.serial_port.flush()

    def print(self):
        #time.sleep(0.01)
        if(self.serial_port):
            print(f'Controller Debug: {self.serial_port.read_all()}')