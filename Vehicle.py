from enum import IntEnum
from typing import List

class Intention(IntEnum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class BasicVehicle(object):
    def __init__(self, ID, intention=[Intention.STRAIGHT]):
        self.ID : str = ID
        self.intention : List[Intention] = intention
        self.follower : BasicVehicle = None
        self.exitLaneID : str = ''
        self.correctExit : bool = False
        self.exited: bool = False

