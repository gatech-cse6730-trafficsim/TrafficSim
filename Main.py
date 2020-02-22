
from Vehicle import Intention as intention, BasicVehicle
from Lane import Direction
from Intersection import FourWayIntersection
from Event import *
import numpy as np
import csv

MAX_T = 100

def main():

    # initialize an intersection
    intersection1 = FourWayIntersection('1')
    intersection2 = FourWayIntersection('2')
    # Make intersection 2 north of intersection 1
    intersection1.connectIntersection(intersection2, Direction.N)
    vid = 0


    for T in range(1,10,1):
        intersection1.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.LEFT), Direction.N)
        vid += 1
        intersection1.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.STRAIGHT), Direction.N)
        vid += 1
    for T in range(10,20,1):
        intersection1.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.STRAIGHT), Direction.N)
        vid += 1
        intersection1.enterIntersectionFromDirection(T, BasicVehicle(vid, intention.LEFT), Direction.N)
        vid += 1

    intersection1.startTrafficLight(0)
    intersection2.startTrafficLight(1)

    while not Q.empty():
        event = Q.get()

        if event.T >= MAX_T:
            break

        event.execute()

    with open('history.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(RECORD)

if __name__ == "__main__":
    main()