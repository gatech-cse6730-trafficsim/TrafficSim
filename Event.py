import Vehicle
import Lane
import TrafficLight
from TrafficLight import TrafficLightState
from Vehicle import Intention
from Lane import Direction
import Intersection
import queue

CORRECT_EXIT_LANE = 0

# Unit Delay. It takes one unit delay to move the car 1 unit ahead in the list
DELAY = 0.1

# initialize Event Queue
Q = queue.PriorityQueue(maxsize=0)

# output csv
RECORD = []

class Event(object):
    def __init__(self, T: float, vehicle, light, lane):
        self.T = 0  # Global Time
        self.V = None  # Vehicle ID

    def execute(self):
        pass

    def dispatch(self, event):
        # Put another event into the event queue
        Q.put(event)

    def chain(self, event):
        # This method is used to immediately invoke another event
        if self.T < event.T:
            print("Cannot Chain Future Event, Bug in design")
        else:
            event.execute()

    def __lt__(self, other):
        return self.T < other.T

    def __gt__(self, other):
        return self.T > other.T

    def __le__(self, other):
        return self.T <= other.T


class ArriveCrossing(Event):
    def __init__(self, T: float, V: Vehicle, C: Intersection, L: Lane, retry = 0):
        self.T = T
        self.V = V
        self.L = L
        self.C = C
        self.retry = retry

    def execute(self):
        light = self.C.light

        # Update the lane front pointer
        self.L.front = self.V
        intention = self.V.intention[-1]
        direction = self.L.direction

        if self.retry:
            print("%.4f:::Car %s retry %d time passing intersection %s from lane %s, Light is %s, Intention is %s" %
                  (self.T, self.V.ID, self.retry, self.C.ID, self.L.ID, TrafficLightState(light.State).name,
                   Intention(intention).name))
        else:
            print("%.4f:::Car %s Arrived the Intersection %s from lane %s, Light is %s, Intention is %s" %
                  (self.T, self.V.ID, self.C.ID, self.L.ID, TrafficLightState(light.State).name,
                   Intention(intention).name))

        # If the the lane the vehicle is travelling to is full, add this vehicle to waitlist of the target lane
        if self.L.getExitLane(intention).isFull():
            print("%.4f:::Car %s blocked" % (self.T, self.V.ID))
            self.L.getExitLane(intention).waitlist.put_nowait(self)

        # if the vehicle can immediately pass the crossing, send a exit event
        elif light.canPass(intention, direction):
            print("%.4f:::Car %s Immediate Exited" % (self.T, self.V.ID))
            self.chain(ExitCrossing(self.T, self.V, self.C, self.L))

        # Otherwise find out the exit time (waitTime, wT), at that time, retry ArriveCrossing
        else:
            wt = min([T for LS, T in light.nextStateGlobalT.items() if light.canPass(intention, direction, LS) and T >= self.T ]) - self.T
            print("%.4f:::Car %s will wait at crossing %s until %f" % (self.T, self.V.ID, self.C.ID, self.T+wt))
            self.dispatch(ArriveCrossing(self.T + wt, self.V, self.C, self.L, retry=self.retry+1))



class ExitCrossing(Event):
    def __init__(self,  T: float, V: Vehicle,  C: Intersection, L: Lane):
        self.T = T
        self.V = V
        self.C = C
        self.L = L

    def execute(self):

        light = self.C.light
        intention = self.V.intention[-1]

        # Set lane front pointer to Null and decrease the counter
        self.L.front = None
        self.L.nV -= 1

        if self.L.getExitLane(intention).isFull():
            print("!!!!!!! CHECK BUG !!!!!!!!")

        print("%.4f:::Car %s Left the Intersection %s from Lane %s, Light is %s, Intention is %s" %
              (self.T, self.V.ID, self.C.ID, self.L.ID, TrafficLightState(light.State).name, Intention(intention).name))

        # Add the vehicle to another lane
        self.chain(EnterLane(self.T, self.V, self.L.getExitLane(intention).sink, self.L.getExitLane(intention)))

        # if there is no more vehicle in this lane, update the tail pointer
        if self.L.isFull():
            self.L.tail = None

        # otherwise, make the follower arriving the crossing, after a small delay (Unit Delay)
        elif self.V.follower:
            self.dispatch(ArriveCrossing(self.T + DELAY, self.V.follower, self.C, self.L))

        self.V.follower = None
        self.V.intention.pop()

        # Also notify the waiting list
        if not self.L.waitlist.empty():
            self.chain(NotifyWaitlist(self.T, self.C, self.L))

        RECORD.append([self.T, self.V.ID, self.C.ID, Direction(self.L.direction).name, Intention(intention).name, TrafficLightState(light.State).name])


class EnterLane(Event):
    def __init__(self, T: float, V: Vehicle, C : Intersection, L: Lane):
        self.T = T
        self.V = V
        self.L = L
        self.C = C

    def execute(self):

        if isinstance(self.L, Lane.UnlimitedLane) and self.L.sink is None:
            print("%s Should Exit from %s, Exited from = %s" % (self.V.ID, self.V.exitLaneID, self.L.ID))
            self.V.exited = True
            if self.V.exitLaneID == self.L.ID:
                self.V.correctExit = True
            return

        # This should not happen after initialization
        if self.L.isFull():
            print("INIT PERIOD OKAY::::::::Car %s Waitlisted" % self.V.ID)
            self.L.waitlist.put_nowait(self)
            return


        # if the lane is empty, make it arrival at the crossing after a delay that equals (capacity - nV) * unit delay
        if self.L.isEmpty():
            self.dispatch(ArriveCrossing(self.T + DELAY * (self.L.capacity - self.L.nV), self.V, self.C, self.L))
        # otherwise update its tail
        else:
            self.L.tail.follower = self.V
        self.L.tail = self.V
        self.L.nV += 1
        print("%.4f:::Car %s Entered Intersection %s from Lane %s, nV = %d" % (self.T, self.V.ID, self.C.ID, self.L.ID, self.L.nV))


class LightChange(Event):

    def __init__(self, T: float, light: TrafficLight):
        self.Light = light
        self.T = T

    def execute(self):

        self.Light.setNextState()
        currentState = self.Light.State
        prevState = self.Light.queryPrevState()
        print("%.4f:::Light %s Changed from %s to %s" % (self.T, self.Light.ID,
                                                       TrafficLightState(prevState).name, TrafficLightState(currentState).name))

        nextState = self.Light.queryNextState()
        self.dispatch(LightChange(self.Light.nextStateGlobalT[nextState], self.Light))


class NotifyWaitlist(Event):
    def __init__(self, T: float, C : Intersection, L: Lane):
        self.T = T
        self.L = L
        self.C = C

    def execute(self):

        # Avoid This
        # for e in self.L.waitlist
        #   self.chain(e)
        # Cause deadloop
        print("%.4f:::Notify Waitlist %s" % (self.T, self.L.ID))
        buf = []
        while not self.L.waitlist.empty():
            buf.append(self.L.waitlist.get_nowait())
        for e in buf:
            # Update Timestamp
            e.T = self.T
            self.chain(e)