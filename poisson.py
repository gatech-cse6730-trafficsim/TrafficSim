# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:22:34 2020

@author: yuyue
"""

import numpy as np
import json

class trafficflow():
    def __init__(self, num_intersection=2, num_time=3, traffic_flow=[[1000,3000,200],[1,300,200]], \
                 side_road = True, bidir = True, rand = 'exp', side_ratio = 0.3, name=''):
        self.intersections = num_intersection
        self.time = num_time
        self.traffic_flow = traffic_flow # number of vehicles per hour
        self.side_road = side_road
        self.bidir = bidir
        self.rand = rand
        self.turning_ratio = {'L': 0.1, 'R': 0.3, 'S': 0.6}
        self.cars = {}
        self.side_ratio = side_ratio
        self.name = name
    
    def generate_arrive_time(self, param, rand = 'exp', time = 0):
        interval = 1/(param/3600) #param: density (vehicle/s)
        if rand == 'exp':
            arrive_time = np.cumsum(np.random.exponential(interval, size=10000))
            arrive_time = arrive_time[arrive_time<3600]
        elif rand == 'uniform': #uniform distribution
            arrive_time = np.sort(np.random.uniform(0, 3600, int(param)))
        else: # uniform time distribution
            arrive_time = np.linspace(1, 3600, int(param))
        return arrive_time + 3600*time
    
    def gen_traffic_flow_main(self, inter_idx, param= 200, t = 0):
        #idx = 0
        arrive_id = '%d_N'%(inter_idx) if inter_idx == 0 else '%d_S'%(self.intersections - 1)
        arrive_time = self.generate_arrive_time(param, rand = self.rand, time = t)
        for idx, time in enumerate(arrive_time):
            carid = 'vehicle_%d_main_%d_%.1f'%(inter_idx, idx, time)
            direction = []
            for i in range(self.intersections):
                if np.random.rand() < self.turning_ratio["L"]:
                    direction.append("L")
                    leave_id = '%d_W'%(i) if inter_idx == 0 else '%d_E'%(self.intersections - i - 1) 
                    break
                elif np.random.rand() > 1 - self.turning_ratio["R"]:
                    direction.append("R")
                    leave_id = '%d_E'%(i) if inter_idx == 0 else '%d_W'%(self.intersections - i - 1) 
                    break
                else:
                    direction.append("S")
                    leave_id = '%d_N'%(i) if inter_idx == 0 else '%d_S'%(self.intersections - i - 1) 
            self.cars[carid] = {"arrive": arrive_id, "leave": leave_id, "direction": direction, "time": time}
            
            
    def gen_traffic_flow_leftside(self, inter_idx, param=200, t = 0):
        arrive_id = '%d_E'%(inter_idx)
        arrive_time = self.generate_arrive_time(param, rand = self.rand, time = t)
        for idx, time in enumerate(arrive_time):
            carid = 'vehicle_%d_sidel_%d_%.1f'%(inter_idx, idx, time)
            direction = []
            if np.random.rand() < self.turning_ratio["L"]:
                direction = ['L'] + ['S'] * (self.intersections - inter_idx - 1)
                leave_id = '%d_N'%(self.intersections - 1) 
            elif np.random.rand() > 1 - self.turning_ratio["R"]:
                direction = ['R'] + ['S'] * inter_idx
                leave_id = '0_S'
            else:
                direction = ['S'] 
                leave_id = '%d_E'%(inter_idx)
            self.cars[carid] = {"arrive": arrive_id, "leave": leave_id, "direction": direction, "time": time}
    
    def gen_traffic_flow_rightside(self, inter_idx, param=200, t = 0):
        arrive_id = '%d_W'%(inter_idx)
        arrive_time = self.generate_arrive_time(param, rand = self.rand, time = t)
        for idx, time in enumerate(arrive_time):
            carid = 'vehicle_%d_sider_%d_%.1f'%(inter_idx, idx, time)
            direction = []
            if np.random.rand() < self.turning_ratio["L"]:
                direction = ['L'] + ['S'] * (inter_idx)
                leave_id = '0_S' 
            elif np.random.rand() > 1 - self.turning_ratio["R"]:
                direction = ['R'] + ['S'] * (self.intersections - inter_idx - 1)
                leave_id  = '%d_N'%(self.intersections - 1)
            else:
                direction = ['S']      
                leave_id = '%d_W'%(inter_idx)
            self.cars[carid] = {"arrive": arrive_id, "leave": leave_id, "direction": direction, "time": time}
    
    def main(self):
        for i in range(self.time):
            self.gen_traffic_flow_main(0, param = self.traffic_flow[0][i], t = i)
            if self.bidir:
                self.gen_traffic_flow_main(self.intersections - 1, param = self.traffic_flow[1][i], t =  i)
            if self.side_road:
                for j in range(self.intersections):
                    self.gen_traffic_flow_leftside(inter_idx = j, param = self.traffic_flow[0][i]*self.side_ratio, t= i)
                    if self.bidir:
                        self.gen_traffic_flow_rightside(inter_idx = j, param = self.traffic_flow[1][i]*self.side_ratio, t= i)

    def write(self):
        with open('trafficflow_%s.json'%(self.name), 'w') as f:
            f.write(json.dumps(self.cars))

if __name__ == '__main__':
    #main()
    x = trafficflow()
    x.main()
    s = x.cars
    x.write()
    side_ratio = 0.3
    data = {
                "peach": {"bidir": True, "time": 12, 
                          "N": [131,76,54,33,36, 100,214,359,482,410, 450,500], 
                          "S": [131,76,61,42,34, 87,254,416,494,464, 350,372],
                          "side": True}, 
                "10th":  {"bidir": True, "time": 24, 
                          "N": [132,81,66,69,63, 137,198,250,797,666, 404,439,469,435,411, 409,404,404,419,390, 366,340,238,187], 
                          "S": [132,81,66,34,63, 114,250,538,299,393, 405,505,522,476,434, 504,611,660,608,544, 367,349,283,206],
                          "side": True}, 
                "spring":{"bidir": False, "time": 24, 
                          "N": [122,84,60,60,49, 159,437,834,994,823, 688,715,830,915,1038, 1494,1992,2463,2147,1260, 606,440,297,218], 
                          "S": [], 
                          "side": False}, 
            }
    for d in data:
        flow_N = data[d]["N"]
        flow_S = data[d]["S"]
        side = data[d]["side"]
        bidir = data[d]["bidir"]
        name = d
        num_time = data[d]["time"]
        x= trafficflow(num_time = num_time, traffic_flow = [flow_N, flow_S], side_road = side, bidir = bidir, rand = 'exp', side_ratio = side_ratio, name = name)
        x.main()
        s = x.cars
        x.write()
        with open('trafficflow_%s.json'%(name), 'r') as f:
            z = json.load(f)
