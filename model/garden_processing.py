import pandas as pd
from copy import deepcopy

class Plant(object):
    def __init__(
        self,
        name: str,
        space_needed: int,
        sun_exposure: str,
        ):
        self.name = name
        self.space_needed = space_needed
        self.sun_exposure = sun_exposure
    
    def read_from_demand(demand_df):
        plants = []
        for _, row in demand_df.iterrows():
            name = row["name"]
            space_needed = row["space_needed"]
            sun_exposure = row["sun"]
            plant = Plant(
                name=name,
                space_needed = space_needed,
                sun_exposure = sun_exposure
            )
            for quantity in range(row["quantity"]) :
                plants.append(plant)
        return plants

    @staticmethod
    def get_size_per_plant(plant_demand_df, plants) :
        space_demand = plant_demand_df.set_index("name").to_dict()["space_needed"] # In cm
        demand = []
        for plant in plants:
            if plant.name in space_demand:
                demand.append(space_demand[plant.name])
            else :
                demand.append(0)
        return demand

class ContainerGrid(object):
    def __init__(
        self,
        length: int,
        width: int,
        cell_size: int
        ):
        self.length = length
        self.width = width
        self.cell_size = cell_size
        self.grid = self.get_grid()
    
    def get_grid(self):
        self.no_x = self.length//self.cell_size
        self.no_y = self.width//self.cell_size
        grid = [[[] for x in range(self.no_x)] for y in range(self.no_y)]
        return grid

        
