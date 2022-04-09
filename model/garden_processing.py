import os
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
            plants.append(plant)
        return plants
