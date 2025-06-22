import transition
import conditions.condition
import executors.executor
import numpy.typing
import cv2

class State:
    name:str
    action: executors.executor.Executor
    transitions: list[transition.Transition]

    def __init__(self, action:executors.executor.Executor, name:str) -> None:
        self.action = action
        self.name = name
        self.transitions = []
    
    def add_transition(self, condition: conditions.condition.Condition, next_state: 'State') -> None:
        self.transitions.append(transition.Transition(condition, next_state))

    def process(self, raw_screenshot: numpy.typing.NDArray) -> 'State' :
        next_state = self
        self.action.enable()

        image_to_search = cv2.cvtColor(raw_screenshot, cv2.IMREAD_COLOR)
        display_screenshot = raw_screenshot.copy()

        for transition in self.transitions:
            if(transition.condition.isMet(image_to_search)):
                next_state = transition.next_state
            display_screenshot = transition.condition.draw(display_screenshot, transition.next_state.name)

        cv2.imshow('screen', display_screenshot)

        if(next_state is not self):
            self.action.disable()
        
        return next_state
