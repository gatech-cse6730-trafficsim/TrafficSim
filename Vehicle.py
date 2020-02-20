from enum import IntEnum


class Intention(IntEnum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class BasicVehicle(object):
    def __init__(self, ID, intention=Intention.STRAIGHT):
        self.ID : str = ID
        self.intention : Intention = intention
        self.follower : BasicVehicle = None
