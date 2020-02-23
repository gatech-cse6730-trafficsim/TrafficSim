
from Vehicle import Intention as intention, BasicVehicle
from Lane import Direction, AllLanes
from Intersection import FourWayIntersection
from Event import *
import numpy as np
import csv
import json

MAX_T = 15000


def main():

    allV = []

    mInt = {
        'L': Intention.LEFT,
        'R': Intention.RIGHT,
        'S': Intention.STRAIGHT
    }
    mArrive = {
        'N': Direction.N,
        'S': Direction.S,
        'E': Direction.E,
        'W': Direction.W
    }
    mLeave = {
        'N': Direction.S,
        'S': Direction.N,
        'E': Direction.W,
        'W': Direction.E
    }
    # initialize an intersection
    numIntersection = 2
    numVehicles = 0
    intersections = [FourWayIntersection(str(i)) for i in range(numIntersection)]
    # Make intersection 2 north of intersection 1
    intersections[0].connectIntersection(intersections[1], Direction.S)
    vid = 0
    with open('trafficflow.json', 'r') as f:
        z = json.load(f)

        for k,v in z.items():
            vid = k
            direction_in = v["arrive"][-1]
            direction_out = v["leave"][-1]
            iid_in = int(v["arrive"][0])
            iid_out = v["leave"][0]
            intent = [mInt[d] for d in v["direction"]][::-1] # reverse to make pop more efficient
            T = v["time"]
            vehicle = BasicVehicle(vid, intent)
            vehicle.exitLaneID = iid_out+direction_out+'_'
            intersections[iid_in].enterIntersectionFromDirection(T, vehicle, mArrive[direction_in])
            numVehicles+=1
            allV.append(vehicle)

    #for intersection in intersections:
    intersections[0].startTrafficLight(0)
    intersections[1].startTrafficLight(2)

    while not Q.empty():
        event = Q.get()

        if event.T >= MAX_T:
            break

        event.execute()

    print("Exit Lanes Correct = %d, Exited = %d,  Total = %d" % (sum([v.correctExit for v in allV]),sum([v.exited for v in allV]), numVehicles))

    with open('history.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(RECORD)

if __name__ == "__main__":
    main()