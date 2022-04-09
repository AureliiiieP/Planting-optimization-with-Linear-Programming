import os
import pandas as pd
from copy import deepcopy

class PlantDemand:
    def __init__(self, config: dict):
        self.config = deepcopy(config)
    
    def generate_demand(self):
        # Read quantity from config file
        quantity_dict = dict((key,d[key]) for d in self.config["seed_quantity"] for key in d)
        quantity_df = pd.DataFrame.from_dict(quantity_dict, orient="index", columns = ["quantity"]).reset_index()
        quantity_df = quantity_df.rename(columns = {'index':'name'})
        # Read plants specs from plant master
        plant_master_df = pd.read_excel(self.config["paths"]["raw"]["plant_master"], engine = 'openpyxl') # pandas uses xlrd by default. xlrd removed support for xlsx files.
        # Get demand for each plant
        self.demand = pd.merge(quantity_df, plant_master_df, on="name")
        return self.demand
