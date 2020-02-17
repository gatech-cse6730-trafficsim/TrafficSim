import Vehicle
from Vehicle import Intention
from queue import Queue
from enum import IntEnum

AllLanes = dict()


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class BasicLane(object):
    def __init__(self, source, sink, direction: Direction):
        self.source = source
        self.sink = sink
        self.direction = direction
        self.ID = ''
        self.updateID()

        self.front: Vehicle = None
        self.tail: Vehicle = None
        self.capacity: int = 20  # initialize to 20 cars
        self.nV: int = 0  # initialize to zero

        # The incoming cars that were blocked due to limited capacity
        # TODO: This is FIFO, We need PriorityQueue
        self.waitList = Queue(3)

    def isFull(self):
        return self.nV == self.capacity

    def isEmpty(self):
        return self.nV == 0

    def updateID(self):
        if self.ID in AllLanes:
            del AllLanes[self.ID]
        sourceID = '0' if self.source is None else self.source.ID
        sinkID = '0' if self.sink is None else self.sink.ID
        self.ID = sourceID + self.direction.name + sinkID
        AllLanes[self.ID] = self

    def getExitLane(self, intention: Vehicle.Intention):
        exitDirection = (self.direction + intention) % len(Direction)
        return self.sink.divergenceLanes[exitDirection]


class UnlimitedLane(BasicLane):
    def __init__(self, source, sink, direction: str):
        self.source = source
        self.sink = sink
        self.direction = direction
        self.ID = ''
        self.updateID()
        self.front: Vehicle = None
        self.tail: Vehicle = None
        self.capacity: int = 2**31  # initialize to unlimited
        self.nV: int = 0  # initialize to zero

        # The incoming cars that were blocked due to limited capacity
        # TODO: This is FIFO, We need PriorityQueue
        self.waitList = Queue(3)