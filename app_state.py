from enum import Enum

class RightCard(Enum):
    IDLE = 'idle'
    LOADING = 'loading'
    READY = 'ready'

class CardManager:
    def __init__(self, on_update):
        self.state = RightCard.IDLE
        self._callback = on_update

    def transition_to(self, new_state: RightCard):
        if self.state != new_state:
            self.state = new_state
            self._callback()

