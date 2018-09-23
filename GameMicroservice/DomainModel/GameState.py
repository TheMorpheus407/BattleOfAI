from enum import Enum


class GameState(Enum):
    WAITING = 0
    STARTED = 1
    ABORTED = 2
    FINISHED = 3