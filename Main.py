
from Vehicle import Intention as intention, BasicVehicle
from Lane import Direction
from Intersection import FourWayIntersection
from Event import *


MAX_T = 100

def main():

    # initialize an intersection
    intersection1 = FourWayIntersection('1')
    intersection2 = FourWayIntersection('2')
    intersection1.connectIntersection(intersection2, Direction.N)
    vid = 0


    for T in range(1,10,1):
        intersection1.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.LEFT), Direction.S)
        vid += 1
        intersection1.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.STRAIGHT), Direction.S)
        vid += 1
    for T in range(10,20,1):
        intersection2.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.STRAIGHT), Direction.N)
        vid += 1
        intersection2.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.STRAIGHT), Direction.N)
        vid += 1

    intersection1.startTrafficLight(0)
    intersection2.startTrafficLight(0)

    while not Q.empty():
        event = Q.get()

        if event.T >= MAX_T:
            return

        event.execute()

if __name__ == "__main__":
    main()