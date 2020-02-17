from enum import IntEnum


class Intention(IntEnum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class BasicVehicle(object):
    def __init__(self, ID, intention=Intention.STRAIGHT):
        self.ID = ID
        self.intention = intention
        self.follower = None
