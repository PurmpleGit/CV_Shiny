from conditions.condition import Condition

class Transition:
    condition: Condition

    def __init__(self, condition: Condition, next_state) -> None:
        self.condition = condition
        self.next_state = next_state