

# TrafficSim
Python app for Simulating Lane-based Traffic Data at a four-way crossing

## Running

To generate an input data, run poisson.py (Python poisson.py)
To simulate the traffic, run main.py (Python main.py)
Note that the parameters in main.py should be changed if the input file name changes.

## Output

Sample console output:  
  
1575.1000:::Car vehicle_0_sidel_22_1552.3 retry 1 time passing intersection 1 from lane 0N1, Light is SR, Intention is STRAIGHT  
1575.1000:::Car vehicle_0_sidel_22_1552.3 Immediate Exited  
1575.1000:::Car vehicle_0_sidel_22_1552.3 Left the Intersection 1 from Lane 0N1, Light is SR, Intention is STRAIGHT    
vehicle_0_sidel_22_1552.3 Should Exit from 1N_, Exited from = 1N_  
vehicle_1_sidel_15_1574.9  
1575.4393:::Car vehicle_1_sidel_15_1574.9 Arrived the Intersection 1 from lane _E1, Light is SR, Intention is RIGHT  
1575.4393:::Car vehicle_1_sidel_15_1574.9 will wait at crossing 1 until 1580.100000  
1578.0000:::Light 0 Changed from SR to RS  
1578.7408:::Car vehicle_1_main_49_1578.7 Entered Intersection 1 from Lane _S1, nV = 1  
vehicle_1_main_49_1578.7  
1579.2408:::Car vehicle_1_main_49_1578.7 Arrived the Intersection 1 from lane _S1, Light is SR, Intention is RIGHT  

File Output:

Check output.csv for the details. The csv file contains four columns:  
`` Sequence Number, Vehicle Enter Time , Vehicle Exit Time, Vehicle ID,  Delta Time``
### Advanced Usage

To create your own intersections, use the three APIs below.
```python
def enterIntersectionFromDirection(self, T, V, direction : Direction): 

def connectIntersection(self, C2: Intersection, direction : Direction):

def startTrafficLight(self, T):
```
See below for a code snippet that creates three intersections, and connected them horizontally. (0-1-2)

```python
numIntersection = 2
intersections = [FourWayIntersection(str(i)) for i in range(numIntersection)]
intersections[0].connectIntersection(intersections[1], Direction.E)
intersections[1].connectIntersection(intersections[2], Direction.E)
```