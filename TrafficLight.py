from enum import IntEnum
from Vehicle import Intention
from Lane import Direction


# enum in this class should be defined in order
class TrafficLightState(IntEnum):
    LR = 0
    SR = 1
    RS = 2
    RL = 3

class FourStatesTrafficLight(object):
    def __init__(self, ID: str, state=TrafficLightState.LR, lengthLR=3, lengthSR=3, lengthRS=3, lengthRL=3):
        self.ID : str = ID
        self.State : TrafficLightState = state
        self.AllowedIntention = {
            TrafficLightState.LR: [Intention.LEFT],
            TrafficLightState.SR: [Intention.STRAIGHT, Intention.RIGHT],
            TrafficLightState.RS: [Intention.STRAIGHT, Intention.RIGHT],
            TrafficLightState.RL: [Intention.LEFT],
        }
        # TODO: change init state according to input
        self.AllowedDirection = {Direction.N: True,
                                 Direction.E: False,
                                 Direction.S: True,
                                 Direction.W: False}
        self.StateLength = {
            TrafficLightState.LR: lengthLR,
            TrafficLightState.SR: lengthSR,
            TrafficLightState.RS: lengthRS,
            TrafficLightState.RL: lengthRL,
        }
        self.nextStateGlobalT = {
            TrafficLightState.LR: 0,
            TrafficLightState.SR: 0,
            TrafficLightState.RS: 0,
            TrafficLightState.RL: 0
        }

    def queryNextState(self):
        return  (self.State + 1) % len(TrafficLightState)

    def queryPrevState(self):
        return (self.State - 1) % len(TrafficLightState)

    def setNextState(self):
        elapsedT = self.StateLength[self.State]
        self.State = self.queryNextState()
        for k, v in self.AllowedDirection.items():
            self.AllowedDirection[k] = not v
        for k, v in self.nextStateGlobalT.items():
            self.nextStateGlobalT[k] += elapsedT