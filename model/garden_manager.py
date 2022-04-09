import pandas as pd
from copy import deepcopy

class Plant(object):
    def __init__(
        self,
        name: str,
        depth_needed: int,
        capacity_needed: int,
        ):
        self.name = name
        self.depth_needed = depth_needed
        self.capacity_needed = capacity_needed

class Container(object):
    def __init__(
        self,
        name: str,
        capacity: int,
        depth: int
        ):
        self.name = name
        self.capacity = capacity
        self.depth = depth
    
    def is_suitable(self, plant):
        if plant.depth_needed <= self.depth and plant.capacity_needed <= self.capacity:
            return 1
        else :
            return 0
