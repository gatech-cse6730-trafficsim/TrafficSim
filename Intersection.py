from Lane import BasicLane, UnlimitedLane, Direction
from TrafficLight import FourStatesTrafficLight
from Event import *

class FourWayIntersection(object):

    def __init__(self, ID : str, crossingT = 1):
        self.ID = ID
        self.convergenceLanes = dict()
        self.divergenceLanes = dict()
        self.light = FourStatesTrafficLight(self.ID)
        self.crossingT = crossingT

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
        oppositeDirection = (direction + 2) % len(Direction)

        self.divergenceLanes[direction] = C2.convergenceLanes[direction]
        self.divergenceLanes[direction].sink = C2
        self.divergenceLanes[direction].source = self
        self.divergenceLanes[direction].updateID()

        self.convergenceLanes[oppositeDirection] = C2.divergenceLanes[oppositeDirection]
        self.convergenceLanes[oppositeDirection].sink = self
        self.convergenceLanes[oppositeDirection].source = C2
        self.convergenceLanes[oppositeDirection].updateID()