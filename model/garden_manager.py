import pandas as pd
from copy import deepcopy

class Plant(object):
    def __init__(
        self,
        name: str,
        depth_needed: int,
        capacity_needed: int,
        ):
        """Plant that needs to be planted in a container.
        Args:
            name (str): name of variety of plant
            depth_needed (int): depth needed to grow roots
            capacity_needed (int): amount of soil necessary to have enough space and nutrients to grow
        """
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
        """Recipient filled with soil to grow plants.
        Args:
            name (str): name of the container
            capacity (int): capacity of the container in liters
            depth (int): depth/height of the container.
        """
        self.name = name
        self.capacity = capacity
        self.depth = depth
    
    def is_suitable(self, plant):
        """Returns 1 if the plant is suitable to be grown in the container. 0 is not
        All plants have specificities (deep roots, grow very large etc) and need an appropriate container.
        Args:
            plant(Plant) : the plant to compare to the container.
        """
        if plant.depth_needed <= self.depth and plant.capacity_needed <= self.capacity:
            return 1
        else :
            return 0
