from Lane import BasicLane, UnlimitedLane, Direction
from TrafficLight import FourStatesTrafficLight
from Event import *

class FourWayIntersection(object):

    def __init__(self, ID : str):
        self.ID : str = ID
        self.convergenceLanes = dict()
        self.divergenceLanes = dict()
        self.light : FourStatesTrafficLight = FourStatesTrafficLight(self.ID)

        # Initialize the intersection to have 8 lanes, 4 incoming and 4 outgoing lanes
        for direction in Direction:
            self.convergenceLanes[direction] = BasicLane(None, self, direction)
            self.divergenceLanes[direction] = UnlimitedLane(self, None, direction)

    def getLaneStats(self):
        return {i:v for i, v in enumerate(self.lanes)}

    def enterIntersectionFromDirection(self, T, V, direction : Direction):
            Q.put(EnterLane(T, V, self, self.convergenceLanes[direction]))

    def startTrafficLight(self, T):
        Q.put(LightChange(T, self.light))

    def connectIntersection(self, C2: Intersection, direction : Direction):
        oppositeDirection = Direction((direction + 2) % len(Direction))

        C2.convergenceLanes[direction] = BasicLane(self, C2, direction)
        self.divergenceLanes[direction] = C2.convergenceLanes[direction]
        self.divergenceLanes[direction].updateID()

        self.convergenceLanes[oppositeDirection] = BasicLane(C2, self, oppositeDirection)
        C2.divergenceLanes[oppositeDirection] = self.convergenceLanes[oppositeDirection]
        self.convergenceLanes[oppositeDirection].updateID()